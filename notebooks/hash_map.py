class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Mapping:
    def __init__(self):
        self._len = 0
        self._n_buckets = 1000
        self._L = [[] for i in range(self._n_buckets)]

    def rehash(self):
        self._n_buckets *= 2
        new_L = [[] for i in range(self._n_buckets)]
        for bucket in self._L:
            for entry in bucket:
                new_bucket = hash(entry.key) % self._n_buckets
                new_L[new_bucket].append(entry)

        self._L = new_L

    def hash(self, key):
        return key % self._n_buckets
    
    def __len__(self):
        return self._len

    def __setitem__(self, key, value):
        hash_key = hash(key) % self._n_buckets
        bucket = self._L[hash_key]
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return
        
        bucket.append(Entry(key, value))
        self._len += 1
        if len(self) > self._n_buckets:
            self.rehash()
    
    def __getitem__(self, key):
        hash_key = hash(key) % self._n_buckets
        bucket = self._L[hash_key]
        for entry in bucket:
            if entry.key == key:
                return entry.value
        raise KeyError
