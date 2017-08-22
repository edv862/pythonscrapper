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
        url_string = "INSERT INTO url VALUES("
        url_string += url + ",'"
        url_string += last_scrap + "','"
        url_string += last_success + "',"
        url_string += success + ","
        url_string += is_product + ")"

        cur.execute(url_string)


    # category(id, name, sub-category)
    def save_category(self, category, sub_category):
        cur = self.con.cursor()
        url_string = "INSERT INTO url VALUES('"
        url_string += category + "','"
        url_string += sub_category + "')"

        cur.execute(url_string)


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
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
