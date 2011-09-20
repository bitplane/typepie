#!/usr/bin/python
"""RandomList.py by Gaz Davidson 2011
!!ACTUNG!! This is a low entropy toy to shuffle test data, don't 
rely on it to produce data for cryptographic applications !!ACTUNG!!
"""
import random

class RandomList(object):
    """An indexable, lazily evaluated, shuffled list of integers.
    Borne from a discussion in work about having an arbitrary long 
    random sequence that doesn't repeat, can be split across
    multiple machines with minimal communication and/or memory use.
    """

    def __init__(self, length, factor=1.0, seed=0):
        """Constructs a new instance of this class.
        length: The length of the list, as per 'range(length)'.
        factor: The list will be shuffled factor*length times.
            A mixture of a larger factor and length may cause 
            incredibly large lookup times!
        seed: A hashable object used to seed the random number
            generator.
        """
        self.length = length
        self.seed   = seed
        self.factor = factor

    def getItem(self, index):
        """Returns the number at the given position in the list, 
        shuffling as we go along.
        By "shuffle" I mean how I shuffle cards, I clumsily cut a random 
        selection from the middle of the deck to the top, repeating
        until I'm happy that the deck is shuffled. This is not a good way 
        to generate a high-entropy pseudorandom sequence, but other 
        popular methods (Knuth/Fischer-Yates) require an actual list to 
        be held in RAM.
        """
        random.seed(self.seed)
        shuffles = int(self.length * self.factor)
        current  = index
        for i in xrange(shuffles):
            cutPosition = random.randrange(0, self.length)
            cutLength   = random.randrange(1, self.length-cutPosition + 1)
            if current < cutPosition:
                current = current + cutLength
            elif current < cutPosition + cutLength:
                current = current - cutPosition
            
        return current

    def __getitem__(self, index):
        """List index and slice operator."""
        return self.getItem(index)

    def __len__(self):
        """Length operator, so users can call len(myRandomList)"""
        return self.length

    def __contains__(self, value):
        """Checks to see if the list contains the given value"""
        return value == int(value) and 0 <= value < self.length

    def __iter__(self):
        """Allows users to do stuff like 'for item in myRandomList'"""
        for index in xrange(self.length):
            yield self.getItem(index)

    def __repr__(self):
        """Returns the string representation of the object"""
        return '{0}(length={1}, factor={2}, seed={3})'.format(self.__class__.__name__,
                                                              self.length,
                                                              self.factor,
                                                              self.seed)


if __name__ == '__main__':
    test = RandomList(1000)
    print [ test[a] for a in xrange(100) ]
