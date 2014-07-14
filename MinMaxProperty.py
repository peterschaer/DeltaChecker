# -*- coding: utf-8 -*-
try:
	arcpy
except NameError:
	import arcpy
import csv

class MinMaxProperty:
	def __init__(self, oldTable, newTable, fieldName, minMaxType):
		self.oldTable = oldTable
		self.newTable = newTable
		self.fieldName = fieldName
		self.name = minMaxType
		self.alias = minMaxType
		self.order = None

		self.oldValue = self.__getValue(oldTable)
		self.newValue = self.__getValue(newTable)

		self.hasDelta = None
		if self.oldValue == self.newValue:
			self.hasDelta = False
		else:
			self.hasDelta = True

		reader = csv.DictReader(open(r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0\fieldProperties.csv"),delimiter=",")
		for row in reader:
			if row['property'] == self.name:
				self.order = int(row['order'])
		self.results = self.__getResultsDict__()

	def __getValue(self, tbl):
		if self.name == "min":
			appendix = " A"
		elif self.name == "max":
			appendix = " D"
		value = unicode(arcpy.SearchCursor(tbl, "", "", self.fieldName, self.fieldName + appendix).next().getValue(self.fieldName))
		return value
	
	def __getResultsDict__(self):
		d = {'name': self.name,
			'alias': self.alias,
			'oldValue': self.oldValue,
			'newValue': self.newValue,
			'hasDelta': self.hasDelta
			}
		return d