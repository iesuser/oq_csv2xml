#!/usr/bin/env python
# -*- coding: utf-8 -*-


# kitxvebi tunastvis
# 

import csv, sys, os, numpy
import os.path as path
import argparse as ap
from lxml import etree

simple_fault_rows_order = [[False, "source id", "source name", "tectonicRegion"],
						  [True, "faultGeometry latitude", "faultGeometry longitude"],
						  [False, "dip", "upperSeismoDepth", "lowerSeismoDepth"],
						  [False, "faultGeometry longitude", "dip"],
						  [False,"incrementalMFD minMag", "incrementalMFD binWidth", "incrementalMFD occurRates"],
						  [True,"hypo alongStrike", "hypo downDip", "hypo weight"],
						  [True, "slip value", "slip weight"]]

area_source_rows_order =  [[False, "source id", "source name", "tectonicRegion"],
						  [True, "areaGeometry latitude", "areaGeometry longitude"],
						  [False, "upperSeismoDepth", "lowerSeismoDepth"],
						  [False, "incrementalMFD minMag", "incrementalMFD binWidth", "incrementalMFD occurRates"],
						  [True, "nodalPlane strike", "nodalPlane dip","nodalPlane rake", "nodalPlane probability"],
						  [True, "hypoDepth depth", "hypoDepth probability"]]	

compex_fault_rows_order = [[False, "source id", "source name", "tectonicRegion"],
						  [True, "faultTopEdge latitude", "faultTopEdge longitude", "faultTopEdge elevation"],
						  [True, "intermediateEdge latitude", "intermediateEdge longitude", "intermediateEdge elevation"],
						  [True, "faultBottomEdge latitude", "faultBottomEdge longitude", "faultBottomEdge elevation"],
						  [False, "truncGutenbergRichterMFD aValue", "truncGutenbergRichterMFD bValue", "truncGutenbergRichterMFD minMag", "truncGutenbergRichterMFD maxMag"]
						  ]		  

replaces = {"gmlposList":"gml:posList",
			"gmlexterior":"gml:exterior",
			"gmlLinearRing":"gml:LinearRing",
			"gmlLineString":"gml:LineString",
			"xmlnsgml":"xmlns:gml"}

areasource_common_rows = ["source type","source id", "source name", "areaGeometry latitude",
						 "areaGeometry longitude", "upperSeismoDepth", "lowerSeismoDepth",
						  "magScaleRel", "ruptAspectRatio", "incrementalMFD minMag", 
						  "incrementalMFD binWidth", "incrementalMFD occurRates",
						  "nodalPlane strike", "nodalPlane dip", "nodalPlane rake", 
						  "nodalPlane probability", "hypoDepth depth", "hypoDepth probability"]

simplefault_common_rows = ["source type", "source id", "source name", "faultGeometry latitude",
							"faultGeometry longitude", "dip", "upperSeismoDepth", "lowerSeismoDepth",
							"magScaleRel", "ruptAspectRatio", "incrementalMFD minMag",
							"incrementalMFD binWidth", "incrementalMFD occurRates",	"rake", 
							"hypo alongStrike", "hypo downDip", "hypo weight", "slip value", "slip weight"]

compexfault_common_rows = ["source type", "source id", "source name", "faultTopEdge latitude", "faultTopEdge longitude", "faultTopEdge elevation",
						  "intermediateEdge latitude", "intermediateEdge longitude", "intermediateEdge elevation",
						  "faultBottomEdge latitude", "faultBottomEdge longitude", "faultBottomEdge elevation", 
						  "truncGutenbergRichterMFD aValue", "truncGutenbergRichterMFD bValue",
						  "truncGutenbergRichterMFD minMag", "truncGutenbergRichterMFD maxMag"
						  ]


errors = ""		

  
def add_error(error_text):
	global errors
	errors += "\t" + str(add_error.error_index) + ". " + error_text + '\n'
	add_error.error_index += 1
add_error.error_index = 1

