#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from datetime import datetime


# ============================================================
# HAWK EYE
# Nmap Automation & Recon Tool
# Developer: Anas Abdullah
# ============================================================


# -------------------- Colors --------------------

GREEN = "\033[92m"
DARK_GREEN = "\033[32m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"


# -------------------- Banner --------------------

BANNER = f"""
{GREEN}{BOLD}
██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
██║  ██║██╔══██╗██║    ██║██║ ██╔╝
███████║███████║██║ █╗ ██║█████╔╝
██╔══██║██╔══██║██║███╗██║██╔═██╗
██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
{RESET}
{GREEN}              H A W K   E Y E{RESET}
{DARK_GREEN}       Nmap Automation & Recon Tool{RESET}

{GREEN}Developer :{RESET} Anas Abdullah
{GREEN}Version   :{RESET} 1.0.0
{GREEN}LinkedIn  :{RESET} www.linkedin.com/in/anas2abdullah/
"""


# -------------------- Utility Functions --------------------

def clear_screen():
    os.system("clear")


def pause():
    input(f"\n{GREEN}Press ENTER to continue...{RESET}")


def check_nmap():
    return shutil.which("nmap") is not None


def get_target():
    print(f"""
{GREEN}╭──────────────────────────────────────╮
│            TARGET INPUT               │
╰──────────────────────────────────────╯{RESET}

{WHITE}Enter an IP address or domain name.{RESET}
{DARK_GREEN}Examples:
  192.168.1.10
  scanme.nmap.org
  example.com{RESET}
""")

    while True:
        target = input(f"{GREEN}target > {RESET}").strip()

        if not target:
            print(f"{RED}[-] Target cannot be empty.{RESET}")
            continue

        # Basic shell-safety check.
        # We pass the target as a separate subprocess argument,
        # but rejecting shell metacharacters provides another
        # layer of protection.
        forbidden = [
            ";", "&", "|", "$", "`", ">",
            "<", "(", ")", "{", "}", "\n"
        ]

        if any(char in target for char in forbidden):
            print(f"{RED}[-] Invalid target format.{RESET}")
            continue

        return target


def run_nmap(arguments, target):
    """
    Run Nmap safely using subprocess argument lists.
    No shell=True is used.
    """

    command = ["nmap"] + arguments + [target]

    print(f"\n{GREEN}[+] Command:{RESET} {' '.join(command)}")
    print(f"{GREEN}[+] Starting scan...{RESET}\n")

    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if process.stdout:
            print(process.stdout)

        if process.stderr:
            print(f"{YELLOW}{process.stderr}{RESET}")

        return process.returncode, process.stdout

    except FileNotFoundError:
        print(f"{RED}[-] Nmap is not installed.{RESET}")
        print(f"{YELLOW}[!] Install it with: sudo apt install nmap{RESET}")
        return 1, ""

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Scan interrupted by user.{RESET}")
        return 130, ""

    except Exception as error:
        print(f"{RED}[-] Error: {error}{RESET}")
        return 1, ""


