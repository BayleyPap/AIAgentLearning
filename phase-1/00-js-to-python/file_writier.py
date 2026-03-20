from pathlib import Path


def write_lines_to_file(lines):
    Path("data.txt").write_text("\n".join(lines) + "\n", encoding="UTF-8")


write_lines_to_file(["Hello!", "My name is Bayley", "Nice to meet you!"])
