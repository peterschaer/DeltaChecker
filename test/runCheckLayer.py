import arcpy
import os
import ast

#~ Funktion als Variable, es wird lesbarer
dirname = os.path.dirname
scriptDir = dirname(os.path.abspath(__file__))


toolbox = os.path.join(dirname(scriptDir), "DeltaChecker.tbx")
print toolbox
arcpy.ImportToolbox(toolbox)

result = arcpy.CheckLayer_deltachecker("P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12","P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12_A",scriptDir,"'Typ [type]';'Anzahl Dezimalstellen [scale]';'Anzahl Zeichen [length]';'Anzahl Ziffern [precision]'","'Feature-Typ [featureType]';'Geometrie [shapeType]';'hat M [hasM]'","'Bezeichnung [name]'","#","#")

print "HTML-Datei: " + result.getOutput(0)
print "Status: " + result.getOutput(1)

resDict = result.getOutput(2)
table = ast.literal_eval(resDict)
print table

print "Ende"