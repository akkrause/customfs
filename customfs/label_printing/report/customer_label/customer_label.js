// Copyright (c) 2016, Andrew Krause and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Label"] = {
	"filters": [
		{
			"fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item"
		}, {
			"fieldname": "customer_name",
			"label": __("Customer Name"),
			"fieldtype": "Link",
			"options": "Customer"
		}, {
			"fieldname": "print_qty",
			"label": __("Print Qty"),
			"fieldtype": "Int",
			"default": "1",
			"reqd": 1			
		}
	]
}
