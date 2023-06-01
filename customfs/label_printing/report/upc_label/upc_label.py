# Copyright (c) 2018, Andrew Krause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()
	data = get_labels(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("UPC Code"),
			"fieldname": "barcode",
			"fieldtype": "Data",
			"width": 300
		}
	]
	return columns

def get_labels(filters):
	conditions = ""
	if filters.get("item"):
		conditions += " and Item.item_code = '%s'" % (filters.get("item"))
		
		
	label_detail = frappe.db.sql("""
			SELECT
                Item.item_code,
                Item.description,
				Item.item_name,
				ItemBC.barcode
			FROM
				`tabItem` AS Item,
				`tabItem Barcode` AS ItemBC
			WHERE
				ItemBC.parent = Item.name
				And Item.disabled = 0
				{conditions}

			LIMIT 1""".format(conditions=conditions), as_dict=True)
	
	return label_detail	

