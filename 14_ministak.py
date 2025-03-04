# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
        def detectCycle(self, head: ListNode) -> ListNode:
            if not head or not head.next:
                return None
            slow = head
            fast = head
            while(fast and fast.next):
                slow = slow.next
                fast = fast.next.next
                if slow == fast:
                    break
            slow = head
            # алгоритм Флоида: расстояния от начала цикла до точки встречи и до начала массива равны
            while(slow != fast):
                slow = slow.next
                if fast == None:
                    return fast
                else:
                    fast = fast.next
            return slow
