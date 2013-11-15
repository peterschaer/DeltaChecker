# -*- coding: cp1252 -*-
import arcpy
import xml.dom.minidom
import codecs
import traceback
import os

try:
	def FeatureClassListToDict(fcList):
		fcDict = {}
		for fc in fcList:
			base = os.path.basename(fc).split(".")[1]
			fcDict[base] = fc
		return fcDict
		
	scriptHome = r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0"
	ws = os.path.join(scriptHome, "geodb.sde")

	gprName = arcpy.GetParameterAsText(0)
	oldTables = arcpy.GetParameterAsText(1)
	newTables = arcpy.GetParameterAsText(3)
	outputDir = arcpy.GetParameterAsText(4)

	oldTableList = oldTables.split(";")
	newTableList = newTables.split(";")
	
	oldTableDict = FeatureClassListToDict(oldTableList)
	oldSet = set(oldTableDict.keys())
	newTableDict = FeatureClassListToDict(newTableList)
	newSet = set(newTableDict.keys())

	#~ zu vergleichende, geloeschte und neue Ebenen ermitteln
	compareNames = list(newSet & oldSet)
	removedNames = list(oldSet - newSet)
	addedNames = list(newSet - oldSet)

	outputFileName = os.path.join(outputDir, gprName + ".html")
	content = u""
	
	#~ Zu vergleichende FeatureClasses vergleichen
	for key in sorted(compareNames):
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		
		arcpy.AddMessage("Vergleiche: " + oldTableDict[key] + " vs. " + newTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(oldTableDict[key], newTableDict[key], outputDir)
		arcpy.AddMessage(result.getOutput(0))
		
		outputFile = result.getOutput(0)
		DOM = xml.dom.minidom.parse(outputFile)
		content = content + DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"

		del DOM, result
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.RemoveToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		os.remove(outputFile)
	
	#~ neue FeatureClasses vergleichen
	for key in sorted(addedNames):
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		
		arcpy.AddWarning("Eine Ebene ist hinzugekommen: " + newTableDict[key])
		#~ arcpy.AddMessage("Vergleiche: " + newTableDict[key] + " vs. " + newTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(newTableDict[key], newTableDict[key], outputDir)
		arcpy.AddMessage(result.getOutput(0))
		
		outputFile = result.getOutput(0)
		DOM = xml.dom.minidom.parse(outputFile)
		cnt = DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"
		content = content + cnt.replace('<div id="dcContent">','<div id="dcContent" class="changed">')
		
		del DOM, result
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.RemoveToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		os.remove(outputFile)

	#~ gelöschte FeatureClasses vergleichen
	for key in sorted(removedNames):
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		
		arcpy.AddWarning("Eine Ebene ist verschwunden: " + oldTableDict[key])
		#~ arcpy.AddMessage("Vergleiche: " + oldTableDict[key] + " vs. " + oldTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(oldTableDict[key], oldTableDict[key], outputDir)
		arcpy.AddMessage(result.getOutput(0))
		
		outputFile = result.getOutput(0)
		DOM = xml.dom.minidom.parse(outputFile)
		cnt = DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"
		content = content + cnt.replace('<div id="dcContent">','<div id="dcContent" class="old">')
		
		del DOM, result
		#~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.RemoveToolbox(r"K:\Anwend\Tools\ArcGIS10\DeltaChecker\DeltaChecker.tbx")
		os.remove(outputFile)
	
	geruestFilePath = os.path.join(scriptHome,"geruest.txt")
	#~ geruestFile = open(geruestFilePath,"r")
	geruestFile = codecs.open(geruestFilePath,"r","iso-8859-1")
	geruest = geruestFile.read()
	geruestFile.close()

	#~ outputFile = open(outputFileName,"w")
	outputFile = codecs.open(outputFileName,"w","iso-8859-1")
	outputFile.write(geruest.replace('<div id="dcContent"/>',content))
	outputFile.close()
	
except Exception as e:
	arcpy.AddError(e.message)
	arcpy.AddError(traceback.format_exc())
