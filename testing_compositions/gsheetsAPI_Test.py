"""Set up tests for API calls to authorized session."""
import os
import sys
base_path = os.path.abspath(os.path.join('.'))
if base_path not in sys.path:
    sys.path.append(base_path)

# Cusomt imports
from services.gsheetsAPI_Services \
    import GSheetMakeRequests, GSheetsPandas

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1v2FyrUtzoSejoZSQWPxSXIuhusmfazu19E0v9iD2UKk'
SAMPLE_SHEET_NAME = 'Sheet1'
SAMPLE_RANGE = 'A1:H19'


def test_push(session):
    """Write column to test spreadsheet.

    :param session: obj: authorized requests session
    """
    make = GSheetMakeRequests(
        session=session,
        spreadsheet_id=SAMPLE_SPREADSHEET_ID,
        worksheet_name=SAMPLE_SHEET_NAME,
        sheet_range=SAMPLE_RANGE
    )
    reqs = GSheetsPandas(request_service=make)

    sheet_data = reqs.get_spreadsheet_data()

    change_col = 'Today\'s QC Quantity'
    sheet_data[change_col] = 1
    reqs.requests_service.worksheet_name = 'Copy of Sheet1'
    reqs.requests_service.sheet_range = 'A2:A19'

    resp = reqs.update_spreadsheet_data(
        data=sheet_data,
        columns=[change_col],
        sheet_range='F2:F19'
    )

    return sheet_data, resp


if __name__ == '__main__':
    print('Use command line to authorize session & test')
