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
			"fieldname": "upc_code",
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
				Item.upc_code
			FROM
				`tabItem` AS Item
			WHERE
				Item.disabled = 0
				{conditions}

			LIMIT 1""".format(conditions=conditions), as_dict=True)
	test = ""
	odd = 0
	even = 0
	upc = str(label_detail[0].upc_code)
	if len(upc) != 11:
		label_detail[0].item_name = "UPC Code must be an 11 digit number."
		label_detail[0].upc_code = "-----------"
	else:
		for d in range(11):
			if (d % 2) == 0:
				odd += int(upc[d])
			else:
				even += int(upc[d])
		chksum = (odd * 3 + even) % 10
		if chksum > 0:
			chksum =  10 - chksum
		label_detail[0].upc_code += str(chksum)

	return label_detail	

