import re


def format_phone_number(phone_number):
    try:
        formatted_phone = ('(%s) %s-%s' %
                           tuple(re.findall(r'\d{4}$|\d{3}', phone_number)))
    except:
        formatted_phone = phone_number
    return formatted_phone


def remove_phone_format(string):
    digit_list = []
    clean_string = ""
    for char in string:
        if char.isdigit():
            digit_list.append(char)
    for x in digit_list:
        clean_string += x
    return clean_string


def string_cleaner(string):
    string = str(string)
    trailing_punctuation_marks = [".", ",", ";",
                                  "-", "?", "'", '"', ")", "(", "{", "}", "/", ]
    string = string.lower()
    # string = string.encode("ascii", "ignore")
    if 'apos;' in string:
        string = string.replace("&amp;apos;", "'")
    if "&amp;" in string:
        string = string.replace(" &amp; ", "&")
    if "&amp;&amp;" in string:
        string = string.replace("&amp;&amp;", "&")
    if len(string) > 3:
        for punctuation_mark in trailing_punctuation_marks:
            if string[-1] == punctuation_mark:
                string = string[:-1]
                break
    return string
