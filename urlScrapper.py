# -*- coding: utf-8 -*-
import requests
from lxml import html
import json
from datetime import date
from conect_sqlite3 import dbHelper


# Returns a json with products fetched from the search page of cexuk.
def getUrlProducts():
    category = 990
    jsonItems = {"items": []}

    # Headers to allow scrapper to fetch data like it is in the category page.
    # We must iterate until we get a 'No results found'

    # "Category page" headers.
    categoryHeaders = {
        'Host': 'uk.webuy.com',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }

    # "Get more posts" headers. Must add Referer depending the category is in.
    postsHeaders = {
        'Host': 'uk.webuy.com',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': '',
        'Connection': 'keep-alive'
    }

    while category < 992:
        counter = 1
        page = requests.get(
            'https://uk.webuy.com/search/index.php?stext=*&catid=' + str(category),
            headers=categoryHeaders
        )

        tree = html.fromstring(page.content)
        first_products = tree.xpath('/html/head/script/text()')

        # Split to get only "items": [...].
        # Taking advantage of python dinamic typing, first_product is a list

        if first_products[0]:
            if '"listing":' in first_products[0]:
                first_products = first_products[0].split('"listing":')[1]

        
                # Now is a string
                first_products = first_products.split("};")[0]
                
                # Still a string
                first_products = json.loads(first_products)
                
                # Now is a json
                jsonItems['items'] += first_products['items']

        # To know when to stop, there is a hidden input value in the site
        # <input type="hidden" id="maxPage" value="the value we need">
        maxPage = tree.xpath("//input[@id='maxPage']/@value")[0]
        maxPage = 2

        while counter < (maxPage - 1):
            referer = 'https://uk.webuy.com/search/index.php?stext=*&catid=' + str(category)
            postsHeaders['Referer'] = referer

            page = requests.get(
                'https://uk.webuy.com/search/index.php?page=' + str(counter + 1) + '&stext=*&catid=' + str(category) + '&counter=' + str(counter),
                headers=postsHeaders
            )
            tree = html.fromstring(page.content)

            products = tree.xpath('/html/head/script/text()')

            # Split to get only "items": [...].
            # Taking advantage of python dinamic typing, products is a list
            products = products[0].split('"listing":')[1]
            
            # Now is a string
            products = products.split("};")[0]
            
            # Still a string
            products = json.loads(products)
            
            # Now is a json
            jsonItems['items'] += products['items']

            counter += 1

        category += 1

    #print jsonItems['items'][0]['category']
    for item in jsonItems['items']:
        print 'PRODUCTO i'

        db_url = db.save_url(item['url'], str(date.today()), str(date.today()), 1, 1)
        (db_cat, db_subcat) = db.save_category(item['category'], item['subcategory'])

        print item
        print db_url
        print db_cat



if __name__ == '__main__':
    db = dbHelper()
    if db.connect('data.db'):
        print 'conected'
        getUrlProducts()
        
        #db.con.commit()
        db.disconnect()
    else:
        print 'Error connecting to db.'
    

