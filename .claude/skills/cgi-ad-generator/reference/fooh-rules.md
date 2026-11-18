# Rules and plan sheet for fake out-of-home CGI ads

A fake out-of-home (FOOH) ad is phone footage of something impossible in a real place, posted as if someone filmed it on the street. The rules below were written by Claude after it studied seven popular ads of this kind at about four frames a second, then adjusted after our own first stills looked like a sticker on a photo. Treat every number as a starting point and break one only on purpose.

## The idea

1. One impossible thing, and the product is that thing. You should be able to say it in 10 words or fewer.
2. It reads in the first frame with the sound off.
3. The place adds something to the idea, so pick it for a reason (a noodle cup slurping a zebra crossing, a soda can tipping into a fountain).
4. Something happens. A giant product standing still is a picture, so give it an action.

## Timing for one 5 second shot

5. The product is in shot at 0.0 s. Nothing builds up to it.
6. Something visibly changes by 2 s.
7. The brand name is readable in the first frame if possible.
8. The main moment lands between about 2.5 s and 3.75 s (half to three quarters of the way through).
9. The shot holds on the result after that, so the viewer gets a beat to take it in.

A longer ad is several shots cut together. Keep each shot to one action, and use a second, wider shot when the size needs proving.

## Size

10. Put at least one real person on the same ground as the product.
11. Street-scale objects are 2 to 3 times a person's height. Landmark-scale objects can match the landmark.
12. Keep one thing true to life next to it (a person, a scooter, a car) so the eye can measure.
13. Write the size in metres in the prompt, beside a 1.75 m person. Our own cup ended up at 4.6 times a person, over rule 11, so check the size in the still.

## Light and shadow

14. Prefer shade or overcast light. It is the easiest to match, but it does not fix flat shading on its own.
15. If there is sun, write down its direction before anything is generated, and keep the product's shadow pointing the same way as the people's shadows.
16. Every point where the product touches the ground gets a contact shadow.
17. Shiny ground shows the product's reflection.

## Why a still looks like a sticker

These came out of putting our first still next to real ads and measuring the difference:

- **The camera sees into the top.** A phone held at eye level cannot see into a cup that is three times taller than a person. Say where the camera is (eye level, about 1.6 m up, or lower) and that the top is seen from below.
- **Nothing passes in front of it.** Most real ads have something between the camera and the object. Put a passer-by, a lamppost or a branch over the lower part of the product, clear of the logo.
- **The product is the most vivid thing in the frame.** Tone its colours down a little so the street does not look dull beside it.
- **The shading is flat.** Ask for the surface to go from light to dark as it turns away from the light. In our test asking for this barely changed the shading.

The still went from "sticker" to "it looks like it's really there" once the first three fixes went in together, so we cannot say which of them mattered most.

## Camera

18. It should look like a phone: handheld, at eye level or lower.
19. One take per shot.
20. A slow drift or a gentle push-in, so the background moves behind the product and proves it is there.

## Plan sheet

Fill this in before any prompt is written.

| Field | Example (the run in `examples/`) |
|---|---|
| Product | Slurple instant noodles cup, purple, cream lettering |
| The impossible thing, 10 words or fewer | A house-sized noodle cup steams up a whole street |
| Place | A narrow shaded street in the Spanish Quarter of Naples, washing lines overhead |
| Size | 4.4 m tall, about 2.5 times a 1.75 m person |
| Light | Overcast, no hard shadows |
| Camera | Phone at eye level, about 25 m away, slight handheld drift |
| In front of it | A woman with a shopping bag crossing the foreground |
| 0.0 s | Faint steam above the open cup |
| By 2 s | The steam thickens and starts to rise |
| Main moment | About 2.5 s: steam surges into the washing lines and the sheets billow like sails |
| Last frame | Steam drifting, laundry billowing, the cup unmoved |
| Sound | A quiet street, a hiss that swells to a whoosh, sheets flapping |

## Writing the three prompts

Write all three from the one plan sheet, then read them side by side.

- **Opening frame** describes the place, where the product stands, its size in metres next to a person, the light, the camera height and what is in front of it.
- **Final frame** describes only what has changed since the opening frame. Everything else stays where it was.
- **What happens** walks through the action in seconds, from what the opening frame shows to what the final frame shows, and then the sounds.

Before anything runs, check that the first moment of "what happens" matches the opening frame and its last moment matches the final frame, with the same people in the same places. In the project these rules come from, video prompts written without looking at the stills needed facts fixed by hand before the shot came out right.

## Checking the result

Look at the clip at about 4 frames per second and mark each line pass or fail:

- The idea is clear in the first frame with the sound off.
- The product is in shot at 0.0 s, something changes by 2 s, and the main moment lands by about three quarters of the way.
- A person is in shot and the size is close to the plan.
- Shadows point the same way as the people's, with contact shadows where it touches the ground.
- The label stays spelled right in every frame.
- The clip plays forwards, from the opening still to the final still.

## Without Wireflow

The three prompts work in any tool that edits a photo and makes video between a start and an end frame. Make the opening still from the product photo, make the final still as an edit of the opening still, then make the video between them.
