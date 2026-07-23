"""Composition root.

This is the one place in the codebase allowed to know about every concrete
adapter. It wires ports to infrastructure implementations once at startup
(`Container.bootstrap`), and builds per-request object graphs (which need a
request-scoped `AsyncSession`) via `Container.build_orchestrator` /
`Container.build_authenticate_user_use_case`.
"""

from __future__ import annotations

from dataclasses import dataclass

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.agents.gmail.client import GmailClient
from app.agents.gmail.email_sender_adapter import GmailEmailSenderAdapter
from app.agents.gmail.inbox_adapter import GmailInboxAdapter
from app.agents.google_calendar.calendar_port_adapter import GoogleCalendarPortAdapter
from app.agents.google_calendar.client import CalendarClient
from app.agents.google_calendar.schedule_adapter import CalendarScheduleAdapter
from app.agents.google_drive.client import DriveClient
from app.agents.google_drive.drive_port_adapter import GoogleDrivePortAdapter
from app.agents.google_drive.logo_storage_adapter import GoogleDriveLogoStorageAdapter
from app.agents.google_sheets.cash_flow_adapter import GoogleSheetsCashFlowAdapter
from app.agents.google_sheets.client import SheetsClient
from app.agents.project_management.service import WorkspaceService
from app.agents.whatsapp.service import WhatsAppService
from app.application.ports.secret_manager import SecretManagerPort
from app.application.use_cases.authenticate_user import AuthenticateUserUseCase
from app.application.use_cases.cash_flow import CashFlowUseCase
from app.application.use_cases.check_reminders import CheckRemindersUseCase
from app.application.use_cases.finance_overview import FinanceOverviewUseCase
from app.application.use_cases.manage_calendar import ManageCalendarUseCase
from app.application.use_cases.manage_conversation import ManageConversationUseCase
from app.application.use_cases.manage_daily_plan import (
    DailyPlanMetricsUseCase,
    ManageDailyPlanUseCase,
    ManageFocusSessionUseCase,
    ManageGoalsUseCase,
)
from app.application.use_cases.manage_email import ManageEmailUseCase
from app.application.use_cases.manage_files import ManageFilesUseCase
from app.application.use_cases.manage_notifications import ManageNotificationsUseCase
from app.application.use_cases.manage_whatsapp_messages import ManageWhatsAppMessagesUseCase
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
    ManageThoughtsUseCase,
)
from app.application.use_cases.memory_use_cases import RetrieveMemoryUseCase, StoreMemoryUseCase
from app.application.use_cases.send_daily_review import SendDailyReviewUseCase
from app.core.config import SecretManagerBackend, Settings
from app.core.logging import get_logger
from app.core.security import SessionTokenService, TokenCipher
from app.infrastructure.cache.redis_client import RedisCache, create_redis_client
from app.infrastructure.db.repositories.agent_execution_repository import (
    SqlAlchemyAgentExecutionRepository,
)
from app.infrastructure.db.repositories.background_memory_repository import (
    BackgroundMemoryRepository,
)
from app.infrastructure.db.repositories.client_attachment_repository import (
    SqlAlchemyClientAttachmentRepository,
)
from app.infrastructure.db.repositories.client_repository import SqlAlchemyClientRepository
from app.infrastructure.db.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)
from app.infrastructure.db.repositories.daily_plan_repository import SqlAlchemyDailyPlanRepository
from app.infrastructure.db.repositories.daily_plan_swap_repository import (
    SqlAlchemyDailyPlanSwapRepository,
)
from app.infrastructure.db.repositories.focus_session_repository import (
    SqlAlchemyFocusSessionRepository,
)
from app.infrastructure.db.repositories.goal_repository import SqlAlchemyGoalRepository
from app.infrastructure.db.repositories.memory_repository import SqlAlchemyMemoryRepository
from app.infrastructure.db.repositories.notification_repository import (
    SqlAlchemyNotificationRepository,
)
from app.infrastructure.db.repositories.oauth_token_repository import (
    SqlAlchemyOAuthTokenRepository,
)
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.db.repositories.thought_repository import SqlAlchemyThoughtRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.db.repositories.whatsapp_message_repository import (
    SqlAlchemyWhatsAppMessageRepository,
)
from app.infrastructure.db.session import create_engine, create_session_factory
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.infrastructure.google.oauth import GoogleOAuthClient
from app.infrastructure.green_invoice.client import GreenInvoiceClient
from app.infrastructure.llm.anthropic_gateway import AnthropicLLMGateway
from app.infrastructure.llm.openai_embeddings import OpenAIEmbeddingGateway
from app.infrastructure.secrets.env_secret_manager import EnvSecretManager
from app.infrastructure.secrets.gcp_secret_manager import GcpSecretManager
from app.infrastructure.whatsapp.client import WhatsAppClient
from app.orchestrator.agent_registry import AgentRegistry
from app.orchestrator.intent_router import IntentRouter
from app.orchestrator.orchestrator import Orchestrator

