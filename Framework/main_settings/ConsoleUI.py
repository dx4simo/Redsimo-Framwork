# pip install python-nmap, pfliglet, rich
# pyton -m rich
import pyfiglet
#from rich import print
from rich.console import Console
from rich.theme import Theme
#from rich.text import Text
from rich.table import Table
from rich.markdown import Markdown
from rich.progress import track



# ConsoleUI Class  
# ############ Main Style #################
class ConsoleUI:
    def __init__(self):
        self.theme = Theme({
            "success": "green", 
            "error": "bold red", 
            "styled_input": "bold cyan",  # Ensure this style is in the theme
            "input": "bold cyan"  # Added this style to the theme
        })
        self.console = Console(theme=self.theme)
        self.banner = pyfiglet.figlet_format("REDSIMO")
        self.console.print(self.banner, style="bold magenta")
        #main_console.print("CREATED BY: ^^^ DX4SIMO ^^^", style="bold red")
        self.console.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console.print("_" * 30, style="magenta")
        print("")

    # Function to get styled input
    def styled_input(self, prompt, style="styled_input"):
        self.console.print(prompt, style=style, end="")
        return input() # Call the built-in input function

    def print(self, message, style=None):
        self.console.print(message, style=style)



