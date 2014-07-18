# -*- coding: utf-8 -*-
import arcpy
import xml.dom.minidom
import codecs
import traceback
import os
import sys
import json
import pprint

try:
	def FeatureClassListToDict(fcList):
		fcDict = {}
		for fc in fcList:
			base = os.path.basename(fc).split(".")[1]
			fcDict[base] = fc
		return fcDict
	
	def getLegendFieldsFromINFOTables(fc):
		fields = '#' #Initial-Wert (= kein Feld bzw. leer)
# 		TODO: Zugriff auf GDBP (User GDBV) und legendenrelevante Felder der FC aus den INFO-Tabellen holen
		arcpy.AddMessage("Für diese FC werden legendenrelevante Felder geholt: " + str(fc))
		if fc == 'KLEK_WDWCHS':
			fields = 'OBJNR'
		return fields
	
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
	
	gprHasDelta = False
	deltaJSONList = []
	
	scriptPath = os.path.dirname(sys.argv[0])

	# ~ zu vergleichende, geloeschte und neue Ebenen ermitteln
	compareNames = list(newSet & oldSet)
	removedNames = list(oldSet - newSet)
	addedNames = list(newSet - oldSet)

	outputFileName = os.path.join(outputDir, gprName + ".html")
	content = u""
	
	# ~ Zu vergleichende FeatureClasses vergleichen
	for key in sorted(compareNames):
		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		
# 		key ist der Featureclass-Name ohne SDE-File und ohne Schema-Nameq
# 		newTableDict[key] ist der vollständige Pfad zur Featureclass (inkl. SDE-File und Schema-Name)
# 		Legendenrelevante Felder (aus INFO-Tabellen) sollen einem Wertevergleich unterzogen werden
		legendFields = getLegendFieldsFromINFOTables(key)
		arcpy.AddMessage("Vergleiche: " + oldTableDict[key] + " vs. " + newTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(oldTableDict[key], newTableDict[key], outputDir, "#", "#", "#", "#", legendFields)

# 		Prüfen ob die FeatureClass ein Delta aufweist
		outputFile = result.getOutput(0)
		# Der Rückgabewert von result.getOutput ist immer ein Unicode-String (http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//002z0000000n000000)
		# Der Wert muss daher mit Python-Funktionen umgewandelt werden (unicode => integer => boolean)                                                                    
		tblHasDelta = result.getOutput(1)
		
		if tblHasDelta.lower() == 'True'.lower():
			gprHasDelta = True
			
# 		Delta-JSON auslesen
		deltaJSONList.append(json.loads(result.getOutput(2)))

		DOM = xml.dom.minidom.parse(outputFile)
		content = content + DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"

		del DOM, result
		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		os.remove(outputFile)
	
	# ~ neue FeatureClasses vergleichen
	for key in sorted(addedNames):
		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		
		arcpy.AddWarning("Eine Ebene ist hinzugekommen: " + newTableDict[key])
		# ~ arcpy.AddMessage("Vergleiche: " + newTableDict[key] + " vs. " + newTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(newTableDict[key], newTableDict[key], outputDir)
		
		outputFile = result.getOutput(0)
		DOM = xml.dom.minidom.parse(outputFile)
		cnt = DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"
		content = content + cnt.replace('<div id="dcContent">', '<div id="dcContent" class="changed">')
		
# 		Delta-JSON auslesen
		deltaJSON = json.loads(result.getOutput(2))
		
# 		Tabellen-Status auf 'added' setzen
		deltaJSON['status'] = 'added'
		
# 		Delta-JSON in die Liste mit allen Delta-JSONs aufnehmen
		deltaJSONList.append(deltaJSON)

		del DOM, result

		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		os.remove(outputFile)
		
# 		Wenn es eine neue FeatureClass gibt, dann hat das Geoprodukt immer ein Delta
		gprHasDelta = True

	# ~ gelöschte FeatureClasses vergleichen
	for key in sorted(removedNames):
		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		
		arcpy.AddWarning("Eine Ebene ist verschwunden: " + oldTableDict[key])
		# ~ arcpy.AddMessage("Vergleiche: " + oldTableDict[key] + " vs. " + oldTableDict[key]) 
		result = arcpy.CheckLayer_deltachecker(oldTableDict[key], oldTableDict[key], outputDir)
		arcpy.AddMessage(result.getOutput(0))
		
		outputFile = result.getOutput(0)
		DOM = xml.dom.minidom.parse(outputFile)
		cnt = DOM.getElementsByTagName("div")[1].toxml() + "<hr/>"
		content = content + cnt.replace('<div id="dcContent">', '<div id="dcContent" class="old">')
		
# 		Delta-JSON auslesen
		deltaJSON = json.loads(result.getOutput(2))
		
# 		Tabellen-Status auf 'added' setzen
		deltaJSON['status'] = 'removed'
		
# 		Delta-JSON in die Liste mit allen Delta-JSONs aufnehmen
		deltaJSONList.append(deltaJSON)

		del DOM, result
		
		# ~ Nur wenn ImportToolbox und RemoveToolbox in der Schlaufe sind, laeuft das Script auf TS!
		arcpy.ImportToolbox(os.path.join(scriptPath, "DeltaChecker.tbx"))
		os.remove(outputFile)
		
# 		Wenn es eine gelöschte FeatureClass gibt, dann hat das Geoprodukt immer ein Delta
		gprHasDelta = True
		
	
	geruestFilePath = os.path.join(scriptHome, "geruest_utf8.txt")
	# ~ geruestFile = open(geruestFilePath,"r")
	geruestFile = codecs.open(geruestFilePath, "r", "utf-8")
	geruest = geruestFile.read()
	geruestFile.close()

	# ~ outputFile = open(outputFileName,"w")
	outputFile = codecs.open(outputFileName, "w", "utf-8")
	outputFile.write(geruest.replace('<div id="dcContent"/>', content))
	outputFile.close()
	
	# Alle Output-Parameter ausgeben	
	# Der generierte Output-Filename wird als Output-Parameter zurueckgegeben
	arcpy.SetParameterAsText(5,outputFileName)
	arcpy.SetParameter(6,unicode(gprHasDelta))
	arcpy.SetParameterAsText(7,json.dumps(deltaJSONList))
	
except Exception as e:
	arcpy.AddError(e.message)
	arcpy.AddError(traceback.format_exc())
