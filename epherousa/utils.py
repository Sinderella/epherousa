# coding=utf-8

import codecs
import csv


def csvreader(f):
    try:
        for row in csv.reader(f):
            yield row
    except UnicodeEncodeError:
        for row in csv.reader(codecs.iterencode(f, 'utf-8')):
            yield [e.decode('utf-8') for e in row]