def check_rows_order(source_rows, row_orders, source_start_index):
	for row_order in row_orders:
		for i in range(len(source_rows)):
			if source_rows[i][0] == row_order[1].lower():
				for j in range(1, len(row_order) - 1):
					if source_rows[i + j][0] != row_order[j + 1].lower():
						add_error("Next to '%s' must be '%s' at line %d" % (row_order[j], row_order[j + 1], source_start_index + i + j + 1))
						return
					
					if row_order[0] == True:
						for j in range(1, len(row_order) - 1):
							for l in range(2, len(source_rows[i])):
								if source_rows[i][l] == '' and source_rows[i + j][l] == '':
									break
								# print source_rows[i]
								if (source_rows[i][l] != '' and source_rows[i + j][l] == '') or (source_rows[i][l] == '' and source_rows[i + j][l] != ''):

									add_error("Following columns must have same number of values from line %d:\n\t\t" % (start_index + i + 1) + "\n\t\t".join(row_order[1:]))
									return

				# break
def check_common_rows_exist(source_rows, common_rows, source_start_index):
	for i in range(len(common_rows)):
		found = False
		for j in range(len(source_rows)):
			if common_rows[i].lower() == source_rows[j][0].lower():
				found = True
				break
		if not found:
			add_error(common_rows[i] + "does not exist in source type which begin at line " + str(source_start_index + 1))
			return False
	return True
		
			

def check_typing_errors(source_rows, source_start_index):
	if source_rows[0][2] == 'simpleFaultSource':
		if check_common_rows_exist(source_rows, simplefault_common_rows, source_start_index):
			check_rows_order(source_rows, simple_fault_rows_order, source_start_index)
	if source_rows[0][2] == 'areaSource':
		if check_common_rows_exist(source_rows, areasource_common_rows, source_start_index):
			check_rows_order(source_rows, area_source_rows_order, source_start_index)
	if 	source_rows[0][2] == 'complexFaultSource':
		if check_common_rows_exist(source_rows, compexfault_common_rows, source_start_index):
			check_rows_order(source_rows, compex_fault_rows_order, source_start_index)
def replace_tag_names(content):
	for old, new in replaces.iteritems():
		content = content.replace(old, new)
	return content

def round_value(value,decimal_number):
	x = float(value)
	y = int(decimal_number)
	rounded_value = round(x,y)
	return str(rounded_value)	


# სკიპტისთვის გდაცემული არგუმენტების წაკითხვა
parser = ap.ArgumentParser(description = "")
parser.add_argument('csv_file_name', help = 'Path of the csv file')
parser.add_argument("-o", "--output-file-path", help="Path of output xml file")
parser.add_argument("-sm", "--source_model_name", help="Name  of source_model")
args = parser.parse_args()

#source_model saxeli romelic saerto ikneba yvlea source_element - istvis
if args.source_model_name:
	source_model_name = args.source_model_name
else:
	print 'If you do not specify source model name, by default it will be "Caucasus Faults"'
	print 'You  can specify source model name like this : -sm "source model name"'
	source_model_name = 'Caucasus Faults'

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
	return (" ".join(text.split())).lower()

