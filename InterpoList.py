"""
    InterpoList module (c) Gaz Davidson December 2009.

    This is a simple interpolated list type useful for graphing, you
    can set values at any index and it will linearly interpolate between
    the missing ones.

    License:
       Use for any purpose under one condition: I am not to blame for anything.
"""

from bisect import bisect, bisect_left
from math import fabs
import string

class InterpoListItem(object):
    def __init__(self, key, value):
        """ The constructor """
        self.key   = key
        self.value = value
    def __lt__(self, other):
        """ The less than operator, required for sorting """
        return self.key < other.key
    def __repr__(self):
        """ Formal representation of the object """
        return "%s(%s,%s)" % (type(self).__name__, self.key, self.value)
    
class InterpoList(object):
    """
        A list type which automatically does linear interpolation.
        For example:
            >>> a = InterpoList()
            >>> a[0]   = 0
            >>> a[100] = 200
            >>> a[200] = 0
            >>> a[50]
            100.0
            >>> a[125]
            150.0
    """
    def __init__(self, data = {}):
        """ constructor """
        self.items = list()
        for key in data:
            self.__setitem__(key, data[key])

    def __getitem__(self, index):
        """ Returns the value for a given index """
        # create a dummy item for searching
        idx = float(index)
        item = InterpoListItem(idx, 0)
        # find the position where it would be inserted
        i = bisect(self.items, item)

        if i == 0: # or i > len(self.items):
            # refuse to extrapolate
            raise ValueError("Extrapolation is not supported")
        else:
            if self.items[i-1].key == idx:
                # exact
                return self.items[i-1].value
            else:
                if i == len(self.items):
                    # refuse to extrapolate
                    raise ValueError("Extrapolation is not supported")
                else:
                    # interpolate                    
                    factor = (self.items[i].key - idx) / (self.items[i].key - self.items[i-1].key)
                    return self.items[i].value - (self.items[i].value - self.items[i-1].value)*factor

    def __setitem__(self, index, value):
        """ adds a new index or replaces a current one """
        # create a new list item
        findex = float(index)
        item   = InterpoListItem(findex, value)
        # find the insertion point
        i = bisect_left(self.items, item)
        
        # replace existing value?
        if i < len(self.items) and self.items[i].key == findex:
            self.items[i] = item
        else:
            # insert it
            self.items.insert(i, item)

    def __len__(self):
        """ Returns the range of the indices """
        if len(self.items) > 0:
            return fabs(self.items[-1].key - self.items[0].key)
        else:
            return 0.0

    def __repr__(self):
        """ Formal description of the object """
        # Dump the contents into a dict style string using a list comprehension expression.
        # This makes sure there's no outer "loop" as such, which avoids allocating tons of
        # (immutable) strings of increasing length.
        lst = string.join([string.join( (str(i.key), str(i.value) ), ":") for i in self.items], ",")
        # spit the whole thing out
        return "%s(data={%s})" % (type(self).__name__, lst)



