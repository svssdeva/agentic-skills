## Gotchas (hard-won)

- **Seam pop** → connector endpoints were the diorama stills, not the neighbouring
  clips' actual frames. Always extract real frames (Step 5).
- **Seam stutter / camera "jumps backward"** → even with frame-matched seams, if the
  camera *velocity reverses* (forward dive, then a connector that pulls back out) it
  reads as a rewind. This is inherent to architecture B. For any grounded walkthrough use
  architecture A (one continuous forward take — legs chained from actual last frames, no
  pull-back, no `--end-image`); see Step 4.
- **Frozen video / stuck at frame 0** → `seekable=[0,0]`; the host isn't serving byte
  ranges. Use blob URLs (engine does).
- **Huge files** → you used all-intra. Use `-g 8` + blob instead.
- **Soft / low quality** → you downscaled or over-compressed. Encode native 1080p,
  crf ≤ 20, add `unsharp`. Video is inherently softer than the stills — keep the stills
  as the lite fallback for max fidelity.
- **Concurrent gens 503 / "not_enough_credits" race** → transient when many launch at
  once; re-roll the individual failure, it's not really out of credits (verify with
  `higgsfield workspace list`).
- **NSFW false-positives (Seedance `status "nsfw"`)** → the video content filter flags
  perfectly innocuous clips, especially **bedroom, pool, spa/wellness** contexts and
  trigger words like "bed", "pool", "waterfall", "wine", "swim". It's partly the prompt
  wording and partly the reference frames. Fixes, in order: (1) re-roll — it's often
  non-deterministic and passes on the 2nd–3rd try; (2) strip trigger words and add
  "empty, unoccupied, no people, no figures, architectural, tasteful"; (3) regenerate
  just that clip on **`kling3_0`** with the same start/end frames — a different
  provider's filter often passes what Seedance blocks. Expect a slight render-character
  shift on that one clip (each model has its own grain/motion feel); for a 5s connector
  behind a crossfade that usually beats option (4): set the connector slot to `null` —
  the engine crossfades that seam directly (optional connectors), so the page still
  completes. Budget extra credits/time for these re-rolls on interiors/real-estate content.
- **Dark / custom theme** → the engine wraps its default tokens in `@layer sw`, so a
  page-level `:root` / `.sw-root { --sw-bg; --sw-ink; --sw-accent; --sw-font-* }` block
  wins cleanly (no specificity hacks). `--sw-ink` is your primary **text/heading** colour;
  the **accent** fills the primary button and active nav. For a dark theme, set `--sw-bg`
  dark and `--sw-ink` light — the copy scrim and title shadow follow `--sw-bg` automatically.
- **Phone scrub stutters / freezes on a fast flick** → the 1080p master is too heavy for a
  phone decoder and seeks pile up. Ship the `-m.mp4` mobile encodes (720p, `-g 4`) and wire
  `clipMobile`/`connectorsMobile` (Step 6/7). The engine already coalesces seeks; the lighter
  encode is the other half. Still choppy on a low-end device? Tighten GOP (`-g 2` / all-intra).
- **Blank / black scene on iOS (desktop was fine)** → an iOS Safari quirk: a muted video that
  was never played won't paint a seeked frame. The engine fixes this by keeping the still as a
  poster until the clip paints and priming each video on first touch — so **don't** hide the
  still on `loadedmetadata` or strip the `playsinline`/`muted` attributes if you adapt the
  engine into a framework.
- **Page jumps while scrolling on mobile** → something is re-running layout on the URL-bar
  show/hide `resize`. The engine ignores height-only resizes on touch; if you ported it, gate
  your resize handler on a width change (keep the `orientationchange` path for rotation).
- **Copy hidden behind the URL bar / notch on mobile** → use the engine's safe-area-aware
  bottom offset (`env(safe-area-inset-bottom)` + `dvh`); make sure the page's
  `<meta viewport>` includes `viewport-fit=cover` (the template does).
