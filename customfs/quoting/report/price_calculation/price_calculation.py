# Copyright (c) 2018, Andrew Krause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns()

	data = get_data(filters)

	return columns, data

def get_columns():
	columns = [
		{ "label": _("Record Type"), "fieldname": "type", "fieldtype": "Data", "width": 20 },
		{ "label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 100 },
		{ "label": _("Item Name"), "fieldname": "item_name", "fieldtype": "Data", "width": 100 },
		{ "label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 200 },

		{ "label": _("Sales Order"), "fieldname": "sales_order", "fieldtype": "Link", "options": "Sales Order", "width": 100 },
		{ "label": _("Sales Order Sr No"), "fieldname": "sr_no", "fieldtype": "Data", "width": 100 },
		{ "label": _("Customer Name"), "fieldname": "customer_name", "fieldtype": "Data", "width": 100 },
		{ "label": _("PO No"), "fieldname": "po_no", "fieldtype": "Data", "width": 100 },
		{ "label": _("PO Date"), "fieldname": "po_date", "fieldtype": "Date", "width": 60 },
		{ "label": _("Delivery Date"), "fieldname": "delivery_date", "fieldtype": "Date", "width": 60 },
		{ "label": _("Customer Item Code"), "fieldname": "customer_item_code", "fieldtype": "Data", "width": 100 },
		{ "label": _("Alt Box Label"), "fieldname": "alt_box_label", "fieldtype": "Int", "width": 10 },
		{ "label": _("Qty"), "fieldname": "qty", "fieldtype": "Int", "width": 50 },
		{ "label": _("Box Qty"), "fieldname": "box_qty", "fieldtype": "Int", "width": 50 }
	]

	return columns

def get_data(filters):
	conditions = ""
	if filters.get("sales_order"):
		conditions += " and SOI.parent = '%s'" % (filters.get("sales_order"))
		
	if filters.get("sr_no"):
		conditions += " and SOI.idx = '%s'" % (filters.get("sr_no"))
	
	box_qty = filters.get("box_qty")
	if box_qty < 1:
		box_qty = 1
		
	part_qty = filters.get("part_qty")
	if part_qty < 1:
		part_qty = 1

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
				SOI.delivery_date,
				SOI.customer_item_code,
				I.alt_box_label,
				SOI.qty
			FROM
				`tabSales Order Item` AS SOI
				INNER JOIN `tabSales Order` AS SO
					ON SO.name = SOI.parent
				INNER JOIN `tabItem` AS I
					ON SOI.item_code = I.name
			WHERE
				SO.status NOT IN ('Completed', 'Cancelled', 'Closed')
				{conditions}

			GROUP BY SOI.parent
			ORDER BY SOI.idx
			LIMIT 1""".format(conditions=conditions))
			
	labels = []

	if label_detail:
		remaining_qty = part_qty
	
		while box_qty < remaining_qty:
			labels.append(label_detail[0] + (box_qty,))
			remaining_qty -= box_qty

		labels.append(label_detail[0] + (remaining_qty,))

	return labels	


