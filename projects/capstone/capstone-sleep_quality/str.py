def convert_all_to_string(list_to_stringify,quote_string = False):
    stringified = []
    for i in list_to_stringify:
        if isinstance(i, str) and quote_string == True:
            i = '\"' + i + '\"'
        else:
            i = str(i)
        stringified.append(i)
    return stringified
def implode(list_to_implode, separator,quote_string = False):
    return separator.join(convert_all_to_string(list_to_implode,quote_string))