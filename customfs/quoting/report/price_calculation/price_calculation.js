// Copyright (c) 2016, Andrew Krause and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Price Calculation"] = {
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
			"fieldname": "yearly_qty",
			"label": __("Yearly Quantity"),
			"fieldtype": "Int",
			"default": "100",
			"reqd": 1			
		}, {
			"fieldname": "quote_qtys",
			"label": __("Quote Quantities"),
			"fieldtype": "Data",
			"default": "101",
			"reqd": 1			
		}
	]
}