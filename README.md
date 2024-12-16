# **VyKaNFLIX - Netflix Account Checker Tools**

---

## **📌 Description**  
**Netflix Account Checker** is an automated tool written in **Python** that utilizes **Selenium** to validate Netflix accounts from a `combo.txt` file.  

The tool was developed by **VyyKa**, a 3rd-year student at **FPT University**. It cleans the input file, efficiently checks accounts using **multi-threading**, and runs the browser in **headless mode** to optimize system resources.

---

## **✨ Features**
- ✅ **Automatic file cleaning**: Removes invalid or improperly formatted lines from the input file.  
- ✅ **Account validation**: Checks Netflix accounts in the `email:password` format.  
- ✅ Runs the **Edge browser** in **headless mode** (no graphical interface) for resource efficiency.  
- ✅ **Multi-threading**: Processes multiple accounts simultaneously for faster checking.  
- ✅ Saves valid accounts to **Active.txt**.  

---

## **🖥️ System Requirements**
- **Python 3.x**  
- **Edge Browser** and **EdgeDriver** (compatible with your browser version).  
- Required library:
  - `selenium`

---

## **⚙️ Installation**

### **1. Clone the repository**  
```bash
git clone https://github.com/yourusername/netflix-account-checker.git
cd netflix-account-checker
```

### **2. Install required libraries**  
```bash
pip install selenium
```

### **3. Download EdgeDriver**  
- Download the version compatible with your **Edge browser** from [EdgeDriver Official](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).  
- Extract and update the path **`EDGEDRIVER_PATH`** in the script.

---

## **🚀 Usage**

### **1. Prepare the combo.txt file**  
Create a `combo.txt` file containing account details in the following format:  
```plaintext
email1@example.com:password1  
email2@example.com:password2  
```

### **2. Run the tool**  
```bash
python netflix_checker_final.py
```

### **3. Workflow**  
- Displays the **"VKaNFLIX"** banner.  
- Prompts: **"Do you want to run the tool?"** (`yes/no`).  
- Cleans the input file `combo.txt` and saves the result to `cleaned_combo.txt`.  
- Checks each account and writes valid ones to **Active.txt**.  

---

## **📝 Output**

### **📊 Console Output**
```yaml
[+] Valid account: email1@example.com  
[-] Invalid account: email2@example.com  
Total valid accounts: 123  
Tool has completed its task. Exiting.  
```

### **📄 File Active.txt**
```plaintext
email1@example.com:password1  
email3@example.com:password3  
```

---

## **⚠️ Notes**
- Adjust `max_threads` in the script to control the number of parallel browser sessions.  
- Ensure **EdgeDriver** is correctly configured to avoid compatibility issues.  

---

## **📜 License**
This project is licensed under the **MIT License**.

---

## **💡 About the Developer**
- **Name**: VyyKa  
- **Role**: 3rd-year student at **FPT University**  
- **Skills**: Python, Selenium, Automation Tools Development  

---

If you find this tool helpful, don’t forget to ⭐ **star** this repository! 🚀  

---

### **🎉 Happy Checking!**
