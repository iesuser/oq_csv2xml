#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys, os, numpy
import os.path as path
import argparse as ap
from lxml import etree

# სკიპტისთვის გდაცემული არგუმენტების წაკითხვა
parser = ap.ArgumentParser(description = "")
parser.add_argument('csv_file_name', help = 'Path of the csv file')
args = parser.parse_args()

# ფუნქცია აშორებს ზედმეტ სიცარიელეს ტექსტში
def rm_white_space(text):
	return " ".join(text.split())

#xml ფაილის მისამართი სადაც შევინახავთ
xml_file = open('test.xml', 'w')
# შევამოწმოთ მომხარებლის მიერ შეყვანილი csv  ფაილი არსებობს თუ არა
csv_file_name = args.csv_file_name
if not path.isfile(csv_file_name):
	exit( 'File %s does not exist' % csv_file_name)

# csv ფაილის შიგთავსის წაკითხვა
rows = []
with open(csv_file_name) as csv_file:
	csv_data = csv.reader(csv_file)
	for row in csv_data:
		rows.append(row)
if rm_white_space(rows[0][0]) != 'source id':
	exit('First line of csv file must be "source id"')

xml_content = ""
# წავიკითხოთ xml ფაილი ხაზხაზად
for row in rows:
	# თუ ვდგავართ source id - ხაზზე
	if rm_white_space(row[0]) == 'source id':
		# თუ უკვე შექმნილი იყო area_source ვინახავთ დაგროვილ ინფორმაციას ტექსტად xml_content-ში
		if 'area_source' in locals():
			xml_content += etree.tostring(area_source, pretty_print = True)
					
		area_source = etree.Element('simpleFaultSource')
		area_source.attrib['id'] = row[2]
	# თუ შეგვხდა source name დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'source name':
		area_source.attrib['name'] = row[2]
	# თუ შეგვხდა tectonicRegion დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'tectonicRegion':
		area_source.attrib['tectonicRegion'] = row[2]
	
	if rm_white_space(row[0]) == 'areaGeometry latitude':
		simpleFaultGeometry = etree.SubElement(area_source,'simpleFaultGeometry')
		LineString = etree.SubElement(simpleFaultGeometry, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		latitude_values = ''
		longitude_values = ''
		for id in numpy.arange(2,len(row),1):
			if row[id] != '':
				latitude_values += row[id] + ' '
		posList.text = latitude_values

	if rm_white_space(row[0]) == 'areaGeometry longitude':
		longitude_values = ''
		for id in numpy.arange(2,len(row),1):
			if row[id] != '':
				longitude_values += row[id] + ' '
		longitude_latitude_pirs = latitude_values + '\n' + longitude_values		
		posList.text = longitude_latitude_pirs	
	

	# თუ შეგვხდა dip დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'dip':
		dip = etree.SubElement(simpleFaultGeometry,row[0])
		dip.text = row[2]

	# თუ შეგვხდა upperSeismoDepth დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'upperSeismoDepth':
		upperSeismoDepth = etree.SubElement(simpleFaultGeometry,row[0])
		upperSeismoDepth.text = row[2]
	# თუ შეგვხდა lowerSeismoDepth დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'lowerSeismoDepth':
		lowerSeismoDepth = etree.SubElement(simpleFaultGeometry,row[0])
		lowerSeismoDepth.text = row[2]
	# თუ შეგვხდა magScaleRel დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'magScaleRel':
		magScaleRel = etree.SubElement(area_source,row[0])
		magScaleRel.text = row[2]
	# თუ შეგვხდა ruptAspectRatio დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'ruptAspectRatio':
		ruptAspectRatio = etree.SubElement(area_source,row[0])
		ruptAspectRatio.text = row[2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'incrementalMFD minMag':
		print 'yes'
		incrementalMFD = etree.SubElement(area_source,'incrementalMFD')
		incrementalMFD.attrib['minMag'] = row[2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'incrementalMFD binWidth':
		print 'yes'
		incrementalMFD.attrib['binWidth'] = row[2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ area_source როგორც ატრიბუტი
	if rm_white_space(row[0]) == 'incrementalMFD occurRates':
		occurRates = etree.SubElement(incrementalMFD, 'occurRates')
		values = ''
		print len(row)
		for id in numpy.arange(2,len(row),1):
			if row[id] != '':
				values += row[id] + ' '
		occurRates.text = values

		



	# area_source.attrib['ffff'] = '1'
	# prod = etree.SubElement(area_source,'test')
	

xml_content += etree.tostring(area_source, pretty_print=True)
xml_file.write(xml_content)




#   for raw in csv_data:
# 	print raw


		


