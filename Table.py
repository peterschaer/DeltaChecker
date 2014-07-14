# -*- coding: utf-8 -*-
try:
	arcpy
except NameError:
	import arcpy

import Field
import Property

class Table:
	def __init__(self, table1, table2, tableProperties, fieldProperties, spatrefProperties, minMaxFields,compareValueFields):
		self.fields = []
		self.fieldsAsDict = []
		self.tblProperties = []
		self.tblPropertiesAsDict = []
		self.sprefProperties = []
		self.sprefPropertiesAsDict = []
		self.tableProperties = tableProperties
		self.spatrefProperties = spatrefProperties
		fieldNameList1 = self.__getFieldNameList(table1)
		fieldNameList2 = self.__getFieldNameList(table2)
		mergedFieldNames = self.__mergeFieldNameLists(fieldNameList1,fieldNameList2)

		# Felder
		for f in mergedFieldNames:
			arcpy.AddMessage("Bearbeite Feld: " + f)
			fo = Field.Field(table1,table2,f,fieldProperties,minMaxFields,compareValueFields)
			self.fields.append(fo)
			self.fieldsAsDict.append(fo.results)
			
		# Tabellen-Eigenschaften
		arcpy.AddMessage("Bearbeite Tabellen-Eigenschaften")
		for k,v in self.tableProperties.items():
			po = Property.Property(arcpy.Describe(table1),arcpy.Describe(table2),k,v)
			self.tblProperties.append(po)
			self.tblPropertiesAsDict.append(po.results)
			
		# SpatialReference-Eigenschaften
		arcpy.AddMessage("Bearbeite Spatial Reference-Eigenschaften")
		for k,v in self.spatrefProperties.items():
			if hasattr(arcpy.Describe(table1),"spatialReference") & hasattr(arcpy.Describe(table2),"spatialReference"):
				po = Property.Property(arcpy.Describe(table1).spatialReference,arcpy.Describe(table2).spatialReference,k,v)
				self.sprefProperties.append(po)
				self.sprefPropertiesAsDict.append(po.results)

		self.tablePropertiesHTML = self.__getTablePropertiesHTML()
		self.spatrefPropertiesHTML = self.__getSpatrefPropertiesHTML()

	def __getTablePropertiesHTML(self):
		html = "<table><tr>"
		for k,v in self.tableProperties.items():
			html = html + "<th>" + v + "</th>"
		html = html + "</tr><tr>"
		for k,v in self.tableProperties.items():
			for p in self.tblProperties:
				if p.name == k:
					if p.different == True:
						html = html + "<td><span class=\"changed\">" + unicode(p.newValue) + "</span> <span class=\"old\">(" + unicode(p.oldValue) + "</span>)</td>" 
					else:
						html = html + "<td>" + unicode(p.newValue) + "</td>" 
		html = html + "</tr></table>"
		return html

	def __getSpatrefPropertiesHTML(self):
		html = "<table><tr>"
		for k,v in self.spatrefProperties.items():
			html = html + "<th>" + v + "</th>"
		html = html + "</tr><tr>"
		for k,v in self.spatrefProperties.items():
			for p in self.sprefProperties:
				if p.name == k:
					if p.different == True:
						html = html + "<td><span class=\"changed\">" + unicode(p.newValue) + "</span> <span class=\"old\">(" + unicode(p.oldValue) + "</span>)</td>" 
					else:
						html = html + "<td>" + unicode(p.newValue) + "</td>" 
		html = html + "</tr></table>"
		return html

	def __getFieldNameList(self,table):
		described = arcpy.Describe(table)
		describedFields = described.fields
		fieldNames = []
		for field in describedFields:
			fieldNames.append(field.name)
		
		excludedFieldNames = []
		if hasattr(described,"OIDFieldName"):
			excludedFieldNames.append(described.OIDFieldName)
		if hasattr(described,"ShapeFieldName"):
			excludedFieldNames.append(described.ShapeFieldName)
		if hasattr(described,"areaFieldName"):
			excludedFieldNames.append(described.areaFieldName)
		if hasattr(described,"lengthFieldName"):
			excludedFieldNames.append(described.lengthFieldName)
		
		cleanedFieldNames = []
		for fieldName in fieldNames:
			if fieldName not in excludedFieldNames:
				cleanedFieldNames.append(fieldName)
		return cleanedFieldNames
		
	def __mergeFieldNameLists(self,list1,list2):
		result = list2
		for f in list1:
			if f not in list2:
				result.append(f)
		return result
	
		
	
	
	