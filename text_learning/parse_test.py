import sys
sys.path.append("../tools/")
from parse_out_email_text import parseOutText

ff = open("test_email.txt", "r")
text = parseOutText(ff)
print text

