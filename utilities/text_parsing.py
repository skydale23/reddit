import re
from dateutil.parser import parse
from dateutil.parser import ParserError

def convert_to_alphanumeric(input, exclude_list = []):
    """removes special characters, except those specified"""
    #replace newline and return with space
    input = input.replace("\n", " ")
    input = input.replace("\r", " ")

    #replace other characters with empty string
    raw_string = r'[^A-Za-z0-9 ]+'
    for exclude in exclude_list:
        add_location = raw_string.find(" ")
        raw_string = raw_string[:add_location] + exclude + raw_string[add_location:]
    return re.sub(raw_string, '', input)

def get_proceeding_word(text, input_string):
    """returns the next word after input_string in text"""
    input_string_index = text.find(input_string)
    next_word = text[input_string_index + len(input_string):].split()[0]
    return next_word

def parse_date(input_date, return_string = True):
    "attempt to parse string into a date, else return starting string"
    try:
        input_date = parse(input_date)
        return input_date
    except ParserError:
        return input_date if return_string else None   