- **Portrait crops the scene** → a 16:9 clip on a tall phone shows only its centre — which
  is why the mobile version is the native 9:16 chain (§6b), never the crop. If you're seeing
  this on a mobile build, either the crop fallback shipped (call it out to the user) or the
  9:16 encodes aren't actually being served (check `videoWidth < videoHeight`). Keeping each
  scene's focal subject centred (prompts.md) still matters for the desktop film itself.
- **`--generate-audio` errors on seedance** → omit it; mute in HTML and `-an` on encode.
- **Kling rejects your flags** → `kling3_0` has **no `--resolution` param** (don't pass
  one; encode at whatever native res ffprobe reports) and **sound defaults on** — pass
  `--sound off`. Duration default is 5; legs/dives want 10.
- **Seam pop only where you "saved credits"** → you swapped models mid-chain, or used a
  start-image-only model where a connector needs an `--end-image`. One model for the whole
  chain; the only cheap tier is `seedance_2_0_mini`, which keeps frame-locking so it stays
  seamless. (Any model with reference-only inputs can't hold a seam at all — Step 4.)
- **Monid seedance rejects inline images** → "Must be a public https:// URL or an
  asset://<id> reference": frames go through the free `sfs` file system
  (put → `curl -T` → cat → signed URL; pipeline.md → Monid backend), never base64.
  Quirk: `/put` echoes back `home/<path>`, but `/cat` and `/ls` want the **original
  relative path** you gave `/put` — using the echoed path 404s.
- **Monid clip wrong aspect** → the `ratio` default is adaptive and follows the input
  image (a 3:2 still → a 4:3-ish video). Pass `--ratio` — `16:9` desktop, `9:16`
  mobile chain — explicitly on every chained clip.
- **Monid CLI "Polling timed out after 120s"** → only the local wait died; the run
  continues server-side. Re-poll with `monid runs get -r <runId> -w 120` (find the id
  in `monid runs list`). Result URLs expire (~24–48 h) — download immediately.
- **Monid minimax drops the image when a prompt is present** → `prompt` +
  `first_frame_image` together returns an unrelated t2v clip AND bills the wrong matrix
  cell ($0.56 vs $0.28 observed). Image-only frame-locks but has no camera control.
  Until the wrapper is fixed, that endpoint can't chain — use Monid's seedance-2.0.
  (The model itself is fine — the same prompt+image via Higgsfield `minimax_hailuo`
  frame-locks.)
- **Monid billing surprises** → matrix/token-priced endpoints bill by selector match:
  pass every selector field explicitly (`model`, `resolution`, `duration`) and read
  `cost.value` off the run result after each clip. A big base64 field in any body can
  also bounce as an HTML error page ("Unexpected token '<'") — another reason frames
  travel by sfs URL.
- **Monid schema changed since last build** → it happens (seedance was t2v-only until
  late July 2026, then gained first/last-frame support). `monid inspect` before each
  build; re-run the Step 4 qualification probes when the Input schema differs from
  what pipeline.md documents.
- **Codex stills hang at "Reading additional input from stdin..."** → parallel
  `codex exec` calls launched from one script share the parent's stdin; one wins it,
  the rest block forever (observed: 1 of 3 completed, 2 hung, the second batch never
  started). Always append `< /dev/null` to every backgrounded `codex exec` — the
  pipeline's `gen_still_codex` has it; keep it if you adapt the command.
- **White-box scenes** → `gpt_image_2` returns a solid bg; either match the page bg to it
  or knock it out (Step 3).
- **bash 3.2** on macOS → no associative arrays in scripts.
- **Connector grabs the wrong scene's frames** (or errors on a frame that doesn't exist
  yet) → the array loop ran in **zsh** (macOS default interactive shell), where arrays are
  1-indexed, not bash's 0-indexed. Keep every array-driven chain step in a `#!/bin/bash`
  script run via `bash script.sh` — never inline array loops in the interactive shell.

