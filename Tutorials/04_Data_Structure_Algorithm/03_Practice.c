#include <stdio.h>
#include <stdlib.h>

// There are two methods for passing an array in a function:
// 1. Call by value
// 2. Call by reference

/**
 * Function to determine student category based on ID
 * Uses the 7th, 8th, and 9th digits of the ID for categorization
 */
void getStudentID(int arr[9], int len)
{
    int k = arr[6];               // Extracts 7th digit from the array
    int m = arr[7] * 10 + arr[8]; // Forms a two-digit number using the last two digits

    // Checking conditions for student categorization
    if (k == 1 && m % 2 == 1)
    {
        // printf("A1\n");
    }
    else if (k == 1 && m % 2 == 0)
    {
        // printf("A2\n");
    }
    else if (k == 2 && m % 2 == 1)
    {
        // printf("B1\n");
    }
    else
    {
        // printf("B2\n");
    }
}

/**
 * Function to print various patterns
 * Currently contains example implementations in comments
 */
void pattern()
{
    // Example: Uncomment and modify based on required pattern
    // for (int i = 0; i <= rows; i++)
    // {
    //     for (int j = 0; j <= i; j++)
    //     {
    //         printf("* ");
    //     }
    //     printf("\n");
    // }

    // Example: Alphabet pattern
    // char alphabet = 'A';
    // for (int i = 1; i <= (input - 'A' + 1); i++)
    // {
    //     for (int k = 1; k <= i; k++)
    //     {
    //         printf("%c", alphabet);
    //     }
    //     ++alphabet;
    //     printf("\n");
    // }
}

int main()
{
    // ========== ELIGIBILITY CHECK SECTION ==========
    int math = 0, phy = 0, chem = 0;

    // Taking user input for marks (currently commented out)
    // printf("Marks of Math: ");
    // scanf("%d", &math);
    // printf("Marks of Physics: ");
    // scanf("%d", &phy);
    // printf("Marks of Chemistry: ");
    // scanf("%d", &chem);

    // Eligibility check based on subject marks
    if (math >= 65 && phy >= 55 && chem >= 50 && (math + phy + chem) >= 190 && (math + phy) >= 140)
    {
        // printf("Eligible\n");
    }
    else
    {
        // printf("Not eligible\n");
    }

    // ========== STUDENT ID PROCESSING SECTION ==========
    int arr[9];
    // printf("Enter 9 Student IDs (space-separated): ");
    for (int i = 0; i < 9; i++)
    {
        // scanf("%d", &arr[i]);
    }

    int len = sizeof(arr) / sizeof(arr[0]); // Calculate array length

    if (len != 9)
    {
        // printf("Invalid ID\n");
    }

    getStudentID(arr, len); // Call function to process student IDs

    // ========== PATTERN PRINTING SECTION (COMMENTED) ==========
    // int rows = 0;
    // scanf("%d", &rows);
    // pattern(rows); // Call pattern function with rows

    // char input;
    // scanf("%c", &input);
    // pattern(input); // Call pattern function with character input

    // ========== SUM CALCULATION SECTION (COMMENTED) ==========
    // int num, sum = 0;

    // while (1)
    // {
    //     // printf("Enter a number (enter 0 to stop): ");
    //     // scanf("%d", &num);

    //     if (num == 0)
    //     {
    //         break;
    //     }
    //     sum += num;
    // }

    // printf("\nTotal sum of the numbers entered: %d\n", sum);

    // ========== FIND SMALLEST ELEMENTS SECTION (COMMENTED) ==========
    // int new_array[20];

    // int i = 0;
    // printf("Array element: ");
    // for (i = 0; i < 10; i++)
    // {
    //     scanf("%d", &new_array[i]);
    // }

    // int small = new_array[0];
    // int index = 0;

    // for (i = 1; i < 10; i++)
    // {
    //     if (new_array[i] < small)
    //     {
    //         small = new_array[i];
    //         index = i;
    //     }
    // }
    // printf("Smallest element: %d  | Index: %d\n", small, index);

    // int second_small = new_array[0];

    // if (index == 0)
    // {
    //     second_small = new_array[1];
    // }

    // for (i = 0; i < 10; i++)
    // {
    //     if (i == index)
    //     {
    //         continue;
    //     }

    //     if (new_array[i] < second_small)
    //     {
    //         second_small = new_array[i];
    //     }
    // }

    // printf("Second smallest element: %d\n", second_small);

    // ========== FREQUENCY COUNTING SECTION ==========
    int n_arr[20];

    printf("Enter 10 integers: ");
    for (int i = 0; i < 10; i++)
    {
        scanf("%d", &n_arr[i]);
    }

    for (int i = 0; i < 10; i++)
    {
        // This code checks if we've already processed this number before
        int counted = 0;
        for (int j = 0; j < i; j++)
        {
            if (n_arr[i] == n_arr[j])
            {
                counted = 1; // We found this number earlier in the array
                break;
            }
        }
        if (counted == 1)
        {
            continue; // Skip this number as we've already counted its frequency
        }

        int freq = 1;

        for (int k = i + 1; k < 10; k++)
        {
            if (n_arr[i] == n_arr[k])
            {
                freq++;
            }
        }

        printf("Num: %d || Freq: %d\n", n_arr[i], freq);
    }

    return 0;
}
