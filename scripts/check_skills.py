"""Library consistency checks (stdlib only). Run from repo root after adding/removing a skill:
  python -I scripts/check_skills.py   -> 1 frontmatter, 2 unique names, 3 no shadowing installed skills, 4 links, 5 README/CLAUDE.md sync
  --cleanup adds checks 6-12: the one-time gate for the 2026-11 bloat cleanup (needs a `main` branch; not for routine use).
Prints PASS/FAIL/SKIP per check; exits 1 if any check fails."""
import re, subprocess, sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home() / ".claude"
SHADOW_ALLOW = set()  # repo skill names deliberately allowed to share an installed skill's name
TRIMMED = ["frontend/scroll-world", "frontend/design-taste-frontend", "frontend/imagegen-frontend-mobile",
           "frontend/image-to-code", "engineering/reverse-engineer-anything", "frontend/interface-design"]
MAX_WORDS = 2500
REMOVED = {
    "video": "hyperframes hyperframes-cli hyperframes-registry media-use music-to-video talking-head-recut "
             "embedded-captions faceless-explainer website-to-hyperframes",
    "engineering": "brainstorming requesting-code-review systematic-debugging test-driven-development writing-plans "
                   "grill-me grill-with-docs setup-matt-pocock-skills triage to-tickets wayfinder ask-matt wait-what "
                   "implement code-review-and-quality debugging-and-error-recovery planning-and-task-breakdown claude-handoff",
    "utils": "using-superpowers docx compress cavecrew caveman-review caveman-commit caveman-stats using-agent-skills",
    "frontend": "frontend-design high-end-visual-design minimalist-ui",
    "productivity": "pptx lark-doc",
    "cloud": "vercel-react-best-practices vercel-composition-patterns",
    "seo": "seo-audit seo-geo programmatic-seo ai-seo optimize-for-ai seo-aeo-best-practices seo-content-writer "
           "web-quality-seo churn-prevention cold-email lead-magnets",
    "astro": "astro-seo",
    "ai": "langchain-architecture langchain-rag langgraph-fundamentals langgraph-persistence rag-implementation",
    "mobile": "animate-expo expo-tailwind-setup vercel-react-native-skills write-swift ionic ionic-design",
    "bun": "bun-development bun-runtime",
}
REMOVED_PATHS = [f"{c}/{s}" for c, ss in REMOVED.items() for s in ss.split()] + [
    "skills-lock.json", "graphify-out", "frontend/remotion-best-practices/rules",
    "frontend/remotion-best-practices/remotion-markup/remotion-maps"]
KEPT = {
    "utils": "apify-ultimate-scraper audit-website agent-browser caveman caveman-compress",
    "video": "video-edit ai-video-generation 3d-animation-short-generator",
    "ai": "ai-image-generation retrieval-strategy rag-architect",
    "mobile": "sleek-design-mobile-apps capacitor-best-practices",
    "seo": "reddit-automation",
    "database": "neon-postgres postgresql-optimization prisma-driver-adapter-implementation prisma-orm-setup "
                "prisma-postgres-setup prisma-upgrade-v7 supabase",
    "python": "dataverse-python-advanced-patterns dataverse-python-quickstart dataverse-python-usecase-builder",
    "productivity": "jira-integration confluence",
    "frontend": "remotion-best-practices hallmark commodity-ceiling subframe-motion review-animations",
    "engineering": "karpathy-guidelines agentic-build-primitives handoff grilling tdd code-review diagnosing-bugs",
    "bun": "bun",
}
KEPT_PATHS = [f"{c}/{s}" for c, ss in KEPT.items() for s in ss.split()]
MERGES = {"engineering/handoff": ["engineering/claude-handoff"], "bun/bun": ["bun/bun-development", "bun/bun-runtime"]}
REMOVED_VIDEO = REMOVED["video"].split()

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
failed = 0
def check(name, ok, detail=""):
    global failed
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" - {detail}" if detail and not ok else ""))

def short(items, n=10):
    items = sorted(items)
    return ", ".join(items[:n]) + (f" (+{len(items) - n} more)" if len(items) > n else "")

def norm(text):
    return text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")

def read(p):
    return norm(Path(p).read_bytes().decode("utf-8", errors="replace"))

def git_main(path):
    r = subprocess.run(["git", "show", f"main:{path}"], cwd=ROOT, capture_output=True)
    return norm(r.stdout.decode("utf-8", errors="replace")) if r.returncode == 0 else None

