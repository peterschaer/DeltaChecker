# -*- coding: utf-8 -*-
try:
	arcpy
except NameError:
	import arcpy
import csv

class CompareValueProperty:
	def __init__(self, oldTable, newTable, fieldName):
		self.oldTable = oldTable
		self.newTable = newTable
		self.fieldName = fieldName
		self.name = "values"
		self.alias = "Werte"
		self.order = None

		self.oldValues = self.__getValues(oldTable)
		self.newValues = self.__getValues(newTable)
		
		oldList = list(self.oldValues - self.newValues)
		newList = list(self.newValues - self.oldValues)
		
		self.oldValue = " ".join(oldList)
		self.newValue = " ".join(newList)
		
		self.different = None
		if len(oldList) == 0 and len(newList) == 0:
			self.different = False
		else:
			self.different = True

		reader = csv.DictReader(open(r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0\fieldProperties.csv"),delimiter=",")
		for row in reader:
			if row['property'] == self.name:
				self.order = int(row['order'])

	def __getValues(self, tbl):
		
		values = []
		rows = arcpy.SearchCursor(tbl, "", "", self.fieldName, self.fieldName + " A")
		for row in rows:
			values.append(unicode(row.getValue(self.fieldName)))
		uniqueValues = set(values)
		return uniqueValues
