#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import requests
import re
import random
from colorama import init, Fore, Back, Style
from requests.structures import CaseInsensitiveDict

init(autoreset=True)

url = "http://www.insecam.org/en/jsoncountries/"

headers = CaseInsensitiveDict()
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
headers["Cache-Control"] = "max-age=0"
headers["Connection"] = "keep-alive"
headers["Host"] = "www.insecam.org"
headers["Upgrade-Insecure-Requests"] = "1"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

def print_banner():
    banner = """
    ╔════════════════════════════════════╗
    ║         DARK CAM v4.0             ║
    ║         AUTHOR: AMIT              ║
    ║         TEAM: DARK                ║
    ╚════════════════════════════════════╝
    """
    print(Fore.CYAN + Back.BLACK + banner)
    print(Fore.YELLOW + "Powered by Insecam - Stay in the Shadows\n")

def fetch_countries():
    resp = requests.get(url, headers=headers)
    data = resp.json()
    countries = data['countries']
    return countries

def display_countries(countries):
    print(Fore.GREEN + "Available Countries:")
    for key, value in countries.items():
        print(Fore.WHITE + f"Code: {key} - {value['country']} ({value['count']} cameras)")

def fetch_camera_ips(country_code):
    all_ips = []
    try:
        res = requests.get(f"http://www.insecam.org/en/bycountry/{country_code}", headers=headers)
        last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0]

        print(Fore.YELLOW + f"\nScanning {country_code} - Total pages: {last_page}")
        for page in range(int(last_page)):
            res = requests.get(f"http://www.insecam.org/en/bycountry/{country_code}/?page={page}", headers=headers)
            find_ip = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)
            all_ips.extend(find_ip)
            print(Fore.GREEN + f"Page {page + 1}: Found {len(find_ip)} cameras")
    except Exception as e:
        print(Fore.RED + f"Error scanning {country_code}: {e}")
    return all_ips

def main():
    print_banner()
    
    countries = fetch_countries()
    display_countries(countries)
    
    while True:
        country_code = input(Fore.MAGENTA + "\nEnter country code (e.g., US, JP): ").upper()
        if country_code in countries:
            break
        print(Fore.RED + "Invalid code! Check the list and try again.")

    camera_ips = fetch_camera_ips(country_code)
    if not camera_ips:
        print(Fore.RED + "No cameras found for this country.")
        return

    # Select 10 random IPs (or all if less than 10)
    selected_ips = random.sample(camera_ips, min(10, len(camera_ips)))
    
    print(Fore.GREEN + f"\nDisplaying 10 random camera feeds from {countries[country_code]['country']}:")
    for i, ip in enumerate(selected_ips, 1):
        print(Fore.CYAN + f"[{i}] {ip}")
    
    # Save to file
    filename = f"{country_code}_darkcam.txt"
    with open(filename, 'w') as f:
        for ip in selected_ips:
            f.write(f"{ip}\n")
    
    print(Fore.YELLOW + f"\nSaved {len(selected_ips)} links to {filename}")
    print(Fore.CYAN + "DARK CAM operation complete. Test these links in your browser!")

if __name__ == "__main__":
    main()