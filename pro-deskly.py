import csv
import time
import random
import pandas as pd
from playwright.sync_api import sync_playwright

def read_csv_to_lists(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    id_list = df['id'].tolist()
    name_list = df['name'].tolist()
    email_list = df['email'].tolist()
    passwords_list = df['Passwords'].tolist()
    company_name_list = df['Company name'].tolist()
    subdomain_list = df['Subdomain'].tolist()
    return id_list, name_list, email_list, passwords_list, company_name_list, subdomain_list

csv_file = 'prodesklydata.csv'
ids, names, emails, passwords, companies, subdomains = read_csv_to_lists(csv_file)

# Function to select random lat/long from CSV
def get_random_geo_location(csv_file):
    df = pd.read_csv(csv_file)
    random_row = df.sample() # Choose a random row
    latitude = random_row['Latitude'].values[0]  # Extract latitude
    longitude = random_row['Longitude'].values[0] #and longitude from the random row
    return latitude, longitude
def open_browser_with_geo_location():
    for id, company_name, subdomain, name, email, password in zip(ids, companies, subdomains, names, emails, passwords):
        with sync_playwright() as p:
            # browser = p.firefox.launch(proxy={
            #     'server': 'portal.anyip.io:1080',
            #     'username': 'user_17fc81',
            #     'password': 'a7b233'
            # }, headless=False)

            browser = p.firefox.launch_persistent_context(proxy={
                'server': '38.154.227.167:5868',
                'username': 'yweqedqg',
                'password': '4rhfhq8nan0r'
            }, headless=False, user_data_dir="userDir")

            page = browser.new_page()

            print(f'ID: {id}, Company Name: {company_name}, Subdomain: {subdomain}, Name: {name}, Email: {email}, Password: {password}')

            page.goto('https://prodeskly.com/signup', timeout=50000)
            page.fill('//input[@name="company_name"]', company_name, timeout=0)
            page.fill('//input[@placeholder="subdomain"]', subdomain, timeout=0)
            page.fill('//input[@name="name"]', name, timeout=0)
            page.fill('//input[@name="email"]', email, timeout=0)
            page.fill('//input[@name="password"]',password , timeout=0)
            page.click('(//button[@id="submit-register"])', timeout=0)
            time.sleep(8)

            try:
                element = page.query_selector("//div[text()='The sub domain has already been taken.']")
                if element:
                    # generate 2 random numbers
                    random_number = random.randint(1, 100)
                    random_number2 = random.randint(1, 100)
                    print("There Is Subdomain error")
                    page.fill('//input[@placeholder="subdomain"]', f'{subdomain}{random_number}{random_number2}', timeout=0)
                    subdomain = f'{subdomain}{random_number}{random_number2}'
                    page.click('(//button[@id="submit-register"])', timeout=0)
            except:
                pass

            time.sleep(random.randint(5, 9))
            url_of_currentlink = page.url
            time.sleep(2)

            # i want to check if in url there is lonin write or not
            if 'login' in url_of_currentlink:
                account_created = 'Account Created Successfully'
            else:
                print('its bot an its not sure account is created there will be some error')
                account_created = 'Not Sure Account Created or not'
                pass

            try:
                header = ["Id", "Company Name", "Subdomain", "Name", "Email", "Password", "Account Created"]
                with open('prodeskly-accountssss.csv', 'a+', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:  # Write header only if the file is empty
                        writer.writerow(header)
                    writer.writerow([id, company_name, subdomain, name, email, password, account_created])
            except:
                pass
            browser.close()


open_browser_with_geo_location()


