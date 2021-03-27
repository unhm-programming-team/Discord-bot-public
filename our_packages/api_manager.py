"""
defines functions to ease api calling
THIS PACKAGE ONLY SOMETIMES WORKS
TODO: figure out why and fix that
"""

import requests
import json


def assembleargs(args):
    """
    Assembles args into an easily appendable string
    :param args: dictionary of arguments
    :return:
    """
    arg_string = "?"
    for argument in args:
        arg_string += f"{argument}={args[argument]}"
        if list(args.keys())[-1] != argument:
            arg_string += "&"
    return arg_string



def getrequest(link, args=None):
    """
    Takes link and makes a request using args
    :param link: string to endpoint
    :param args: dictionary, name of arguments as keys, values store value to be passed
    :return: api return content
    """
    if args:
        arguments = assembleargs(args)
        response = requests.get(f"{link}{arguments}")
    else:
        response = requests.get(f"{link}")
    r = json.loads(response.content)
    return r
