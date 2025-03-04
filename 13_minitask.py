import random


def quickselect(arr, k):
    """k-ая статистика"""
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k < len(lows):
        return quickselect(lows, k)
    elif k < len(lows) + len(pivots):
        return pivots[0]
    else:
        return quickselect(highs, k - len(lows) - len(pivots))


def find_pipeline_y(oil_wells):
    """находим оптимальную координату y для нефтепровода"""
    y_coords = [y for _, y in oil_wells]
    n = len(y_coords)
    if n % 2 == 1:
        return quickselect(y_coords, n // 2)  # нечёт
    else:
        return (quickselect(y_coords, n // 2 - 1) + quickselect(y_coords, n // 2)) / 2  # чёт


oil_wells = [(1, 3), (2, 1), (3, 7), (4, 5), (5, 9)]
optimal_y = find_pipeline_y(oil_wells)
print("Оптимальная координата Y для нефтепровода:", optimal_y)

