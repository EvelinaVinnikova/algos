#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 100000  // Размер массива


// Классическое разбиение Ломуто
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

int hoare_partition(int arr[], int low, int high) {
    int pivot = arr[low];  // Опорный элемент (первый в массиве)
    int i = low - 1, j = high + 1;

    while (1) {
        do {
            i++;
        } while (arr[i] < pivot);

        do {
            j--;
        } while (arr[j] > pivot);

        if (i >= j)
            return j;  // Возвращаем индекс разделения

        // Обмен arr[i] и arr[j]
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}

void fill_array(int arr[], int size) {
    for (int i = 0; i < size; i++)
        arr[i] = rand() % 1000;  // Заполняем случайными числами
}

void benchmark(void (*partition)(int[], int, int), int arr[], int size, const char *name) {
    clock_t start = clock();
    partition(arr, 0, size - 1);  // Запускаем разбиение
    clock_t end = clock();
    printf("%s: %f секунд\n", name, (double)(end - start) / CLOCKS_PER_SEC);
}

int main() {
    srand(time(NULL));

    int arr1[SIZE], arr2[SIZE], arr3[SIZE];

    fill_array(arr1, SIZE);
    fill_array(arr2, SIZE);
    fill_array(arr3, SIZE);

    benchmark(lomuto_partition, arr1, SIZE, "Ломуто (классический)");
    benchmark(lomuto_branchless_partition, arr2, SIZE, "Ломуто (без ветвлений)");
    benchmark(hoare_partition, arr3, SIZE, "Хоара");

    return 0;
}
