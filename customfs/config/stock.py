from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Labels"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Box Label",
					"doctype": "Sale Order Item",
				}
			]
		}
	]