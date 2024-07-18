import whois
import socket
import sys
import re
from rich.console import Console
from rich.progress import Progress
from datetime import datetime
import time


#### Whois Class
class WhoisClass:
    def __init__(self, console_ui):
        self.console_ui = console_ui


    def menu(self):
        while True:

            self.console_ui.print("[0] [bold]Start Scan")
            self.console_ui.print("[1] [bold]Show Previous Scans")
            self.console_ui.print("[2] [bold]Back to the Main Menu")
            
            user_input = self.console_ui.styled_input(" >>> ", style="input")
            
            if user_input.strip() == "":
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
                continue
            
            try:
                user_input = int(user_input)
                if user_input == 0:
                    self.whois()
                elif user_input == 1:
                    self.console_ui.print("Soon!", style="error")
                elif user_input == 2:
                    return
                else:
                    self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
            except ValueError:
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
    
    
    # Function to validate IP addresses
    def is_valid_ip(self, address):
        try:
            socket.inet_aton(address)
            return True
        except socket.error:
            return False

    # Function to validate URLs
    def is_valid_url(self, url):
        # Advanced regex to validate URLs and domain names...
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # Domain...
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # Domain extension
            r'|'  # OR
            r'localhost'  # localhost
            r'|'  # OR
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IPv4
            r'|'  # OR
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?'  # IPv6
            r'|'  # OR
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # Domain name without protocol
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)'  # Domain extension
            r'(?:/?|[/?]\S+)?$', re.IGNORECASE)
        return re.match(regex, url) is not None

     # Function to get a valid target
    def get_valid_target(self):
        while True:
            target = self.console_ui.styled_input("Enter the Target to scan (URL or IP) >>> ", style="input")
            if self.is_valid_ip(target) or self.is_valid_url(target):
                return target
            else:
                self.console_ui.print("Invalid URL or IP address. Please enter a valid URL or IP address.", style="error")


    def is_registered(self, url):
        try:
            domain = whois.whois(url)
        except Exception as e:
            print(f"Error has occured {e}")
            return False
        else:
            return bool(domain.domain_name)
    

    def whois(self):
        target = self.get_valid_target()
        ip = socket.gethostbyname(target)

        try:

            # Banner
            self.console_ui.print("_" * 30, style="magenta")
            self.console_ui.print(f"[bold]Whois The Target: [green]{target} ({ip})")
            self.console_ui.print("Scanning started at: " + str(datetime.now().date()) + " | " + datetime.now().strftime("%I:%M %p"))
            self.console_ui.print("_" * 30, style="magenta")

            if self.is_registered(ip):
                whois_info = whois.whois(ip)
                self.console_ui.print("[bold][blue][*] Wait a moment... The Scanning in progress :smile:")
                self.console_ui.print(f'[bold][+] Domain Registrar =>[cyan] {whois_info.registrar}')
                self.console_ui.print(f'[bold][+] Domain Server =>[cyan] {whois_info.whois_server}')
                self.console_ui.print(f'[bold][+] Creation Date =>[cyan] {whois_info.creation_date}')
                self.console_ui.print(f'[bold][+] Expiration Date =>[cyan] {whois_info.expiration_date}')
                self.console_ui.print(f'[bold][+] Name Servers =>[cyan] {whois_info.name_servers}')
                self.console_ui.print(f'[bold][+] All Info =>[cyan] {whois_info}')
                
                time.sleep(0.8)

                # Create a file to save the whois result:
                with open("whoisresult.txt", "w") as file:
                    with Progress(console=self.console_ui.console, transient=True) as progress:
                        task = progress.add_task("[bold magenta]Saving Whois result...", total=10)
                        for _ in range(10):
                            file.write(str(whois_info))
                            progress.update(task, advance=1)
                            time.sleep(0.8)  # Slower processing time
                self.console_ui.print("   :thumbs_up: Whois result have been saved ==> <whoisresult.txt>", style="success")
        
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

    