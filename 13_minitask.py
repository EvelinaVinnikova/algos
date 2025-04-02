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
        return quickselect(y_coords, n // 2)
    else:
        return (quickselect(y_coords, n // 2 - 1) + quickselect(y_coords, n // 2)) / 2


oil_wells = [(1, 3), (2, 1), (3, 7), (4, 5), (5, 9)]
optimal_y = find_pipeline_y(oil_wells)
print("Оптимальная координата Y для нефтепровода:", optimal_y)

def test():
    # нечетное количество скважин
    wells1 = [(1, 3), (2, 1), (3, 7), (4, 5), (5, 9)]
    assert find_pipeline_y(wells1) == 5

    # четное количество скважин
    wells2 = [(1, 2), (2, 4), (3, 6), (4, 8)]
    assert find_pipeline_y(wells2) == 5.0

    # все скважины на одной высоте
    wells3 = [(0, 10), (1, 10), (2, 10)]
    assert find_pipeline_y(wells3) == 10

    # сортированные координаты по убыванию
    wells4 = [(0, 9), (1, 7), (2, 5), (3, 3), (4, 1)]
    assert find_pipeline_y(wells4) == 5

    # две скважины
    wells5 = [(0, 10), (1, 20)]  # y = [10, 20] -> (10 + 20)/2 = 15.0
    assert find_pipeline_y(wells5) == 15.0

    # одна скважина
    wells6 = [(0, 42)]
    assert find_pipeline_y(wells6) == 42
    
    print("✅ All tests passed!")

test()
