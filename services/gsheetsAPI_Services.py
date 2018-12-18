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
            worksheet=None,
            worksheet_range=None,
            major_dimension='ROWS'
    ):
        """Grab all data from a specified range for a worksheet.

        :param worksheet: str: worksheet name
        :param worksheet_range: str: range of cells to return withing worksheet.
                                     format example: A1:H19
        :param major_dimension: str: sheets parameter specifying shape of returned
                                     data - 'ROWS' or 'COLUMNS'.
                                     ROWS for conversion to pandas.DataFrame

        :return req_str: str: requests HTTP string for batchGet
        :return parameters: dict: dictionary defining parameters for GET call
        """
        if worksheet is not None:
            self.worksheet_name = worksheet
        if worksheet_range is not None:
            self.sheet_range = worksheet_range

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
        """Get spreadsheet data and return the values as an array."""
        req_str, param = super(GSheetMakeRequests, self).get_batch_in_range(
            worksheet=worksheet,
            worksheet_range=worksheet_range,
            major_dimension=major_dimension
        )

        sheet_data = self.session.get(req_str, params=param).json()

        values = sheet_data['valueRanges'][0]['values']

        return values


class GSheetsPandas:
    """Coordinate interactions between Google Sheets API and pandas DataFrame.
    """
    def __init__(
            self,
            request_service: GSheetMakeRequests,
            data: pd.DataFrame = None
    ):
        self.requests_service = request_service
        self.data = data

    @property
    def requests_service(self):
        return self._requests_service

    @requests_service.setter
    def requests_service(self, new):
        self._requests_service = new

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new):
        self._data = new

    def get_spreadsheet_data(self, header=True):
        """Get spreadsheet data and convert it to pandas DataFrame.

        :param header: bool: specify if data has a header
        """
        sheet_array = self.requests_service.get_batch_in_range()

        if header:
            self.data = pd.DataFrame(data=sheet_array[1:], columns=sheet_array[0])
        else:
            self.data = pd.DataFrame(data=sheet_array)

