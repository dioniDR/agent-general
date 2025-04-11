import code
import sys
import os

def main():
    banner = "Interactive Python Shell\nType 'exit()' or 'Ctrl-D' to exit."
    local_vars = {}

    # Load environment variables if needed
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                var = line.strip().split('=')
                if len(var) == 2:
                    os.environ[var[0]] = var[1]

    # Start the interactive shell
    try:
        code.interact(banner=banner, local=local_vars)
    except SystemExit:
        pass

if __name__ == '__main__':
    sys.exit(main())