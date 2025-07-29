import os
import sys
import argparse
from dotenv import load_dotenv
from knowledge_base import load_knowledge_base
from vector_store import build_vector_store, load_vector_store
from query_handler import handle_user_question_sync

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def setup_environment():
    """Set up the environment by loading the Google API key from .env file."""
    load_dotenv(dotenv_path="../.env")
    if not os.environ.get("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env file")

def run_cli():
    """Run the CLI version of the BeWhoop Bot."""
    setup_environment()
    kb_data = load_knowledge_base("../bewhoop_kb.json")
    # vectorstore = build_vector_store(kb_data)
    # Alternatively, load existing vector store
    vectorstore = load_vector_store()

    print("👋 Hey! I'm the BeWhoop Bot. I can help you with any relevant queries you have.")
    print("Just ask me something about our services, policies, or documentation!\n")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        response = handle_user_question_sync(user_input, vectorstore)

        print(f"🤖 BeWhoop Bot: {response}")

def main():
    """Main function to choose between CLI and API modes."""
    parser = argparse.ArgumentParser(description="BeWhoop Bot")
    parser.add_argument("--mode", choices=["cli", "api"], default="cli", help="Run in CLI or API mode")
    args = parser.parse_args()

    if args.mode == "cli":
        run_cli()
    else:
        from API.main import run_api
        run_api()

if __name__ == "__main__":
    main()