def split_fm(text):
    """Return (frontmatter dict or None, body). Skips leading blank / HTML comment lines."""
    lines = text.split("\n")
    i = 0
    while i < len(lines) and (not lines[i].strip() or re.fullmatch(r"\s*<!--.*-->\s*", lines[i])):
        i += 1
    if i >= len(lines) or lines[i].strip() != "---":
        return None, text
    end = next((j for j in range(i + 1, len(lines)) if lines[j].strip() == "---"), None)
    if end is None:
        return None, text
    fm, fml = {}, lines[i + 1:end]
    for k, line in enumerate(fml):
        m = re.match(r"([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        val = m.group(2).strip()
        if not val or val[:1] in (">", "|"):  # block / multi-line plain scalar: gather indented lines
            block = []
            for nxt in fml[k + 1:]:
                if nxt.strip() and not nxt[:1].isspace():
                    break
                block.append(nxt.strip())
            val = " ".join(b for b in block if b)
        fm[m.group(1)] = val.strip().strip("\"'").strip()
    return fm, "\n".join(lines[end + 1:])

def unlink(s):
    """Blank relative link targets (moves rewrite them; check 4 verifies they resolve). URLs kept."""
    return re.sub(r"\]\((?![a-zA-Z][\w+.-]*:)[^)]*\)", "]()", s)

def content_lines(text, min_len=1, is_skill=True):
    """Significant stripped lines: no blanks, HTML comments, frontmatter (SKILL.md), or pure rules."""
    body = split_fm(text)[1] if is_skill else text
    out = set()
    for line in body.split("\n"):
        s = line.strip()
        if len(s) < min_len or re.fullmatch(r"<!--.*-->", s) or re.fullmatch(r"[-*_=|:\s]+", s):
            continue
        out.add(unlink(s))
    return out

def md_union(folder):
    out = set()
    for p in (ROOT / folder).rglob("*.md") if (ROOT / folder).is_dir() else []:
        out |= {unlink(l.strip()) for l in read(p).split("\n")}
    return out

# ---- discover skills ----
skill_files = sorted(p for p in ROOT.glob("*/*/SKILL.md") if p.parts[-3] not in (".git", "scripts"))
skills = {p.parent.relative_to(ROOT).as_posix(): p for p in skill_files}
fms = {s: split_fm(read(p))[0] for s, p in skills.items()}

# 1 FRONTMATTER
bad = [s for s, fm in fms.items() if not fm or not fm.get("name") or not fm.get("description")]
check("1 frontmatter name+description", not bad, f"{len(bad)} bad: {short(bad)}")

# 2 UNIQUE NAMES
by_name = {}
for s, fm in fms.items():
    if fm and fm.get("name"):
        by_name.setdefault(fm["name"], []).append(s)
dupes = [f"{n}={'+'.join(v)}" for n, v in by_name.items() if len(v) > 1]
check("2 unique names", not dupes, short(dupes))

# 3 NO SHADOWING
def vkey(p):
    return tuple(int(x) for x in re.findall(r"\d+", p.name))
installed = {}
for p in (HOME / "skills").glob("*/SKILL.md"):
    installed[(split_fm(read(p))[0] or {}).get("name") or p.parent.name] = f"~/.claude/skills/{p.parent.name}"
for plugin in (HOME / "plugins" / "cache").glob("*/*"):
    vers = [v for v in plugin.iterdir() if v.is_dir()] if plugin.is_dir() else []
    if vers:
        newest = max(vers, key=vkey)
        for p in newest.glob("skills/*/SKILL.md"):
            installed.setdefault((split_fm(read(p))[0] or {}).get("name") or p.parent.name, f"plugin {plugin.name}")
shadow = [f"{s}({n} vs {installed[n]})" for n, ss in by_name.items() if n in installed and n not in SHADOW_ALLOW for s in ss]
if not (HOME / "skills").is_dir() and not (HOME / "plugins" / "cache").is_dir():
    print("SKIP 3 no shadowing installed skills - no ~/.claude/skills or plugin cache on this machine")
else:
    check("3 no shadowing installed skills", not shadow, f"{len(shadow)}: {short(shadow, 8)}")

# 4 LINKS
LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'][^)]*)?\)")
def broken_links(md):
    bad, fence = [], None
    for line in read(md).split("\n"):
        m = re.match(r"\s*(`{3,}|~{3,})(.*)$", line)  # fences may be indented (lists) and use ``` or ~~~
        if m:
            mark = m.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence) and not m.group(2).strip():
                fence = None
            continue
        if fence:
            continue
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if re.match(r"[a-zA-Z][\w+.-]*:", target) or target.startswith(("#", "/")):  # "/x" = site path
                continue
            path = unquote(target.split("#")[0].split("?")[0])
            if path and not (md.parent / path).exists():
                bad.append(f"{md.relative_to(ROOT).as_posix()}->{target}")
    return bad
docs = list(skill_files) + [ROOT / n for n in ("README.md", "CLAUDE.md", "INSTALL-EXTERNAL.md") if (ROOT / n).exists()]
bad = [b for d in docs for b in broken_links(d)]
check("4 relative links resolve", not bad, f"{len(bad)} broken: {short(bad, 5)}")

