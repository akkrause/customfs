// Copyright (c) 2016, Andrew Krause and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sample Label"] = {
	"filters": [
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		}, {
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		}, {
			"fieldname": "label_qty",
			"label": __("Label Quantity to Print"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}
	]
}