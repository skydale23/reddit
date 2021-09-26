import re

def convert_to_alphanumeric(text, include_spaces = False):
    """convert text to alpha numeric"""
    if include_spaces:
        return re.sub(r'[^A-Za-z0-9 ]+', '', text)
    else:
        return re.sub(r'[^A-Za-z0-9]+', '', text)
