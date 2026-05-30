import asyncio
import atexit
import subprocess
import sys
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen

from mTree.development.mtree_configuration import MTreeConfiguration
from rich.markdown import Markdown
from textual import work
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Footer,
    Log,
    Markdown,
)

# from textual.widgets.option_list import Option, Separator


def start_developer_server():
    command = [
        sys.executable,
        "/workspaces/mTree/mTree/utilities/background_mtree_server.py",
        "Hello, World!",
    ]

    process = subprocess.run(command, capture_output=True, text=True, check=True)

    @atexit.register
    def shutdown_server():
        try:
            process.terminate()  # Request a graceful exit (SIGTERM on POSIX)
            process.wait(timeout=5)  # Wait for a short period for it to close
            if process.poll() is None:
                print("Subprocess did not terminate gracefully, forcing kill.")
                process.kill()  # Force termination (SIGKILL on POSIX)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(f"Error during cleanup: {e}")

    return process
    # try:
    #     # Execute the command
    #     result = subprocess.run(command, capture_output=True, text=True, check=True)

    #     # Print the output from the subprocess
    #     print("Output from subprocess:")
    #     print(result.stdout)

    # except subprocess.CalledProcessError as e:
    #     print(f"Subprocess failed with error: {e.stderr}")
    # except FileNotFoundError:
    #     print("The Python executable or script was not found.")


async def runner():
    current_directory = Path.cwd()
    proc = await run_process()
    # developer_server_monitor = DeveloperServerMonitor(proc)
    # developer_server_monitor.run()


async def run_process():

    # Example: ping 4 times

    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "/workspaces/mTree/mTree/utilities/background_mtree_server.py",
        "Hello, World!",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    print("AFLKJASFLKJAS:LFKJA:LSKFJ")
    return proc


ERROR_TEXT = """
An error has occurred. To continue:

Press Enter to return to Windows, or

Press CTRL+ALT+DEL to restart your computer. If you do this,
you will lose any unsaved information in all open applications.

Error: 0E : 016F : BFF9B3D4
"""

EXAMPLE_MARKDOWN = """\
## Markdown

- Typography *emphasis*, **strong**, `inline code` etc.    
- Headers    
- Lists    
"""


class BSOD(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Log()
        yield Footer()


class WebInfoScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_mount(self):
        # Cleanup resources
        self.content = "askljhflak;sjhf"

    def compose(self) -> ComposeResult:
        temp = MTreeConfiguration()
        temp.read_config_file()
        #         self.admin_password = "adminmtree"
        # self.subject_ids = ["A1234"]
        self.content = f"""Admin Passowrd: {temp.instance.admin_password}\n\n
        Subject IDs: {", ".join(temp.instance.subject_ids)}
        """
        markdown = Markdown(self.content)
        markdown.code_indent_guides = False
        yield markdown
        yield Footer()


class DeveloperServerMonitor(App):
    SCREENS = {"web_info": WebInfoScreen}
    BINDINGS = [
        ("1", "run", "Start Server and View Log"),
        ("b", "push_screen('web_info')", "Web Info"),
        ("ctrl+d", "quit", "Quit"),
    ]

    def on_unmount(self):
        # Cleanup resources
        self.proc.kill()

    def compose(self):
        yield Log()
        yield Footer()

    @work(exclusive=True, thread=True)
    async def action_run(self):
        log = self.query_one(Log)
        log.write("start")

        args = [
            sys.executable,
            "/workspaces/mTree/mTree/utilities/background_mtree_server.py",
            "Hello, World!",
        ]

        self.proc = Popen(args, stdout=PIPE, stderr=STDOUT, text=True)

        @atexit.register
        def shutdown_server():
            try:
                self.proc.terminate()  # Request a graceful exit (SIGTERM on POSIX)
                self.proc.wait(timeout=1)  # Wait for a short period for it to close
                if self.proc.poll() is None:
                    print("Subprocess did not terminate gracefully, forcing kill.")
                    self.proc.kill()  # Force termination (SIGKILL on POSIX)
            except subprocess.TimeoutExpired:
                self.proc.kill()
            except Exception as e:
                print(f"Error during cleanup: {e}")

        while self.proc.poll() is None:
            line = self.proc.stdout.readline()
            if line:
                self.call_from_thread(log.write, line)
