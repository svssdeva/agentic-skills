## Step 1 — Interview the user

The **subject is the user's to state — ask it as an open question in plain prose**, never a
fabricated multiple-choice. A made-up list of industries biases them and reads as you
deciding their business for them; let them answer in their own words (their real business,
a client's, or any idea). Reserve structured multiple-choice (`AskUserQuestion` in Claude
Code; a plain either/or question elsewhere) for the genuinely
enumerable, lower-stakes choices below — art direction, camera style, and brand-kit
approach — and even
there, signal they can go their own way ("Other"). Ask only what you can't sensibly
default. Cover:

1. **Subject** (ask openly, not multiple-choice) — "What should this world be about? Your
   business, a client's, or any idea — a word or a sentence is fine." Capture the
   industry/product + a one-line pitch (e.g. "a bubble tea company, from leaf to last
   sip"), and a brand name if they have one; otherwise you'll propose one below.
2. **Brand kit** — offer three paths, pick one:
   - Import from a URL: `higgsfield marketing-studio brand-kits fetch --url <site> --wait`
     (pulls name, colours, tone). Then read it back with `brand-kits list --json`.
   - The user hands you palette + name + tone directly.
   - You propose a palette + name and let them approve.
   Capture **4–6 named hex values**, a display name, and a tone word or two.
3. **Art direction** — default is "soft matte low-poly **clay diorama**, isometric,
   tilt-shift miniature, warm light." Offer alternatives (flat papercraft, glossy toy,
   claymation, neon night). Whatever is chosen becomes the shared **style preamble**
   reused verbatim in every scene prompt (this is what makes the world cohesive).
4. **Camera style — ALWAYS ask; it's the film's personality, not a technical
   detail.** Ask by feel (`AskUserQuestion` in Claude Code; a plain question
   elsewhere) and record the answer as `CAMERA`. The options map to the Step 4
   architectures — Step 4 then *implements* the choice, it never re-decides it:
   - **"Fly through the world"** — the camera dives into each scene, pulls up and
     out, and hops across the miniature world to the next; angles change
     constantly, big expressive aerial moves (this is the flagship-demo look).
     → Architecture B. Recommend as the default for diorama/miniature art
     directions.
   - **"One continuous walkthrough"** — a single forward flight that glides
     through each scene straight into the next, never pulling back; expressive
     but always-forward moves per scene (camera grammar table). → Architecture A.
     Recommend as the default for grounded/photoreal art directions.
   - **"Locked isometric glide"** — the camera keeps one fixed angle for the whole
     film, Emons-style; the world slides past/toward it, no rotation, no reveals.
     → Architecture A + the locked-iso clause in every leg prompt (prompts.md).
   State the trade-off in one line each (B reverses direction at seams — charming
   in miniature, jarring in realism; locked-iso is the calmest and cheapest to
   re-roll; walkthrough sits between).
5. **The journey (sections)** — the ordered scenes the camera flies through. Propose a
   set derived from the subject's own value chain and let the user edit. 5–7 works well.
   Boba example: farms → pearl kitchen → flagship shop → delivery → community plaza →
   the hero product. Each section needs: a short subject description (what's IN the
   diorama), an eyebrow, a headline, one line of body, and 0–3 tag pills. The last
   section is usually the hero product + the CTA.
6. **Mobile version — ALWAYS ask this; never silently generate both.** Ask as a
   two-option choice (`AskUserQuestion` in Claude Code; a plain question elsewhere):
   *"Want a mobile-optimized version too? The mobile version is a second camera chain
   rendered natively in **9:16 portrait** — composed for phones, not a crop of the
   landscape film — which roughly doubles the Higgsfield credit spend (state the
   estimated number)."*
   Options: "Desktop only" / "Desktop + mobile (native 9:16 — ~2× credits)". The
   credit cost must be stated to the user, not just implied.
   What the answer gates:
   - **Yes** → render the parallel 9:16 portrait chain and ship it as the mobile variants
     (Step 6 / pipeline.md §6b): portrait start canvases → 9:16 dives + connectors
     frame-locked against their own renders → 720-wide `-m.mp4` encodes → `stillMobile`
     portrait posters. Wire `clipMobile`/`connectorsMobile`/`stillMobile` (Step 7); run
     the full mobile QA (Step 8). Budget ~2N-1 extra video gens + NSFW re-rolls.
     **Never ship the centre-crop as the mobile version by default** — if credits can't
     cover the portrait chain, say so and offer the crop encodes (pipeline.md §6) as an
     explicitly-labelled stopgap the user must approve.
   - **No** → skip the mobile encodes and wiring entirely. The engine's phone hardening
     (seek-coalescing, iOS priming, safe-area CSS) is always on regardless — that's not
     a "mobile version," it's just the page not breaking when a phone visits — so a
     desktop-only build still degrades gracefully.