def area_source_generator(i, source_element):
	global xml_content
	global areaGeometry
	global incrementalMFD
	if rows[i][0] == 'source id':
		source_element.attrib['id'] = rows[i][2]
	# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'source name':
		source_element.attrib['name'] = rows[i][2]
	# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'tectonicregion':
		source_element.attrib['tectonicRegion'] = rows[i][2]
	if rows[i][0] == 'areageometry latitude':
		areaGeometry = etree.SubElement(source_element, 'areaGeometry')
		Poligon = etree.SubElement(areaGeometry, 'gmlPoligon')
		exterior = etree.SubElement(Poligon, 'gmlexterior')
		LinearRing = etree.SubElement(exterior, 'gmlLinearRing')
		posList = etree.SubElement(LinearRing, 'gmlposList')
		lat_long_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rows[i][id] !=  '':
				lat_long_pairs += '\n                ' +  rows[i][id] + ' ' + rows[i+1][id]
		posList.text = 	lat_long_pairs

	if rows[i][0] == 'upperseismodepth':
		
		upperSeismoDepth = etree.SubElement(areaGeometry, 'upperSeismoDepth')
		upperSeismoDepth.text = rows[i][2]
	

	if rows[i][0] == 'lowerseismodepth':
		lowerSeismoDepth = etree.SubElement(areaGeometry, 'lowerSeismoDepth')
		lowerSeismoDepth.text = rows[i][2]	

	if rows[i][0] == 'magscalerel':
		magScaleRel = etree.SubElement(source_element, 'magScaleRel')
		magScaleRel.text = rows[i][2]

	# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'ruptaspectratio':
		ruptAspectRatio = etree.SubElement(source_element, 'ruptAspectRatio')
		ruptAspectRatio.text = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd minmag':
		incrementalMFD = etree.SubElement(source_element, 'incrementalMFD')
		incrementalMFD.attrib['minMag'] = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd binwidth':
		incrementalMFD.attrib['binWidth'] = rows[i][2]
	# თუ შეგვხდა incrementalMFD occurRates დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd occurrates':
		occurRates = etree.SubElement(incrementalMFD, 'occurRates')
		occurrate_values = ''
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				occurrate_values += rows[i][id] + ' '
		occurRates.text = occurrate_values	

	if rows[i][0] == 'nodalplane strike':
		nodalPlaneDist = etree.SubElement(source_element, 'nodalPlaneDist')
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				nodalPlane = etree.SubElement(nodalPlaneDist, 'nodalPlane')
				nodalPlane.attrib['probability'] = rows[i+3][id]
				nodalPlane.attrib['strike'] = rows[i][id]	
				nodalPlane.attrib['dip'] = rows[i+1][id]
				nodalPlane.attrib['rake'] = rows[i+2][id]

	if rows[i][0] == 'hypodepth depth':
		hypoDepthDist = etree.SubElement(source_element, 'hypoDepthDist')
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				hypoDepth = etree.SubElement(hypoDepthDist, 'hypoDepth')
				hypoDepth.attrib['probability'] = rows[i+1][id]
				hypoDepth.attrib['depth'] = rows[i][id]							

