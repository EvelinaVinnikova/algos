class Solution(object):
    ''' realization of the 2**k -1 Shell sort'''
    def shellSort(self, arr):
        k = 1
        gaps = []
        gap = 2**k - 1
        while gap < len(arr):
            gaps.append(gap)
            k += 1
            gap = 2**k - 1

        for i in range(len(gaps) - 1, -1, -1):
            gap = gaps[i]
            for j in range(gap, len(arr)):
                temp = arr[j]
                k = j
                while k >= gap and arr[k - gap] < temp:
                    arr[k] = arr[k - gap]
                    k -= gap
                arr[k] = temp

    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        self.shellSort(citations)
        h = 0
        n = len(citations)
        i = 0
        while i < n and citations[i] >= i + 1:
            h = i + 1
            i += 1
        return h
