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
		_("Item Code") + ":Link/Item:100",
		_("Description") + ":Data:200",
		_("Customer ID") + ":Data:100",
		_("Customer Name") + ":Data:100",
		_("Customer Item Code") + ":Data:100"
	]
	return columns

def get_labels(filters):
	conditions = ""
	if filters.get("item"):
		conditions += " and Item.item_code = '%s'" % (filters.get("item"))
		
	if filters.get("customer"):
		conditions += " and ICD.customer_name = '%s'" % (filters.get("customer"))
	
	label_qty = filters.get("label_qty")
	if label_qty < 1:
		label_qty = 1
		
	label_detail = frappe.db.sql("""
			SELECT
				Item.item_code,
				Item.description,
				Cust.name,
				Cust.customer_name,
				ICD.ref_code
			FROM
				`tabItem` AS Item
				INNER JOIN `tabItem Customer Detail` AS ICD
					ON Item.name = ICD.parent
				INNER JOIN `tabCustomer` Cust
					ON Cust.name = ICD.customer_name
			WHERE
				Item.disabled = 0
				{conditions}

			LIMIT 1""".format(conditions=conditions))
			
	labels = []

	for x in range(label_qty):
		if len(label_detail) > 0:
			labels.append(label_detail[0])

	return labels	

