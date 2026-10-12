---
name: retrieval-strategy
description: Decide how an AI system should find data BEFORE building a vector index. Use when designing RAG, agent search tools, enterprise search over SaaS apps, a coding agent's code search, or a knowledge base, or whenever someone asks "do we need a vector database". Compares one-shot RAG pipelines, agentic search loops, keyword/BM25, live MCP connectors and pre-compiled knowledge wikis by accuracy, cost and latency, and gives defaults.
---

# Retrieval Strategy

The vector database is no longer the centre of the stack. It is one index among several, and the
first question is not "which vector DB" but **how many hops does a typical question need, and how
long can the user wait for the slow ones?** Answer that, then pick from the four options below.

## The two deciding questions

1. **Hops.** Can the answer be assembled from the few chunks nearest to the question (1 hop), or
   does it need several documents found one after another (multi-hop)?
2. **Latency tolerance.** Is 1-2 s per answer required (search box, autocomplete, high-volume
   lookups), or is a 30-120 s worst case acceptable (research, analysis, a chat with a human)?

## The four options

| Option | How it works | Wins when | Costs |
|---|---|---|---|
| **One-shot RAG pipeline** | Chunk, embed, fetch top-k, optionally rerank, paste into one prompt. One shot; a reranker can reorder chunks but cannot decide "none of these are good, search again". | Simple 1-hop lookups at high volume; price and speed matter most. | Loses on multi-hop questions. |
| **Agentic search loop** | The model holds search tools (keyword, vector, grep, connectors) and loops: search, read, note what is missing, search again. | Multi-hop and hard questions; accuracy matters more than cost. | ~3x the tokens and input per question; slow tail (a few questions eat most of the budget). |
| **Live MCP connectors** | No index. The agent queries Notion, Salesforce, Slack, Jira, etc. directly over MCP with the user's own login and permissions. | Data you don't own, strict permissions, apps that forbid bulk export (Slack API terms, ChatGPT admin-only sync). | As slow as the slowest app queried; each app ranks its own results; several times the tokens of an index. |
| **Compiled knowledge (wiki / markdown folder)** | An AI compiles the corpus into curated documents once; queries read the compiled answer. | Stable, valuable knowledge where citation quality matters. | ~100x the tokens to build vs an index AND ~20x more per query in the one published study, so no break-even; only when stability justifies it. |

## Keyword search before vectors

Inside any loop, give the agent **BM25 / exact keyword search first** and vectors second.

- Embedding models trained on public text do not know your code names, acronyms, customer IDs or
  ticket numbers. "Customer IDs need equality, not a soulmate."
- Vectors still earn a slot for fuzzy meaning: semantic search on top of grep made one coding
  agent measurably more accurate and needed fewer searches on research benchmarks.
- Embeddings are cheap (cents per million tokens). The expensive part is the loop that calls them.

## Evidence (as reported by the vendors and papers cited; verify before quoting)

| Benchmark | Result |
|---|---|
| FRAMES (824 multi-hop questions, 12k Wikipedia articles), PipesHub | Agent loop 92.7% vs best fixed pipeline 78.9%; perfect retrieval 93%. On 5+ article questions: 90% vs 62%. Agent ~3x cost/question; worst answer 134 s vs 54 s. |
| LREC 2026 agentic retrieval study | Same shape: >3x input tokens, ~50% more time; a plain reranker beat the agent at *ranking*. |
| EnterpriseRAG-Bench (0.5M Slack/Gmail/Jira/Confluence/GitHub docs), Onyx | BM25 68.8% vs vector 51.4%, even on questions written to favour vectors. |
| BrowseComp-Plus, GPT-5 as search agent | 70.1% with embedding retriever vs 55.9% with BM25 (the BM25 vendor disputes the tuning). |
| Glean vs live connectors | Live-connector task ~$2.98 vs ~$0.58 with an index, >3x tokens. |
| LLM wiki vs RAG cost study (1 author, 13 questions) | Wiki ~21x tokens per query, no break-even; but 40% of cited claims held up vs 19% for RAG. |

## Defaults

- **New build, mixed questions:** an agent with cheap search tools. Keyword search first, vectors
  for fuzzy meaning, live connectors for apps you don't own. Add a one-shot pipeline only for the
  high-volume simple lookups that need to be fast and cheap.
- **Coding agent or a small document set:** grep plus a notes file. No index.
- **Under ~10 million vectors:** Postgres + pgvector (0.8.7 or newer; earlier versions have a
  security fix outstanding). A dedicated vector DB is not justified below that scale.
- **Company data spread across SaaS apps:** start with live connectors; add an index only where
  latency or ranking demonstrably hurts.
- **Compile knowledge** only when the corpus is stable and the citation quality is worth the
  build and per-query cost.

## Checklist before paying for a vector index

- [ ] Measured how many hops typical questions need on a sample of real queries.
- [ ] Tried BM25/keyword search as the agent's first tool and measured accuracy.
- [ ] Decided the acceptable worst-case latency and the per-question budget.
- [ ] Checked whether the source apps even permit bulk export; if not, connectors are the only option.
- [ ] If under 10M vectors, defaulted to pgvector before evaluating a hosted vector DB.
