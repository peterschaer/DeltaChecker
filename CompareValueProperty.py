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
		
		self.hasDelta = None
		if len(oldList) == 0 and len(newList) == 0:
			self.hasDelta = False
		else:
			self.hasDelta = True

		reader = csv.DictReader(open(r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0\fieldProperties.csv"),delimiter=",")
		for row in reader:
			if row['property'] == self.name:
				self.order = int(row['order'])
		self.results = self.__getResultsDict__()

	def __getValues(self, tbl):
		
		values = []
		rows = arcpy.SearchCursor(tbl, "", "", self.fieldName, self.fieldName + " A")
		for row in rows:
			values.append(unicode(row.getValue(self.fieldName)))
		uniqueValues = set(values)
		return uniqueValues
	
	def __getResultsDict__(self):
		d = {'name': self.name,
			'alias': self.alias,
			'oldValue': self.oldValue,
			'newValue': self.newValue,
			'hasDelta': self.hasDelta
			}
		return d