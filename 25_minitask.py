import hashlib
import math

class BloomFilter:
    def __init__(self, expected_elements, false_positive_prob):
        self.n = expected_elements
        self.p = false_positive_prob
        self.m = self._get_bit_array_size()
        self.k = self._get_hash_count()
        self.bit_array = [0] * self.m

    def _get_bit_array_size(self):
        return int(-self.n * math.log(self.p) / (math.log(2) ** 2))

    def _get_hash_count(self):
        return int((self.m / self.n) * math.log(2))

    def _hash(self, item, i):
        hash_value = int(hashlib.md5(f'{item}{i}'.encode()).hexdigest(), 16)
        return hash_value % self.m

    def add(self, item):
        for i in range(self.k):
            hash_index = self._hash(item, i)
            self.bit_array[hash_index] = 1

    def contains(self, item):
        for i in range(self.k):
            hash_index = self._hash(item, i)
            if self.bit_array[hash_index] == 0:
                return False
        return True


bf = BloomFilter(expected_elements=1000, false_positive_prob=0.01)

bf.add("192.168.0.1")
assert bf.contains("192.168.0.1")

ip_unknown = "10.0.0.1"
result = bf.contains(ip_unknown)
assert result in (True, False)

for i in range(100):
    bf.add(f"10.0.0.{i}")

for i in range(100):
    assert bf.contains(f"10.0.0.{i}")
