import nmap
import socket
import sys
import re
#from rich import print
from rich.console import Console
from rich.theme import Theme
#from rich.text import Text
from rich.progress import Progress
from rich.table import Table
from datetime import datetime
import time

#### PortScanner Class
class PortScanner:
    def __init__(self, console_ui):
        self.console_ui = console_ui
        self.previous_results = []  # Initialize as an empty list
    
    def menu(self):
        while True:
            self.console_ui.print("[0] [bold]Scan the Target")
            self.console_ui.print("[1] [bold]Show Previous Scan")
            self.console_ui.print("[2] [bold]Back to the Main Menu")
            
            user_input = self.console_ui.styled_input(" >>> ", style="input")
            
            if user_input.strip() == "":
                self.console_ui.print("Invalid choice. Please select a valid option.", style="error")
                continue
            
            try:
                user_input = int(user_input)
                if user_input == 0:
                    self.scan_ports()
                elif user_input == 1:
                    self.display_previous_results()
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

    def get_port(self, prompt):
        while True:
            try:
                return int(self.console_ui.styled_input(prompt))
            except ValueError:
                self.console_ui.print("Invalid port number. Please enter a valid port number.", style="error")

    def scan_ports(self):
        target = self.get_valid_target()
        ip = socket.gethostbyname(target)
        
        start_port = self.get_port("Specify the start range of ports: ")
        end_port = self.get_port("Specify the end range of ports: ")

        # Banner
        self.console_ui.print("_" * 30, style="magenta")
        self.console_ui.print(f"[bold]Scanning The Target: [green]{target} ({ip})[/] at Range Port [green]({start_port}-{end_port})")
        self.console_ui.print("Scanning started at: " + str(datetime.now().date()) + " | " + datetime.now().strftime("%I:%M %p"))
        self.console_ui.print("_" * 30, style="magenta")

        try:
            # Instialize the nmap.PortScanner() object
            nm = nmap.PortScanner()
            #print(nm.scan(ip, '1-100'))
            # Port range for scanning
            # Perform the scan
            self.console_ui.print("[bold][blue][*] Wait a moment... The Scanning in progress :smile:")

            open_ports = []
            for port in range(start_port, end_port + 1):
                try:

                    my_scan = nm.scan(ip, str(port))
                    result_state = my_scan['scan'][ip]['tcp'][port]['state']
                    if result_state == 'open':
                        self.console_ui.print(f'[bold][+] Port {port} is [cyan]{result_state}')
                        open_ports.append(port)
                    else:
                        self.console_ui.print(f'[bold][+] Port {port} is [red]{result_state}') 
                except KeyError:
                    continue


            # Save the Port scan result to previous_results list
            self.previous_results.append({
                "Target": target,
                "IP" : ip,
                "Ports": open_ports,
            })

            # Create a file to save the open ports:
            with open("openports.txt", "w") as file:
                with Progress(console=self.console_ui.console, transient=True) as progress:
                    task = progress.add_task("[bold magenta]Saving open ports...", total=len(open_ports))
                    for port in open_ports:
                        file.write(f'port {port} is open\n')
                        progress.update(task, advance=1)
                        time.sleep(0.8)  # Simulate processing time
                                   
            self.console_ui.print("   :thumbs_up: Open Ports have been saved ==> <openports.txt>", style="success")
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

    # Show the prevoius result
    def add_previous_result(self, result):
        self.previous_results.append(result)

    def display_previous_results(self):
        try:
            if self.previous_results:
                table = Table(title="Previous Port Scans", show_header=True, header_style="bold magenta")
                table.add_column("Target")
                table.add_column("IP")
                table.add_column("Ports")

                for result in self.previous_results:
                    table.add_row(
                        str(result.get("Target", "")),
                        str(result.get("IP", "")),
                        str(result.get("Ports", "")),
                    )

                self.console_ui.print(table)
            else:
                self.console_ui.print("No previous results available.", style="error")
        except Exception as e:
            self.console_ui.print(f"An error occurred while displaying results: {e}", style="error")
