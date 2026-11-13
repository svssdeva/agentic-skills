## Step 4 — Camera architecture (implements the Step 1.4 choice)

How the camera moves *between* scenes is the single biggest quality lever. The user
already chose the style at the interview (`CAMERA`, Step 1.4): fly-through → **B**,
walkthrough → **A**, locked-iso → **A + the locked-iso leg clause** (prompts.md). If
the interview somehow skipped it, ask now — never silently pick for them. The two
shapes, and the grammar that colors them:

### Video model — pick ONE for the whole chain

**This skill only ships seamless output**, so the only usable models are ones that can
frame-lock a seam: every chained clip must accept `--start-image`, and connectors also
need `--end-image`. That capability — not preference — is the selection rule. Check any
model with `higgsfield model get <job_type>` and **skip anything whose media inputs are
reference-only** (no start/end image): it can only *condition* a generation, not
*continue* a shot, so it physically can't hold a seam. Schemas below were confirmed
against the CLI:

| Model | start/end image | Notes |
|---|---|---|
| `seedance_2_0` (default) | ✓ / ✓ | Full chain (legs + connectors). `--mode std --resolution 1080p`. Its NSFW filter is the touchy one (see Gotchas). |
| `kling3_0` | ✓ / ✓ | Full chain — tested: `--mode std --sound off --duration 5` with start+end images accepted, seams frame-lock cleanly. **No `--resolution` param** (don't pass one; `--mode std` returns **720p native** — encode what ffprobe reports, never upscale). Sound defaults **on** → `--sound off`. `--duration` default 5, try 10 for legs. Different content filter than Seedance — the sanctioned NSFW fallback. |
| `seedance_2_0_mini` | ✓ / ✓ | Cheap draft tier that keeps frame-locking (720p). The previz tier: run the whole chain here first, then re-render final legs on the full model — still seamless, so it translates directly. |

Those three are the roster — all do both architectures. (`kling3_0_turbo` also frame-locks
via `--start-image`, but has no `--end-image`, so it's architecture-A-only and can't make
connectors; it also takes a different flag set — no `--mode`, has `--resolution` — so it
doesn't drop into the pipeline as-is. It's not in the default roster; only reach for it, and
wire it by hand, if architecture A's sequential render time is a proven bottleneck and you've
benchmarked it as actually faster.)

One more architecture-A-only candidate, worth knowing because it is by far the cheapest
probe: **`minimax_hailuo`** (Hailuo-2.3, ~6 credits per 768p/6s clip vs 22–72 for the
roster). Verified 2026-07: `--start-image` + prompt frame-locks (output frame 0 ≡ input,
PSNR 33 dB) and a forward-glide prompt was obeyed, gently. Constraints: the 2.3 variant
rejects `end_image` (no connectors → arch A only), output aspect follows the input image
(hand it a 16:9 canvas, not a bare 3:2 still), motion runs subtler than seedance, and
don't pass `--resolution` (the CLI mis-types the enum; the 768 default works — 1080
supports 6s only). One clip ≠ a chain: qualify a leg-to-leg handoff before betting a
full build on it.

Rules:
- **One model for all chained clips.** Each renderer has its own motion/color/grain
  character; mixing models mid-chain keeps *position* continuity (frames still hand off)
  but the render-character shift reads as a subtle pop. The one sanctioned exception is
  the NSFW fallback for a single stubborn clip (Gotchas) — a slight character shift on
  one 5s connector beats a missing connector.
- Default to `seedance_2_0`, rendered through **Monid by default** (per-clip USD —
  next section) with Higgsfield credits as the fallback biller (Step 0.1/1.6); honor
  a user's stated preference **only if the model qualifies** (frame-locking). If it
  doesn't, say so and use a supported model — never ship a non-seamless build to
  satisfy a model request. `kling3_0` and `seedance_2_0_mini` exist only on the
  Higgsfield side.
- The pipeline scripts take the model as `$VMODEL` with per-model flags already cased
  out (`references/pipeline.md`).

### Monid backend — the DEFAULT chain biller (qualified 2026-07-25)

Monid's **`bytedance /v1/video/seedance-2.0`** passed both paid probes on
2026-07-25 and is the **default** way this skill renders the chain, for **both
architectures** — it is the roster's `seedance_2_0` served pay-per-USD (wiring in
pipeline.md → "Monid backend"; Higgsfield renders the chain only as the fallback
biller or for Higgsfield-only models):

- **Leg probe** (prompt + `first_frame` image): output frame 0 ≡ input still
  (PSNR 31.6 dB), forward-glide prompt obeyed, billed the advertised cell
  ($0.279 / 480p 4s).
- **Connector probe** (prompt + `first_frame` + `last_frame`): start locked
  (31.6 dB); the end **lands close but not pixel-perfect** (27.5 dB, same
  composition, prop-level drift) — the exact end-image behavior Seedance shows
  on Higgsfield, covered by the engine's seam crossfade and by using the next
  dive's ACTUAL first frame as the end-image (Step 5 law, unchanged).

The I/O contract differs from the Higgsfield CLI — three rules:

