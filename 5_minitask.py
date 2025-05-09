def shell_sort(array: list[int]):
    n = len(array)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap //= 2
    return array

class Solution(object):
    def wiggleSort(self, nums):
        shell_sort(nums)
        half = len(nums) // 2 + len(nums) % 2

        small_half = nums[:half]
        large_half = nums[half:]

        index_nums, index_nums_2 = 0, 1
        for i in range (len(small_half) - 1, -1, -1):
            nums[index_nums] = small_half[i]
            index_nums += 2
            nums[index_nums_2] = large_half[i]
            index_nums_2 += 2
