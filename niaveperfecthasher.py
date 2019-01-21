from collections import MutableMapping

INITIAL_SIZE = 4


class NaivePerfectHash(MutableMapping):
    """A simple and space inefficient perfect hash

    Whenever there's a collision, we double the array size, so the worst case
    space complexity is based on the size of the max key, if it is a power of
    two from another key. A pathological example is of the keys 0 and 2**10.

    The class supports a Python dict interface.
    """

    def __init__(self, size=INITIAL_SIZE):
        self._hashtable = [None] * size

    def __len__(self):
        return len(self._hashtable)

    def _fetchindex(self, key):
        """A helper function to get hashtable index

        Returns a pair where the second element is the hash index and the
        first element is:
        - True if key is in the hashtable
        - None if slot corresponding to key is empty
        - False if key is not in hashtable but corresponding slot is taken
        """
        index = hash(key) % len(self)
        item = self._hashtable[index]
        if not isinstance(item, tuple):
            return (None, index)

        stored_key, _ = item
        if stored_key == key:
            return (True, index)
        return (False, index)

    def __contains__(self, key):
        return self._fetchindex(key)[0] is True

    def get(self, key, default=None):
        found, index = self._fetchindex(key)
        if found:
            return self._hashtable[index][1]
        return default

    def __getitem__(self, key):
        found, index = self._fetchindex(key)
        if found:
            return self._hashtable[index][1]
        raise KeyError(key)

    def __setitem__(self, key, value):
        found, index = self._fetchindex(key)
        while found is False:  # deal with collision
            self._doublethehash()
            found, index = self._fetchindex(key)

        self._hashtable[index] = (key, value)

    def __delitem__(self, key):
        found, index = self._fetchindex(key)
        if found:
            self._hashtable[index] = None
        else:
            raise KeyError(key)

    def items(self):
        return iter(filter(None, self._hashtable))

    def keys(self):
        return (key for (key, value) in self.items())

    def values(self):
        return (value for (key, value) in self.items())

    def __iter__(self):
        return self.keys()

    def _doublethehash(self):
        """
        Double the hash table size

        Using powers of two assures no collisions between existing keys
        """
        newhashtable = [None] * (2 * len(self))
        for key, value in self.items():
            newindex = hash(key) % len(newhashtable)
            newhashtable[newindex] = (key, value)
        self._hashtable = newhashtable


if __name__ == '__main__':
    # example usage:
    ph = NaivePerfectHash()
    ph[0] = 2
    print(len(ph))
    ph[1024] = 3
    print(len(ph))
    print(ph.get(0, 42))
    del ph[0]
    print(list(ph))
