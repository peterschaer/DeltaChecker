# -*- coding: cp1252 -*-
try:
	arcpy
except NameError:
	import arcpy

import Table
import os.path
import uuid
import sys
import xml.dom.minidom
import codecs
import traceback
import operator

def processParameter(paramString):
	propList = {}
	params = paramString.split(";")
	for param in params:
		parts = param.split("[")
		name = parts[0][1:-1]
		code = parts[1][:-2]
		propList[code] = name
	return propList
	
def getTableName(table):
	desc = arcpy.Describe(table)
	name = desc.name
	if "." in name:
		name = name.split(".")[1]
	return name
try:
	scriptHome = r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0"

	oldTable = arcpy.GetParameterAsText(0)
	newTable = arcpy.GetParameterAsText(1)

	fieldProperties = processParameter(arcpy.GetParameterAsText(3))
	tableProperties = processParameter(arcpy.GetParameterAsText(4))
	spatrefProperties = processParameter(arcpy.GetParameterAsText(5))

	#~ Felder für die die Minimum- und Maximum-Werte verglichen werden
	minMaxFields = arcpy.GetParameterAsText(6)
	if len(minMaxFields) > 0:
		fieldProperties["min"] ="Minimum"
		fieldProperties["max"] ="Maximum"

	#~ Felder für die die Werte miteinander verglichen werden
	compareValueFields = arcpy.GetParameterAsText(7)
	if len(compareValueFields) > 0:
		fieldProperties["values"] = "Werte"

	content = u"<div id=\"dcContent\">"

	outputDir = arcpy.GetParameterAsText(2)
	filename = str(uuid.uuid4()) + ".html"
	outputFile = os.path.join(outputDir, filename)
	#~ Der generierte Output-Filename wird als Output-Parameter zurueckgegeben
	arcpy.SetParameterAsText(8,outputFile)

	#~ outFile = open(outputFile,"w")
	outFile = codecs.open(outputFile,"w","iso-8859-1")

	t = Table.Table(oldTable, newTable, tableProperties, fieldProperties, spatrefProperties, minMaxFields, compareValueFields)

	geruestFilePath = os.path.join(scriptHome,"geruest.txt")
	#~ geruestFile = open(geruestFilePath,"r")
	geruestFile = codecs.open(geruestFilePath,"r","iso-8859-1")
	geruest = geruestFile.read()
	geruestFile.close()

	if arcpy.Describe(newTable).datasetType != "Table":
		content = content + "<h3>Ebene: " + getTableName(newTable) + "</h3>"
		content = content + "<p>Ebene alt: " + oldTable + "</p>"
		content = content + "<p>Ebene neu: " + newTable + "</p>"
	else:
		content = content + "<h3>Tabelle: " + getTableName(newTable) + "</h3>"
		content = content + "<p>Tabelle alt: " + oldTable + "</p>"
		content = content + "<p>Tabelle neu: " + newTable + "</p>"

	#~ Eigenschaften der Tabelle ausgeben
	if len(tableProperties) > 0:
		if arcpy.Describe(oldTable).datasetType == "Table":
			content = content + "<h4>Eigenschaften der Tabelle</h4>"
		else:
			content = content + "<h4>Eigenschaften der Ebene</h4>"
		content = content + t.tablePropertiesHTML

	#~ Eigenschaften der SpatialReference ausgeben
	if len(spatrefProperties) > 0:
		if arcpy.Describe(oldTable).datasetType != "Table":
			content = content + "<h4>Eigenschaften der Spatial Reference</h4>"
			content = content + t.spatrefPropertiesHTML

	#~ Eigenschaften der Felder ausgeben
	content = content + "<h4>Eigenschaften der Felder</h4>"
	fields = t.fields

	content = content +"<table><tr><th>Feldname</th>"
	#~ for k,v in fieldProperties.items():
		#~ content = content + "<th>" + v + "</th>"
	if len(t.fields) > 0:
		for prop in sorted(fields[0].properties, key=operator.attrgetter('order')):
			content = content + "<th>" + prop.alias + "</th>"
	else:
		for k,v in fieldProperties.items():
			content = content + "<th>" + v + "</th>"
	content = content + "</tr>"

	for f in fields:
		content = content + f.html
	content = content + "</table></div>"

	outFile.write(geruest.replace('<div id="dcContent"/>',content))
	outFile.close()

except Exception as e:
	arcpy.AddError(e.message)
	arcpy.AddError(traceback.format_exc())

