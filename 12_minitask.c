#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <string.h>

#define SIZE 4000000 // Размер массива

static inline void swap(long* a, long* b) {
    long temp = *a;
    *a = *b;
    *b = temp;
}

long* lomuto_partition(long* first, long* last) {
    assert(first <= last);
    if (last - first < 2)
        return first;

    --last;

    if (*first > *last)
        swap(first, last);

    long* pivot_pos = first;
    long pivot = *first;

    do {
        ++first;
    } while (*first < pivot);

    assert(first <= last);

    // Main course.
    for (long* read = first + 1; read < last; ++read) {
        long x = *read;
        if (x < pivot) {
            *read = *first;
            *first = x;
            ++first;
        }
    }

    // Put the pivot where it belongs.
    assert(*first >= pivot);
    --first;
    *pivot_pos = *first;
    *first = pivot;
    return first;
}

void lomuto_sort(long* arr, long* arr_last) {
    if (arr >= arr_last - 1) return;
    long* p = lomuto_partition(arr, arr_last);
    lomuto_sort(arr, p);
    lomuto_sort(p+1, arr_last);
}

long* lomuto_partition_branchfree(long* first, long* last) {
    assert(first <= last);
    if (last - first < 2)
        return first;

    --last;
    if (*first > *last)
        swap(first, last);

    long* pivot_pos = first;
    long pivot = *first;

    do {
        ++first;
        assert(first <= last);
    } while (*first < pivot);

    for (long* read = first + 1; read < last; ++read) {
        long x = *read;
        int smaller = -(x < pivot);
        long delta = smaller & (read - first);

        first[delta] = *first;
        read[-delta] = x;
        first -= smaller;
    }

    assert(*first >= pivot);
    --first;
    *pivot_pos = *first;
    *first = pivot;
    return first;
}

void lomuto_branchfree_sort(long* arr, long* arr_last) {
    if (arr >= arr_last - 1) return;
    long* p = lomuto_partition_branchfree(arr, arr_last);
    lomuto_branchfree_sort(arr, p);
    lomuto_branchfree_sort(p+1, arr_last);
}

long* hoare_partition(long* first, long* last) {
    assert(first <= last);
    if (last - first < 2)
        return first;

    --last;
    if (*first > *last)
        swap(first, last);

    long* pivot_pos = first;
    long pivot = *pivot_pos;

    for (;;) {
        ++first;
        long f = *first;
        while (f < pivot)
            f = *++first;

        long l = *last;
        while (pivot < l)
            l = *--last;

        if (first >= last)
            break;

        *first = l;
        *last = f;
        --last;
    }

    --first;
    swap(first, pivot_pos);
    return first;
}

void hoare_sort(long* arr, long* arr_last) {
    if (arr >= arr_last - 1) return;
    long* p = hoare_partition(arr, arr_last);
    hoare_sort(arr, p);
    hoare_sort(p+1, arr_last);
}

void fill_array(long* arr, size_t size) {
    for (size_t i = 0; i < size; i++) {
        arr[i] = rand();
    }
}

void benchmark(void (*sort)(long*,long*), long* first ,long* last, const char *name) {
    clock_t start = clock();
    sort(first, last);
    clock_t end = clock();
    printf("%s: %f секунд\n", name, (double)(end - start) / CLOCKS_PER_SEC);
}

int main() {
    srand((unsigned)time(NULL));

    long* arr1 = malloc(SIZE * sizeof(long));
    long* arr2 = malloc(SIZE * sizeof(long));
    long* arr3 = malloc(SIZE * sizeof(long));

    if (!arr1 || !arr2 || !arr3) {
        fprintf(stderr, "Ошибка: не удалось выделить память.\n");
        return 1;
    }

    fill_array(arr1, SIZE);
    memcpy(arr2, arr1, SIZE*sizeof(long));
    memcpy(arr3, arr1, SIZE*sizeof(long));

    benchmark(lomuto_sort, arr1, arr1 + SIZE, "Lomuto");
    benchmark(lomuto_branchfree_sort, arr2, arr2 + SIZE, "Lomuto(branch free)");
    benchmark(hoare_sort, arr3, arr3 + SIZE, "Hoare");

    free(arr1);
    free(arr2);
    free(arr3);

    return 0;
}