1. **Images go by URL, never inline.** `content` items are
   `{"type":"image_url","image_url":{"url":…},"role":"first_frame"|"last_frame"}`;
   base64 data URLs are **rejected** ("Must be a public https:// URL or an
   asset://<id> reference"). Local frames travel through Monid's free workspace
   file system: `sfs /put` → `curl -T` the bytes → `sfs /cat` returns a signed
   public URL to paste into the body ($0, explicitly built for this).
2. **Pass `ratio` explicitly** (`16:9`, or `9:16` for the mobile chain) — the
   adaptive default follows the input image's aspect instead.
3. **Bill-check every clip**: cost is token-priced
   (`w × h × 24 × sec / 1024` at $7–7.7/1M); read `cost.value` off each run.

History that shaped these rules (still true as of 2026-07-25): the seedance
endpoints were text-to-video-only until late July 2026 — **re-`inspect` before
each build; the catalog moves in both directions.** `minimax
/v1/video_generation` (Hailuo-2.3) remains disqualified: sending `prompt` +
`first_frame_image` together silently drops the image (unrelated t2v output,
wrong price cell); image-only frame-locks (33 dB) but has no camera control.

**Qualification protocol for any new/changed Monid endpoint** (each probe is one
cheap 480p clip): (1) prompt + first-frame from a real still — frame 0 must
match the input to codec noise (PSNR ≳ 30 dB) and `cost.value` must match the
advertised cell; (2) for connector duty, add a `last_frame` from a different
still — the end must land on that composition (Seedance-style near-miss is fine,
the crossfade covers it). Pass → pay-per-clip tier (arch A if start-only; full
roster if start+end).

### A) Continuous forward take — RECOMMENDED for grounded / realistic / walkthrough
One camera that only ever glides **forward**, first scene through last, as a single take.
Generate the legs **sequentially**: leg 0 from scene-0's still (glide forward into it);
then each leg's `--start-image` = the **previous leg's ACTUAL last frame** (extract with
ffmpeg), prompt *"continue gliding smoothly FORWARD into [scene i], never pulling back"*
(or an expressive mid-leg move under the motion-handoff contract — see **Camera grammar**
below), and **no `--end-image`** — an end-image of a wide establishing shot forces the
camera to pull back, which is the #1 cause of stutter. Extract each leg's last frame to feed the
next. Result: every seam is frame-identical **and** the camera never reverses. There are
**no connectors** (skip Step 5) — the legs ARE the journey. Wire each leg as a section
clip with `connectors: []` and a small `crossfade` (~0.08). Even without an `--end-image`
the legs still arrive at distinct rooms (the prompt steers the content). Cost: strictly
**sequential** (can't parallelize) and slower; interiors trip the NSFW filter, so build in
re-rolls (3 attempts/leg).

### B) Dive-in + aerial connector — only for diorama / miniature / god's-eye worlds
A "dive into each scene" clip + a connector that pulls **up and out** and flies over to the
next scene (Step 5). The pull-out **reverses camera direction at every seam** (forward dive
→ backward pull-out). In a miniature/diorama world that reads as an intentional "zoom out
to the map, fly to the next island"; in a grounded first-person walkthrough it reads as a
jarring **rewind/stutter**. Use B only for the map-like aesthetic — which is exactly
what the "fly through the world" interview answer opts into; the reversal reads as
intentional there. If the user picked B against a grounded/photoreal direction, say
why it will read as a stutter and confirm before rendering.

### Camera grammar — the move should fit the concept (A is NOT "forward only")

"Forward only" is the *seam* rule, not the *leg* rule. The physics of the chain:

- **Position continuity** at a seam comes from the frame handoff (next leg starts from the
  previous leg's actual last frame).
- **Velocity continuity** at a seam means the camera must never *reverse across a seam* —
  that's the rewind stutter.
- **Inside a single leg the camera is free.** One leg is one continuous render — there is
  no seam to break mid-leg, so orbits, crane-ups, lateral tracking, even a push-in that
  eases back out are all safe *within* the clip. Reversals are only fatal *across* seams.

So give each leg an expressive move chosen from the scene's own logic, under a **motion
handoff contract**: every leg **ends by settling into a slow, steady forward drift** toward
the next destination (final ~1 s), and every leg **begins by continuing that same drift**.
Keep both clauses in the prompts verbatim (templates in `references/prompts.md`).

Pick the grammar from the concept:

| Concept / tone | Mid-leg move |
|---|---|
| Product / luxury retail | slow half-orbit around the hero object, then continue past it |
| Real estate / hospitality | steadicam glide through doorways; gentle crane-up in atria |
| Industrial / process / logistics | low lateral track alongside the line, foreground parallax |
| Travel / outdoors / campus | drone-style rise-and-reveal, then a descending swoop |
| Food / craft / detail-driven | push in close to the craft moment, ease back, carry on |
| Playful miniature (arch. B) | dives + aerial hops — the connector IS the grammar |

Honest costs: expressive mid-leg moves raise re-roll odds — the model can end a fancy move
in a state that isn't a clean forward drift. Mitigations: keep the final-second settle
clause verbatim; **eyeball each leg's last frame before chaining the next** (it should look
like a frame from a gentle forward glide — if not, re-roll before wasting the next leg);
budget ~1 extra re-roll per expressive leg. A plain forward glide stays the zero-risk
default — use it for legs where the scene itself is the show.

**Locked-iso variant** (`CAMERA` = locked isometric glide): architecture A where every
leg pins the view instead of taking a mid-leg move — "the camera keeps exactly the same
high isometric angle throughout, no rotation, no orbit, no tilt; it only travels
straight and level, the world sliding past beneath the same view" (verbatim clause in
prompts.md). The handoff contract is unchanged. Seedance drifts the angle slightly on
long legs — the existing eyeball-each-last-frame rule is the catch; re-roll a leg whose
view has rotated. Calmest look, cheapest re-rolls, and the closest to the Emons
reference.

Two related pacing knobs live in the engine (Step 7): per-section `scroll` (more scroll
distance = longer dwell in that scene) and `linger` (the camera settles mid-scene exactly
while the copy peaks, then picks up speed toward the seam). Prefer expressive motion in the
*clip* and restraint in the *scrub mapping* — they compound.

And remember scroll is a scrubber: visitors can scroll **up**, so every move also plays in
reverse. That's free and expected — no extra work — but it's another reason seam velocity
must be consistent in both directions (a seam that reads fine forward reads as a stutter
backward too if velocity flips).

**For B**, one camera flight per scene: starts high/outside, descends into the interior,
structure opens. Model: the chain model you picked above (default **`seedance_2_0`**),
`--start-image = the scene still`.

- Use the **solid-background still** (not the knocked-out transparent one) as the
  start image, so the video has a full frame.
- Prompt: "Single continuous cinematic camera move, no cuts. Begin high and far looking
  at the whole <scene> from outside … descend and fly inside toward <focal point> … the
  roof/walls gently open to reveal the interior. <style>, smooth graceful slow motion.
  No text." (Template in `references/prompts.md`.)
- Params (seedance): `--mode std --resolution 1080p --aspect_ratio 16:9 --duration 8`.
  For Kling: drop `--resolution` (no such param), add `--sound off`, `--duration 10`.
  Do **not** pass `--generate-audio` (it errors on seedance; audio is wasted anyway —
  you'll mute).
- Run concurrently, detached, then download each `.result_url`. Re-roll individual
  failures. Keep the raw 1080p sources — you need their frames next.

---

## Step 5 — Connectors (architecture B only)

Skip this whole step for architecture **A** — the forward take has no connectors; its legs
already chain seamlessly. This step applies to **B** (diorama/miniature), and note the
reversal caveat from Step 4.

The connector clips are what make the world feel *connected* instead of cut. A connector
flies from the end of scene i out and into the start of scene i+1. **Both of its
endpoints must be the ACTUAL RENDERED FRAMES of the neighbouring clips — never the
original diorama still.**

Why: every Higgsfield generation renders slightly differently. If a connector *ends* on
a fresh render of "the kitchen diorama," but the next dive clip *starts* on its own
different render of that same diorama, the two won't match and you get a pop at the seam.
The fix is to hand off the exact pixels:

```
For each connector between dive_i and dive_{i+1}:
  start-image = the LAST frame extracted from dive_i's rendered video
  end-image   = the FIRST frame extracted from dive_{i+1}'s rendered video
```

Now every seam is frame-identical on *both* sides:
`dive_i.end == connector.start` and `connector.end == dive_{i+1}.start`.

Extract the boundary frames from the rendered dives (not the stills):

```bash
ffmpeg -sseof -0.15 -i dive_i.mp4   -frames:v 1 -q:v 2 dive_i_last.png    # interior of i
ffmpeg -ss 0      -i dive_{i+1}.mp4 -frames:v 1 -q:v 2 dive_next_first.png # establishing of i+1
```

Generate the connector (`--duration 5` is plenty). Connectors need `--end-image`, so the
model must accept it — any roster model does (`seedance_2_0`, `seedance_2_0_mini`,
`kling3_0`):

```bash
higgsfield generate create "$VMODEL" \
  --prompt "$(cat connector_i.txt)" \
  --start-image dive_i_last.png --end-image dive_next_first.png \
  $VOPTS --aspect_ratio 16:9 --duration 5 --wait --json
# seedance: VOPTS="--mode std --resolution 1080p"; kling3_0: VOPTS="--mode std --sound off"
```

Connector prompt: "Single continuous camera move, no cuts. Pull up and back out of
<scene i>, rise into the sky, glide across the connected miniature world, and arrive
above <scene i+1>, beginning to descend toward it. Seamless flowing aerial transition.
<style>. No text." (Template in `references/prompts.md`.)

Insurance: Seedance lands *close* to the end-image but not always pixel-perfect, so the
engine still applies a **short crossfade** (a few frames) at each seam. Frame-matched
endpoints + a small crossfade = no visible cut. Never skip the actual-frame handoff and
rely on the crossfade alone; a big content jump can't be hidden by a crossfade.

---

