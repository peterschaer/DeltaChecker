# -*- coding: cp1252 -*-
try:
	arcpy
except NameError:
	import arcpy
import csv


class Property:
	def __init__(self, oldObject, newObject, propName,propAlias):
		self.name = propName
		self.alias = propAlias
		self.oldValue = None
		self.newValue = None
		self.different = None
		self.order = None
		
		if oldObject != None:
			if hasattr(oldObject,self.name):
				self.oldValue = getattr(oldObject,self.name)

		if newObject != None:
			if hasattr(newObject,self.name):
				self.newValue = getattr(newObject,self.name)
				
		if self.oldValue == self.newValue:
			self.different = False
		else:
			self.different = True

		reader = csv.DictReader(open(r"\\geodb.infra.be.ch\freigabe\Anwendungen\DeltaChecker\v10.0.0\fieldProperties.csv"),delimiter=",")
		for row in reader:
			if row['property'] == self.name:
				self.order = int(row['order'])
		self.results = self.__getResultsDict__()
	
	def __getResultsDict__(self):
		d = {'name': self.name,
			'alias': self.alias,
			'oldValue': self.oldValue,
			'newValue': self.newValue,
			'different': self.different
			}
		return d