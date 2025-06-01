import sys
import json
from colorama import Fore, Style

def decode_unicode(line):
    try:
        return line.encode('utf-8').decode('unicode_escape')
    except Exception:
        return line

def colorize(line):
    if "ERROR" in line:
        return f"{Fore.RED}{line}{Style.RESET_ALL}"
    elif "WARNING" in line:
        return f"{Fore.YELLOW}{line}{Style.RESET_ALL}"
    elif "INFO" in line:
        return f"{Fore.CYAN}{line}{Style.RESET_ALL}"
    return line

for line in sys.stdin:
    decoded = decode_unicode(line)
    print(colorize(decoded), end='')
