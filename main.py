import subprocess
import sys

def main():
    """Main entry point for the application."""
    script_path = "scripts/replicate_chats.py"
    args = ["python", script_path] + sys.argv[1:]
    subprocess.run(args)

if __name__ == "__main__":
    main()
