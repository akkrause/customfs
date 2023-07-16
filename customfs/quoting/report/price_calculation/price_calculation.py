# Copyright (c) 2018, Andrew Krause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, flt, getdate

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	columns = [
		{ "label": _("Record Type"), "fieldname": "type", "fieldtype": "Data", "width": 20 },
		# Common fields
		{ "label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 100 },
		{ "label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 100 },
		{ "label": _("Description"), "fieldname": "desc", "fieldtype": "Data", "width": 200 },
		{ "label": _("Customer"), "fieldname": "cust", "fieldtype": "Link", "options": "Customer", "width": 100 },
		{ "label": _("Commission"), "fieldname": "comm", "fieldtype": "Data", "width": 100 },  #from customer
		{ "label": _("Margin"), "fieldname": "margin", "fieldtype": "Data", "width": 100 },  #from customer
		{ "label": _("Yearly Quantity"), "fieldname": "yearly_qty", "fieldtype": "Int", "width": 100 },
		{ "label": _("Labor Rate"), "fieldname": "labor_rate", "fieldtype": "Data", "width": 100 },
		{ "label": _("Quote Quantities"), "fieldname": "quote_qtys", "fieldtype": "Data", "width": 100 },
		# Results
		{ "label": _("Quote Quantity"), "fieldname": "qty", "fieldtype": "Data", "width": 100 },
		{ "label": _("Quote Price"), "fieldname": "price", "fieldtype": "Data", "width": 100 },
		# Operations
		{ "label": _("Operation"), "fieldname": "operation", "fieldtype": "Link", "options": "Operation", "width": 100 },
		{ "label": _("Quantity"), "fieldname": "qty", "fieldtype": "Int", "width": 100 },
		{ "label": _("Scrap"), "fieldname": "scrap", "fieldtype": "Float", "width": 60 },
		{ "label": _("Operation Cost"), "fieldname": "opr_cost", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Operation Material Cost"), "fieldname": "opr_matl_cost", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Operation Labor Cost"), "fieldname": "opr_lbr_cost", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Operation Consumables"), "fieldname": "opr_cons_cost", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Operation Overhead"), "fieldname": "opr_ovrhd_cost", "fieldtype": "Currency", "width": 100 },
		# Unit Costs
		{ "label": _("Material 1"), "fieldname": "material_1", "fieldtype": "Link", "options": "Item", "width": 100 },
		{ "label": _("Freight Dim 1"), "fieldname": "frt_dim_1", "fieldtype": "Float", "width": 100 },
		{ "label": _("Yield 1"), "fieldname": "yield_1", "fieldtype": "Float", "width": 100 },
		{ "label": _("Material Cost 1"), "fieldname": "matl_cost_1", "fieldtype": "Currency", "options": "Currency", "width": 100 },
		{ "label": _("Freight In 1"), "fieldname": "frt_in_1", "fieldtype": "currency", "options": "Currency", "width": 100 },
		{ "label": _("Material 2"), "fieldname": "material_2", "fieldtype": "Link", "options": "Item", "width": 100 },
		{ "label": _("Freight Dim 2"), "fieldname": "frt_dim_2", "fieldtype": "Float", "width": 100 },
		{ "label": _("Yield 2"), "fieldname": "yield_2", "fieldtype": "Float", "width": 100 },
		{ "label": _("Material Cost 2"), "fieldname": "matl_cost_2", "fieldtype": "Currency", "options": "Currency", "width": 100 },
		{ "label": _("Freight In 2"), "fieldname": "frt_in_2", "fieldtype": "currency", "options": "Currency", "width": 100 },
		{ "label": _("Material 3"), "fieldname": "material_3", "fieldtype": "Link", "options": "Item", "width": 100 },
		{ "label": _("Freight Dim 3"), "fieldname": "frt_dim_3", "fieldtype": "Float", "width": 100 },
		{ "label": _("Yield 3"), "fieldname": "yield_3", "fieldtype": "Float", "width": 100 },
		{ "label": _("Material Cost 3"), "fieldname": "matl_cost_3", "fieldtype": "Currency", "options": "Currency", "width": 100 },
		{ "label": _("Freight In 3"), "fieldname": "frt_in_3", "fieldtype": "currency", "options": "Currency", "width": 100 },
		{ "label": _("Time"), "fieldname": "time", "fieldtype": "Float", "width": 100 },
		{ "label": _("Stack"), "fieldname": "stack", "fieldtype": "Int", "width": 100 },
		{ "label": _("Consumables"), "fieldname": "consumables", "fieldtype": "currency", "width": 100 },
		{ "label": _("Power"), "fieldname": "power", "fieldtype": "currency", "width": 100 },
		{ "label": _("Water"), "fieldname": "water", "fieldtype": "currency", "width": 100 },
		# Batch Costs
		{ "label": _("Administration"), "fieldname": "admin_cost", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Setup"), "fieldname": "setup", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Shipping Labor"), "fieldname": "ship_labor", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Freight Out"), "fieldname": "freight_out", "fieldtype": "Currency", "width": 100 },
		# Facility Costs
		{ "label": _("Building"), "fieldname": "building", "fieldtype": "Currency", "width": 100 },
		{ "label": _("Equipment"), "fieldname": "equipment", "fieldtype": "Currency", "width": 100 }
	]

	return columns

