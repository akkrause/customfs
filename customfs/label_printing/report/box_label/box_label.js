// Copyright (c) 2016, Andrew Krause and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Box Label"] = {
	"filters": [
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"options": "Sales Order"
		}, {
			"fieldname": "sr_no",
			"label": __("Sales Order Line No"),
			"default": "1",
			"fieldtype": "Data"
		}, {
			"fieldname": "box_qty",
			"label": __("Qty per Box"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}, {
			"fieldname": "part_qty",
			"label": __("Sales Order Line Qty"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}
	]
}