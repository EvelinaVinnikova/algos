def lsd_radix_sort_strings(arr):
    if not arr:
        return

    max_len = len(arr[0])
    for word in arr:
        if len(word) != max_len:
            raise ValueError("All strings must be the same length")

    for i in range(max_len - 1, -1, -1):
        count = [0] * 256
        output = ["" for _ in arr]

        for word in arr:
            count[ord(word[i])] += 1

        for j in range(1, 256):
            count[j] += count[j - 1]

        for word in reversed(arr):
            c = ord(word[i])
            count[c] -= 1
            output[count[c]] = word
        arr = output
    return arr

def test():
    assert lsd_radix_sort_strings(['pbc', 'bca', 'dbb', '!ag']) == ['!ag', 'bca', 'dbb', 'pbc']

    assert lsd_radix_sort_strings(['aaa', 'aaa', 'aaa']) == ['aaa', 'aaa', 'aaa']

    assert lsd_radix_sort_strings(['123', '321', '213', '111']) == ['111', '123', '213', '321']

    assert lsd_radix_sort_strings(['a@c', 'a#c', 'a$c']) == ['a#c', 'a$c', 'a@c']

    assert lsd_radix_sort_strings([
        'hellopythonrock',
        'hellopythoncode',
        'hellopythonjava',
        'hellopythonsort'
    ]) == [
        'hellopythoncode',
        'hellopythonjava',
        'hellopythonrock',
        'hellopythonsort'
    ]

    try:
        lsd_radix_sort_strings(['abc', 'abcd'])
        assert False, "Expected ValueError for strings of different lengths"
    except ValueError:
        pass

    print("✅ All tests passed!")

test()
