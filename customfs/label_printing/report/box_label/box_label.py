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
		_("Sales Order") + ":Link/Sales Order:100",
		_("Sales Order Sr No") + ":Data:100",
		_("Item Code") + ":Link/Item:100",
		_("Item Name") + ":Data:100",
		_("Description") + ":Data:200",
		_("Customer Name") + ":Data:100",
		_("PO No") + ":Data:100",
		_("PO Date") + ":Date:60",
		_("Customer Item Code") + ":Data:100",
		_("Qty") + ":Int:50",
		_("Box Qty") + ":Int:50"
	]

	return columns

def get_labels(filters):
	conditions = ""
	if filters.get("sales_order"):
		conditions += " and SOI.parent = '%s'" % (filters.get("sales_order"))
		
	if filters.get("sr_no"):
		conditions += " and SOI.idx = '%s'" % (filters.get("sr_no"))
	
	box_qty = filters.get("box_qty")
	if box_qty < 1:
		box_qty = 1
		
	print_qty = filters.get("print_qty")
	if print_qty < 1:
		print_qty = 1

	label_detail = frappe.db.sql("""
			SELECT
				SOI.parent,
				SOI.idx,
				SOI.item_code,
				SOI.item_name,
				SOI.description,
				SO.customer_name,
				SO.po_no,
				SO.po_date,
				SOI.customer_item_code,
				SOI.qty
			FROM
				`tabSales Order Item` AS SOI
				INNER JOIN `tabSales Order` AS SO
					ON SO.name = SOI.parent
			WHERE
				SO.status NOT IN ('Completed', 'Cancelled', 'Closed')
				{conditions}

			GROUP BY SOI.parent
			ORDER BY SOI.idx
			LIMIT 1""".format(conditions=conditions))
			
	labels = []

	if label_detail:
		remaining_qty = print_qty
	
		while box_qty < remaining_qty:
			labels.append(label_detail[0] + (box_qty,))
			remaining_qty -= box_qty

		labels.append(label_detail[0] + (remaining_qty,))

	return labels	

