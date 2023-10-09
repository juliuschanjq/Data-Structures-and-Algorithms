# Python3 program to implement
# interpolation search
# with recursion
# If x is present in arr[0..n-1], then
# returns the index of it, else returns -1.
def interpolationSearch(arr, lo, hi, x):
    # Since the array is sorted, an element present
    # in the array must be in the range defined by the corners.
    if (lo <= hi and x >= arr[lo] and x <= arr[hi]):
        # Probing the position with keeping
        # uniform distribution in mind.
        pos = lo + ((hi - lo) // (arr[hi] - arr[lo])) * (x - arr[lo])
        # Condition of target found
        if arr[pos] == x:
            return pos
        # If x is larger, x is in the right subarray
        if arr[pos] < x:
            return interpolationSearch(arr, pos + 1, hi, x)
        # If x is smaller, x is in the left subarray
        if arr[pos] > x:
            return interpolationSearch(arr, lo, pos - 1, x)
    return -1

# Driver code
# Array of items in which
# search will be conducted
arr = [10, 12, 13, 16, 18, 19, 20,
       21, 22, 23, 24, 33, 35, 42, 47]
n = len(arr)
# Element to be searched
x = 18
index = interpolationSearch(arr, 0, n - 1, x)
if index != -1:
    print("Element found at index", index)
else:
    print("Element not found")
