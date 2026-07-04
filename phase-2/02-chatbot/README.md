# Chatbot

## What It Does
Consumes Anthropic API with custom system prompt providing linux assistance. Chatbot client supports load/save/clear of chat history.

## Why I Built It
This is a rebuild of an earlier prototype with much more extensive testing and far better organised code base. I made this to further refine my programming but also to prove that I can write more production oriented code rather than a single bloated .py file 

## How to Run It
```bash
cd phase-2/02-chatbot
python -m venv venv
source venv/bin/activate #fish: source venv/bin/activate.fish
pip install -r requirements.txt
#create a .env with your ANTHROPIC_API_KEY
python main.py
```

## Commands
Slash commands available inside the session:

| Command | Action |
|---|---|
| `/help` | Print the command list |
| `/history` | Print the full conversation so far |
| `/save <filename>` | Save history to `<filename>.json` |
| `/load <filename>` | Load history from `<filename>.json` |
| `/clear` | Wipe history, keep the session running |
| `/quit` | Exit and print a summary |

Ctrl+C also exits cleanly with a summary. The `.json` suffix is appended automatically on save and load, so pass the name without it.

## Configuration
All settings live in `config.py`:

| Setting | Default | Purpose |
|---|---|---|
| `MODEL` | `claude-haiku-4-5-20251001` | Anthropic model. Haiku is cheapest and fine here. |
| `MAX_TOKENS` | `1024` | Response length ceiling. |
| `MAX_INPUT_LENGTH` | `2000` | Input longer than this is rejected before it hits the API. |
| `SYSTEM_PROMPT` | terse Linux persona | Defines the assistant's behaviour (see below). |

## Testing
​```bash
pytest -v
​```
Tests cover history load/save/clear and summary logic, input validation, and API error handling (connection, rate limit, and status errors).

### Default system prompt
The bot runs as a terse senior sysadmin and Linux expert: code first, one short explanation after, no preamble, no bullet points. Anything outside Linux and open-source systems gets a single refusal line, `Not a Linux concern.`

Change the persona by editing `SYSTEM_PROMPT` in `config.py`. Nothing else needs to change; the full prompt string lives there so it stays in one place.

## What I Learned
Logging module and logging levels. Importance of writing maintainable code via the separation of modules and architecture planning before writing your first lines of code. 

## What I Would Do Differently
Commands to adjust the system prompt in the program. Adding a UI (possibly a local webui). Support for md formatting in output/terminal 