def save_report(target, scan_name, output):
    if not output:
        print(f"{YELLOW}[!] Nothing to save.{RESET}")
        return

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    safe_target = target.replace("/", "_").replace(":", "_")

    filename = (
        f"reports/"
        f"{safe_target}_{scan_name}_{timestamp}.txt"
    )

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("HAWK EYE - Nmap Scan Report\n")
            file.write("=" * 60 + "\n")
            file.write(f"Developer : Anas Abdullah\n")
            file.write(f"Target    : {target}\n")
            file.write(f"Scan      : {scan_name}\n")
            file.write(
                f"Time      : "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            file.write("=" * 60 + "\n\n")
            file.write(output)

        print(f"\n{GREEN}[+] Report saved:{RESET} {filename}")

    except Exception as error:
        print(f"{RED}[-] Could not save report: {error}{RESET}")


# -------------------- Scan Functions --------------------

def quick_scan():
    target = get_target()

    return run_nmap(
        ["-T4", "-F"],
        target
    )


def port_scan():
    target = get_target()

    print(f"""
{GREEN}Port Scan Options{RESET}

[1] Common ports
[2] Specific ports
[3] Full TCP port range

""")

    choice = input(f"{GREEN}port-scan > {RESET}").strip()

    if choice == "1":
        arguments = ["-T4", "--top-ports", "100"]

    elif choice == "2":
        ports = input(
            f"{GREEN}Enter ports (example: 22,80,443): {RESET}"
        ).strip()

        if not ports:
            print(f"{RED}[-] No ports entered.{RESET}")
            return 1, ""

        arguments = ["-T4", "-p", ports]

    elif choice == "3":
        arguments = ["-T4", "-p-"]

    else:
        print(f"{RED}[-] Invalid option.{RESET}")
        return 1, ""

    return run_nmap(arguments, target)


def service_detection():
    target = get_target()

    return run_nmap(
        ["-T4", "-sV"],
        target
    )


def os_detection():
    target = get_target()

    print(
        f"{YELLOW}[!] OS detection may require "
        f"root privileges.{RESET}"
    )

    return run_nmap(
        ["-T4", "-O"],
        target
    )


def aggressive_scan():
    target = get_target()

    print(
        f"{YELLOW}[!] Aggressive scan combines several "
        f"Nmap detection features.{RESET}"
    )

    return run_nmap(
        ["-T4", "-A"],
        target
    )


def custom_scan():
    target = get_target()

    print(f"""
{GREEN}Custom Nmap Arguments{RESET}

Example:
  -sV
  -sC -sV
  -p 22,80,443
  -sV --top-ports 100

{YELLOW}Enter Nmap arguments only.
The target is added automatically by HAWK EYE.{RESET}
""")

    raw_arguments = input(
        f"{GREEN}nmap-args > {RESET}"
    ).strip()

    if not raw_arguments:
        print(f"{RED}[-] No arguments entered.{RESET}")
        return 1, ""

    # Do not use shell parsing. Split simple whitespace-separated
    # Nmap arguments into individual subprocess arguments.
    arguments = raw_arguments.split()

    return run_nmap(arguments, target)


# -------------------- Menu --------------------

def main_menu():

    while True:

        print(f"""
{GREEN}╭──────────────────────────────────────╮
│            H A W K   E Y E            │
│      Nmap Automation & Recon          │
├──────────────────────────────────────┤
│ [1] Quick Scan                        │
│ [2] Port Scan                         │
│ [3] Service Detection                 │
│ [4] OS Detection                      │
│ [5] Aggressive Scan                   │
│ [6] Custom Nmap Scan                  │
│ [0] Exit                              │
╰──────────────────────────────────────╯{RESET}
""")

        choice = input(
            f"{GREEN}hawk-eye > {RESET}"
        ).strip()

        output = ""
        target = ""
        scan_name = ""

        if choice == "1":

            target = get_target()
            return_code, output = run_nmap(
                ["-T4", "-F"],
                target
            )
            scan_name = "quick_scan"

        elif choice == "2":

            target = get_target()

            print(f"""
{GREEN}Port Scan Options{RESET}

[1] Common ports
[2] Specific ports
[3] Full TCP port range
""")

            port_choice = input(
                f"{GREEN}port-scan > {RESET}"
            ).strip()

            if port_choice == "1":
                arguments = ["-T4", "--top-ports", "100"]

            elif port_choice == "2":
                ports = input(
                    f"{GREEN}Ports: {RESET}"
                ).strip()

                if not ports:
                    print(f"{RED}[-] No ports entered.{RESET}")
                    pause()
                    continue

                arguments = ["-T4", "-p", ports]

            elif port_choice == "3":
                arguments = ["-T4", "-p-"]

            else:
                print(f"{RED}[-] Invalid option.{RESET}")
                pause()
                continue

            return_code, output = run_nmap(
                arguments,
                target
            )

            scan_name = "port_scan"

        elif choice == "3":

            target = get_target()

            return_code, output = run_nmap(
                ["-T4", "-sV"],
                target
            )

            scan_name = "service_detection"

        elif choice == "4":

            target = get_target()

            print(
                f"{YELLOW}[!] OS detection may require "
                f"root privileges.{RESET}"
            )

            return_code, output = run_nmap(
                ["-T4", "-O"],
                target
            )

            scan_name = "os_detection"

        elif choice == "5":

            target = get_target()

            return_code, output = run_nmap(
                ["-T4", "-A"],
                target
            )

            scan_name = "aggressive_scan"

        elif choice == "6":

            target = get_target()

            raw_arguments = input(
                f"{GREEN}Nmap arguments: {RESET}"
            ).strip()

            if not raw_arguments:
                print(f"{RED}[-] No arguments entered.{RESET}")
                pause()
                continue

            arguments = raw_arguments.split()

            return_code, output = run_nmap(
                arguments,
                target
            )

            scan_name = "custom_scan"

        elif choice == "0":

            print(
                f"\n{GREEN}[+] Thank you for using HAWK EYE.{RESET}"
            )
            print(
                f"{DARK_GREEN}[*] Developed by "
                f"Anas Abdullah{RESET}"
            )
            sys.exit(0)

        else:

            print(
                f"{RED}[-] Invalid option. "
                f"Choose 0-6.{RESET}"
            )
            pause()
            continue

        # After every scan
        if output:

            print(f"""
{GREEN}╭──────────────────────────────────────╮
│              SCAN COMPLETE            │
╰──────────────────────────────────────╯{RESET}
""")

            save_choice = input(
                f"{GREEN}Save this result? [y/N]: {RESET}"
            ).strip().lower()

            if save_choice == "y":
                save_report(
                    target,
                    scan_name,
                    output
                )

        pause()
        clear_screen()
        print(BANNER)


# -------------------- Main --------------------

def main():

    clear_screen()
    print(BANNER)

    if not check_nmap():

        print(
            f"\n{RED}[-] Nmap was not found.{RESET}"
        )

        print(
            f"{YELLOW}[!] Install Nmap with:{RESET}"
        )

        print(
            f"{GREEN}    sudo apt install nmap{RESET}"
        )

        sys.exit(1)

    print(
        f"{GREEN}[+] Nmap detected: READY{RESET}"
    )

    print(
        f"{GREEN}[+] HAWK EYE initialized.{RESET}"
    )

    pause()

    clear_screen()
    print(BANNER)

    main_menu()


if __name__ == "__main__":
    main()