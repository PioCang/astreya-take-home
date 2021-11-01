""" Utility functions """

import traceback
from pprint import pprint

def dump_thorough_stack_trace():
    """ Dumps a needed stack trace """

    traceback.print_exc()
    pprint(locals(), indent=4)
