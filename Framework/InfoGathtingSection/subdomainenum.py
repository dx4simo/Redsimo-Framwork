# pip install dnspython
from datetime import datetime
import socket
import sys
from rich.console import Console
from rich.progress import Progress
from datetime import datetime
import time
import dns.resolver
from urllib.request import urlopen


#### Sub Enum Class
class SubdomainEnum:
    def __init__(self, console_ui):
        self.console_ui = console_ui
    
    def menu(self):
        while True:
            
            self.console_ui.print("[0] [bold]Start Enumeration")
            self.console_ui.print("[1] [bold]Show Previous Results")
            self.console_ui.print("[2] [bold]Back to the Main Menu")
            
            user_input = self.console_ui.styled_input(" >>> ", style="input")
            if user_input.strip() == "":
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
                continue
            
            try:
                user_input = int(user_input)
                if user_input == 0:
                    self.startSubdomainEnum()
                elif user_input == 1:
                    self.console_ui.print("Soon!", style="error")
                elif user_input == 2:
                    return
                else:
                    self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
            except ValueError:
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")

    def startSubdomainEnum(self):
        subdomains_url = 'https://raw.githubusercontent.com/rbsec/dnscan/master/subdomains-10000.txt'
        subdomains_list = urlopen(subdomains_url).read().decode("UTF-8").split('\n')

        # Get the domain name from user input
        domain = self.console_ui.styled_input('Enter the domain name >>> ', style="input")
        try:
            ip = socket.gethostbyname(domain)
            # Banner
            self.console_ui.print("_" * 30, style="magenta")
            self.console_ui.print(f"[bold]Start Enumeration...: [green]{domain} ({ip})")
            self.console_ui.print("Scanning started at: " + str(datetime.now().date()) + " | " + datetime.now().strftime("%I:%M %p"))
            self.console_ui.print("_" * 30, style="magenta")

            subdomain_store = []
            for subdom in subdomains_list:
                try:
                    ip_value = dns.resolver.resolve(f'{subdom}.{domain}', 'A')
                    if ip_value:
                        subdomain_store.append(f'{subdom}.{domain}')
                        self.console_ui.print(f'{subdom}.{domain} valid!', style="success")
                except dns.resolver.NXDOMAIN:
                    pass
                except dns.resolver.NoAnswer:
                    pass
                except KeyboardInterrupt:
                    quit()
                
            # Create a file to save the whois result:
            with open("subdomains.txt", "w") as file:
                with Progress(console=self.console_ui.console, transient=True) as progress:
                    task = progress.add_task("[bold magenta]Saving Subdomains ...", total=10)
                    for _ in range(10):
                        file.write(str(subdomain_store))
                        progress.update(task, advance=1)
                        time.sleep(0.8)  # Slower processing time
            self.console_ui.print("   :thumbs_up: Subdomains have been saved ==> <subdomains.txt>", style="success")
        
        except KeyboardInterrupt:  #Ctrl + C
            self.console_ui.print("\n Exiting ...", style="bold")
            sys.exit() #Exit the script
        except socket.error:
            self.console_ui.print("\n Host is not responding :cry:", style="error")
            sys.exit()
        except socket.gaierror:
            self.console_ui.print("\n The Connection Failed :(", style="error")
            sys.exit()
        except Exception as e:
            self.console_ui.print(f"\n Host is not responding :cry: => {e}", style="error")
            sys.exit()
        
