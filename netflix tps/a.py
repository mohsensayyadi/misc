

print("Hello, World!")

def merge(nums1, m, nums2, n):
    """
    :type nums1: List[int]
    :type m: int
    :type nums2: List[int]
    :type n: int
    :rtype: None Do not return anything, modify nums1 in-place instead.
    """
    x, y = m-1, n-1
    for i in range(m+n-1, -1, -1):
        print(i,x,y, "winner", max(nums1[x] , nums2[y]))
        if nums1[x] > nums2[y]:
            nums1[i] = nums1[x]
            x -=1
        else:
            nums1[i] = nums2[y]
            y -=1
    
    print(nums1)

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3

merge(nums1, m, nums2, n)
