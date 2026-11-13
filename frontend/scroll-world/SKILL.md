<!-- Source: https://github.com/oso95/scroll-world -->
<!-- Install: npx skills add https://github.com/oso95/scroll-world --skill scroll-world -->

---
name: scroll-world
description: >
  Build an immersive scroll-scrubbed "fly through the world" landing page for any
  industry or brand using Higgsfield. As the visitor scrolls, a pre-rendered camera
  flies from outside each scene into its interior, then flows on to the next scene
  with NO cuts — one continuous connected flight (Emons-style isometric diorama world,
  or any art direction you pick). The skill interviews the user for the topic, the
  story beats/sections, and brand kit, then generates cohesive scenes + seamless camera
  clips with Higgsfield and wires a portable, framework-agnostic scroll-scrub engine.
  The video chain renders through Monid by default (Seedance 2.0, pay-per-clip
  USD — capability re-checked each build, see Step 4) with Higgsfield credits as
  the fallback biller. Use when the user wants a "3D world" /
  "browse-through-the-industry" hero, a scroll cinematic, a diorama landing, or to
  turn a business into a scrollable world.
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion, Skill
---

# scroll-world

Produces a landing page where **scroll drives a camera**: it dives from outside a scene
into its interior, then flies out and into the next scene, continuously, with no visible
cuts. The visuals are AI-generated — stills via Higgsfield (or Codex), the video chain
via **Monid by default** (pay-per-clip Seedance 2.0; Higgsfield credits as fallback) —
and the page just scrubs pre-rendered video by scroll position. This is the same technique behind Apple's scroll-through product
pages — the camera genuinely moves, scroll only drives time.

**What you generate:** N scene stills → N "dive-in" camera clips → N-1 "connector" clips
that join consecutive scenes seamlessly → a portable scrub engine that plays the whole
chain as one flight.

**The one rule that makes or breaks it:** seams must be *frame-identical*. Read
[The seamless chain](references/camera-architecture.md) before generating any
connector. Getting this wrong is the single most common failure and produces a visible
"pop" between scenes.

Do not assume a frontend framework. The scrub engine in `references/scrub-engine.js` is
self-contained vanilla JS (it builds its own DOM + injects its own CSS into a container
you give it), so it drops into plain HTML, Next.js, Vue, a Python-served page, anything.
The value of this skill is the Higgsfield pipeline, the prompts, and the seam method —
not the framework.

---

## Step 0 — Bootstrap

1. **Monid CLI — the default video-chain backend.** Check `monid --version`,
   `monid keys list` (active key) and `monid balance` — the chain is billed per
   clip in USD (Step 1.7 has the numbers; a 1080p N=6 chain ≈ $27). If the CLI is
   missing or the balance can't cover the chain, say so and fall back to
   rendering the chain on Higgsfield credits instead — same model, same
   pipeline, different biller (Step 4 → Monid backend).
2. **Higgsfield CLI — still required even on the Monid path**: it renders the
   scene stills (`gpt_image_2`) and is the home of the `kling3_0` NSFW fallback
   and the fallback chain. If `higgsfield` is not on `$PATH`, install per the
   `higgsfield-generate` skill. If `higgsfield workspace list` fails auth, ask the user
   to run `higgsfield auth login` (interactive OAuth — you cannot run it) and, if needed,
   `higgsfield workspace set <id>`. Confirm credits cover the stills (~N image
   gens) — plus `(2N-1)` video gens if the chain falls back here.
3. **ffmpeg / ffprobe** on `$PATH` (frame extraction + encoding).
4. **An image tool** for background knockout if you want floating scenes: PIL
   (`python3 -c "import PIL"`), or `cwebp`/`sips`. Optional — see Step 3.
5. **(Optional) Codex CLI** — if `codex` is on `$PATH` (≥ 0.125) and
   `codex login status` reports a ChatGPT login, the scene stills can be generated
   through Codex's built-in `image_gen` (the same gpt-image-2 model) billed to the
   user's ChatGPT subscription instead of Higgsfield credits — offer it at
   Step 1.7, command in Step 2. Absence just removes the option.
