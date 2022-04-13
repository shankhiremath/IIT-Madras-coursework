# no libraries are allowed

""" Add your functions here """
def euclid_dist(ax, ay, bx, by):
    '''
    Input: x and y coordinates of 2 points
    Output: euclidean distance between the 2 points
    '''
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

def partition(arr, low, high):
	# partitions the array such that the pivot (middle element in this case) is in its
	# correct position

    pivot = arr[(low + high) // 2]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, k, low, high):
    # modified quicksort to sort the right half of the array only when needed
	# we need the first k smallest elements to be sorted. The rest are not required
    if low < high:
        p = partition(arr, low, high)

        # recursive call on the left of pivot. This call is always present since we want the
        # first k smallest elements.
        quicksort(arr, k, low, p - 1)

        if p < k:
            # recursive call on the right of pivot of partition is less than k because we only need the
            # first k smallest elements
            quicksort(arr, k, p + 1, high)

def insertionsort(arr):
	# For small arrays, insertion sort is used
    l = len(arr)
    for i in range(1, l):
        idx = i
        curr = arr[i]
    while idx > 0 and arr[idx - 1] > curr:
        arr[idx] = arr[idx - 1]
        idx -= 1
    arr[idx] = curr

def k_closest_points(x_array, y_array, point, k):
	"""
	(list of float, list of float, tuple of two floats, int) -> (list of float), (list of float)
	
	>>> k_closest_points([1.0, 1.0, 3.0, 5.0], [0.0, 3.0, 4.0, 5.0], (0.0, 0.0), 2)
	    [1.0, 1.0], [0.0, 3.0]
	"""
	""" Add your code here """
	px, py = point
	distances, dist_dict = [], {}
	# Calculate the euclidean distances for all n points
	l = len(x_array)
	for i in range(l):
		dist = euclid_dist(x_array[i], y_array[i], px, py)
		distances.append(dist)
		dist_dict[dist] = i
	
	# For arrays of length less than 30, insertion sort is used. Else, a modified quicksort is used
	if l < 30:
		insertionsort(distances)
	else:
		quicksort(distances, k, 0, l - 1)
	
	distances, x_out, y_out = distances[:k], [], []
	for d in distances:
		ans_idx = dist_dict[d]
		x_out.append(x_array[ans_idx])
		y_out.append(y_array[ans_idx])

    # Print final answer
	print(x_out, ', ', y_out, sep = '')

	# Euclidean distance for n elements = O(n)
	# Sorting the distances takes O(n log n) because we are using insertion sort or a modified quicksort
	# where the complexity is O(n log n).
	# The rest of the operations like accessing the elements do not have high time complexity.
	# Hence, the whole operation has a time complexity of O(n log n).

test = k_closest_points([1.0, 1.0, 3.0, 5.0], [0.0, 3.0, 4.0, 5.0], (0.0, 0.0), 2)