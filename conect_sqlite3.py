#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

class dbHelper:
    con = None

    # Functions to manage sqlite database.
    def connect(self, database):
        try:
            self.con = lite.connect(database)

            cur = self.con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')

            data = cur.fetchone()

            print "SQLite version: %s" % data
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
        finally:
            return self.con


    # URL(id, url, last_scrap, last_success, success, is_product)
    def save_url(self, url, last_scrap, last_success, success, is_product):
        cur = self.con.cursor()
        #url_string += str(is_product) + ")"

        cur.execute("INSERT INTO url VALUES(NULL,?,?,?,?)",(last_scrap, last_success, success,url))
        return cur.lastrowid


    # category(id, name, sub-category)
    def save_category(self, category, sub_category):
        cur = self.con.cursor()

        cur.execute("SELECT id from subcategory WHERE name=?",(sub_category,))
        row = cur.fetchone()
        if row:
            subcat_id = row[0]
        else:
            cur.execute("INSERT INTO subcategory VALUES(NULL,?)",(sub_category,))
            subcat_id = cur.lastrowid

        cur.execute("SELECT id from category WHERE name=?",(category,))
        row = cur.fetchone()
        if row:
            cat_id = row[0]
        else:
            cur.execute("INSERT INTO category VALUES(NULL,?,?)",(category, subcat_id))
            cat_id = cur.lastrowid

        return (cat_id, subcat_id)

    # grade(id, type, active)
    def save_grade(self, t, active):
        cur = self.con.cursor()
        cur.execute("SELECT id from grade WHERE type=?",(t,))
        row = cur.fetchone()
        if row:
            grade_id = row[0]
        else:
            cur.execute("INSERT INTO grade VALUES(NULL,?,?)",(t, active))
            grade_id = cur.lastrowid
        return grade_id

    # price(grade, sell_price, buy_price, voucher_price)
    def save_price(self, grade, sell_price, buy_price, voucher_price):
        cur = self.con.cursor()
        cur.execute("INSERT INTO price VALUES(NULL,?,?,?,?)",(grade, sell_price, buy_price, voucher_price))
        return cur.lastrowid

    def save_product(self, make, model, colour, capacity, img, sku, url, category, subcategory, grade, price, lastupdt, frequent, name):
        cur = self.con.cursor()
        cur.execute("SELECT id from product WHERE sku=?",(sku,))
        row = cur.fetchone()
        if row:
            p_id = row[0]
            query = "UPDATE product SET (make=?,model=?,colour=?,capacity=?,img=?,sku=?,url=?,category=?,subcategory=?,grade=?,price=?,"
            query += "lastupdt=?,frequent=?,name=?) WHERE sku=?"
            cur.execute(query,(make, model, colour, capacity, img, sku, url, category, subcategory, grade, price, lastupdt, frequent, name, sku))
            p_id = cur.lastrowid
        else:
            cur.execute("INSERT INTO product VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (make, model, colour, capacity, img, sku, url, category, subcategory, grade, price, lastupdt, frequent,name))
            p_id = cur.lastrowid

        return p_id

    def disconnect(self):
        try:
            if self.con:
                self.con.close()
                print "DB closed."
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
