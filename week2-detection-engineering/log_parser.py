import re
from collections import defaultdict
import json

def parse_auth_logs(file_path):
    """
    Parses the Linux auth.log file to detect brute-force attacks.
    Extracts the IP addresses that have failed password attempts.
    """
    # Dictionary to store the count of failed attempts per IP
    # defaultdict is used for performance, avoiding KeyError when adding new IPs
    failed_attempts = defaultdict(int)

    # Regex pattern to capture the IP address specifically from 'Failed password' lines
    # Example log: "Failed password for msfadmin from 10.62.118.147 port 2222 ssh2"
    regex_pattern = r"Failed password.*from\s+(\d+\.\d+\.\d+\.\d+)"

    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                # Search for the regex pattern in the current line
                match = re.search(regex_pattern, line)
                if match:
                    # If matched, extract the first group (which is the IP address)
                    attacker_ip = match.group(1)
                    failed_attempts[attacker_ip] += 1

        return failed_attempts

    except FileNotFoundError:
        print(f"[-] Error: The file {file_path} was not found.")
        return None

def main():
    print("[+] Starting Security Log Analysis (Detection Engineering)...")
    
    # Target log file. It must be in the same directory as this script.
    log_file_path = "auth.log" 
    
    results = parse_auth_logs(log_file_path)

    if results:
        print("[+] Analysis Complete. Suspicious Activities Detected:\n")
        
        # Formatting a clean table for terminal output
        print(f"{'Attacker IP Address':<25} | {'Failed Attempts'}")
        print("-" * 45)
        
        # Sorting the dictionary by the highest number of attempts
        for ip, count in sorted(results.items(), key=lambda item: item[1], reverse=True):
            print(f"{ip:<25} | {count}")
            
        # Exporting the results to a JSON file for professional reporting
        output_file = "threat_report.json"
        with open(output_file, "w") as json_file:
            json.dump(results, json_file, indent=4)
            
        print(f"\n[+] Detailed JSON report saved successfully as '{output_file}'.")
    else:
        print("[-] No failed password attempts found or file is empty.")

if __name__ == "__main__":
    main()
