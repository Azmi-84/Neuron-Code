#include <stdio.h>

// Swap function for integers
void swap_int(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Bubble sort for integer array (ascending)
void bubble_sort_int_asc(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                swap_int(&arr[j], &arr[j + 1]);
            }
        }
    }
}

// Bubble sort for integer array (descending)
void bubble_sort_int_desc(int arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] < arr[j + 1])
            {
                swap_int(&arr[j], &arr[j + 1]);
            }
        }
    }
}

// Custom string compare function (similar to strcmp but without using libraries)
int my_strcmp(const char *a, const char *b)
{
    while (*a && *b)
    {
        if (*a != *b)
            return *a - *b;
        a++;
        b++;
    }
    return *a - *b;
}

// Swap function for string pointers
void swap_str(char **a, char **b)
{
    char *temp = *a;
    *a = *b;
    *b = temp;
}

// Bubble sort for array of strings (ascending)
void bubble_sort_str_asc(char *arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (my_strcmp(arr[j], arr[j + 1]) > 0)
            {
                swap_str(&arr[j], &arr[j + 1]);
            }
        }
    }
}

// Bubble sort for array of strings (descending)
void bubble_sort_str_desc(char *arr[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (my_strcmp(arr[j], arr[j + 1]) < 0)
            {
                swap_str(&arr[j], &arr[j + 1]);
            }
        }
    }
}

int main()
{
    // Sorting integer arrays
    int num_arr[] = {5, 2, 9, 1, 5, 6};
    int n = 6;

    printf("Original integer array: ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", num_arr[i]);
    }
    printf("\n");

    bubble_sort_int_asc(num_arr, n);
    printf("Sorted integers (asc): ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", num_arr[i]);
    }
    printf("\n");

    bubble_sort_int_desc(num_arr, n);
    printf("Sorted integers (desc): ");
    for (int i = 0; i < n; i++)
    {
        printf("%d ", num_arr[i]);
    }
    printf("\n\n");

    // Sorting array of strings
    char *str_arr[] = {"banana", "apple", "cherry", "date"};
    int m = 4;

    printf("Original string array: ");
    for (int i = 0; i < m; i++)
    {
        printf("%s ", str_arr[i]);
    }
    printf("\n");

    bubble_sort_str_asc(str_arr, m);
    printf("Sorted strings (asc): ");
    for (int i = 0; i < m; i++)
    {
        printf("%s ", str_arr[i]);
    }
    printf("\n");

    bubble_sort_str_desc(str_arr, m);
    printf("Sorted strings (desc): ");
    for (int i = 0; i < m; i++)
    {
        printf("%s ", str_arr[i]);
    }
    printf("\n");

    return 0;
}
