list_basic = [1, 2, 3, 45, 356, 569, 600, 705, 923]


def search(number: id) -> bool:
    left = 0
    right = len(list_basic) - 1
    while left <= right:
        middle = (left + right) // 2
        if list_basic[middle] == number:
            return True
        elif list_basic[middle] > number:
            right = middle - 1
        else:
            left = middle + 1
    return False


print(search(1))
print(search(200))
print(search(923))
