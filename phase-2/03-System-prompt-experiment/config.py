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
