"""
A module handling the command line option
"""

from getopt import getopt, GetoptError
from sys import argv

__author__ = 'Ma Zijun'
__date__ = '2017-04-23'


class Preprocessor(object):
    """
    A class to process the command line option
    """
    # Error type 1: an option lack parameter
    LACK_PARAM = 1
    # Error type 2: an option has invalid parameter
    INVALID_PARAM = 2

    def __init__(self):
        """
        initialize cmd parameters
        """
        # exit flag
        self.terminate = False
        # input file name derived from the cmd
        self.input_file_name = ''
        # output file name derived from the cmd
        self.output_file_name = ''
        # the breaker character derived from the cmd
        self.breaker = ''

    def check_error(self):
        """
        check if cmd option error exists
        """
        if not self.input_file_name:
            show_error('-i', Preprocessor.LACK_PARAM)
            self.terminate = True

        if not self.output_file_name:
            show_error('-o', Preprocessor.LACK_PARAM)
            self.terminate = True

        if not self.breaker:
            show_error('--breaker', Preprocessor.LACK_PARAM)
            self.terminate = True

        if len(self.breaker) > 1:
            show_error('--breaker', Preprocessor.INVALID_PARAM)
            self.terminate = True

    def run(self):
        """
        get options from cmd and update parameters
        """
        try:
            opts = getopt(argv[1:], 'hi:o:', ['breaker='])[0]
        except GetoptError as e:
            print(e)
            self.terminate = True
            return

        for op, value in opts:
            if op == '-i':
                self.input_file_name = value
            elif op == '-o':
                self.output_file_name = value
            elif op == '-h':
                show_usage()
                self.terminate = True
            else:
                self.breaker = value

        self.check_error()

    def get_options(self):
        """
        get cmd options
        :return:
          * name of the input data file
          * name of the output file
          * single character as breaker
        """
        self.run()
        if self.terminate:
            exit(1)
        else:
            return self.input_file_name, self.output_file_name, self.breaker

def show_usage():
    """
    print help message
    """
    print('''Options and arguments:
-h                      : show option message
-i  name                : specify the file which stores the input data
-o  name                : specify the file which the function dependencies will be written to
--breaker=character     : specify the breaker which separate each column in input file, must be single character
Usage example:
python <name>.py -i input.txt -o output.txt --breaker=,''')


def show_error(option, error_type):
    """
    print error message according to the error type
    :param option: cmd option
    :param error_type: LACK_PARAM or INVALID_PARAM
    """
    if error_type == Preprocessor.LACK_PARAM:
        print("%s lacks parameter!" % option)
    else:
        print("%s has an invalid parameter!" % option)
