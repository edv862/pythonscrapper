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

        return cat_id


    # grade(id, type, active)
    def save_grade(self, type, active):
        cur = self.con.cursor()
        url_string = "INSERT INTO url VALUES('"
        url_string += type + "',"
        url_string += active + ")"

        cur.execute(url_string)


    def disconnect(self):
        try:
            if self.con:
                self.con.close()
                print "DB closed."
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
