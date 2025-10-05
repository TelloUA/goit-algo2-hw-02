def min_max_find(array):
    # дробимо до мінімального списку, і в такому списку повертаємо єдине значення цього списку
    if len(array) <= 1:
        return (array[0], array[0])
    
    mid = len(array) // 2
    left = min_max_find(array[:mid])
    right = min_max_find(array[mid:])

    return mm_merge(left, right)

def mm_merge(left, right):
    #  на етапі обʼєднання робимо простий if з двумя елементами
    min = left[0] if left[0] < right[0] else right[0]
    max = left[1] if left[1] > right[1] else right[1]
    return (min, max)

arr = [38, 27, -43, 3, 9, -46, 82, 10, 5, 16, 101]
min_max = min_max_find(arr)
print(min_max)