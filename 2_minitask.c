#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define BASE 10 //numeral system
#define MIN_LENGTH_FOR_KARATSUBA 4 //figures that are shorter than this number are multiplied with the quadratic method

typedef unsigned long int size_length; //type for the length of the figure

struct long_value { //type for large figures
  int* values; //the array of numbers in reverse order
  size_length length; //the length of the figure

};

void* nc_malloc(size_t size){
    void* result = malloc(size);
    if (result == NULL){
        printf("Out of memory\n");
        exit(1);
    }
    return result;
}

typedef struct long_value long_value;
 
long_value sum(long_value a, long_value b) { //summarizing two long figures. Longest figure is taken as the first argument.

    long_value s;

    s.length = a.length + 1;
    s.values = (int*)nc_malloc(s.length*sizeof(int));
    s.values[a.length - 1] = a.values[a.length - 1];
    s.values[a.length] = 0;

    for (size_length i = 0; i < b.length; ++i)
    s.values[i] = a.values[i] + b.values[i];
    return s;

}


long_value* sub(long_value* a, long_value b) { //substracting one long figure from another.
  for (size_length i = 0; i < b.length; ++i)
    a->values[i] -= b.values[i];

  return a;

}


void normalize(long_value l) { // normalizing the figure according to it's base

  for (size_length i = 0; i < l.length - 1; ++i) {
    if (l.values[i] >= BASE) { //if the figure is larger than the max, то организовавается перенос
      int carryover = l.values[i] / BASE;
      l.values[i + 1] += carryover;
      l.values[i] -= carryover * BASE;

    } else if (l.values[i] < 0) { //если меньше - borrow
      int carryover = (l.values[i] + 1) / BASE - 1;
      l.values[i + 1] += carryover;
      l.values[i] -= carryover * BASE;
    }
  }
}

 
long_value karatsuba(long_value a, long_value b) {
  long_value product; //resulting произведение
  product.length = a.length + b.length;
  product.values = (int*)nc_malloc(product.length*sizeof(int));

  if (a.length < MIN_LENGTH_FOR_KARATSUBA) { //если число короче то apply native умножение
    memset(product.values, 0, sizeof(int) * product.length);
    for (size_length i = 0; i < a.length; ++i){
      for (size_length j = 0; j < b.length; ++j){
        product.values[i + j] += a.values[i] * b.values[j];
        }
    }

  } else { //multiplying with метод Карацубы
    long_value a_part1; //младшая часть числа a
    a_part1.values = a.values;
    a_part1.length = (a.length + 1) / 2;

    long_value a_part2; //старшая часть числа a
    a_part2.values = a.values + a_part1.length;
    a_part2.length = a.length / 2;
 
    long_value b_part1; //младшая часть числа b
    b_part1.values = b.values;
    b_part1.length = (b.length + 1) / 2;

    long_value b_part2; //старшая часть числа b
    b_part2.values = b.values + b_part1.length;
    b_part2.length = b.length / 2; 

    long_value sum_of_a_parts = sum(a_part1, a_part2); //cумма частей числа a
    normalize(sum_of_a_parts);

    long_value sum_of_b_parts = sum(b_part1, b_part2); //cумма частей числа b
    normalize(sum_of_b_parts);

    long_value product_of_sums_of_parts = karatsuba(sum_of_a_parts, sum_of_b_parts);

 
    long_value product_of_first_parts = karatsuba(a_part1, b_part1); //младший член
    long_value product_of_second_parts = karatsuba(a_part2, b_part2); //старший член
    long_value* sum_of_middle_terms = sub((sub(&product_of_sums_of_parts, product_of_first_parts)), product_of_second_parts);

    //finding the sum of the middle members
    //Summarizing of многочлена

    memcpy(product.values, product_of_first_parts.values, product_of_first_parts.length * sizeof(int));

    memcpy(product.values + product_of_first_parts.length, product_of_second_parts.values, product_of_second_parts.length * sizeof(int));

    for (size_length i = 0; i < (sum_of_middle_terms->length); ++i){
      product.values[a_part1.length + i] += sum_of_middle_terms->values[i];
    }

    free(sum_of_a_parts.values);
    free(sum_of_b_parts.values);
    free(product_of_sums_of_parts.values);
    free(product_of_first_parts.values);
    free(product_of_second_parts.values);
  }

  normalize(product);
  return product;
}


