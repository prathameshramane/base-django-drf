import sys
import subprocess
import os

def run_command(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(e.returncode)

def main():
    if not os.path.exists('.env'):
        print("Error: .env file not found. Please run 'python generate_env.py' first.")
        sys.exit(1)

    args = sys.argv[1:]

    command = args[0] if len(args) > 0 and not args[0].startswith("--") else None

    flags = []
    if "--build" in args:
        flags.append("--build")
    if "--nocache" in args:
        flags.append("--no-cache")

    if command is None:
        print("Starting development server...")
        run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "up"] + flags)
    elif command == "prod":
        print("Starting production server locally...")
        run_command(["docker", "compose", "-f", "docker-compose.prod.yml", "up"] + flags)
    elif command == "restart":
        print("Restarting containers...")
        if "--build" in args:
            print("Building and starting...")
            run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "up"] + flags + ["-d"])
        else:
            run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "restart"])
    elif command == "rebuild":
        print("Rebuilding containers completely...")
        run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "down", "-v"])
        run_command(["docker", "image", "prune", "-a", "-f"])
        run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "build", "--no-cache"])
        run_command(["docker", "compose", "-f", "docker-compose.dev.yml", "up", "-d"])
    else:
        print(f"Unknown command: {command}")
        print("Available commands:")
        print("  (none)      - Start dev server")
        print("  prod        - Start prod server locally")
        print("  restart     - Restart containers (supports --build, --nocache)")
        print("  rebuild     - Down containers, prune images, build no-cache, and start")

if __name__ == "__main__":
    main()
