from heapq import heappush, heappop
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        heap = []
        
        for i, lst in enumerate(lists):
            if lst:
                heappush(heap, (lst.val, i, lst))

        dummy = ListNode(0)
        current = dummy

        while heap:
            val, i, node = heappop(heap)
            current.next = node
            current = node

            if node.next:
                heappush(heap, (node.next.val, i, node.next))

        return dummy.next
