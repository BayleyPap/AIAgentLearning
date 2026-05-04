from api import API
from anthropic import APIConnectionError,RateLimitError,APIStatusError
from config import QUESTIONS, SYSTEM_PROMPTS
import json
from pathlib import Path

def main():
    api = API()
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    for system_prompt in SYSTEM_PROMPTS:
        result = []
        
        for question in QUESTIONS:
            try:
                result.append({"question": question, "answer":api.query_anthropic(question,system_prompt["system"]) })
            except APIConnectionError:
                print("Issue connecting to anthropic, check network")
                result.append({"question": question, "error": "connection_error"})
            except (RateLimitError, APIStatusError):
                print("Anthropic API issue, try again later")
                result.append({"question": question, "error": "api_error"})
        write_to_file(result,output_dir / f"{system_prompt['name']}.json")
            
    
def write_to_file(data: list, path: Path):
    path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
