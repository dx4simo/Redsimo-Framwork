import pyfiglet
from main_settings.ConsoleUI import ConsoleUI
from InfoGathtingSection.info_gathering import InfoGathering
from ExploitationSection.exploit_tools import Exploitation
import time

#### Main Application Class
class App:
    def __init__(self):
        self.console_ui = ConsoleUI()
        self.info_gathering = InfoGathering(self.console_ui)
        self.exploit_tools = Exploitation(self.console_ui)


    # Info. Gathering menu
    def info_show_banner(self):
        self.console_ui.print(pyfiglet.figlet_format("INFO. GATHERING"), style="bold magenta")
        self.console_ui.print("Version: 1.0", style="bold")
        self.console_ui.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console_ui.print("_" * 30, style="magenta")
        
    
    # Exploitation menu
    def exploit_show_banner(self):
        self.console_ui.print(pyfiglet.figlet_format("Exploitation Tools"), style="bold magenta")
        self.console_ui.print("Version: 1.0", style="bold")
        self.console_ui.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console_ui.print("_" * 30, style="magenta")

    def main_menu(self):
        try:

            while True:
                self.console_ui.print("*** Tools Friend ***", style="bold yellow")
                self.console_ui.print("[1] [bold]Info. Gathering")
                self.console_ui.print("[2] [bold]Exploitation")
                self.console_ui.print("[3] [bold]Quit")

                # Take input as a string first
                user_input = self.console_ui.styled_input("(Choose the Tool | q, x to exit) >>> ", style="input").lower()
                
                # Check if the user wants to exit
                if user_input in ['q', 'quit', 'exit', 'x']:
                    self.console_ui.print("Exiting...", style="bold")
                    time.sleep(0.5)
                    break
                
                if user_input.strip() == "":
                    self.console_ui.print("Invalid input. Please enter a number between 1 and 4.", style="error")
                    continue
            

                choice = int(user_input)
                if choice == 1:
                    self.info_show_banner()
                    self.info_gathering.menu()
                elif choice == 2:
                    self.exploit_show_banner()
                    self.exploit_tools.menu()
                elif choice == 3:
                    self.console_ui.print("Quitting Program...", style="bold")
                    time.sleep(0.5)
                else:
                    self.console_ui.print("Invalid choice. Please enter a number between 1 and 3.", style="error")
                    
        except ValueError:
            self.console_ui.print("Invalid input. Please enter a number between 1 and 3.", style="error")
        except KeyboardInterrupt:
            self.console_ui.print("\n Exiting ...", style="bold")
            time.sleep(0.5)

        self.console_ui.print("Program Terminated!", style="success")
        time.sleep(0.5)

if __name__ == "__main__":
    app = App()
    app.main_menu()
    
    