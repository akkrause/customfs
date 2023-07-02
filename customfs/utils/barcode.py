# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

# IMPORTANT: only import safe functions as this module will be included in jinja environment
import frappe
# from frappe.utils.data import flt, get_number_format_info, in_words, cint

#
# convert currency to words
#
def encode128(barcode_text):
	"""
	Returns barcode 128 encoded string.
	"""
	from frappe.utils import get_defaults
	_ = frappe._

	barcode = "ÌHello World!WÎ"
	return barcode

