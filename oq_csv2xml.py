#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv, sys, os, numpy
import os.path as path
import argparse as ap
from lxml import etree

replaces = {"gmlposList":"gml:posList",
			"gmlexterior":"gml:exterior",
			"gmlLinearRing":"gml:LinearRing",
			"gmlLineString":"gml:LineString"}

def replace_tag_names(content):
	for old, new in replaces.iteritems():
		# print type(content)
		# print old,new
		content = content.replace(old, new)
	return content


# სკიპტისთვის გდაცემული არგუმენტების წაკითხვა
parser = ap.ArgumentParser(description = "")
parser.add_argument('csv_file_name', help = 'Path of the csv file')
parser.add_argument("-o", "--output-file-path", help="Path of output xml file")
args = parser.parse_args()

# შევამოწმოთ მომხარებლის მიერ შეყვანილი csv  ფაილი არსებობს თუ არა
csv_file_name = args.csv_file_name
if not path.isfile(csv_file_name):
	exit( 'File %s does not exist' % csv_file_name)

# შევამოწმოთ სკრიპტს მიწოდებული აქვსთ თუ არა --output-file-path პარამეტრი
if args.output_file_path:
	output_file_path = args.output_file_path
	if os.path.isdir(output_file_path):
		exit("Output file path (%s) is a directory. \nNote: It must be a file path and not a directory path" % output_file_path)

else:
	output_file_path = csv_file_name.rsplit(".", 1)[0] + ".xml"

# ფუნქცია აშორებს ზედმეტ სიცარიელეს ტექსტში
def rm_white_space(text):
	return " ".join(text.split())

# xml ფაილის მისამართი სადაც შევინახავთ
xml_file = open(output_file_path, 'w')


# csv ფაილის შიგთავსის წაკითხვა
rows = []
with open(csv_file_name) as csv_file:
	csv_data = csv.reader(csv_file)
	for row in csv_data:
		rows.append(row)
if rm_white_space(rows[0][0]) != 'source type':
	exit('First line of csv file must be "source id"')

xml_content = ""


def area_source_generator(i):
	global xml_content
	global source_element
	global areaGeometry
	global incrementalMFD
	if rm_white_space(rows[i][0]) == 'source id':
		source_element.attrib['id'] = rows[i][2]
	# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'source name':
		source_element.attrib['name'] = rows[i][2]
	# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'tectonicRegion':
		source_element.attrib['tectonicRegion'] = rows[i][2]
	if rm_white_space(rows[i][0]) == 'areaGeometry latitude':
		areaGeometry = etree.SubElement(source_element,'areaGeometry')
		gml_poligon = "gml:Poligon"
		Poligon = etree.SubElement(areaGeometry, 'gmlPoligon')
		exterior = etree.SubElement(Poligon, 'gmlexterior')
		LinearRing = etree.SubElement(exterior, 'gmlLinearRing')
		posList = etree.SubElement(LinearRing, 'gmlposList')
		lat_long_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rm_white_space(rows[i][id]) !=  '':
				lat_long_pairs += '\n            ' + rows[i][id] + ' ' + rows[i+1][id]
		posList.text = 	lat_long_pairs

	if rm_white_space(rows[i][0]) == 'upperSeismoDepth':
		
		upperSeismoDepth = etree.SubElement(areaGeometry,rows[i][0])
		upperSeismoDepth.text = rows[i][2]

	if rm_white_space(rows[i][0]) == 'lowerSeismoDepth':
		lowerSeismoDepth = etree.SubElement(areaGeometry,rows[i][0])
		lowerSeismoDepth.text = rows[i][2]	

	if rm_white_space(rows[i][0]) == 'magScaleRel':
		magScaleRel = etree.SubElement(source_element,rows[i][0])
		magScaleRel.text = rows[i][2]

	# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'ruptAspectRatio':
		ruptAspectRatio = etree.SubElement(source_element,rows[i][0])
		ruptAspectRatio.text = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'incrementalMFD minMag':
		incrementalMFD = etree.SubElement(source_element,'incrementalMFD')
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

	if rm_white_space(rows[i][0]) == 'NodalPlane strike':
		nodalPlaneDist = etree.SubElement(source_element,'nodalPlaneDist')
		for id in numpy.arange(2,len(rows[i]),1):
			if rm_white_space(rows[i][id]) != '' :
				nodalPlane = etree.SubElement(nodalPlaneDist,'nodalPlane')
				nodalPlane.attrib['probability'] = rows[i+3][id]
				nodalPlane.attrib['strike'] = rows[i][id]	
				nodalPlane.attrib['dip'] = rows[i+1][id]
				nodalPlane.attrib['rake'] = rows[i+2][id]

	if rm_white_space(rows[i][0]) == 'hypoDepth depth':
		hypoDepthDist = etree.SubElement(source_element,'hypoDepthDist')
		for id in numpy.arange(2,len(rows[i]),1):
			if rm_white_space(rows[i][id]) != '' :
				hypoDepth = etree.SubElement(hypoDepthDist,'hypoDepth')
				hypoDepth.attrib['probability'] = rows[i+1][id]
				hypoDepth.attrib['depth'] = rows[i][id]							

