# Fix encoding problem in python 2.7
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError as e:
    pass
