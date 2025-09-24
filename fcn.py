import re
def properFloat(string):
    return float(re.sub('[^0-9\.]+', '', string))