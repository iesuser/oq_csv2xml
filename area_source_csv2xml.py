#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys, os, numpy
import os.path as path
import argparse as ap
from lxml import etree

# # სკიპტისთვის გდაცემული არგუმენტების წაკითხვა
# parser = ap.ArgumentParser(description = "")
# parser.add_argument('csv_file_name', help = 'Path of the csv file')
# args = parser.parse_args()

# # ფუნქცია აშორებს ზედმეტ სიცარიელეს ტექსტში
# def rm_white_space(text):
# 	return " ".join(text.split())

# #xml ფაილის მისამართი სადაც შევინახავთ
# xml_file = open('source_model.xml', 'w')
# # შევამოწმოთ მომხარებლის მიერ შეყვანილი csv  ფაილი არსებობს თუ არა
# csv_file_name = args.csv_file_name
# if not path.isfile(csv_file_name):
# 	exit( 'File %s does not exist' % csv_file_name)

# # csv ფაილის შიგთავსის წაკითხვა
# rows = []
# with open(csv_file_name) as csv_file:
# 	csv_data = csv.reader(csv_file)
# 	for row in csv_data:
# 		rows.append(row)
# if rm_white_space(rows[0][0]) != 'source id':
# 	exit('First line of csv file must be "source id"')


# xml_content = ""
# test = '	'
# if test.strip() == '':
# 	print 'yes'


mylist = [['a','b'],['c'],['d','e']]
a = 1
b = 2
myorder = [a,b]
new_list = list()
mylist = [ mylist[i] for i in myorder]
# for i in myorder:
# 	print i
# 	print mylist[i]
# 	new_list += mylist[i]

print mylist



x = '5141845.48548745'

print round(float(x), 3)
