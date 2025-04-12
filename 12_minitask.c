#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 2000000 // Размер массива

int lomuto_partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Опорный элемент (последний в массиве)
    int i = low - 1;  // Индекс меньших элементов

    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            // Обмен элементов arr[i] и arr[j]
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    // Ставим pivot на своё место
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return i + 1;  // Возвращаем индекс pivot
}

void lomuto_sort(int arr[], int low, int high) {
    if (low < high) {
        int p = lomuto_partition(arr, low, high);
        lomuto_sort(arr, low, p - 1);
        lomuto_sort(arr, p + 1, high);
    }
}

int lomuto_branchless_partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        int smaller = -(arr[j] <= pivot);  // Если arr[j] <= pivot → smaller = -1, иначе 0
        i += smaller & 1;  // Увеличиваем i, если arr[j] <= pivot

        // Обмен arr[i] и arr[j] без условия
        int temp1 = arr[i];
        int temp2 = arr[j];
        arr[i] = temp2 ^ ((temp1 ^ temp2) & smaller);
        arr[j] = temp1 ^ ((temp1 ^ temp2) & smaller);
    }

    // Ставим pivot на своё место
    int temp1 = arr[i + 1];
    int temp2 = arr[high];
    arr[i + 1] = temp2 ^ ((temp1 ^ temp2) & -1);
    arr[high] = temp1 ^ ((temp1 ^ temp2) & -1);

    return i + 1;
}

void lomuto_branchless_sort(int arr[], int low, int high) {
    if (low < high) {
        int p = lomuto_branchless_partition(arr, low, high);
        lomuto_branchless_sort(arr, low, p - 1);
        lomuto_branchless_sort(arr, p + 1, high);
    }
}

int hoare_partition(int *arr, int low, int high) {
    int pivot = arr[low];
    int i = low - 1;
    int j = high + 1;

    while (1) {
        int ai;
        do {
            i++;
            ai = arr[i];
        } while (ai < pivot);

        int aj;
        do {
            j--;
            aj = arr[j];
        } while (aj > pivot);

        if (i >= j)
            return j;

        // Обмен без временной переменной (опционально)
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void hoare_sort(int arr[], int low, int high) {
    if (low < high) {
        int p = hoare_partition(arr, low, high);
        hoare_sort(arr, low, p - 1);
        hoare_sort(arr, p + 1, high);
    }
}

void fill_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand();
    } // Заполняем случайными числами
}

void benchmark(void (*sort)(int[], int, int), int arr[], int size, const char *name) {
    clock_t start = clock();
    sort(arr, 0, size - 1);  // Запускаем разбиение
    clock_t end = clock();
    printf("%s: %f секунд\n", name, (double)(end - start) / CLOCKS_PER_SEC);
}

int main() {
    srand((unsigned)time(NULL));

    // Выделение больших массивов в куче
    int *arr1 = malloc(SIZE * sizeof(int));
    int *arr2 = malloc(SIZE * sizeof(int));
    int *arr3 = malloc(SIZE * sizeof(int));

    if (!arr1 || !arr2 || !arr3) {
        fprintf(stderr, "Ошибка: не удалось выделить память.\n");
        return 1;
    }

    fill_array(arr1, SIZE);
    fill_array(arr2, SIZE);
    fill_array(arr3, SIZE);

    benchmark(lomuto_sort, arr1, SIZE, "Lomuto");
    benchmark(lomuto_branchless_sort, arr2, SIZE, "Lomuto(branch free)");
    benchmark(hoare_sort, arr3, SIZE, "Hoare");

    free(arr1);
    free(arr2);
    free(arr3);

    return 0;
}
