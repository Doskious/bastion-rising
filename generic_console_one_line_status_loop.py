import sys
from __future__ import print_function
from dummy import iterable


FLUSH_BUFFER = u"\033[K"

for item in iterable:
	print(u"{} Item output:{}".format(
	    FLUSH_BUFFER, item.iter_out), end=u'\r')
	sys.stdout.flush()
