# AI Agent Journey

Building production-grade AI agents on self-hosted infrastructure over 12 months.

This repo is my public learning log — every phase, every project, every concept note committed as I go. The three capstone projects live in their own repos (linked below) and are referenced here by phase.

---

## About This Journey

**Background:** CS degree + IT help desk + advanced coding experience
**Focus:** Data-private, self-hosted open-source LLMs — no cloud lock-in
**Stack:** Python · LangChain · LangGraph · LlamaIndex · Ollama · vLLM · Docker · FastAPI

---

## Capstone Projects

| Project | Description | Repo |
|---|---|---|
| 🔬 Multi-Agent Learning Tool | Four-agent pipeline: Research → Index → Teach → Fact-Check any topic | [llm-learning-tool](#) |
| 📝 LinkedIn Content Agent | Reads Obsidian notes + GitHub commits → drafts LinkedIn posts via Telegram | [ai-linkedin-agent](#) |
| 🤖 Personal Assistant Agent | Gmail + Google Calendar + travel time + iPhone alarm, fully self-hosted | [personal-assistant-agent](#) |

> Links will be updated as each capstone is completed.

---

## Roadmap

| Phase | Timeline | Focus | Status |
|---|---|---|---|
| Phase 00 | Days 1–20 | CPU foundations — chatbot + ReAct loop in raw Python | ⬜ |
| Phase 1 | Weeks 3–6 | Local LLMs — benchmarks, structured outputs, hardened ReAct | ⬜ |
| Phase 2 | Months 3–4 | Agentic frameworks — LangChain, LlamaIndex, CrewAI + 2 capstones | ⬜ |
| Phase 3 | Months 5–6 | Business integration — Slack, SQL, Gmail, Calendar + capstone | ⬜ |
| Phase 4 | Months 7–9 | Production + self-hosting — Docker, vLLM, LangFuse | ⬜ |
| Phase 5 | Months 10–12 | Credentials + job conversion | ⬜ |

---

## Repository Structure

```
ai-agent-journey/
├── pre-phase/
│   ├── chatbot/              # Multi-turn chatbot, raw Python, cloud API
│   └── react-loop/           # ReAct loop from scratch, no frameworks
│
├── phase-1/
│   ├── model-benchmarks/     # Llama 3 vs Mistral vs Phi-4 on structured tasks
│   ├── structured-extractor/ # Prompt → validated JSON via Pydantic
│   └── react-loop-v2/        # Hardened loop: tool schemas, error handling, limits
│
├── phase-2/
│   ├── doc-qa-agent/         # LlamaIndex + Ollama Q&A over private knowledge base
│   └── coding-assistant/     # Agent that writes, runs, and debugs Python
│
├── phase-3/
│   ├── slack-bot/            # Webhook receiver, message classification, routing
│   └── nl-to-sql/            # Natural language → SQL via LangChain SQL Agent
│
└── notes/
    ├── concepts/             # Polished concept notes: RAG, ReAct, quantisation, etc.
    └── retrospectives/       # End-of-phase write-ups
```

Capstone projects are in their own repositories — see the table above.

---

## Certifications

| Certification | Provider | Status |
|---|---|---|
| Hugging Face NLP Course | Hugging Face | ⬜ |
| LangChain Academy (LangChain + LangGraph) | LangChain | ⬜ |
| deeplearning.ai — Agentic RAG with LlamaIndex | deeplearning.ai | ⬜ |
| deeplearning.ai — Functions, Tools & Agents | deeplearning.ai | ⬜ |
| DeepLearning.AI — AI Agents in LangGraph | deeplearning.ai | ⬜ |
| AWS AI Engineer Associate / Azure AI-102 | AWS / Microsoft | ⬜ |

---

## Concept Notes

Polished explanations of key concepts written in my own words after building with them.
All concept notes live in [`/notes/concepts/`](./notes/concepts/).

---

## Connect

- [LinkedIn](www.linkedin.com/in/bayley-papworth-6593a8130)
- Built in public · Feedback welcome via Issues
