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
			"label": __("Sales Order Sr No"),
			"fieldtype": "Data"
		}, {
			"fieldname": "box_qty",
			"label": __("Box Qty"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}, {
			"fieldname": "print_qty",
			"label": __("Print Qty"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}
	]
}