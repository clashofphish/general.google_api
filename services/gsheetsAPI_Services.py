"""File to serve as base classes for organizing Google Sheets API calls."""
from google.auth.transport.requests import AuthorizedSession
import pandas as pd


class GSheetsFormatRequests:
    """Class for wrapping Google Sheets API requests.

    :param spreadsheet_id: str: spreadsheet uri
    :param worksheet_name: str: name of worksheet holding data of interest
    :param sheet_range: str: range of cells to return withing worksheet.
                             format example: A1:H19
    """

    def __init__(
            self,
            spreadsheet_id=None,
            worksheet_name=None,
            sheet_range=None
    ):
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.sheet_range = sheet_range

    @property
    def spreadsheet_id(self):
        return self._spreadsheet_id

    @spreadsheet_id.setter
    def spreadsheet_id(self, new):
        self._spreadsheet_id = new

    @property
    def worksheet_name(self):
        return self._worksheet_name

    @worksheet_name.setter
    def worksheet_name(self, new):
        self._worksheet_name = new

    @property
    def sheet_range(self):
        return self._sheet_range

    @sheet_range.setter
    def sheet_range(self, new):
        self._sheet_range = new

    def get_batch_in_range(
            self,
            major_dimension='ROWS'
    ):
        """Grab all data from a specified range for a worksheet.

        :param major_dimension: str: sheets parameter specifying shape of returned
                                     data - 'ROWS' or 'COLUMNS'.

        :return req_str: str: requests HTTP string for batchGet
        :return parameters: dict: dictionary defining parameters for GET call
        """
        req_str = (
                'https://sheets.googleapis.com/v4/spreadsheets/'
                + self.spreadsheet_id
                + '/values:batchGet'
        )
        parameters = {
            'ranges': self.worksheet_name + '!' + self.sheet_range,
            'majorDimension': major_dimension
        }

        return req_str, parameters

    def put_batch_in_range(
            self,
            data,
            major_dimension='COLUMNS'
    ):
        """Put data into a specified range for a worksheet.

        :param data: array: data to post to spreadsheet
        :param major_dimension: str: sheets parameter specifying shape of returned
                                     data - 'ROWS' or 'COLUMNS'.

        :return req_str: str: requests HTTP string for batchGet
        :return parameters: dict: dictionary defining parameters for GET call
        """
        req_str = (
                'https://sheets.googleapis.com/v4/spreadsheets/'
                + self.spreadsheet_id
                + '/values:batchUpdate'
        )
        parameters = {
            'valueInputOption': 'RAW',
            'data': {
                'range': self.worksheet_name + '!' + self.sheet_range,
                'majorDimension': major_dimension,
                'values': data
            }
        }

        return req_str, parameters


class GSheetMakeRequests(GSheetsFormatRequests):
    """Class for executing request actions to interact with Google Sheets API.

    :param session: obj: session object for making requests
    :param spreadsheet_id: str: spreadsheet uri
    :param worksheet_name: str: name of worksheet holding data of interest
    :param sheet_range: str: range of cells to return withing worksheet.
                             format example: A1:H19
    """

    def __init__(
            self,
            session: AuthorizedSession,
            spreadsheet_id=None,
            worksheet_name=None,
            sheet_range=None
    ):
        super().__init__(
            spreadsheet_id=spreadsheet_id,
            worksheet_name=worksheet_name,
            sheet_range=sheet_range
        )
        self.session = session

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, new):
        self._session = new

    def get_batch_in_range(
            self,
            worksheet=None,
            worksheet_range=None,
            major_dimension='ROWS'
    ):
        """Get spreadsheet data and return the values as an array.

        :param worksheet: str: worksheet name
        :param worksheet_range: str: range of cells to return withing worksheet.
                                     format example: A1:H19
        :param major_dimension: str: sheets parameter specifying shape of returned
                                     data - 'ROWS' or 'COLUMNS'.

        :return values: array: data from range in spreadsheet
        """
        if worksheet is not None:
            self.worksheet_name = worksheet
        if worksheet_range is not None:
            self.sheet_range = worksheet_range

        req_str, param = super(GSheetMakeRequests, self).get_batch_in_range(
            major_dimension=major_dimension
        )

        sheet_data = self.session.get(req_str, params=param).json()

        values = sheet_data['valueRanges'][0]['values']

        return values

    def put_batch_in_range(
            self,
            data,
            worksheet=None,
            worksheet_range=None,
            major_dimension='COLUMNS'
    ):
        """Get spreadsheet data and return the values as an array.

        :param data: array: data to post to the spreadsheet
        :param worksheet: str: worksheet name
        :param worksheet_range: str: range of cells to return withing worksheet.
                                     format example: A1:H19
        :param major_dimension: str: sheets parameter specifying shape of returned
                                     data - 'ROWS' or 'COLUMNS'.

        :return response: dict: response of post request
        """
        if worksheet is not None:
            self.worksheet_name = worksheet
        if worksheet_range is not None:
            self.sheet_range = worksheet_range

        req_str, param = super(GSheetMakeRequests, self).put_batch_in_range(
            data=data,
            major_dimension=major_dimension
        )

        response = self.session.post(req_str, json=param).json()

        return response


class GSheetsPandas:
    """Coordinate interactions between Google Sheets API and pandas DataFrame.
    """
    def __init__(
            self,
            request_service: GSheetMakeRequests
    ):
        self.requests_service = request_service

    @property
    def requests_service(self):
        return self._requests_service

    @requests_service.setter
    def requests_service(self, new):
        self._requests_service = new

    def get_spreadsheet_data(self, header=True):
        """Get spreadsheet data and convert it to pandas DataFrame.

        :param header: bool: specify if data has a header
        """
        sheet_array = self.requests_service.get_batch_in_range()

        if header:
            data = pd.DataFrame(data=sheet_array[1:], columns=sheet_array[0])
        else:
            data = pd.DataFrame(data=sheet_array)

        return data

    def update_spreadsheet_data(self, data, columns, sheet_range):
        """Update data in the spreadsheet from pandas DataFrame.
        Note:
            Can only set contiguous with a single call at this time.

        :param data: pd.DataFrame: DataFrame holding data to be posted
        :param columns: list(str): list of columns for which to post data
        :param sheet_range: str: range in which to post data
        """
        if type(columns) != list:
            columns = [columns]

        sheet_array = []
        for col in columns:
            sheet_array.append(
                data[col].tolist()
            )

        response = self.requests_service.put_batch_in_range(
            data=sheet_array,
            worksheet_range=sheet_range
        )
        return response
