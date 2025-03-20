# resolver2IP
IP resolution in bulk
# IP Address Lookup Script

This Python script processes an Excel file containing IP addresses and retrieves geographical and network information for each IP using the `ip-api.com` service. The results are then written back to the Excel file.

## Prerequisites

* Python 3.6 or higher
* `openpyxl` library
* `pandas` library
* `aiohttp` library

You can install the required libraries using pip:

```bash
pip install openpyxl pandas aiohttp
Usage
Prepare your Excel file:

Create an Excel file (.xlsx) with IP addresses in the first column (column A), starting from the second row (the first row is assumed to be a header).
Run the script:

Open a terminal or command prompt.
Navigate to the directory where you saved resolver2.py.
Run the script using:
Bash

python3 resolver2.py
Provide file paths:

The script will prompt you to enter the full path to the input Excel file.
Then, it will prompt you to enter the full path to save the updated Excel file. Make sure to include .xlsx at the end of the filename.
View the results:

The script will process the IP addresses and add the following columns to your Excel file:
ASN (Autonomous System Number)
ASN Name (ISP)
Country
State/Region
The processed results will also be printed to the console.
Check error logs:

Any errors encountered during the processing will be logged in error.log in the same directory as the script.
Optimization
The script uses aiohttp for asynchronous requests, which significantly speeds up processing.
pandas is used for efficient data manipulation and Excel file handling.
Retry logic is implemented to handle temporary API errors.
Error Handling
The script logs errors and warnings to error.log.
It handles network errors, API errors, and unexpected exceptions.
If an IP address is empty, it will write "Empty" in the result columns.
Notes
The script uses the ip-api.com service, which has usage limits. Be mindful of processing very large files, as you may encounter rate limiting.
The script assumes that the first column of the Excel file contains IP addresses.
The script requires internet access to perform IP lookups.
