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
		# Results
		{ "label": _("Record Type"), "fieldname": "type", "fieldtype": "Data", "width": 20 },
		{ "label": _("Quantity"), "fieldname": "quantity", "fieldtype": "Int", "width": 100 },
		{ "label": _("Price"), "fieldname": "price", "fieldtype": "Currency", "width": 100 },
		# Common fields
		{ "label": _("BOM Name"), "fieldname": "bom_name", "fieldtype": "Data", "width": 100 },
		{ "label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 100 },
		{ "label": _("Description"), "fieldname": "desc", "fieldtype": "Data", "width": 200 },
		{ "label": _("Customer"), "fieldname": "cust", "fieldtype": "Link", "options": "Customer", "width": 100 },
		{ "label": _("Commission"), "fieldname": "comm", "fieldtype": "Data", "width": 100 },  #from customer
		{ "label": _("Margin"), "fieldname": "margin", "fieldtype": "Data", "width": 100 },  #from customer
		{ "label": _("Yearly Quantity"), "fieldname": "yearly_qty", "fieldtype": "Int", "width": 100 },
		{ "label": _("Labor Rate"), "fieldname": "labor_rate", "fieldtype": "Data", "width": 100 },
		# Operations
		{ "label": _("Operation"), "fieldname": "operation", "fieldtype": "Link", "options": "Operation", "width": 100 },
		{ "label": _("Workstation"), "fieldname": "workstation", "fieldtype": "Link", "options": "Workstation", "width": 100 },
		{ "label": _("Work Instructions"), "fieldname": "work_inst", "fieldtype": "Data", "width": 100 },
		{ "label": _("Quantity"), "fieldname": "qty", "fieldtype": "Int", "width": 100 },
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
		BOM_conditions += " and I.name = '%s'" % (filters.get("item"))
		
	if filters.get("customer"):
		Cust_conditions += "WHERE C.name = '%s'" % (filters.get("customer"))
	
	if filters.get("yearly_qty"):
		yearly_qty = filters.get("yearly_qty")

	if filters.get("quote_qtys"):
		quote_qtys = filters.get("quote_qtys").split()


	BOM = frappe.db.sql("""
			SELECT
			    BOM.name,
				BOM.item_name,
				BOM.description,
		     	BOM.quantity,
		     	I.item_group
			FROM
		     	`tabItem` AS I,
				`tabBOM` AS BOM 
			WHERE
		     	I.default_bom = BOM.name
				{conditions}

			LIMIT 1""".format(conditions=BOM_conditions),as_dict = 1)
			
	CUST = frappe.db.sql("""
			SELECT
			    C.name,
				C.customer_name
			FROM
		     	`tabCustomer` AS C
				{conditions}

			LIMIT 1""".format(conditions=Cust_conditions),as_dict = 1)
			
	OPL = frappe.db.sql("""
		    SELECT
		    	OPL.parent,
		     	OPL.operation,
		     	OPL.idx,
		    	OPL.workstation,
		    	OPL.description,
		    	OPL.time_in_mins,
		    	OPL.hour_rate,
		     	IFNULL(OPL.material_1, "") AS material_1,
		     	IFNULL(OPL.material_2, "") AS material_2,
		     	IFNULL(OPL.material_3, "") AS material_3
		    FROM
		    	`tabBOM Operation` AS OPL
		    WHERE
		    	{conditions}
		    ORDER BY
		     	OPL.idx
		    """.format(conditions="OPL.parent = '" + BOM[0]["name"] + "'"),as_dict=1)
	
	quote = []
	if OPL:
		for OP in OPL:
			MTL_conditions = "I.disabled = FALSE AND I.name IN ('{OP[material_1]}','{OP[material_2]}','{OP[material_3]}')"
			MTL = frappe.db.sql("""
				SELECT
					I.height
				FROM
					`tabItem` AS I
				WHERE
					{conditions}
				""".format(conditions=MTL_conditions),as_dict=1)
			
			quote.append([
				"O",						# Record Type
				0,							# Quote Quantity
				0,							# Quote Price
				BOM[0]["name"],				# BOM Name
				BOM[0]["item_name"],		# Item Name
				BOM[0]["description"],		# Description
				CUST[0]["customer_name"],	# Customer
				0,							# Commission from customer
				0.25,						# Margin from Item Group unless set on BOM.
				yearly_qty,					# Yearly Quantity
				25,							# Labor Rate
				OP["operation"],			# Operation
				OP["workstation"],			# Workstation
				OP["description"],			# Work Instructions
				BOM[0]["quantity"],			# Quantity per BOM, from BOM
				0,							# Operation Total Cost
				0,							# Operation Material Cost
				0,							# Operation Labor Cost
				0,							# Operation Consumables
				0,							# Operation Overhead
				OP["material_1"],			# Material 1, From Operation
				3.01,				# Freight Dim 1, from tabItem
				0.123,				# Yield 1,  Need yield per material and yield per part quantity.  From operation.
									# Pieces/Stock Unit or Stock Units/Piece, From Operation
									# Pieces per operation
				201.00,				# Material Cost 1, from Item Price for supplier
				202.00,				# Freight In 1, from Supplier where idx = 1 in `tabItem Supplier`
									# Scrap 1, From BOM operation
									# Supplier 1, From Item Price.
				OP["material_2"],			# Material 2
				4.01,				# Freight Dim 2
				0.124,				# Yield 2
									# Pieces/Stock Unit or Stock Units/Piece, From Operation
									# Pieces per operation
				301.00,				# Material Cost 2
				302.00, 			# Freight In Rate 2, From supplier
									# Scrap 2, From BOM operation
									# Supplier 2, From Item Price.
				OP["material_3"],			# Material 3
				5.01,				# Freight Dim 3
				0.125,				# Yield 3
									# Pieces/Stock Unit or Stock Units/Piece, From Operation
									# Pieces per operation
				401.00,				# Material Cost 3
				402.00,				# Freight In Rate 3, From supplier
									# Scrap 3, From BOM operation
									# Supplier 3, From Item Price.
				OP["time_in_mins"],				# Time
				1,					# Stack
				6.01,				# Consumables
				7.01,				# Power
				8.01,				# Water
				9.01,				# Administration
				10.01,				# Setup, Add field to tabOperation
				11.01,				# Shipping Labor
				12.01,				# Freight Out
				13.01,				# Building
				14.01				# Equipment
			])
	for qty in quote_qtys:
		quote.append([
			"T",						# Record Type
			qty,						# Quote Quantity
			1,							# Quote Price
			BOM[0]["name"],				# BOM Name
			BOM[0]["item_name"],		# Item Name
			BOM[0]["description"],		# Description
			CUST[0]["customer_name"],	# Customer
			0,							# Commission from customer
			0.25,						# Margin from customer
			yearly_qty,					# Yearly Quantity
			25,							# Labor Rate
			None,						# Operation
			None,						# Workstation
			None,						# Work Instructions
			BOM[0]["quantity"],			# Quantity per BOM, from BOM
			101.00,				# Operation Total Cost
			102.00,				# Operation Material Cost
			103.00,				# Operation Labor Cost
			104.00,				# Operation Consumables
			105.00,				# Operation Overhead
			"",							# Material 1, From Operation
			3.01,				# Freight Dim 1, from tabItem
			0.123,				# Yield 1,  Need yield per material and yield per part quantity.  From operation.
								# Pieces/Stock Unit or Stock Units/Piece, From Operation
								# Pieces per operation
			201.00,				# Material Cost 1, from Item Price for supplier
			202.00,				# Freight In 1, from Supplier where idx = 1 in `tabItem Supplier`
								# Scrap 1, From BOM operation
								# Supplier 1, From Item Price.
			"",							# Material 2
			4.01,				# Freight Dim 2
			0.124,				# Yield 2
			301.00,				# Material Cost 2
			302.00, 			# Freight In 2
								# Scrap 2, From BOM operation
			"",							# Material 3
			5.01,				# Freight Dim 3
			0.125,				# Yield 3
			401.00,				# Material Cost 3
			402.00,				# Freight In 3
								# Scrap 3, From BOM operation
								# Supplier 3, From Item Price.
			None,				# Time
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