7. **Budget — engines shown by cost, decided before anything renders.** Present the
   render tiers (`AskUserQuestion`), then compute and state the estimated total for
   the user's N scenes — `N stills + (2N−1) videos [videos ×2 if mobile] + ~15%
   re-roll headroom` — and get a go before generating.
   - **Video tier** (roster only — every option frame-locks seams, Step 4):

     | Tier | Model | Rough cost |
     |---|---|---|
     | Draft / previz | `seedance_2_0_mini` (720p) | ~¼ of Standard |
     | Standard (default) | `seedance_2_0` (1080p) | baseline |
     | Alternate | `kling3_0` (720p native) | ≈ Standard; different look + content filter |

     Draft doubles as the previz path: run the whole chain cheap, approve the
     journey, re-render final legs on Standard (pipeline.md Notes) — suggest it
     unprompted when the balance reads tight.
   - **Backend — Monid is the DEFAULT biller for the chain** (Step 0.1; wiring
     in pipeline.md → Monid backend). Same Seedance 2.0, per-clip USD instead of
     credits. Token-priced `width × height × 24 × seconds / 1024` at $7/1M
     (480p/720p) or $7.7/1M (1080p) — measured: 1080p 8s dive ≈ $2.99, 5s
     connector ≈ $1.87; 720p ≈ $1.21 / $0.76; 480p ≈ $0.28 / $0.35. An N=6
     desktop chain ≈ $27 at 1080p / ~$11 at 720p vs Higgsfield Plus-monthly ≈
     $32 / $16 — ~15% cheaper per clip, parity with Plus-annual; structurally
     better for one-off builds (pay-per-use, no monthly expiry). On Monid the
     Draft/previz tier is simply the **same endpoint at 480p** — no model swap,
     so previz→final stays one-model by construction. State `monid balance`
     against the estimate; **fall back to Higgsfield credits** (per-model tiers
     above) when the user prefers their subscription, the balance is short, or
     the model must be `kling3_0` (Higgsfield-only). It's the same underlying
     model (`seedance_2_0` ≙ Monid's `seedance-2.0`), so finishing a stranded
     chain on the other biller is a reasonable rescue — but the serving stacks
     differ and cross-provider seam character is **untested**: eyeball the first
     rescued seam before rendering the rest, same as any model swap.
   - **Stills source** (only offer if the Codex CLI is present, Step 0.5):
     Higgsfield `gpt_image_2` (spends credits) vs **Codex `image_gen`** — the same
     gpt-image-2 model billed to the ChatGPT subscription (zero credits; counts
     toward Codex usage limits; 1536×1024 output — exactly 3:2, slightly under
     Higgsfield's 2k). Stills are plain PNGs handed to `--start-image`, so the
     video chain is indifferent to their source. Command in Step 2. **One source
     for all N stills of a build** — the two render with slightly different
     character (verified: Codex runs warmer/lighter), and mixing sources across
     scenes reads as style drift, same reason the video chain uses one model.
   - **Calibrate costs, don't guess.** The CLI exposes no pricing and plans differ.
     Run ONE still and ONE video first, diff `higgsfield workspace list` before/
     after, extrapolate to the full run, and warn the user whenever the estimate
     exceeds ~70% of the balance. (Observed on a plus plan, 2026-07: Standard
     video ≈ 40–55 credits, still ≈ 15.) A real `not_enough_credits` mid-run is
     recoverable (finished clips survive; resume after top-up) but ugly — the
     whole point of this step is that the user decides *before* the spend.

If the user names a video model outside the roster, honor it **only if it can
frame-lock seams** (Step 4). This skill only ships seamless output, so a model that
can't frame-lock is declined with a one-line why, not substituted in — use a roster
model instead.

Keep the scroll mechanic fixed (continuous fly-through) — that's the point of the skill.
See `references/prompts.md` for the intake checklist and copy structure.

---

