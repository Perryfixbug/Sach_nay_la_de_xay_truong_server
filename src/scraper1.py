import requests, os
from bs4 import BeautifulSoup
from random import randint
# from cs50 import SQL
import sqlite3

print('SCAN TU TRANG NAO DEN TRANG NAO:')
input = input()
start, end = input.split()
start, end = int(start), int(end)

# db = SQL('sqlite:///DB.db')
create_table_query = """
CREATE TABLE IF NOT EXISTS "product" (
	"id"	INTERGER NOT NULL,
	"name"	VARCHAR(100) NOT NULL,
	"img"	VARCHAR(100) NOT NULL,
	"price"	INTEGER NOT NULL,
	"author"	VARCHAR(50) NOT NULL,
	"detail"	VARCHAR(200),
	"category"	VARCHAR(50) NOT NULL,
	"stock"	INTEGER,
	PRIMARY KEY("id")
);
"""

create_placeholder_value = """INSERT INTO product ("id", "name", "img", "price", "author", "detail", "category", "stock") VALUES ('0', 'placeholder', 'https://google.com', '69420', 'tao', 'lam deo gi co detail', '2 10', '-1');"""

# print(os.path.dirname(__file__) + '/user.db')

dirname = os.path.dirname(__file__)
conn = sqlite3.connect(dirname + '/user.db')
cursor = conn.cursor()
check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product';").fetchone()[0]

tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
# print(tables)

# print(check)

if check != 'product':
    cursor.execute(create_table_query)
    cursor.execute(create_placeholder_value)
    conn.commit()

# print(conn.total_changes)

for numpg in range(start, end):
    print(numpg)
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'My User Agent 1.0',
        }
    )
    src_link = 'https://www.fahasa.com/sach-trong-nuoc.html?order=num_orders&limit=24&p=' + str(numpg)
    response = requests.get(src_link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    titles = soup.findAll('h2', class_='p-name-list')
    links = [link.find('a').attrs['href'] for link in titles]
    # print(links)
    # print(cursor.execute('SELECT id, name, img, price, author, detail, genre, stock FROM product').fetchall())
    # img_count, name_count, price_count, desc_count, category_count = 0, 0, 0, 0, 0
    id = cursor.execute('SELECT MAX(id) FROM product').fetchone()[0]
    # print(type(id))
    for link in links:
        # print(link)
        book = requests.get(link, headers=headers)
        soup = BeautifulSoup(book.content, 'html.parser')
        temp_name = soup.find('h1', class_='fhs_name_product_desktop')
        name = 'temp'
        # print(name)
        if temp_name and name != temp_name.text:
            # print(id)
            # print(temp_name.text)
            name = temp_name.text
            # print(name)
            # name_count += 1
            # img_count += 1
            # print(name)
            price_finder = soup.find('p', class_='special-price')
            price = price_finder.find('span', class_='price').text
            # price_count += 1
            # print(price)
            author_finder = soup.find('td', class_='data_author')
            if author_finder:    
                author = author_finder.text
                # print(author)
                desc_finder = soup.find('div', id='product_tabs_description_contents')
                if desc_finder:
                    desc = desc_finder.text
                    # desc_count += 1
                    # print(desc)
                    # print('DEM =', desc_count)
                    category_finder = soup.findAll('td', class_='data_genres')
                    cf = category_finder
                    category = ''
                    for i in category_finder:
                        cf = i.find('div', class_='attribute_link_container').text
                        # print(cf)
                        # arr = cf.strip(", ")
                        # print(arr.type())
                        for j in cf.split(",\xa0"):
                            # print(j)
                            if j in ["Comedy", "Adventure", "Action", "Fantasy", "Sci Fi", "Supernatural", "Romance", "Horror"]:
                                category = category + j +" "
                    # print(category)
                    if category != '':
                        # category_count += 1
                        # print(category_count, category)
                        # break
                        # stock_finder = soup.find('div', class_='product-view-qty-num')
                        stock = randint(1, 99999)
                        # print(stock)
                        id += 1
                        img_finder = soup.find('div', class_='swiper-wrapper-item')
                        img = img_finder.find('img').attrs['src']
                        img_name = link.split(".html")
                        img_name = str(img_name[0])
                        # print(img_name)
                        img_name = img_name.split("https://www.fahasa.com/")
                        img_name = str(img_name[1])
                        # print(img_name)
                        with open(dirname + '/image/' + img_name + '.jpg', 'wb') as file:
                            # print(file.name)
                            download = requests.get(img)
                            file.write(download.content)
                        image = img_name + '.jpg'
                        print(image)
                        # break
                        cursor.execute('INSERT INTO product (id, name, img, price, author, detail, category, stock) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (id, name, image, price, author, desc, category, stock))
                        # print(id, name, image, price, author, desc, category, stock)
                        conn.commit()
                        # print(id)
cursor.close()
conn.close()
#"Comedy", "Adventure", "Action", "Fantasy", "Sci Fi", "Supernatural", "Romance", "Horror"
# 'Adventure,\xa0Comedy,\xa0Drama,\xa0Mystery,\xa0Romance,\xa0School Life,\xa0Shounen'