import time
from typing import Callable, List


def StandartMatrixMultip(first_matrix: list[int], second_matrix: list[int]) -> list[int]:
    assert len(first_matrix) == len(second_matrix), "Matrix are not equal in size"
    n = int(len(first_matrix)**0.5)
    result_matrix = [0] * n * n
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result_matrix[i * n + j] += first_matrix[i * n + k] * second_matrix[k * n + j]
    return result_matrix


#####################################################################################################
def SplitMatrix(a: list[int], n: int, a_11, a_12, a_21, a_22):
    for i in range(0, n // 2):
        for j in range(0, n // 2):
            a_11[i * n // 2 + j] = a[i * n + j]

    for i in range(0, n // 2):
        for j in range(n // 2, n):
            a_12[i * n // 2 + j - (n // 2)] = a[i * n + j]

    for i in range(n // 2, n):
        for j in range(0, n // 2):
            a_21[(i - n // 2) * n // 2 + j] = a[i * n + j]

    for i in range(n // 2, n):
        for j in range(n // 2, n):
            a_22[(i - n // 2) * n // 2 + j - n // 2] = a[n * i + j]


def SummMatrix(a: list[int], b: list[int])-> list[int]:
    assert len(a) == len(b), 'Summarizing not equal-sized matrix'
    c = [0] * len(a)
    n = int(len(a)**0.5)
    for i in range(n):
        for j in range(n):
            c [n*i+j] = a[n * i + j] + b[n * i + j]
    return c


def MergeMatrix(c_11, c_12, c_21, c_22) -> list[int]:
    n = int((len(c_11) + len(c_12) + len(c_21)+ len(c_22))**0.5)
    c = [0] * (n * n)
    for i in range(0, n//2):
        for j in range(0, n//2):
            c[n * i + j] = c_11[(n//2)*i+j]

    for i in range(0, n//2):
        for j in range(n//2, n):
            c[n * i + j] = c_12[(n//2)*i + (j-n//2)]

    for i in range(n//2, n):
        for j in range(0, n // 2):
            c[n * i + j] = c_21[(n // 2) * (i - n//2) + j]

    for i in range(n//2, n):
        for j in range(n//2, n):
            c[n * i + j] = c_22[(n // 2) * (i - n//2) + (j - n // 2)]
    return c


def QuickMatrixMultip(a: list[int], b: list[int]) -> list[int]:
    assert len(a) == len(b), "Matrix are not equal in size"
    n = int(len(a) ** 0.5)
    if len(a) > 2:
        a_11, a_12, a_21, a_22 = ([0] * (n // 2 * n // 2) for _ in range(4))
        SplitMatrix(a, n, a_11, a_12, a_21, a_22)

        b_11, b_12, b_21, b_22 = ([0] * (n // 2 * n // 2) for _ in range(4))
        SplitMatrix(b, n, b_11, b_12, b_21, b_22)

        top_left = SummMatrix(QuickMatrixMultip(a_11, b_11), QuickMatrixMultip(a_12, b_21))
        #print(f"top left:{top_left}")
        top_right = SummMatrix(QuickMatrixMultip(a_11, b_12), QuickMatrixMultip(a_12, b_22))
        #print(f"top_right:{top_right}")
        low_left = SummMatrix(QuickMatrixMultip(a_21, b_11), QuickMatrixMultip(a_22, b_21))
        #print(f"low_left:{low_left}")
        low_right = SummMatrix(QuickMatrixMultip(a_21, b_12), QuickMatrixMultip(a_22, b_22))
        #print(f"low_right:{low_right}")
        return MergeMatrix(top_left, top_right, low_left, low_right)

    else:
        return StandartMatrixMultip(a, b)


####################################################################################################
def SubMatrix(a: list[int], b: list[int]) -> list[int]:
    assert len(a) == len(b), "Subtraction requires equal-sized matrices"
    return [a[i] - b[i] for i in range(len(a))]

def StrassenMatrixMultip(a: list[int], b: list[int]) -> list[int]:
    assert len(a) == len(b), "Matrix are not equal in size"
    n = int(len(a) ** 0.5)
    if len(a) > 4:
        a_11, a_12, a_21, a_22 = ([0] * (n // 2 * n // 2) for _ in range(4))
        b_11, b_12, b_21, b_22 = ([0] * (n // 2 * n // 2) for _ in range(4))

        SplitMatrix(a, n, a_11, a_12, a_21, a_22)
        SplitMatrix(b, n, b_11, b_12, b_21, b_22)

        P1 = StrassenMatrixMultip(a_11, SubMatrix(b_12, b_22))
        P2 = StrassenMatrixMultip(SummMatrix(a_11, a_12), b_22)
        P3 = StrassenMatrixMultip(SummMatrix(a_21, a_22), b_11)
        P4 = StrassenMatrixMultip(a_22, SubMatrix(b_21, b_11))
        P5 = StrassenMatrixMultip(SummMatrix(a_11, a_22), SummMatrix(b_11, b_22))
        P6 = StrassenMatrixMultip(SubMatrix(a_12, a_22), SummMatrix(b_21, b_22))
        P7 = StrassenMatrixMultip(SubMatrix(a_11, a_21), SummMatrix(b_11, b_12))

        Q1 = SummMatrix(SubMatrix(SummMatrix(P5, P4), P2), P6)
        Q2 = SummMatrix(P1, P2)
        Q3 = SummMatrix(P3, P4)
        Q4 = SummMatrix(SubMatrix(SummMatrix(P1, P5), P3), SubMatrix([0]*len(P7), P7))

        return MergeMatrix(Q1, Q2, Q3, Q4)
    else:
        return StandartMatrixMultip(a, b)


########################################################################################################
# a = [1, 2, 3, 4, 5, 6, 7, 0, 9, 10, 11, 12, 13, 14, 15, 16]
# b = [1, 2, 3, 9, 2, 1, 0, 8, 16, 32, 0, 56, 9, 0, 1, 2]
# result = StrassenMatrixMultip(a, b)
# print(result)


def CheckAlgorithms(algorithms: List[Callable], data_sets: List[tuple], algo_names: List[str]) -> None:
    report = []

    for data_id, (matrix_a, matrix_b) in enumerate(data_sets):
        print(f"\nData Set {data_id + 1} (Size: {int(len(matrix_a) ** 0.5)}x{int(len(matrix_a) ** 0.5)}):")
        for algo, name in zip(algorithms, algo_names):
            start_time = time.perf_counter()
            result = algo(matrix_a, matrix_b)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            report.append({
                'Algorithm': name,
                'Data Set': data_id + 1,
                'Matrix Size': int(len(matrix_a) ** 0.5),
                'Time (s)': elapsed_time
            })
            print(f"  {name}: {elapsed_time:.6f} seconds")

    print("\nSummary Report:")
    print(f"{'Algorithm':<25}{'Data Set':<10}{'Matrix Size':<12}{'Time (s)':<10}")
    for record in report:
        print(
            f"{record['Algorithm']:<25}{record['Data Set']:<10}{record['Matrix Size']:<12}{record['Time (s)']:<10.6f}")

    # Когда Штрассен начнет выигрывать
    print("\nStrassen Advantage Report:")
    sizes = sorted(set(record['Matrix Size'] for record in report))
    for size in sizes:
        strassen_time = next(
            (r['Time (s)'] for r in report if r['Algorithm'] == 'Strassen Multiplication' and r['Matrix Size'] == size),
            float('inf'))
        standard_time = next(
            (r['Time (s)'] for r in report if r['Algorithm'] == 'Standard Multiplication' and r['Matrix Size'] == size),
            float('inf'))
        quick_time = next(
            (r['Time (s)'] for r in report if r['Algorithm'] == 'Quick Multiplication' and r['Matrix Size'] == size),
            float('inf'))

        if strassen_time < standard_time and strassen_time < quick_time:
            print(f"Strassen starts winning at size {size}x{size}.")
            break



algorithms = [
    StandartMatrixMultip,
    QuickMatrixMultip,
    StrassenMatrixMultip
]
algo_names = [
    "Standard Multiplication",
    "Quick Multiplication",
    "Strassen Multiplication"
]

data_sets = [
    (
        [1, 2, 3, 4],  # 2x2 матрица A
        [5, 6, 7, 8]  # 2x2 матрица B
    ),
    (
        [i for i in range(16)],  # 4x4 мартица A
        [i * 2 for i in range(16)]  # 4x4 матрица B
    ),
    (
        [i for i in range(64)],  # 8x8 матрица A
        [i * 3 for i in range(64)]  # 8x8 матрица B
    ),
    (
        [i for i in range(256)],  # 16x16 матрица A
        [i * 2 for i in range(256)]  # 16x16 матрица B
    ),
    (
        [i for i in range(1024)],  # 32x32 матрица A
        [i * 2 for i in range(1024)]  # 32x32 матрица B
    )
]

CheckAlgorithms(algorithms, data_sets, algo_names)
