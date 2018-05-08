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
xml_file = open('source_model.xml', 'w')
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
for i in range(len(rows)):
	for j in range(1):
		# თუ ვდგავართ source id - ხაზზე
		if rm_white_space(rows[i][0]) == 'source id':
			# თუ უკვე შექმნილი იყო simpleFaultSource ვინახავთ დაგროვილ ინფორმაციას ტექსტად xml_content-ში
			if 'simpleFaultSource' in locals():
				xml_content += etree.tostring(simpleFaultSource, pretty_print = True)
						
			simpleFaultSource = etree.Element('simpleFaultSource')
			simpleFaultSource.attrib['id'] = rows[i][2]
		# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'source name':
			simpleFaultSource.attrib['name'] = rows[i][0]
		# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'tectonicRegion':
			simpleFaultSource.attrib['tectonicRegion'] = rows[i][0]
		
		if rm_white_space(rows[i][0]) == 'faultGeometry latitude':
			simpleFaultGeometry = etree.SubElement(simpleFaultSource,'simpleFaultGeometry')
			LineString = etree.SubElement(simpleFaultGeometry, 'gmlLineString')
			posList = etree.SubElement(LineString, 'gmlposList')
			latitude_values = ''
			longitude_values = ''
			for id in numpy.arange(2,len(rows[i]),1):
				if rm_white_space(rows[i][id]) !=  '':
					latitude_values += rows[i][id] + ' '
					longitude_values += rows[i+1][id] + ' '
			posList.text = latitude_values + '\n' + longitude_values	

		# თუ შეგვხდა dip დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'dip':
			dip = etree.SubElement(simpleFaultGeometry,rows[i][0])
			dip.text = rows[i][2]

		# თუ შეგვხდა upperSeismoDepth დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'upperSeismoDepth':
			upperSeismoDepth = etree.SubElement(simpleFaultGeometry,rows[i][0])
			upperSeismoDepth.text = rows[i][2]
		# თუ შეგვხდა lowerSeismoDepth დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'lowerSeismoDepth':
			lowerSeismoDepth = etree.SubElement(simpleFaultGeometry,rows[i][0])
			lowerSeismoDepth.text = rows[i][2]
		# თუ შეგვხდა magScaleRel დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'magScaleRel':
			magScaleRel = etree.SubElement(simpleFaultSource,rows[i][0])
			magScaleRel.text = rows[i][2]
		# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'ruptAspectRatio':
			ruptAspectRatio = etree.SubElement(simpleFaultSource,rows[i][0])
			ruptAspectRatio.text = rows[i][2]
		# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'incrementalMFD minMag':
			incrementalMFD = etree.SubElement(simpleFaultSource,'incrementalMFD')
			incrementalMFD.attrib['minMag'] = rows[i][2]
		# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'incrementalMFD binWidth':
			incrementalMFD.attrib['binWidth'] = rows[i][2]
		# თუ შეგვხდა incrementalMFD occurRates დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'incrementalMFD occurRates':
			occurRates = etree.SubElement(incrementalMFD, 'occurRates')
			occurrate_values = ''
			for id in numpy.arange(2,len(rows[i]),1):
				if rm_white_space(rows[i][id]) != '' :
					occurrate_values += rows[i][id] + ' '
			occurRates.text = occurrate_values
		# თუ შეგვხდა rake minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'rake':
			rake = etree.SubElement(simpleFaultSource,rows[i][0])
			rake.text = rows[i][2]	
		# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
		if rm_white_space(rows[i][0]) == 'hypo alongStrike':
			hypolist = etree.SubElement(simpleFaultSource,'hypoList')
			for id in numpy.arange(2,len(rows[i]),1):
				if rm_white_space(rows[i][id]) != '' :
					hypo = etree.SubElement(hypolist,'hypo')
					hypo.attrib['alongStrike'] = rows[i][id]
					hypo.attrib['downDip'] = rows[i+1][id]		

		# თუ შეგვხდა slip value minMag დავამატოთ slipList როგორც simpleFaultSource subelement
		if rm_white_space(rows[i][0]) == 'slip value':
			slipList = etree.SubElement(simpleFaultSource,'slipList')
			for id in numpy.arange(2,len(rows[i]),1):
				if rm_white_space(rows[i][id]) != '' :
					slip = etree.SubElement(slipList,'slip')
					slip.attrib['weight'] = rows[i][id]
					slip.text = rows[i+1][id]
			
xml_content += etree.tostring(simpleFaultSource, pretty_print=True)
xml_file.write(xml_content)
