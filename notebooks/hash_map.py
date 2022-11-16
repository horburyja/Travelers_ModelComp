class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Mapping:
    def __init__(self):
        self.n_buckets = 100
        self._L = [[] for i in range(self.n_buckets)]
        self._len = 0
        self._max_buckets = 1600

    def __setitem__(self, key, value):
        bucket = self.hash(key)

        # Case 1: item in mapping
        for entry in self._L[bucket]:
            if entry.key == key:
                entry.value = value
                return

        # Case 2: item not in mapping
        self._L[bucket].append(Entry(key, value))
        self._len += 1

        if (self.n_buckets < self._max_buckets and len(self) > self.n_buckets):
            self.rehash()

    def hash(self, key):
        return key % self.n_buckets

    def prime_hash(self, key, a_prime_number):
        # 1) Throw a ValueError exception when the prime_number is < than the number of buckets
        # (no need to check whether the a_prime_number is actually prime)
        if a_prime_number < self.n_buckets:
            raise ValueError

        # 2) return the hash value that is equal to
        # (key mod prime_number ) mod (number of buckets)
        return (key % a_prime_number) % self.n_buckets
      
    def __getitem__(self, key):
        bucket = self.hash(key)
        for entry in self._L[bucket]:
            if entry.key == key: return entry.value
        raise KeyError("key {} not in Mapping".format(key))

    # Increase the number of buckets only when the
    # increase_size argument is true
    def rehash(self, increase_size = True):

        if (increase_size):
            self.n_buckets *= 2

        new_L = [[] for i in range(self.n_buckets)]

        # move all items to new list
        for bucket in self._L:
            for entry in bucket:
                new_bucket = self.hash(entry.key)
                new_L[new_bucket].append(entry)

        self._L = new_L[:]

    def balance(self, hash_func):
        self.hash = hash_func
        self.rehash(False)

    # Return the index of the bucket with the largest number of items
    # and the number of items in that bucket
    def max_load_bucket(self):
        biggest = self._L[0]
        biggest_i = 0
        for bucket in range(1, len(self._L)):
            if len(self._L[bucket]) > len(biggest):
                biggest = self._L[bucket]
                biggest_i = bucket
        return biggest_i, len(biggest)

    # Return the index of the bucket with the largest number of items
    # and the number of items in that bucket
    def min_load_bucket(self):
        smallest_i = 0
        smallest = self._L[0]
        for bucket in range(1, len(self._L)):
            if len(self._L[bucket]) < len(smallest):
                smallest = self._L[bucket]
                smallest_i = bucket
        return smallest_i, len(smallest)

    def __len__(self):
        return (self._len)

