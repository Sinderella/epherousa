#!/usr/bin/env python
# coding=utf-8

import os
import sys

if __name__ == '__main__':
    path = os.path.dirname(sys.modules[__name__].__file__)
    path = os.path.join(path, '..')
    sys.path.insert(0, path)

    # Fix encoding problem in python 2.7
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
    except NameError as e:
        pass
    from epherousa import main

    main()
