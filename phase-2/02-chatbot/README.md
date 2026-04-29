# Chatbot

## What It Does
Consumes Anthropic API with custom system prompt providing linux assistance. Chatbot client supports load/save/clear of chat history.

## Why I Built It
This is a rebuild of an earlier prototype with much more extensive testing and far better organised code base. I made this to further refine my programming but also to prove that I can write more production oriented code rather than a single bloated .py file 

## How to Run It
```fish
cd phase-2/02-chatbot
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
cp .env.example .env  # add your ANTHROPIC_API_KEY
python main.py
```

## What I Learned
Logging module and logging levels. Importance of writing maintainable code via the separation of modules and architecture planning before writing your first lines of code. 

## What I Would Do Differently
Commands to adjust the system prompt in the program. Adding a UI (possibly a local webui). Support for md formatting in output/terminal 