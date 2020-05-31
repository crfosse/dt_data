
## Helper Functions ##
def get_number(string):
    for s in string.split():
        if s.isdigit():
            return int(s)


