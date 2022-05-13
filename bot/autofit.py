# -*- coding: utf-8 -*-


def columns(spreadsheet):
	update = {
			"requests": [{
					"autoResizeDimensions": {
						"dimensions": {
								"sheetId": spreadsheet.get_worksheet(0).id,
								"dimension": "COLUMNS",
								"startIndex": 0,
								"endIndex": spreadsheet.get_worksheet(0).col_count
						}
					}
			}]
	}
	spreadsheet.batch_update(update)


def rows(spreadsheet):
	update = {
			"requests": [{
					"autoResizeDimensions": {
						"dimensions": {
								"sheetId": spreadsheet.get_worksheet(0).id,
								"dimension": "ROWS",
								"startIndex": 0,
								"endIndex": spreadsheet.get_worksheet(0).row_count
						}
					}
			}]
	}
	spreadsheet.batch_update(update)
