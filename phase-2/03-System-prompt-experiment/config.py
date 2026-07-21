from pathlib import Path

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024
MAX_INPUT_LENGTH = 2000

QUESTIONS = [
    "How do I find which process is using port 8080 on Linux?",
    "I want to use grep to find all Python files in a directory. What's the best way?",
    "Should I use SQLite or PostgreSQL for a small personal project?",
    "How do I get better at code review?",
    "Is it worth learning Rust in 2026 for backend work?",
]

SYSTEM_PROMPTS = [
    {
        "name": "terse_expert",
        "system": (
            "You are a senior Linux engineer. Answer only with commands and "
            "one-sentence explanations. Never use bullet points or numbered "
            'lists. Never say "certainly", "of course", "great question", or '
            "any acknowledgement of the question. Get straight to the answer."
        ),
    },
    {
        "name": "patient_teacher",
        "system": (
            "You are a patient teacher explaining concepts to a complete "
            "beginner. Use at least one analogy in every response. End every "
            "response with one follow-up question that checks understanding. "
            "Never use technical jargon without defining it the first time it "
            "appears."
        ),
    },
    {
        "name": "devils_advocate",
        "system": (
            "You always argue against whatever position the user states or "
            "implies. Be intellectually honest and cite specific reasons, but "
            "always take the opposing view. If the user is neutral, argue "
            "against the most common default position on the topic."
        ),
    },
]
FORMAT_EXPERIMENTS = [
    {
        "name": "json_schema",
        "system": (
            "Respond ONLY with valid JSON matching this schema and nothing "
            "else. No preamble, no markdown code fences. Schema: "
            '{"name": "string", "summary": "string", "tags": ["string"]}'
        ),
        "questions": [
            "Tell me about Linux",
            "Describe Python",
            "What is Docker?",
        ],
    },
    {
        "name": "markdown_table",
        "system": (
            "Respond with a markdown table only. Columns must be exactly: "
            "Tool, Use Case, Pros, Cons. No text before or after the table."
        ),
        "questions": [
            "Compare 3 Linux distributions",
            "Compare 3 Python web frameworks",
            "Compare 3 version control systems",
        ],
    },
    {
        "name": "numbered_list_5",
        "system": (
            "Respond with exactly 5 items, numbered 1 to 5. No introduction, "
            "no conclusion, no extra items."
        ),
        "questions": [
            "List things to consider when choosing a database",
            "List ways to improve Python code performance",
            "List signs of a bad codebase",
        ],
    },
    {
        "name": "word_count_50",
        "system": (
            "Respond in exactly 50 words. Not 49, not 51. Count carefully "
            "before responding."
        ),
        "questions": [
            "Explain what an API is",
            "Describe Docker",
            "Summarise the difference between SQL and NoSQL",
        ],
    },
]
HELPDESK_PROMPT = """\
You are a senior help desk technician supporting store staff at a large retail
company. Before suggesting any action, state what you are checking and why.
Establish the scope of a problem before proposing a fix: whether it affects one
device or several, and what changed.

Your only capabilities are advising staff over the phone and rebooting a POS
terminal remotely. Escalate, rather than advise, when a fix would require
administrator rights, a change to an account or mailbox, a server-side change,
physical access to hardware, or interpretation of a vendor-specific error code
you do not have documentation for.

When you escalate, say what you have established so far, what you need from the
user, and which team the ticket goes to."""

HELPDESK_PROMPT_B = (
    HELPDESK_PROMPT
    + """

You get one response. The user is not able to answer questions before you act.
Every response ends with a decision: either the specific action you are advising
the user to take now, or an escalation with the team it goes to. Where you need
information you do not have, state your best assessment on the information given,
name what would change it, and include the questions alongside the decision rather
than in place of it."""
)

SCENARIOS_PATH = Path(__file__).parent / "scenarios.json"