void reverse_array(char* array_symb){ 
    size_t left = 0;
    size_t right = strlen(array_symb) - 1;
    char temp;
    while(left < right){
        temp = array_symb[left];
        array_symb[left] = array_symb[right];
        array_symb[right] = temp;
        left++;
        right--;
    }
}

void printing(long_value result){
    size_t started = 0;
    for(int i = result.length - 1; i >= 0; i--){
        if(result.values[i] == 0 && started == 0)
            continue;
        started = 1;
        printf("%d",result.values[i]);
    }
    printf("\n");
}


#define MAX_LEN 100

void scanning_number(char array[]){
    char tmp;
    size_t i = 0;
    while(scanf("%c", &tmp)!= 0 && tmp != '\n'){
        array[i++] = tmp;
    }
    array[i] = '\0';
}

long_value to_struct(char* word){
    long_value result;
    result.values = (int*)nc_malloc(strlen(word)*sizeof(int));
    reverse_array(word);
    for(size_t i = 0; i < strlen(word); i++){
        result.values[i] = word[i] - '0';
    }
    result.length = (size_length)strlen(word);
    return result;
}

int compare_arrays(int* arr1, int* arr2, int size1, int size2) {
    for (int i = 0; i < size1; i++) {
        if (arr1[(size1-1)-i] != arr2[i]) {
            return 0;
        }
    }
    return 1;
}

int main(){
    // char frst_num[MAX_LEN];
    // scanning_number(frst_num);
    // char scnd_num[MAX_LEN];
    // scanning_number(scnd_num);
    
///CHECK_1
    // char frst_num[] = {'9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '\0'};
    // char scnd_num[] = {'8', '8', '8', '8', '8', '8', '8', '8', '8', '8', '\0'};
    // long_value frst = to_struct(&frst_num);
    // long_value scnd = to_struct(&scnd_num);
    // int exp_result[] = {8,8,8,8,8,8,8,8,8,7,1,1,1,1,1,1,1,1,1,2};
    // int len_exp_res = sizeof(exp_result)/sizeof(exp_result[0]);
    // long_value real_res = karatsuba(frst, scnd);
    // int* real_result = real_res.values;
    // int len_real_res = real_res.length;
///CHECK_2
    // char frst_num[] = {'9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '8', '6', '4', '3', '\0'};
    // char scnd_num[] = {'8', '8', '8', '8', '8', '1', '1', '1', '8', '8', '1', '1', '1', '1', '\0'};
    // long_value frst = to_struct(&frst_num);
    // long_value scnd = to_struct(&scnd_num);
    // int exp_result[] = {8,8,8,8,8,1,1,1,8,7,9,9,0,4,7,8,8,3,2,1,7,7,3,3,2,3,7,3};
    // int len_exp_res = sizeof(exp_result)/sizeof(exp_result[0]);
    // long_value real_res = karatsuba(frst, scnd);
    // int* real_result = real_res.values;
    // int len_real_res = real_res.length;
///CHECK_3
    char frst_num[] = {'6', '4', '3', '\0'};
    char scnd_num[] = {'8', '1', '1', '\0'};
    long_value frst = to_struct(&frst_num);
    long_value scnd = to_struct(&scnd_num);
    int exp_result[] = {5,2,1,4,7,3};
    int len_exp_res = sizeof(exp_result)/sizeof(exp_result[0]);
    long_value real_res = karatsuba(frst, scnd);
    int* real_result = real_res.values;
    int len_real_res = real_res.length;

    if(compare_arrays(exp_result, real_result, len_exp_res, len_real_res)){
        printf("Succesful result!\n");
    }
    // printing(real_res);
    free(frst.values);
    free(scnd.values);
    free(real_res.values);
    return 0;
}
