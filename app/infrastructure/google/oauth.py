"""Google OAuth2 login flow (Authorization Code + PKCE).

This is the *login* side: building the consent URL and exchanging the
returned code for tokens + the user's Google identity. Building authorized
API clients for the agents (Drive/Gmail/Calendar/Sheets) from already-stored
tokens is handled separately in `api_client_factory.py`.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from typing import cast

import google_auth_oauthlib.flow

import google.oauth2.id_token
from app.application.use_cases.authenticate_user import GoogleProfile
from app.core.exceptions import AuthError
from app.domain.value_objects import OAuthTokenSet
from google.auth.transport.requests import Request as GoogleAuthRequest

_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_TOKEN_URL = "https://oauth2.googleapis.com/token"  # noqa: S105 - public well-known endpoint, not a secret

# Google's token endpoint returns granted scopes in canonical full-URL form
# (e.g. "profile" -> "https://www.googleapis.com/auth/userinfo.profile") and
# can widen the set via `include_granted_scopes` picking up scopes granted in
# earlier consent flows. oauthlib's default is to hard-fail any exact-string
# mismatch between requested and granted scope — this is the documented
# escape hatch, not a workaround for a bug on our side.
os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")


class GoogleOAuthClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: list[str],
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scopes = scopes

    def _build_flow(
        self, state: str | None = None, code_verifier: str | None = None
    ) -> google_auth_oauthlib.flow.Flow:
        client_config = {
            "web": {
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "auth_uri": _AUTHORIZATION_BASE_URL,
                "token_uri": _TOKEN_URL,
                "redirect_uris": [self._redirect_uri],
            }
        }
        return google_auth_oauthlib.flow.Flow.from_client_config(
            client_config,
            scopes=self._scopes,
            redirect_uri=self._redirect_uri,
            state=state,
            code_verifier=code_verifier,
        )

    def build_authorization_url(self, state: str) -> tuple[str, str]:
        """Returns (authorization_url, code_verifier).

        google-auth-oauthlib auto-generates a PKCE code_verifier per Flow
        instance and never persists it — the caller must store it (e.g. in a
        cookie, alongside `state`) and pass it back into `exchange_code` on
        the callback, since that's a separate request handled by a fresh
        Flow object with no memory of this one.
        """
        flow = self._build_flow(state=state)
        authorization_url, _ = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        return cast(str, authorization_url), cast(str, flow.code_verifier)

    def exchange_code(
        self, code: str, state: str, code_verifier: str
    ) -> tuple[OAuthTokenSet, GoogleProfile]:
        flow = self._build_flow(state=state, code_verifier=code_verifier)
        try:
            flow.fetch_token(code=code)
        except Exception as exc:  # noqa: BLE001 - any OAuth exchange failure is an auth failure
            raise AuthError(f"Google OAuth code exchange failed: {exc}") from exc

        credentials = flow.credentials
        id_info = google.oauth2.id_token.verify_oauth2_token(  # type: ignore[no-untyped-call]
            credentials.id_token, GoogleAuthRequest(), self._client_id
        )

        profile = GoogleProfile(
            sub=id_info["sub"], email=id_info["email"], name=id_info.get("name", id_info["email"])
        )
        expires_at = (
            credentials.expiry.replace(tzinfo=UTC)
            if credentials.expiry and credentials.expiry.tzinfo is None
            else (credentials.expiry or datetime.now(UTC) + timedelta(hours=1))
        )
        tokens = OAuthTokenSet(
            access_token=credentials.token,
            refresh_token=credentials.refresh_token,
            scopes=tuple(credentials.scopes or self._scopes),
            expires_at=expires_at,
        )
        return tokens, profile
