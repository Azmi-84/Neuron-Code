// Practice have to be done


// 1. Write a program in C to read n number of values in an array and display them
// in reverse order.
// 2. Write a program in C to copy the elements of one array into another array.
// 3. Write a program in C to find the maximum and minimum elements in an array.
// 4. Write a program in C to merge two arrays of the same size sorted in
// descending order.
// 5. Addition of two matrix
// 6. Find sum of row values and column values of a matrix
// 7. Write a program in C to print or display the lower triangular
// matrix by setting the upper values as zero
// 8. Matrix multiplication of 2 matrix
// Pass array to a function


//     int a, b;
//     int valid_input = 1; // Flag to track valid input
    
//     printf("First input: ");
//     if(scanf("%d", &a) != 1) {
//         valid_input = 0;
//     }
    
//     printf("Second input: ");
//     if(scanf("%d", &b) != 1) {
//         valid_input = 0;
//     }
    
//     // Clear input buffer if there was invalid input
//     if(!valid_input) {
//         while(getchar() != '\n');
//     }

//     int res = 0;
//     if (valid_input)
//     {
//         int ch;
//         printf("1. Add\n2. Substract\n3. Multiply\n4. Divide\n");
//         printf("Choice: ");
//         if(scanf("%d", &ch) != 1) {
//             printf("Invalid choice\n");
//             return 1;
//         }
        
//         switch (ch)
//         {
//         case 1:
//             res = a + b;
//             printf("%d\n", res);
//             break;
//         case 2:
//             res = a - b;
//             printf("%d\n", res);
//             break;
//         case 3:
//             res = a * b;
//             printf("%d\n", res);
//             break;
//         case 4:
//             res = a / b;
//             printf("%d\n", res);
//             break;
//         default:
//             printf("Invalid choice\n");
//             break;
//         }
//     } else {
//         printf("Invalid input: Please enter integers only\n");
//     }
//     return 0;

//     int num;
//     scanf("%d", &num);
//     getFactorial(num);
//     return 0;
// }

// int getFactorial(int num) {
//     int res = 1;
//     if(num == 0) {
//         printf("%d\n", res);
//     } else {
//         for (int i = 1; i <= num; i++)
//         {
//             res = res*i;
//         }
//     }
//     printf("%d\n", res);
//     return res;

    // int size;
    // printf("size: ");
    // scanf("%d", &size);

    // int array[size];
    // for (int i = 0; i < size; i++)
    // {
    //     printf("[%d] ", i+1);
    //     scanf("%d", &array[i]);
    // }
    // int *ptr = array;
    // int sum = 0;
    
    // for (int i = 0; i < size; i++)
    // {
    //     sum += *(ptr+i);
    // }
    // printf("%d\n", sum);
    // printf("%d\n", *array);

    // int i, sum = 0;
    // for(int i=5; ; ++i) {
    //     if (i == 10)
    //     {
    //         continue;
    //     }
    //     if (i == 15)
    //     {
    //         break;
    //     }
    //     sum += i;
    //     printf("%d\n", sum);
    // }

    #include <stdio.h>

    // typedef struct employeeInfo {
    //     int ID;
    //     char NAME[50];
    //     float SALARY;
    // } employeeInfo;

    // int change(int *one, int *two) {
    //     printf("%d, %d\n", *one, *two);
    //     int temp;  // Use int, not int*
    //     temp = *two;
    //     *two = *one;
    //     *one = temp;
    //     printf("%d, %d\n", *one, *two);
    //     return 0;  // Add return statement
    // }
    
    int main() {
        int size;
        printf("Size: ");
        scanf("%d", &size);
        int arr[size];
        for (int i = 0; i < size; i++)
        {
            printf("%d element: ", i+1);
            scanf("%d", &arr[i]);
        }
        // int sum = 0;
        // for (int i = 0; i < size; i++)
        // {
        //     sum += arr[i];
        // }
        // float res = sum/size;
        // printf("Average %f\n", res);
        // Display array elements in reverse order
        // for (int i = size - 1; i >= 0; i--)
        // {
        //     printf("%d ", arr[i]);
        // }
        // int second_arr[size];
        // for (int i = 0; i < size; i++)
        // {
        //     second_arr[i] = arr[i];
        // }
        // for (int i = 0; i < size; i++)
        // {
        //     printf("%d ", second_arr[i]);
        // }

        // int max = arr[0];
        // int index = 0;
        // for (int i = 1; i < size; i++)
        // {
        //     if (max < arr[i])
        //     {
        //         index = i;
        //         max = arr[i];
        //     }
            
        // }
        // printf("Max %d\n", arr[index]);
        // printf("Max %d\n", max);
        int size_02;
        printf("Size: ");
        scanf("%d", &size_02);
        int second_arr[size_02];
        for (int i = 0; i < size_02; i++)
        {
            scanf("%d",&second_arr[i]);
        }
        int third_arr[size+size_02];
        for (int i = 0; i < size; i++)
        {
            third_arr[i] = arr[i];
        }
        for (int i = 0; i < size_02; i++)
        {
            third_arr[size + i] = second_arr[i];
        }
        for (int i = 0; i < (size+size_02); i++)
        {
            printf("%d ", third_arr[i]);
        }
        // Sort array in descending order using bubble sort
        for (int i = 0; i < (size+size_02)-1; i++)
        {
            for (int j = 0; j < (size+size_02)-i-1; j++)
            {
                if (third_arr[j] < third_arr[j+1]) // For descending order use < instead of >
                {
                    int temp = third_arr[j];
                    third_arr[j] = third_arr[j+1];
                    third_arr[j+1] = temp;
                }
            }
        }
        
        printf("\nSorted array in descending order: \n");
        for (int i = 0; i < (size+size_02); i++)
        {
            printf("%d ", third_arr[i]);
        }
    }