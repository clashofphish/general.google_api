"""Components needed to I/O with files."""
import json


class FileHandling:
    """Base class for handling loading and saving of files.
    Currently handles:
        reading of text files, reading of json, writing of json
    """
    @staticmethod
    def read_text_file(filename):
        """Read a text file & return contents as string.
        :arg
            filename (str) : location and name of file to open
        """
        file_handle = open(filename, 'r')
        text = file_handle.read()
        file_handle.close()
        return text

    @staticmethod
    def read_json(filename):
        """Read a json file & return contents as json object.
        :arg
            filename (str) : location and name of file to open
        """
        with open(filename) as json_data:
            json_obj = json.load(json_data)
        return json_obj

    @staticmethod
    def write_json(filename, json_obj):
        """Read a json file & return contents as json object.
        :arg
            filename (str) : location and name of file to open
            json_obj (obj) : json object to save
        """
        with open(filename, 'w') as outfile:
            json.dump(json_obj, outfile)
