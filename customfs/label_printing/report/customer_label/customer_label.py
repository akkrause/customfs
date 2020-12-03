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
			"width": 100
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100
		},
		{
			"label": _("Customer Item Code"),
			"fieldname": "customer_item_code",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Label File"),
			"fieldname": "label_file",
			"fieldtype": "Data",
			"width": 200
		}
	]

	return columns

def get_labels(filters):
	conditions = ""
	if filters.get("item_code"):
		conditions += " and Item.item_code = '%s'" % (filters.get("item_code"))
		
	if filters.get("customer_name"):
		conditions += " and ICN.customer_name = '%s'" % (filters.get("customer_name"))

	print_qty = filters.get("print_qty")
	if print_qty < 1:
		print_qty = 1

	label_detail = frappe.db.sql("""
			SELECT
				Item.item_code,
				Item.item_name,
				Item.description,
                                C.customer_name,
                                ICN.ref_code
			FROM
				`tabItem` AS Item
				INNER JOIN `tabItem Customer Detail` AS ICN
					ON Item.name = ICN.parent
                                INNER JOIN `tabCustomer` AS C
                                        ON C.name = ICN.customer_name
			WHERE
				Item.disabled = 0
				{conditions}

			ORDER BY ICN.idx
			LIMIT 1""".format(conditions=conditions))
			
	labels = []

	if label_detail:
		label_count = 0
		while label_count < print_qty:
			labels.append(label_detail[0] + ("https://epe.foamsurface.com/Item/" + label_detail[0][0][5] + "/" + label_detail[0][0][6:8] + "/" + label_detail[0][0][8:10] + "/label/" + label_detail[0][0] + ".png",)) 
#			labels.append(label_detail[0] + ("/files/" + label_detail[0][0] + ".html",))
			label_count += 1
	return labels	

