import csv
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog, messagebox


def scrape_amazon_products(name, min_price):
    url = f"https://www.amazon.com/s?k={name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for item in soup.find_all('div', class_='s-result-item'):
        try:
            item_name = item.find('h2').text.strip()
            item_price_raw = item.find('span', class_='a-price').get_text(strip=True)
            item_price = float(''.join(filter(str.isdigit, item_price_raw))) / 100.0
            if item_price >= min_price:
                rating = item.find('span', class_='a-icon-alt').text.strip()
                products.append({'Name': item_name, 'Price': item_price, 'Rating': rating})
        except AttributeError:
            pass

    return products


def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)


def get_user_input():
    root = tk.Tk()
    root.withdraw()

    name_min_price = simpledialog.askstring("Input", "Enter product name and minimum price (separated by a comma):")
    name, min_price = name_min_price.split(',')
    min_price = float(min_price.strip())  # Convert min_price to float

    return name.strip(), min_price


if __name__ == "__main__":
    name, min_price = get_user_input()
    products = scrape_amazon_products(name, min_price)

    if products:
        save_to_csv(products, 'amaz.csv')
        messagebox.showinfo("Success", f"Product information scraped and saved to 'amaz.csv'")
    else:
        messagebox.showinfo("No Products Found", "No products found matching the criteria.")