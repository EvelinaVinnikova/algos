class Solution:
    # def sortArray(self, nums: List[int]) -> List[int]:
    #     self.quicksort_hoare(nums, 0, len(nums) - 1)
    #     return nums

    # def quicksort_hoare(self, nums: List[int], low: int, high: int) -> None:
    #     if low < high:
    #         p = self.partition_hoare(nums, low, high)
    #         self.quicksort_hoare(nums, low, p)
    #         self.quicksort_hoare(nums, p + 1, high)

    # def partition_hoare(self, nums: List[int], low: int, high: int) -> int:
    #     # выбираем случайный опорный элемент и меняем его с первым элементом
    #     pivot_index = random.randint(low, high)
    #     nums[pivot_index], nums[low] = nums[low], nums[pivot_index]
    #     pivot = nums[low]
    #     i = low - 1
    #     j = high + 1
    #     while True:
    #         # ищем элемент слева, который не меньше опорного
    #         i += 1
    #         while nums[i] < pivot:
    #             i += 1
    #         # ищем элемент справа, который не больше опорного
    #         j -= 1
    #         while nums[j] > pivot:
    #             j -= 1
    #         if i >= j:
    #             return j
    #         nums[i], nums[j] = nums[j], nums[i]


    def sortArray(self, nums: List[int]) -> List[int]:
        self.quicksort_lomuto(nums, 0, len(nums) - 1)
        return nums

    def quicksort_lomuto(self, nums: List[int], low: int, high: int) -> None:
            if low < high:
                lt, gt = self.partition_lomuto(nums, low, high)
                self.quicksort_lomuto(nums, low, lt - 1)
                self.quicksort_lomuto(nums, gt + 1, high)

    def partition_lomuto(self, nums: List[int], low: int, high: int) -> (int, int):
        # выбираем случайный опорный элемент и меняем его с последним
        pivot_index = random.randint(low, high)
        nums[pivot_index], nums[high] = nums[high], nums[pivot_index]
        pivot = nums[high]

        lt = low    # элементы < pivot
        gt = high   # элементы > pivot
        i = low

        while i <= gt:
            if nums[i] < pivot:
                nums[i], nums[lt] = nums[lt], nums[i]
                lt += 1
                i += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1  # не увеличиваем i, т.к. нужно проверить новый nums[i]
            else:
                i += 1  # nums[i] == pivot, просто переходим дальше

        return lt, gt  # lt - начало блока == pivot, gt - конец блока == pivot
