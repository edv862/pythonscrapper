# -*- coding: utf-8 -*-
import requests
import logging
import json
import re
import time

from lxml import html
from datetime import date
from conect_mysql import dbHelper
from logging.handlers import RotatingFileHandler


# https://uk.webuy.com/search/index.php?stext=*&section=
def getCategories():
    categoriIdList = []

    headers = {
        'Host': 'uk.webuy.com',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }

    page = requests.get(
        'https://uk.webuy.com/search/index.php?stext=*&section=',
        headers=headers
    )

    tree = html.fromstring(page.content)
    categoryList = tree.xpath('/html/body/div[5]/div[2]/div[2]/div[2]/div[2]/ul/li/a/@href')

    for cat in categoryList:
        categoriIdList.append(cat.split('=')[-1])

    return categoriIdList


# Returns a json with products fetched from the search page of cexuk.
def getUrlProducts():
    categories = getCategories()

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

    for cat in categories:
        products = ''
        jsonItems = {"items": []}
        counter = 1
        page = requests.get(
            'https://uk.webuy.com/search/index.php?stext=*&section=&CategoryID=' + cat,
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
        maxPage = int(tree.xpath("//input[@id='maxPage']/@value")[0])

        while counter < (maxPage - 1):
            referer = 'https://uk.webuy.com/search/index.php?stext=*&section=&CategoryID=' + cat
            postsHeaders['Referer'] = referer

            page = requests.get(
                'https://uk.webuy.com/search/index.php?page=' + str(counter + 1) + '&stext=*&section=&CategoryID=' + cat + '&counter=' + str(counter),
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

        # Process each item in current category
        for item in jsonItems['items']:
            db_grade = ''
            db_url = db.save_url('https://uk.webuy.com/'+item['url'], str(date.today()), str(date.today()), 1, 1)
            (db_cat, db_subcat) = db.save_category(item['category'], item['subcategory'])
                
            patternA = re.compile("((,.*[ |\t]A)|(\/A))(?![a-zA-Z0-9])")
            patternB = re.compile("((,.*[ |\t]B)|(\/B))(?![a-zA-Z0-9])")
            patternC = re.compile("((,.*[ |\t]C)|(\/C))(?![a-zA-Z0-9])")

            if bool(patternA.search(item['name'])):
                db_grade = db.save_grade('A', 1)
            elif bool(patternB.search(item['name'])):
                db_grade = db.save_grade('B', 1)
            elif bool(patternC.search(item['name'])):
                db_grade = db.save_grade('C', 1)

            image = 'https://uk.webuy.com/product_images/' + item['category'] + '/' + item['subcategory'] + '/' + item['id'] + '_s.jpg'

            # def save_product(self, make, model, colour, capacity, img, sku, url, category, subcategory, grade, lastupdt, frequent, name,
            # unit_price, cash_price, exchange_price):
            db.save_product(
                '', '', '', '',
                image.replace(" ","%20"),
                item['id'],
                db_url,
                db_cat,
                db_subcat,
                db_grade,
                str(date.today()),
                0,
                item['name'],
                item['unit_price'],
                item['cash_price'],
                item['exchange_price']
            )

if __name__ == '__main__':
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = '.\log'
    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    app_log = logging.getLogger('webuy')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)

    while 1:
        try:
            db = dbHelper()

            if db.connect():
                app_log.info("Conected and Updating database.")
                getUrlProducts()
                print "Finished loading all products...."
                print "Starting again in 10 min."
                app_log.info("Finished loading all products.... Starting again in 10 min.")
            else:
                app_log.error('Error connecting to db.')
        except Exception, e:
            print "Error %s" % e
            app_log.error(str(e))
        # Sleep 10 min
        time.sleep(600)
