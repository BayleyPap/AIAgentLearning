import logging

from agent import run_react_loop


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    query = input("What is your query?>")
    print(run_react_loop(query))


if __name__ == "__main__":
    main()
