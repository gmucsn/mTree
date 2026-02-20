import sys

from mTree.developer_server.developer_server import DeveloperServer


def main():
    """Main function of the script."""
    name = sys.argv[1]
    developer_server = DeveloperServer()
    developer_server.run_server()


if __name__ == "__main__":
    main()
