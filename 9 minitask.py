def lsd_radix_sort_strings(arr):
    if not arr:
        return
    indx_arr = [0] * 256
    max_len = len(arr[0]) # длина всех строк в массиве

    for i in range(max_len - 1, -1, -1): # итерация по слову
        new_arr = []
        for j in range(0, len(arr)): # итерация по всему массиву из строк
            k = ord(arr[j][i])
            indx_arr[k] += 1
        dict = {ord(word[i]): word for word in arr}
        print(dict)
        for n in range(len(indx_arr)):
            while(indx_arr[n] > 0):
                new_arr.append(dict[n])
                indx_arr[n] -= 1
        print(new_arr)
        arr = new_arr


arr = ['pbc', 'bca', 'dbb', '!agh']
lsd_radix_sort_strings(arr)
