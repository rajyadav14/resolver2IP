#!/usr/bin/python3
import asyncio
import aiohttp
import openpyxl
import pandas as pd
import logging
import os
import time

# Configure logging
logging.basicConfig(filename='error.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def ip_lookup(session, ip_address, retry_count=3):
    """Asynchronous IP lookup with retries."""
    for attempt in range(retry_count):
        try:
            url = f"http://ip-api.com/json/{ip_address}?fields=status,message,as,isp,country,regionName"
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                data = await response.json()

                if data["status"] == "fail":
                    logging.warning(f"Failed lookup (attempt {attempt+1}/{retry_count}) for {ip_address}: {data.get('message', 'Unknown error')}")
                    if attempt < retry_count - 1:
                        await asyncio.sleep(2)
                        continue
                    else:
                        return {"ASN": "Error", "ASN Name": "Error", "Country": "Error", "State": "Error"}

                return {
                    "ASN": data.get("as", "N/A"),
                    "ASN Name": data.get("isp", "N/A"),
                    "Country": data.get("country", "N/A"),
                    "State": data.get("regionName", "N/A"),
                }

        except aiohttp.ClientError as e:
            logging.error(f"Request error (attempt {attempt+1}/{retry_count}) for {ip_address}: {e}")
            if attempt < retry_count - 1:
                await asyncio.sleep(2)
                continue
            else:
                return {"ASN": "Error", "ASN Name": "Error", "Country": "Error", "State": "Error"}
        except Exception as e:
            logging.error(f"Unexpected error (attempt {attempt+1}/{retry_count}) for {ip_address}: {e}")
            if attempt < retry_count - 1:
                await asyncio.sleep(2)
                continue
            else:
                return {"ASN": "Error", "ASN Name": "Error", "Country": "Error", "State": "Error"}
    return {"ASN": "Error", "ASN Name": "Error", "Country": "Error", "State": "Error"}

async def process_ips(ips):
    """Process a list of IPs asynchronously."""
    async with aiohttp.ClientSession() as session:
        tasks = [ip_lookup(session, ip) for ip in ips]
        results = await asyncio.gather(*tasks)
        return results

if __name__ == "__main__":
    file_path = input("Enter the full path to the spreadsheet: ").strip()
    if not os.path.exists(file_path):
        print("Error: File not found.")
        exit(1)

    try:
        df = pd.read_excel(file_path, header=0, usecols=[0], names=['IP'])
        ips = df['IP'].dropna().tolist()

        results = asyncio.run(process_ips(ips))

        df[['ASN', 'ASN Name', 'Country', 'State']] = pd.DataFrame(results)

        save_path = input("Enter the full path to save the updated spreadsheet: ").strip()
        if not save_path.lower().endswith('.xlsx'):
            print("Error: Output file must be an .xlsx file")
            exit(1)

        df.to_excel(save_path, index=False)
        print(f"Spreadsheet saved successfully at {save_path}")

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        print("An error occurred. Check error.log for details.")