def fault_source_generator(i, source_element):
	global xml_content
	global incrementalMFD
	global simpleFaultGeometry
	# global source_element
	if rows[i][0] == 'source id':
		source_element.attrib['id'] = rows[i][2]
	# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'source name':
		source_element.attrib['name'] = rows[i][2]
	# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'tectonicregion':
		source_element.attrib['tectonicRegion'] = rows[i][2]

	if rows[i][0] == 'faultgeometry latitude':
		simpleFaultGeometry = etree.SubElement(source_element, 'simpleFaultGeometry')
		LineString = etree.SubElement(simpleFaultGeometry, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		lat_long_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rows[i][id] !=  '':
				lat_long_pairs += '\n            ' + rows[i][id] + ' ' + rows[i+1][id]
		posList.text = 	lat_long_pairs	

	# თუ შეგვხდა dip დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'dip':
		dip = etree.SubElement(simpleFaultGeometry, 'dip')
		dip.text = rows[i][2]

	# თუ შეგვხდა upperSeismoDepth დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'upperseismodepth':
		upperSeismoDepth = etree.SubElement(simpleFaultGeometry, 'upperSeismoDepth')
		upperSeismoDepth.text = rows[i][2]
	# თუ შეგვხდა lowerSeismoDepth დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'lowerseismodepth':
		lowerSeismoDepth = etree.SubElement(simpleFaultGeometry, 'lowerSeismoDepth')
		lowerSeismoDepth.text = rows[i][2]
	# თუ შეგვხდა magScaleRel დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'magscalerel':
		magScaleRel = etree.SubElement(source_element, 'magScaleRel')
		magScaleRel.text = rows[i][2]
	# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'ruptaspectratio':
		ruptAspectRatio = etree.SubElement(source_element, 'ruptAspectRatio')
		ruptAspectRatio.text = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd minmag':
		incrementalMFD = etree.SubElement(source_element, 'incrementalMFD')
		incrementalMFD.attrib['minMag'] = rows[i][2]
	# თუ შეგვხდა incrementalMFD minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd binwidth':
		incrementalMFD.attrib['binWidth'] = rows[i][2]
	# თუ შეგვხდა incrementalMFD occurRates დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'incrementalmfd occurrates':
		occurRates = etree.SubElement(incrementalMFD, 'occurRates')
		occurrate_values = ''
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				occurrate_values += rows[i][id] + ' '
		occurRates.text = occurrate_values
	# თუ შეგვხდა rake minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'rake':
		rake = etree.SubElement(source_element, 'rake')
		rake.text = rows[i][2]	
	# თუ csv ფაილში  შეგვხდა hypo alongStrike  დავამატოთ hypoList როგორც ქვეელემენტი
	if rows[i][0] == 'hypo alongstrike':
		hypolist = etree.SubElement(source_element, 'hypoList')
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				# აქ ხდება hypo ტეგის დამატება hypolist -ის ქვეელემენტად და ივსება მისი ატრიბუტები
				hypo = etree.SubElement(hypolist, 'hypo')
				hypo.attrib['alongStrike'] = rows[i][id]
				hypo.attrib['downDip'] = rows[i+1][id]
				hypo.attrib['weight'] = rows[i+2][id]	


	# თუ შეგვხდა slip value minMag დავამატოთ slipList როგორც simpleFaultSource subelement
	if rows[i][0] == 'slip value':
		slipList = etree.SubElement(source_element, 'slipList')
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				slip = etree.SubElement(slipList, 'slip')
				slip.attrib['weight'] = rows[i+1][id]
				slip.text = rows[i][id]

def complex_fault_generator(i, source_element):
	global xml_content
	global incrementalMFD
	global complexFaultGeometry
	# global source_element
	if rows[i][0] == 'source id':
		source_element.attrib['id'] = rows[i][2]
	# თუ შეგვხდა source name დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'source name':
		source_element.attrib['name'] = rows[i][2]
	# თუ შეგვხდა tectonicRegion დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'tectonicregion':
		source_element.attrib['tectonicRegion'] = rows[i][2]
	
	if rows[i][0] == 'faulttopedge latitude':
		complexFaultGeometry = etree.SubElement(source_element, 'complexFaultGeometry')
		faultTopEdge = etree.SubElement(complexFaultGeometry, 'faultTopEdge')
		LineString = etree.SubElement(faultTopEdge, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		lat_long_elev_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rows[i][id] !=  '':
				lat_long_elev_pairs += '\n            ' + rows[i][id] + ' ' + rows[i+1][id] + ' ' + rows[i+2][id]
		posList.text = 	lat_long_elev_pairs	

	if rows[i][0] == 'intermediateedge latitude':
		complexFaultGeometry = etree.SubElement(source_element, 'complexFaultGeometry')
		faultTopEdge = etree.SubElement(complexFaultGeometry, 'faultTopEdge')
		LineString = etree.SubElement(faultTopEdge, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		lat_long_elev_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rows[i][id] !=  '':
				lat_long_elev_pairs += '\n            ' + rows[i][id] + ' ' + rows[i+1][id] + ' ' + rows[i+2][id]
		posList.text = 	lat_long_elev_pairs	

	if rows[i][0] == 'faultbottomedge latitude':
		complexFaultGeometry = etree.SubElement(source_element, 'complexFaultGeometry')
		faultTopEdge = etree.SubElement(complexFaultGeometry, 'faultTopEdge')
		LineString = etree.SubElement(faultTopEdge, 'gmlLineString')
		posList = etree.SubElement(LineString, 'gmlposList')
		lat_long_elev_pairs = ''
		for id in numpy.arange(2, len(rows[i]), 1):
			if rows[i][id] !=  '':
				lat_long_elev_pairs += '\n            ' + rows[i][id] + ' ' + rows[i+1][id] + ' ' + rows[i+2][id]
		posList.text = 	lat_long_elev_pairs	

	# თუ შეგვხდა magScaleRel დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'magscalerel':
		magScaleRel = etree.SubElement(source_element, 'magScaleRel')
		magScaleRel.text = rows[i][2]
	
	# თუ შეგვხდა ruptAspectRatio დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'ruptaspectratio':
		ruptAspectRatio = etree.SubElement(source_element, 'ruptAspectRatio')
		ruptAspectRatio.text = rows[i][2]		
	if rows[i][0] == 'truncgutenbergrichtermfd avalue':
		truncGutenbergRichterMFD = etree.SubElement(source_element, 'truncGutenbergRichterMFD')
		for id in numpy.arange(2,len(rows[i]),1):
			if rows[i][id] != '' :
				# აქ ხდება hypo ტეგის დამატება hypolist -ის ქვეელემენტად და ივსება მისი ატრიბუტები
				truncGutenbergRichterMFD.attrib['aValue'] = rows[i][id]
				truncGutenbergRichterMFD.attrib['abValue'] = rows[i+1][id]
				truncGutenbergRichterMFD.attrib['minMag'] = rows[i+2][id]
				truncGutenbergRichterMFD.attrib['maxMag'] = rows[i+3][id]

	# თუ შეგვხდა rake minMag დავამატოთ simpleFaultSource როგორც ატრიბუტი
	if rows[i][0] == 'rake':
		rake = etree.SubElement(source_element, 'rake')
		rake.text = rows[i][2]				
	

# xml ფაილის მისამართი სადაც შევინახავთ
xml_file = open(output_file_path, 'w')

# csv ფაილის შიგთავსის წაკითხვა
rows = []
source_type_indexes = []
row_index = 0
with open(csv_file_name) as csv_file:
	csv_data = csv.reader(csv_file)
	for row in csv_data:
		row[0] = rm_white_space(row[0])
		if row[0] == 'source type':
			source_type_indexes.append(row_index) 
		rows.append(row)
		row_index += 1

if rows[0][0] != 'source type':
	exit('First line of csv file must be "source type"')

for i in range(len(source_type_indexes)):
	start_index = source_type_indexes[i]
	# ინდექსი თუ არის მასივის ბოლო ელემენტზე
	if i == len(source_type_indexes) - 1:
		end_index = len(rows) - 1
	else:
		end_index = source_type_indexes[i + 1] - 1
	
	check_typing_errors(rows[start_index : end_index + 1], start_index)

# თუ გვაქვს შეცდომები დავბეჭდოთ და დავხუროთ სკრიპტი
if errors:
	exit("Errors:\n" + errors)

# aq iqmneba xml failis root element tegi tavisi atributebit da qve elementebit 
# romelic saerto ikneba shemdgomshi yvela dagenerirebuli source_element- istvis
root_element = etree.Element('nrml')
root_element.attrib['xmlnsgml'] = "http://www.opengis.net/gml"
root_element.attrib['xmlns'] = "http://openquake.org/xmlns/nrml/0.4"
source_model = etree.SubElement(root_element, 'sourceModel')
source_model.attrib['name'] = source_model_name

# წავიკითხოთ csv ფაილი ხაზხაზად
for i in range(len(rows)):
	if rows[i][0] == 'source type':
		# თუ უკვე შექმნილი იყო simpleFaultSource ვინახავთ დაგროვილ ინფორმაციას ტექსტად xml_content-ში
		source_type = rows[i][2]
		if 'source_element' in locals():
			# im shemtxvevashi tu source_element ukve arsebobda aq shemosvlisas 
			# vinaxavt source_model-shi ro ar moxdes informaciis dakargva 
			source_model.append(source_element)
		
		# am adgilas source_element iqmneba yoveltvis axlidan 
		source_element = etree.Element(rows[i][2])
	

	if source_type == 'simpleFaultSource':
		fault_source_generator(i, source_element)
	if source_type == 'areaSource':
		area_source_generator(i, source_element)
	if  source_type == 'complexFaultSource':
		complex_fault_generator(i, source_element)
# aq xdeba bolos dagenerirebuli source_element - is damateba source_model - shi 
source_model.append(source_element)
xml_content = etree.tostring(root_element, pretty_print=True)
xml_file.write(replace_tag_names(xml_content))
xml_file.close()
