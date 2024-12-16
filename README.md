# VyKaNFLIX Netflix-Account-Checker-Tools
Netflix Account Checker
Description
Netflix Account Checker is an automated tool written in Python using Selenium to validate Netflix accounts from a combo.txt file. The tool cleans the input file, checks accounts efficiently with multi-threading, and runs the browser in headless mode for resource optimization.

Features
Automatically cleans the input file to remove invalid or improperly formatted lines.
Checks Netflix accounts in the email:password format.
Runs Edge browser in headless mode (no graphical interface) to save resources.
Utilizes multi-threading to speed up the checking process.
Outputs valid accounts to Active.txt.
System Requirements
Python 3.x
Edge Browser and EdgeDriver (compatible with your browser version).
Required libraries:
selenium
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/netflix-account-checker.git
cd netflix-account-checker
Install required dependencies:

bash
Copy code
pip install selenium
Download EdgeDriver:

Download the version compatible with your Edge browser from here.
Extract it and set the correct path for EDGEDRIVER_PATH in the code.
Usage
Create a combo.txt file in the following format:

scss
Copy code
email1@example.com:password1
email2@example.com:password2
Run the tool:

bash
Copy code
python netflix_checker_final.py
The tool will:

Display the VKaNFLIX banner.
Ask if you want to run the tool (yes/no).
Clean the input file and save the result to cleaned_combo.txt.
Check each account and save valid ones to Active.txt.
Output:

Valid accounts will be saved in Active.txt.
Example Output
Console:

yaml
Copy code
[+] Valid account: email1@example.com
[-] Invalid account: email2@example.com
Total valid accounts: 123
Tool has completed its task. Exiting.
Active.txt:

scss
Copy code
email1@example.com:password1
email3@example.com:password3
Notes
Adjust max_threads in the script to control the number of parallel browser sessions.
Ensure EdgeDriver is correctly configured to avoid compatibility issues.
License
This project is licensed under the MIT License.

