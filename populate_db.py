import os
import sqlite3
import requests
import json
import pprint


def fetch_product_data(product_id):
    url = f'https://fakestoreapi.com/products/{product_id}'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    if response.status_code == 200:
        try:
            product_data = response.json()
            product_data['image'] = f"prod_images/{os.path.basename(product_data['image'])}"

            return product_data

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for product ID {product_id}: {e}")
    else:
        print(f"Failed to fetch data for product ID {product_id}. Status code: {response.status_code}")

    return None


def insert_product_data(cursor, product_data):
    cursor.execute(
        '''INSERT INTO "products_product" ("name", "description", "image", "price", "quantity", "category_id")
    VALUES (?, ?, ?, ?, ?, ?);''',
        (product_data['title'], product_data['description'], product_data['image'], product_data['price'], 10, 5))


conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
for i in range(22):
    prod_data = fetch_product_data(i)
    if prod_data:
        insert_product_data(cur, prod_data)
        print(f'id: {prod_data["id"]} image: {prod_data["image"]} done!')
conn.commit()
conn.close()
