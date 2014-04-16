import arcpy
import os

#~ Funktion als Variable, es wird lesbarer
dirname = os.path.dirname
scriptDir = dirname(os.path.abspath(__file__))


toolbox = os.path.join(dirname(scriptDir), "DeltaChecker.tbx")
print toolbox
arcpy.ImportToolbox(toolbox)

arcpy.CheckLayer_deltachecker("P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12","P:/Z_Systems/GeoDB/Zusatzdaten/Arbeitsserver.sde/MRI0.FP12_FP12_A",scriptDir,"'Typ [type]';'Anzahl Dezimalstellen [scale]';'Anzahl Zeichen [length]';'Anzahl Ziffern [precision]'","'Feature-Typ [featureType]';'Geometrie [shapeType]';'hat M [hasM]'","'Bezeichnung [name]'","#","#")