def get_data(filters):
	BOM_conditions = ""
	Cust_conditions = ""
	if filters.get("item"):
		BOM_conditions += " and I.item = '%s'" % (filters.get("item"))
		
	if filters.get("customer"):
		Cust_conditions += " and CUST.name = '%s'" % (filters.get("customer"))
	
	if filters.get("yearly_qty"):
		yearly_qty = filters.get("yearly_qty")

	if filters.get("quote_qtys"):
		quote_qtys = filters.get("quote_qtys").split()

	BOM = frappe.db.sql("""
			SELECT
			    BOM.item,
				BOM.item_name,
				BOM.description
			FROM
		     	`tabItem` AS I,
				`tabBOM` AS BOM 
			WHERE
		     	I.default_bom = BOM.name
				{conditions}

			LIMIT 1""".format(conditions=BOM_conditions))
			
	
	quote = []
	quote.append([
		"T",				# Record Type
		"Item-00123",		# Item Code
		"Test Item",		# Item Name
		"Test Description",	# Description
		"Cust-00010",		# Customer
		0,					# Commission from customer
		0.25,				# Margin from customer
		1,					# Yearly Quantity
		25,					# Labor Rate
		"1,2",				# Quote Quantities
		1,					# Quote Quantity
		1,					# Quote Price
		"Waterjet",			# Operation
		100,				# Quantity
		0.01,				# Scrap
		101.00,				# Operation Total Cost
		102.00,				# Operation Material Cost
		103.00,				# Operation Labor Cost
		104.00,				# Operation Consumables
		105.00,				# Operation Overhead
		"Item-04321",		# Material 1
		3.01,				# Freight Dim 1
		0.123,				# Yield 1
		201.00,				# Material Cost 1
		202.00,				# Freight In 1
		"Item-03321",		# Material 2
		4.01,				# Freight Dim 2
		0.124,				# Yield 2
		301.00,				# Material Cost 2
		302.00, 			# Freight In 2
		"Item-02321",		# Material 3
		5.01,				# Freight Dim 3
		0.125,				# Yield 3
		401.00,				# Material Cost 3
		402.00,				# Freight In 3
		"555",				# Time
		1,					# Stack
		6.01,				# Consumables
		7.01,				# Power
		8.01,				# Water
		9.01,				# Administration
		10.01,				# Setup
		11.01,				# Shipping Labor
		12.01,				# Freight Out
		13.01,				# Building
		14.01				# Equipment
	])
	return quote


