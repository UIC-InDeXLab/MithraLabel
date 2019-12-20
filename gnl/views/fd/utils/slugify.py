"""
A helper module implementing slugify function
"""

__author__ = 'Ma Zijun'
__date__ = '2017-04-23'

def slugify(elements, connector):
    """
    Get a string with all the elements connected by connector
    :param elements: a sequence of elements
    :param connector: a single character serves as a connector between elements
    :return: the connected string
    """
    return connector.join([str(x) for x in sorted(elements)])
