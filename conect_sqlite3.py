#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = None


# Functions to manage sqlite database.
def connect(database):
    try:
        con = lite.connect('test.db')

        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')

        data = cur.fetchone()

        print "SQLite version: %s" % data
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)


# URL(id, url, last_scrap, last_success, success, is_product)
def save_url(url, last_scrap, last_success, success, is_product):
    cur = con.cursor()
    url_string = "INSERT INTO url VALUES("
    url_string += url + ",'"
    url_string += last_scrap + "','"
    url_string += last_success + "',"
    url_string += success + ","
    url_string += is_product + ")"

    cur.execute(url_string)


# category(id, name, sub-category)
def save_category(category, sub_category):
    cur = con.cursor()
    url_string = "INSERT INTO url VALUES('"
    url_string += category + "','"
    url_string += sub_category + "')"

    cur.execute(url_string)


# grade(id, type, active)
def save_grade(type, active):
    cur = con.cursor()
    url_string = "INSERT INTO url VALUES('"
    url_string += type + "',"
    url_string += active + ")"

    cur.execute(url_string)


def disconnect():
    try:
        if con:
            con.close()
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
