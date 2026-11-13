# Skills installed outside this library

Some skills are maintained upstream and installed straight into Claude Code instead of being copied here. A library copy goes stale and, because the library is searched first, shadows the newer installed one.

Rule: if a skill with the same `name:` is installed in `~/.claude/skills` or by a plugin, the installed one wins. Don't re-add a copy here.

| Removed from | Get it from |
|---|---|
| engineering/brainstorming, engineering/requesting-code-review, engineering/systematic-debugging, engineering/test-driven-development, engineering/writing-plans, utils/using-superpowers | Plugin: `/plugin install superpowers@claude-plugins-official` |
| frontend/frontend-design | Plugin: `/plugin install frontend-design@claude-plugins-official` |
| utils/docx, productivity/pptx | Available as `anthropic-skills:docx` / `anthropic-skills:pptx` in this setup (claude.ai account skills). Otherwise `npx skills add https://github.com/anthropics/skills --skill docx` (or `--skill pptx`) |
| cloud/vercel-react-best-practices, cloud/vercel-composition-patterns | Already in this library as `react/vercel-react-best-practices` and `react/vercel-composition-patterns` (the cloud/ folders were copies) |
| video/hyperframes, video/hyperframes-cli, video/hyperframes-registry, video/media-use | HyperFrames CLI, into `~/.claude/skills`: `npx hyperframes skills` (refresh later with `npx hyperframes skills update`; check with `npx hyperframes skills check`) |
| video/music-to-video, video/talking-head-recut, video/embedded-captions, video/faceless-explainer | On-demand HyperFrames skills: `npx hyperframes skills update music-to-video talking-head-recut embedded-captions faceless-explainer` |
| video/website-to-hyperframes | Superseded upstream by `product-launch-video` (it covers site tours): `npx hyperframes skills update product-launch-video` |
