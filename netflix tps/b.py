import heapq
class Solution(object):
    def lastStoneWeight(self, stones):
        """
        :type stones: List[int]
        :rtype: int
        """
        
        stones2 = [0]*len(stones)
        for i in range(len(stones)):
            stones2[i] = -stones[i]
        
        h = heapq.heapify(stones2)

        while len(h) > 1:
            lrg = heapq.heappop(h)
            nlrg = heapq.heappop(h)
            
            heapq.heappushpop(h, abs(h-n))
        
        return 0 if len(h) == 0 else -h[0]