def fault_source_generator(i, source_element):
	global xml_content
	global incrementalMFD
	global simpleFaultGeometry
	# global source_element
	if rm_white_space(rows[i][0]) == 'source id':
		source_element.attrib['id'] = rows[i][2]
	# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'source name':
		source_element.attrib['name'] = rows[i][2]
	# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'tectonicRegion':
		source_element.attrib['tectonicRegion'] = rows[i][2]

	if rm_white_space(rows[i][0]) == 'faultGeometry latitude':
		simpleFaultGeometry = etree.SubElement(source_element,'simpleFaultGeometry')
		LineString = etree.SubElement(simpleFaultGeometry, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		lat_long_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rm_white_space(rows[i][id]) !=  '':
				lat_long_pairs += '\n          ' + rows[i][id] + ' ' + rows[i+1][id]
		posList.text = 	lat_long_pairs	

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
		magScaleRel = etree.SubElement(source_element,rows[i][0])
		magScaleRel.text = rows[i][2]
	# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'ruptAspectRatio':
		ruptAspectRatio = etree.SubElement(source_element,rows[i][0])
		ruptAspectRatio.text = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'incrementalMFD minMag':
		incrementalMFD = etree.SubElement(source_element,'incrementalMFD')
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
		rake = etree.SubElement(source_element,rows[i][0])
		rake.text = rows[i][2]	
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rm_white_space(rows[i][0]) == 'hypo alongStrike':
		hypolist = etree.SubElement(source_element,'hypoList')
		for id in numpy.arange(2,len(rows[i]),1):
			if rm_white_space(rows[i][id]) != '' :
				hypo = etree.SubElement(hypolist,'hypo')
				hypo.attrib['alongStrike'] = rows[i][id]
				hypo.attrib['downDip'] = rows[i+1][id]
				hypo.attrib['weight'] = rows[i+2][id]	


	# თუ შეგვხდა slip value minMag დავამატოთ slipList როგორც simpleFaultSource subelement
	if rm_white_space(rows[i][0]) == 'slip value':
		slipList = etree.SubElement(source_element,'slipList')
		for id in numpy.arange(2,len(rows[i]),1):
			if rm_white_space(rows[i][id]) != '' :
				slip = etree.SubElement(slipList,'slip')
				slip.attrib['weight'] = rows[i+1][id]
				slip.text = rows[i][id]

# წავიკითხოთ xml ფაილი ხაზხაზად
for i in range(len(rows)):
	if rm_white_space(rows[i][0]) == 'source type':
		# თუ უკვე შექმნილი იყო simpleFaultSource ვინახავთ დაგროვილ ინფორმაციას ტექსტად xml_content-ში
		source_type = rows[i][2]
		if 'source_element' in locals():
			xml_content += etree.tostring(source_element, pretty_print = True)
			xml_content += '\n'
		source_element = etree.Element((rm_white_space(rows[i][2])))

	if source_type == 'simpleFaultSource':
		fault_source_generator(i, source_element)
	if source_type == 'areaSource':
		area_source_generator(i)
# root_tag = etree.Element('test')
# root_tag.insert(0, source_element)
xml_content += etree.tostring(source_element, pretty_print=True)
xml_file.write(replace_tag_names(xml_content))
xml_file.close()
