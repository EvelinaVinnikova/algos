class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) == 0:
            return
        i = -1
        amount_operations = len(nums)
        while (amount_operations > 0):
            i += 1
            if nums[i] == 0:
                nums.pop(i)
                nums.insert(0, 0)
                amount_operations -= 1
                continue
            if nums[i] == 1:
                amount_operations -= 1
                continue
            if nums[i] == 2:
                nums.pop(i)
                nums.append(2)
                i -= 1
                amount_operations -= 1
