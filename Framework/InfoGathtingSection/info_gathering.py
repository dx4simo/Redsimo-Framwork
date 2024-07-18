import pyfiglet
from .whois import WhoisClass
from .port_scanner import PortScanner
from .subdomainenum import SubdomainEnum

#### Info. Gathering Class
class InfoGathering:
    def __init__(self, console_ui):
        self.console_ui = console_ui
        self.whois = WhoisClass(self.console_ui)
        self.port_scanner = PortScanner(self.console_ui)
        self.subdomainenum = SubdomainEnum(self.console_ui)

    # Whois menu
    def whois_show_banner(self):
        self.console_ui.print(pyfiglet.figlet_format("WHOIS"), style="bold magenta")
        self.console_ui.print("Version: 1.0", style="bold")
        self.console_ui.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console_ui.print("_" * 30, style="magenta")

    # Port Scanner menu
    def port_show_banner(self):
        self.console_ui.print(pyfiglet.figlet_format("PORT SCANNER"), style="bold magenta")
        self.console_ui.print("Version: 1.0", style="bold")
        self.console_ui.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console_ui.print("_" * 30, style="magenta")

    # Subdomain Enum menu
    def subdomain_show_banner(self):
        self.console_ui.print(pyfiglet.figlet_format("Subdomain Enumeration"), style="bold magenta")
        self.console_ui.print("Version: 1.0", style="bold")
        self.console_ui.print("[bold]CREATED BY: [green]^^^[/] [red]DX4SIMO [/][green]^^^[/].")
        self.console_ui.print("_" * 30, style="magenta")

    def menu(self):
        while True:

            self.console_ui.print("[0] [bold]Whois")
            self.console_ui.print("[1] [bold]Subdomain Enumeration")
            self.console_ui.print("[2] [bold]PORT SCANNER")
            self.console_ui.print("[3] [bold]Back to the Main Menu")
            
            user_input = self.console_ui.styled_input(" >>> ", style="input")
            
            if user_input.strip() == "":
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
                continue
            
            try:
                user_input = int(user_input)
                if user_input == 0:
                    self.whois_show_banner()
                    self.whois.menu()
                if user_input == 1:
                    self.subdomain_show_banner()
                    self.subdomainenum.menu()
                elif user_input == 2:
                    self.port_show_banner()
                    self.port_scanner.menu()
                    #self.port_scanner.scan_ports()
                elif user_input == 3:
                    return
                else:
                    self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
            except ValueError:
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")


    