#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mysql
import sys

class dbHelper:
    # Functions to manage mysql database.
    def connect(self):
        try:
            con = mysql.connect('localhost', 'root', 'mynameis862', 'webuyscrapper')

            cur = con.cursor()
            cur.execute("SELECT VERSION()")

            ver = cur.fetchone()
            
            return con
        except mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

    # URL(id, url, last_scrap, last_success, success, is_product)
    def save_url(self, url, last_scrap, last_success, success, is_product):
        try:
            con = self.connect()
            cur = con.cursor()
            cur.execute("SELECT id from url WHERE url_dir=%s", (url,))
            row = cur.fetchone()
            if row:
                url_id = row[0]
            else:
                cur.execute("INSERT INTO url VALUES(NULL, DATE(%s), DATE(%s), %s, %s)", (last_scrap, last_success, success, url))
                url_id = cur.lastrowid

            con.commit()
            self.disconnect(con)

            return url_id
        except mysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

    # category(id, name)
    def save_category(self, category, sub_category):
        con = self.connect()
        cur = con.cursor()

        cur.execute("SELECT id from category WHERE name=%s", (category,))
        categoryRow = cur.fetchone()

        if categoryRow:
            cat_id = categoryRow[0]
            cur.execute("SELECT id from subcategory WHERE category=%s", (categoryRow,))
            subCategoryRow = cur.fetchone()
            if subCategoryRow:
                subcat_id = subCategoryRow[0]
            else:
                cur.execute("INSERT INTO subcategory VALUES(NULL,%s)",(sub_category,))
                subcat_id = cur.lastrowid
        else:
            cur.execute("INSERT INTO category VALUES(NULL,%s)",(category,))
            cat_id = cur.lastrowid
            cur.execute("INSERT INTO subcategory VALUES(NULL,%s, %s)",(sub_category, cat_id))
            subcat_id = cur.lastrowid

        con.commit()
        self.disconnect(con)
        return (cat_id, subcat_id)

    # grade(id, type, active)
    def save_grade(self, t, active):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT id from grade WHERE type=%s",(t,))
        row = cur.fetchone()
        if row:
            grade_id = row[0]
        else:
            cur.execute("INSERT INTO grade VALUES(NULL,%s,%s)",(t, active))
            grade_id = cur.lastrowid

        con.commit()
        self.disconnect(con)

        return grade_id

    # price(grade, sell_price, buy_price, voucher_price)
    def save_price(self, grade, sell_price, buy_price, voucher_price):
        con = self.connect()
        cur = con.cursor()

        grade = None if grade == '' else grade

        cur.execute("INSERT INTO price VALUES(NULL,%s,%s,%s,%s)", (grade, sell_price, buy_price, voucher_price))

        con.commit()
        self.disconnect(con)

        return cur.lastrowid

    def save_product(self, make, model, colour, capacity, img, sku, url, category, subcategory, grade, lastupdt, frequent, name,
        unit_price, cash_price, exchange_price):
        con = self.connect()
        cur = con.cursor()
        cur.execute("SELECT id, price from product WHERE sku=%s",(sku,))
        row = cur.fetchone()

        grade = None if grade == '' else grade

        if row:
            p_id = row[0]
            cur.execute("UPDATE price SET grade=%s,sell_price=%s,buy_price=%s,voucher_price=%s WHERE id=%s",
                (grade, unit_price, cash_price, exchange_price, row[1]))

            query = """UPDATE product SET make=%s,model=%s,colour=%s,capacity=%s,img=%s,sku=%s,url=%s,category=%s,sub_category=%s,grade=%s,
                last_updated=%s,frequent=%s,name=%s WHERE sku=%s"""
            cur.execute(query,(make, model, colour, capacity, img, sku, url, category, subcategory, grade, lastupdt, frequent, name, sku))
            p_id = cur.lastrowid
        else:
            price = self.save_price(grade, unit_price, cash_price, exchange_price)
            cur.execute("INSERT INTO product VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,DATE(%s),%s,%s)",
                (make, model, colour, capacity, img, sku, url, category, subcategory, grade, price, lastupdt, frequent, name))
            p_id = cur.lastrowid

        con.commit()
        self.disconnect(con)

        return p_id

    def disconnect(self, connection):
        try:
            connection.close()
        except Exception as e:
            print "error en disconect"
            print "Error %s:" % e.args[0]
            sys.exit(1)
