# -*- coding: utf-8 -*-
try:
	arcpy
except NameError:
	import arcpy

import Property
import MinMaxProperty
import CompareValueProperty
import operator

class Field:
	def __init__(self, table1, table2, fieldName, fieldProps, minMaxFields, compareValueFields):
		self.properties = []
		self.propertiesAsDict = []
		self.name = fieldName
		self.table1 = table1
		self.table2 = table2
# 		TODO: Der status ist nicht nur abhängig davon, ob es ein neues oder gelöschtes Feld ist, sondern auch ob sich irgendeine Eigenschaft des Feldes geändert hat
		self.status = self.__determineStatus()
		fieldObj1 = self.__getFieldObject(table1)
		fieldObj2 = self.__getFieldObject(table2)
		
		for pn, an in fieldProps.items():
			print "Bearbeite Feld-Property " + pn
			if pn in ("min","max") and self.status == "stable" and self.name in minMaxFields:
				p = MinMaxProperty.MinMaxProperty(self.table1, self.table2, self.name,pn)
			elif pn in ("values") and self.status == "stable" and self.name in compareValueFields:
				p = CompareValueProperty.CompareValueProperty(self.table1, self.table2, self.name)
			else:
				p = Property.Property(fieldObj1,fieldObj2,pn,an)
			self.properties.append(p)
			self.propertiesAsDict.append(p.results)
		
		self.html = self.__createHTMLTableRow()
		self.results = self.__getResultsDict__()

	def __getResultsDict__(self):
		d = {'name': self.name,
			'properties': self.propertiesAsDict
			}
		return d		
		
	def __createHTMLTableRow(self):
		html = u""
		if self.status == "stable":
			html = "<tr><td>" + self.name + "</td>"
		elif self.status == "removed":
			html = "<tr><td><span class=\"old\">" + self.name + "</span></td>"
		elif self.status == "added":
			html = "<tr><td><span class=\"changed\">" + self.name + "</span></td>"
		for p in sorted(self.properties, key=operator.attrgetter('order')):
			if self.status == "stable":
				if p.hasDelta == True:
					html = html + "<td><span class=\"changed\">" + unicode(p.newValue) + "</span> (<span class=\"old\">" + unicode(p.oldValue) + "</span>)</td>"
				else:
					if p.newValue == None:
						html = html + "<td> </td>"
					else:
						html = html + "<td>" + unicode(p.newValue) + "</td>"
			elif self.status == "removed":
				if p.oldValue == None:
					html = html + "<td> </td>"
				else:
					html = html + "<td>" + unicode(p.oldValue) + "</td>"
			elif self.status == "added":
				if p.newValue == None:
					html = html + "<td> </td>"
				else:
					html = html + "<td>" + unicode(p.newValue) + "</td>"
		html = html + "</tr>"		
		return html
		
	def __determineStatus(self):
		result = ""
		fieldNames1 = self.__getFieldNames(self.table1)
		fieldNames2 = self.__getFieldNames(self.table2)

		if self.name in fieldNames1 and self.name in fieldNames2:
			result = "stable"
		elif self.name in fieldNames1 and self.name not in fieldNames2:
			result = "removed"
		elif self.name not in fieldNames1 and self.name in fieldNames2:
			result = "added"
		
		return result
	
	def __getFieldNames(self,tbl):
		names = []
		for f in arcpy.Describe(tbl).fields:
			names.append(f.name)
		return names
		
	def __getFieldObject(self,tbl):
		flds = arcpy.Describe(tbl).fields
		result = None
		for f in flds:
			if f.name == self.name:
				result = f
		return result
		
		