logger = get_logger(__name__)


@dataclass(slots=True)
class RequestScopedServices:
    orchestrator: Orchestrator
    manage_conversation: ManageConversationUseCase
    authenticate_user: AuthenticateUserUseCase
    manage_clients: ManageClientsUseCase
    manage_projects: ManageProjectsUseCase
    manage_tasks: ManageTasksUseCase
    manage_thoughts: ManageThoughtsUseCase
    manage_whatsapp_messages: ManageWhatsAppMessagesUseCase
    dashboard_summary: DashboardSummaryUseCase
    list_activity: ListActivityUseCase
    manage_notifications: ManageNotificationsUseCase
    check_reminders: CheckRemindersUseCase
    send_daily_review: SendDailyReviewUseCase
    manage_calendar: ManageCalendarUseCase
    manage_email: ManageEmailUseCase
    manage_files: ManageFilesUseCase
    manage_goals: ManageGoalsUseCase
    manage_daily_plan: ManageDailyPlanUseCase
    manage_focus_sessions: ManageFocusSessionUseCase
    daily_plan_metrics: DailyPlanMetricsUseCase
    finance_overview: FinanceOverviewUseCase
    cash_flow: CashFlowUseCase


class Container:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.secret_manager: SecretManagerPort = (
            GcpSecretManager(settings.gcp_project_id)
            if settings.secret_manager_backend == SecretManagerBackend.GCP
            else EnvSecretManager()
        )

        self.token_cipher = TokenCipher(settings.token_encryption_key)
        self.session_tokens = SessionTokenService(
            signing_key=settings.jwt_signing_key,
            access_ttl_minutes=settings.jwt_access_token_ttl_minutes,
            refresh_ttl_days=settings.jwt_refresh_token_ttl_days,
        )

        self.engine: AsyncEngine = create_engine(settings.database_url)
        self.session_factory: async_sessionmaker[AsyncSession] = create_session_factory(self.engine)

        self.redis_client: Redis = create_redis_client(settings.redis_url)
        self.cache = RedisCache(self.redis_client)

        self.google_oauth_client = GoogleOAuthClient(
            client_id=settings.google_oauth_client_id,
            client_secret=settings.google_oauth_client_secret,
            redirect_uri=settings.google_oauth_redirect_uri,
            scopes=settings.google_oauth_scopes_list,
        )

        self.llm_gateway = AnthropicLLMGateway(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            max_tokens=settings.anthropic_max_tokens,
        )
        self.embedding_gateway = OpenAIEmbeddingGateway(
            api_key=settings.openai_api_key, model=settings.embedding_model
        )

        self.google_api_client_factory = GoogleApiClientFactory(
            session_factory=self.session_factory,
            token_cipher=self.token_cipher,
            client_id=settings.google_oauth_client_id,
            client_secret=settings.google_oauth_client_secret,
        )

        self.agent_registry = AgentRegistry()
        self.workspace_service = WorkspaceService(session_factory=self.session_factory)

        self.whatsapp_client = WhatsAppClient(
            access_token=settings.whatsapp_access_token,
            phone_number_id=settings.whatsapp_phone_number_id,
        )
        self.green_invoice_client = GreenInvoiceClient(
            api_id=settings.green_invoice_api_id,
            api_secret=settings.green_invoice_api_secret,
            base_url=settings.green_invoice_base_url,
        )
        self.whatsapp_service = WhatsAppService(
            session_factory=self.session_factory, client=self.whatsapp_client
        )

        # Storing a just-handled command as long-term memory doesn't need to
        # block the response — session-per-call (like WorkspaceService above)
        # so the Orchestrator can fire it in the background safely, without
        # racing the request-scoped session's teardown.
        self.background_memory_repo = BackgroundMemoryRepository(self.session_factory)
        self.background_store_memory = StoreMemoryUseCase(
            self.embedding_gateway, self.background_memory_repo
        )

        gmail_client = GmailClient(self.google_api_client_factory)
        calendar_client = CalendarClient(self.google_api_client_factory)
        drive_client = DriveClient(self.google_api_client_factory)
        sheets_client = SheetsClient(self.google_api_client_factory)
        self.inbox_port = GmailInboxAdapter(gmail_client)
        self.schedule_port = CalendarScheduleAdapter(calendar_client)
        self.email_sender_port = GmailEmailSenderAdapter(gmail_client)
        self.calendar_port = GoogleCalendarPortAdapter(calendar_client)
        self.drive_port = GoogleDrivePortAdapter(drive_client)
        self.client_logo_storage = GoogleDriveLogoStorageAdapter(drive_client)
        self.cash_flow_port = GoogleSheetsCashFlowAdapter(
            sheets_client, settings.cash_flow_spreadsheet_id
        )

    def build_request_scope(self, session: AsyncSession) -> RequestScopedServices:
        conversations = SqlAlchemyConversationRepository(session)
        memory_repo = SqlAlchemyMemoryRepository(session)
        executions = SqlAlchemyAgentExecutionRepository(session)
        users = SqlAlchemyUserRepository(session)
        oauth_tokens = SqlAlchemyOAuthTokenRepository(session, self.token_cipher)
        clients_repo = SqlAlchemyClientRepository(session)
        client_attachments_repo = SqlAlchemyClientAttachmentRepository(session)
        projects_repo = SqlAlchemyProjectRepository(session)
        tasks_repo = SqlAlchemyTaskRepository(session)
        thoughts_repo = SqlAlchemyThoughtRepository(session)
        whatsapp_messages_repo = SqlAlchemyWhatsAppMessageRepository(session)
        notifications_repo = SqlAlchemyNotificationRepository(session)
        goals_repo = SqlAlchemyGoalRepository(session)
        daily_plans_repo = SqlAlchemyDailyPlanRepository(session)
        focus_sessions_repo = SqlAlchemyFocusSessionRepository(session)
        daily_plan_swaps_repo = SqlAlchemyDailyPlanSwapRepository(session)

        retrieve_memory = RetrieveMemoryUseCase(self.embedding_gateway, memory_repo)

        intent_router = IntentRouter(
            llm_gateway=self.llm_gateway,
            agent_registry=self.agent_registry,
            agent_execution_repository=executions,
        )
        orchestrator = Orchestrator(
            conversation_repository=conversations,
            intent_router=intent_router,
            retrieve_memory=retrieve_memory,
            store_memory=self.background_store_memory,
        )

        authenticate_user = AuthenticateUserUseCase(
            user_repository=users,
            oauth_token_repository=oauth_tokens,
            allowed_owner_email=self.settings.owner_email or None,
        )

        return RequestScopedServices(
            orchestrator=orchestrator,
            manage_conversation=ManageConversationUseCase(conversations),
            authenticate_user=authenticate_user,
            manage_clients=ManageClientsUseCase(
                clients_repo,
                projects_repo,
                tasks_repo,
                self.client_logo_storage,
                client_attachments_repo,
            ),
            manage_projects=ManageProjectsUseCase(projects_repo),
            manage_tasks=ManageTasksUseCase(tasks_repo),
            manage_thoughts=ManageThoughtsUseCase(thoughts_repo),
            manage_whatsapp_messages=ManageWhatsAppMessagesUseCase(whatsapp_messages_repo),
            dashboard_summary=DashboardSummaryUseCase(
                projects_repo, tasks_repo, clients_repo, self.inbox_port, self.schedule_port
            ),
            list_activity=ListActivityUseCase(executions),
            manage_notifications=ManageNotificationsUseCase(notifications_repo),
            check_reminders=CheckRemindersUseCase(
                user_repository=users,
                task_repository=tasks_repo,
                notification_repository=notifications_repo,
                email_sender=self.email_sender_port,
                calendar_port=self.calendar_port,
            ),
            send_daily_review=SendDailyReviewUseCase(
                user_repository=users,
                task_repository=tasks_repo,
                calendar_port=self.calendar_port,
                notification_repository=notifications_repo,
                email_sender=self.email_sender_port,
                daily_plan_repository=daily_plans_repo,
                app_base_url=self.settings.app_base_url,
            ),
            manage_calendar=ManageCalendarUseCase(self.calendar_port),
            manage_email=ManageEmailUseCase(self.inbox_port),
            manage_files=ManageFilesUseCase(self.drive_port),
            manage_goals=ManageGoalsUseCase(goals_repo),
            manage_daily_plan=ManageDailyPlanUseCase(
                daily_plans_repo, daily_plan_swaps_repo, tasks_repo
            ),
            manage_focus_sessions=ManageFocusSessionUseCase(focus_sessions_repo, daily_plans_repo),
            daily_plan_metrics=DailyPlanMetricsUseCase(
                daily_plans_repo, focus_sessions_repo, daily_plan_swaps_repo, tasks_repo
            ),
            finance_overview=FinanceOverviewUseCase(
                self.green_invoice_client, clients_repo, self.cache
            ),
            cash_flow=CashFlowUseCase(self.cash_flow_port),
        )

    def build_user_repository(self, session: AsyncSession) -> SqlAlchemyUserRepository:
        return SqlAlchemyUserRepository(session)

    def bootstrap_agents(self) -> None:
        """Registers every agent's tools into this container's registry. Call once at startup."""
        from app.agents import register_all_agents

        register_all_agents(
            self.google_api_client_factory,
            self.workspace_service,
            self.whatsapp_service,
            self.agent_registry,
        )
        logger.info("agents_bootstrapped", agents=self.agent_registry.list_agents())

    async def shutdown(self) -> None:
        await self.redis_client.aclose()
        await self.engine.dispose()