6. Caveats: macOS ships **bash 3.2** (no `declare -A`); don't use associative arrays in
   scripts. Higgsfield generations take **3–8 min each** — always run them detached
   (background) and poll, never a foreground blocking call. Reference-by-job-UUID is
   rejected by media flags — pass **local file paths** to `--image/--start-image/--end-image`.
   Video models differ in accepted params (e.g. Kling has no `--resolution`) and in whether
   they support start/end-image conditioning at all — before batching, confirm the chosen
   model's schema with `higgsfield model get <job_type>` and see the Step 4 model table.

---

## Step 1 — Interview the user

Read [references/interview-the-user.md](references/interview-the-user.md) now — do this before Step 2.

## Step 2 — Generate the scene stills

One image per section, **all sharing the same style preamble** for cohesion. Default
model **`gpt_image_2`** (crisp, great at isometric illustration; returns a solid/white
background which is perfect for floating diorama "islands"). Use `nano_banana_2` only if
the brief is character/cartoon-heavy (note: `nano_banana_2` is a CLI alias — it resolves
to `nano_banana_pro`; it won't appear under that name in `higgsfield model list`).

Prompt shape (full templates in `references/prompts.md`):

```
<STYLE PREAMBLE, identical every time>. On a plain solid <bg> background with a soft
contact shadow. <PALETTE hexes>. No text, no letters, no logos, centered, 3:2.
Subject: <what is in THIS diorama>.
```

- Run all N concurrently, detached. Command per scene:
  `higgsfield generate create gpt_image_2 --prompt "$(cat scene_i.txt)" --aspect_ratio 3:2 --resolution 2k --quality high --wait --wait-timeout 15m --json > scene_i.json 2>scene_i.err`
- Result URL is `.[]0.result_url` in the `--wait --json` output. `curl` it down.
- **Codex stills variant** (if chosen at Step 1.7 — subscription-billed, zero
  credits): same prompt files, same byte-identical preamble, generated by Codex's
  built-in `image_gen`:

  ```bash
  codex exec -C "$WORK" -s workspace-write --skip-git-repo-check \
    'Use the image generation tool ($imagegen) to generate: '"$(cat "$WORK/still_i.txt")"' Wide 3:2 landscape, high resolution. Save it as ./still_i.png. Do not do anything else.' \
    < /dev/null
  ```

  Single-quote the `$imagegen` segment (the shell must not expand it); if editing
  with reference images, the prompt goes BEFORE any `-i` flag (it's variadic).
  ~1–3 min per image; run a few in parallel, not all N at once — and keep the
  `< /dev/null`: parallel `codex exec` calls sharing a script's stdin hang
  waiting for input (Gotchas). Output lands at
  1536×1024 (3:2) — fine for `--start-image` and posters. Everything downstream
  (cohesion review, knockout, dives) is unchanged.
- A generation may fail transiently (HTTP 503) — re-roll that one individually; don't
  restart the batch.
- **Review the stills before continuing.** They must read as one cohesive world (same
  angle, palette, light). If one is off-style, regenerate it, optionally passing an
  approved scene as `--image` to lock style.

See `references/pipeline.md` for the exact batch script.

---

## Step 3 — (Optional) Float the scenes

If you want the dioramas to float over an atmospheric background instead of sitting in a
solid box, knock out the flat background to transparency with
`references/knockout.py` (border-connected flood fill — preserves interior colour that
matches the bg, e.g. cream walls). Then encode to webp. If you'd rather keep it simple,
just make the page background the same colour as the scene background and skip this.

These stills double as **video posters and lazy-load fallbacks**, so keep them.

---

## Step 4 — Camera architecture (implements the Step 1.4 choice)

Read [references/camera-architecture.md](references/camera-architecture.md) (Step 4) before generating the video chain.

## Step 5 — Connectors (architecture B only)

Read [references/camera-architecture.md](references/camera-architecture.md) (Step 5) for the connector clips, architecture B only.

## Step 6 — Encode for smooth scrubbing

Scrubbing = setting `video.currentTime` from scroll. Two things matter, and they are
often gotten wrong:

1. **Seekability, not keyframe density, is what makes scrubbing work.** Many static
   hosts (and `python -m http.server`) don't serve HTTP byte-range requests, which pins
   `video.seekable` to `[0,0]` and clamps *every* seek to frame 0 — the video looks
   frozen. The robust fix is to **fetch each clip as a `Blob` and play it from an
   in-memory object URL** (blobs are always fully seekable). The engine does this.
   Because of it, you do **not** need all-intra video.
2. **Don't shrink quality to get smooth seeks.** Encode at the **native resolution**
   (1080p from Seedance — don't downscale), `crf ~20`, a **small GOP** (`-g 8`) rather
   than all-intra (all-intra bloats an 8s clip to ~25 MB; GOP 8 is ~8 MB and scrubs
   fine via blob). Strip audio, add faststart, and a light `unsharp` counters video
   softness:

```bash
ffmpeg -i src.mp4 -an -vf "unsharp=5:5:0.8:5:5:0.0" \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
  -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart out.mp4
```

Encode all 2N-1 clips (dives + connectors) with the same settings for uniform quality.

**Mobile encodes (only if the user opted in at Step 1.6).** The mobile version is
the **native 9:16 portrait chain** (pipeline.md §6b): portrait renders of every dive and
connector, encoded **720 wide (`scale=720:-2`), `-g 4`** (more keyframes = cheaper seeks —
phone decoders' seek cost scales with GOP length), crf 23 — wired as `clipMobile` /
`connectorsMobile`, with each portrait dive's first frame extracted as the section's
`stillMobile` poster (Step 7). The engine serves them automatically on phones and falls
back to the desktop clip when absent. The 16:9 centre-crop `encm()` encodes
(pipeline.md §6) are a **fallback only** — for when credits can't cover the portrait
chain — and shipping them must be called out to the user, never silent. If the user chose
desktop-only, skip this — the engine still hardens phone scrubbing regardless
(seek-coalescing, iOS priming), so the page degrades gracefully rather than breaking.

---

## Step 7 — Assemble the page

Copy `references/scrub-engine.js` (and, if you want a fully standalone page, the tiny
`references/index-template.html`) into the user's project — or adapt into their
framework. It's config-driven and self-contained:

```js
mountScrollWorld(document.getElementById('world'), {
  brand: { name: 'Pearl & Co.' },
  diveScroll: 1.3, connScroll: 0.9,          // viewport-heights of scroll per clip
  sections: [
    { id:'farm', label:'The Farms', still:'assets/farm.webp',
      clip:'assets/vid/farm.mp4',
      clipMobile:'assets/vid/farm-m.mp4',      // mobile opt-in only: native 9:16 render
      stillMobile:'assets/farm-m.webp',        // its first frame as the portrait poster
      scroll: 1.6, linger: 0.45,   // optional pacing: longer dwell + camera settles mid-scene
      accent:'#8FB98A', eyebrow:'From leaf to last sip', title:'It starts in the hills.',
      body:'…', tags:['Single-origin','Hand-picked'] },
    // …one per section; last may carry a `cta`
  ],
  connectors:       ['assets/vid/conn1.mp4','assets/vid/conn2.mp4',   /* … length = sections-1 */],
  connectorsMobile: ['assets/vid/conn1-m.mp4','assets/vid/conn2-m.mp4' /* … same length; mobile opt-in only */],
});
```

The engine handles: the ordered dive/connector chain, scroll→currentTime with rAF
smoothing, blob loading, lazy prefetch of nearby clips, frame-matched crossfades, pinned
per-section copy (first section greets on landing, last holds its CTA), a route rail,
`prefers-reduced-motion`, and mobile. **Pacing per section:** `scroll` overrides
`diveScroll` for that scene (more scroll = longer dwell) and `linger` (0–1, keep ≤ 0.6)
remaps time so the camera settles mid-scene — exactly while the copy peaks — then speeds
up toward the seam; seam frames are untouched (f(0)=0, f(1)=1). Give the hero and finale
scenes a higher `scroll` + some `linger`; keep transit scenes brisk. Theme it with CSS variables (`--accent`,
`--sw-bg`, `--sw-ink`, …) — the visual identity comes from the generated clips, so the
chrome stays quiet. See the header of `scrub-engine.js` for the full config + CSS vars.

**On phones the engine adapts automatically** (coarse pointer or ≤860px): it serves
`clipMobile` / `connectorsMobile` when present, **coalesces seeks** (never queues a new
`currentTime` while the decoder is still seeking — this is what stops a fast flick from
freezing the clip), **keeps the still as a poster until the clip paints its first frame**
and **primes each video on first touch** (fixes iOS's blank-until-played video), drops the
drifting particles, ignores URL-bar-only resizes (no scroll jump), and uses safe-area
insets so copy clears the notch/home indicator. All of this hardening is on by default —
no config needed. The `clipMobile`/`connectorsMobile` encodes are the opt-in part
(Step 1.6): only wire them when the user asked for the mobile version.

For non-JS backends (Python/Rails/etc.): serve the assets and drop the engine `<script>`
into the rendered HTML; nothing about it is framework-specific.

---

## Step 8 — QA the seams (don't skip)

Drive the page in a headless browser and **verify frame continuity at the seams**, which
is the thing most likely to be wrong:

- Screenshot at scroll positions just before and just after each seam. The two frames
  must be near-identical (the dive's last frame == the connector's first frame). If they
  pop, you used the diorama still instead of the actual rendered frame (redo Step 5), or
  the crossfade band is too short. Calibration: judge seams by *composition*, not raw
  PSNR — at 720p/1080p a correctly frame-locked seam can read ~18–25 dB from detail
  shimmer alone (observed on a verified-good build); a real mismatch shows as different
  composition/props, not just softness.
- Check the console for errors, confirm `video.seekable.end(0) > 0` (blob working), and
  that `currentTime` tracks scroll across each clip's band.
- **Mobile — full checklist only if the user opted into the mobile version (Step 1.6).**
  For a desktop-only build, just sanity-check a phone viewport once: page loads, still
  posters show, nothing overlaps — the engine's hardening covers graceful degradation.
  For the mobile build (do this on a real phone or an emulated one, portrait + landscape):
  - Emulate a phone viewport **with CPU throttled 4–6×** and scroll fast — the clip should
    track without freezing (the seek-coalescing + `-m.mp4` encodes are what make this hold).
  - Confirm the first scene shows immediately (its still is the poster) and the video takes
    over the instant you scroll — no blank/black scene (the iOS priming fix). Test iOS Safari
    specifically; it's the one that goes blank if this regresses.
  - Verify the `-m.mp4` variant is actually served on mobile (Network panel), and the
    heavy 1080p master on desktop. The mobile clips must be **natively portrait**
    (`videoWidth < videoHeight` — not a downscaled 16:9 file), and the `stillMobile`
    posters must be served and match each portrait clip's first frame (no
    landscape→portrait flash when the video paints).
  - Slowly scroll so the URL bar collapses — the page must **not jump** (height-only resizes
    are ignored on touch). Rotate the device — layout should recompose cleanly.
  - Only if the crop **fallback** shipped (no credits for the portrait chain): portrait
    crops a 16:9 clip to its centre — confirm the focal subject still reads, and remind
    the user this is the stopgap, not the mobile version.
- Check reduced-motion (should fall back to the stills, no video, no particles).

---

## Gotchas (hard-won)

Read [references/gotchas.md](references/gotchas.md) before building the page and during QA.

## References

- `references/prompts.md` — the intake checklist, style-preamble pattern, and every
  prompt template (scene still, dive, connector) with fill-in slots.
- `references/pipeline.md` — copy-paste batch scripts for the whole run (generate →
  extract frames → connectors → encode → mobile encode), bash-3.2-safe.
- `references/scrub-engine.js` — the portable, config-driven scrub engine (builds DOM +
  injects CSS; blob-seek, lazy load, seam crossfade, copy, route rail, reduced-motion, and
  phone hardening: mobile encodes, seek-coalescing, iOS priming, safe-area, no-jump resize).
- `references/index-template.html` — a minimal standalone page that mounts the engine.
- `references/knockout.py` — border-connected background knockout for floating scenes.

## Moved sections (references/)

Read the file that matches the task; all text moved here verbatim from this SKILL.md.

- [Step 1 — Interview the user](references/interview-the-user.md) — read at the start of every run, before Step 2: questions to ask, story beats, brand kit, camera-architecture choice (1.4).
- [Step 4 and Step 5 — Camera architecture, Connectors](references/camera-architecture.md) — read when generating the video chain (dives, architecture A/B), and the connector clips for architecture B.
- [Gotchas (hard-won)](references/gotchas.md) — read before building the page and during QA, and whenever a seam, scrub or mobile problem shows up.
