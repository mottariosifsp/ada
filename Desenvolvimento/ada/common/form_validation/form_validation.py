def is_blank(values):

    for value in values:
        value = str(value).lower()
        value = value.replace(' ', '')
        if value == '':
            return True
        if value == None:
            return True
        if value == 'none':
            return True
        if value == 'null':
            return True
        if value.isspace():
            return True
        if value == 'nan':
            return True
        if value == '-':
            return True

# gource
        
        