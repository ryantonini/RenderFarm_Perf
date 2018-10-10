"""
Simple helper functions.
"""


def try_except_typecast(func, value, failure):
    """Generic try except handler for type cast.

    Input arguments
        - func:   type conversion function
        - value:  value to be casted
        - failure:  value to return on error
    Return values:
        - casted value or failure
    """
    try:
        return func(value)
    except ValueError:
        return failure