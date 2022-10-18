// Copyright (c) 2016, Andrew Krause and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["UPC Label"] = {
	"filters": [
		{
			"fieldname": "item",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item"
		}
	]
}
