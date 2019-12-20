"""
A module serving as a reader of the raw data file
"""

__author__ = 'Ma Zijun'
__date__ = '2017-04-23'

class Reader(object):
    """
    Class serves as a raw data file reader
    """
    def __init__(self):
        pass

    @classmethod
    def read_table_from_file(cls, input_file_name, breaker):
        """
        get a table from the input file
        :param input_file_name: name of the input file
        :param breaker: a single character that separates columns in the file
        :return: a table
        """
        try:
            with open(input_file_name, 'r') as f:
                raw_data = f.read()
        except IOError as e:
            print(e)
            exit(1)

        row_strs = raw_data.strip().split('\n')
        table = []
        for row_str in row_strs:
            row = [x.strip() for x in row_str.split(breaker)]
            table.append(row)
        return table
