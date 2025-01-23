def binary_search(arr, x):
	low = 0
	high = len(arr) - 1
	while low <= high:
		mid = (low + high) // 2
		if arr[mid] == x:
			return mid
		elif arr[mid] < x:
			low = mid + 1
		else:
			high = mid - 1
	return -1

# Example usage
arr = [2, 5, 7, 11, 14, 21, 27, 30, 36]
target = 27
print(binary_search(arr, target))