# 5 README SYNC
readme, claude_md = read(ROOT / "README.md"), read(ROOT / "CLAUDE.md")
m = re.search(r"\*\*(\d+) drop-in skills\*\*", readme)
check("5a README headline count", bool(m) and int(m.group(1)) == len(skills),
      f"README says {m.group(1) if m else '?'}, found {len(skills)}")
linked = {unquote(x) for x in re.findall(r"\]\(([^)#\s]+)/SKILL\.md\)", readme)}
missing, extra = set(skills) - linked, linked - set(skills)
check("5b README table paths == skill folders", not missing and not extra,
      f"missing {len(missing)}: {short(missing)}; extra {len(extra)}: {short(extra)}")
m = re.search(r"library of (\d+)", claude_md.split("\n\n", 2)[1] if "\n\n" in claude_md else claude_md)
check("5c CLAUDE.md count", bool(m) and int(m.group(1)) == len(skills),
      f"CLAUDE.md says {m.group(1) if m else '?'}, found {len(skills)}")

if "--cleanup" not in sys.argv[1:]:
    sys.exit(1 if failed else 0)
# ---- one-time 2026-11 cleanup gate (checks 6-12) ----

# 6 REMOVED
present = [p for p in REMOVED_PATHS if (ROOT / p).exists()]
check("6 removed paths gone", not present, f"{len(present)} still present: {short(present)}")

# 7 KEPT
gone = [p for p in KEPT_PATHS if not (ROOT / p / "SKILL.md").is_file()]
if not (ROOT / "frontend/remotion-best-practices/remotion-maps/REFERENCE.md").is_file():
    gone.append("frontend/remotion-best-practices/remotion-maps")
check("7 kept skills present", not gone, f"{len(gone)} missing: {short(gone)}")

# 8 MERGES lossless
for dest, srcs in MERGES.items():
    have = md_union(dest) if (ROOT / dest).is_dir() else set()
    for src in srcs:
        old = git_main(f"{src}/SKILL.md")
        if old is None:
            check(f"8 merge {src} -> {dest}", False, f"main:{src}/SKILL.md not found")
            continue
        lost = [l[:60] for l in sorted(content_lines(old) - have)]
        check(f"8 merge {src} -> {dest}", not lost, f"{len(lost)} lines missing, e.g. {lost[:3]}")

# 9 TRIMS lossless + short
for s in TRIMMED:
    p = ROOT / s / "SKILL.md"
    if not p.is_file():
        check(f"9 trim {s}", False, "SKILL.md missing")
        continue
    words = len(split_fm(read(p))[1].split())
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", "main", "--", s], cwd=ROOT, capture_output=True, text=True)
    main_mds = [f for f in r.stdout.splitlines() if f.endswith(".md")]
    if not main_mds:
        check(f"9 trim {s}", False, f"no .md files for {s} on main")
        continue
    have, lost = md_union(s), []
    for f in main_mds:
        old = git_main(f)
        lines = content_lines(old, 4, f.endswith("/SKILL.md")) if old is not None else set()
        lost += [f"{f.rsplit('/', 1)[-1]}: {l[:60]}" for l in sorted(lines - have)]
    check(f"9 trim {s}", words <= MAX_WORDS and not lost,
          f"{words} words (max {MAX_WORDS}); {len(lost)} main lines lost, e.g. {lost[:3]}")

# 10 INSTALL GUIDE
inst = ROOT / "INSTALL-EXTERNAL.md"
if not inst.is_file():
    check("10 INSTALL-EXTERNAL.md", False, "file missing")
else:
    t = read(inst)
    names = REMOVED_VIDEO + ["superpowers", "frontend-design", "docx", "pptx"]
    miss = [n for n in names if not re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", t, re.I)]
    if "npx hyperframes skills" not in t:
        miss.append("'npx hyperframes skills'")
    check("10 INSTALL-EXTERNAL.md", not miss, f"not mentioned: {short(miss)}")

# 11 GLOBAL RULE
gpath = HOME / "CLAUDE.md"
g = read(gpath) if gpath.is_file() else ""
sec = re.search(r"^# Skill Loading Order.*?(?=^# |\Z)", g, re.M | re.S)
ok = bool(sec) and any("~/.claude/skills" in l and "same" in l and "name:" in l for l in sec.group(0).split("\n"))
check("11 global installed-wins rule", ok, "no line with '~/.claude/skills' + 'same' + 'name:' in Skill Loading Order")

# 12 graphify references gone
hits = [f"CLAUDE.md:{w}" for w in ("graphify-out", "/graphify") if w in claude_md]
hits += ["README.md:graphify-out"] if "graphify-out" in readme else []
check("12 no graphify refs", not hits, short(hits))

sys.exit(1 if failed else 0)
