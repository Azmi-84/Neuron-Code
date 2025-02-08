#include <stdio.h>
#include <stdlib.h>

// Function prototypes
void inputArray(int arr[], int size);
void printEvenOdd(int arr[], int size);
int sumEven(int arr[], int size);
int sumOdd(int arr[], int size);
int findMax(int arr[], int size);
int findMin(int arr[], int size);
int findSecondMax(int arr[], int size, int max);
int findSecondMin(int arr[], int size, int min);
void insertAtBeginning(int arr[], int size, int newElement);
void insertAtBeginningDynamic(int arr[], int size);
void insertAtEnd(int arr[], int size);
void insertAtPosition(int arr[], int size);
void countFrequency(int arr[], int size);
void printUniqueElements(int arr[], int size);
void separateEvenOdd(int arr[], int size);
void searchElement(int arr[], int size);
void sortArray(int arr[], int size);

int main()
{
    int arr[5];
    printf("Enter 5 elements: \n");
    inputArray(arr, 5);

    printEvenOdd(arr, 5);
    printf("Sum of all even numbers: %d\n", sumEven(arr, 5));
    printf("Sum of all odd numbers: %d\n", sumOdd(arr, 5));
    int max = findMax(arr, 5);
    printf("Maximum number: %d\n", max);
    int min = findMin(arr, 5);
    printf("Minimum number: %d\n", min);
    printf("Second largest number: %d\n", findSecondMax(arr, 5, max));
    printf("Second smallest number: %d\n", findSecondMin(arr, 5, min));

    insertAtBeginning(arr, 5, 10);
    insertAtBeginningDynamic(arr, 5);
    insertAtEnd(arr, 5);
    insertAtPosition(arr, 5);
    countFrequency(arr, 6);
    printUniqueElements(arr, 6);
    separateEvenOdd(arr, 6);
    searchElement(arr, 6);
    sortArray(arr, 6);

    return 0;
}

// Function to take input for an array
void inputArray(int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &arr[i]);
    }
}

// Function to print whether numbers are even or odd
void printEvenOdd(int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        if (arr[i] % 2 == 0)
            printf("%d is even\n", arr[i]);
        else
            printf("%d is odd\n", arr[i]);
    }
}

// Function to calculate sum of even numbers
int sumEven(int arr[], int size)
{
    int evenSum = 0;
    for (int i = 0; i < size; i++)
    {
        if (arr[i] % 2 == 0)
            evenSum += arr[i];
    }
    return evenSum;
}

// Function to calculate sum of odd numbers
int sumOdd(int arr[], int size)
{
    int oddSum = 0;
    for (int i = 0; i < size; i++)
    {
        if (arr[i] % 2 != 0)
            oddSum += arr[i];
    }
    return oddSum;
}

// Function to find the maximum element in the array
int findMax(int arr[], int size)
{
    int max = arr[0];
    for (int i = 1; i < size; i++)
    {
        if (arr[i] > max)
            max = arr[i];
    }
    return max;
}

// Function to find the minimum element in the array
int findMin(int arr[], int size)
{
    int min = arr[0];
    for (int i = 1; i < size; i++)
    {
        if (arr[i] < min)
            min = arr[i];
    }
    return min;
}

// Function to find the second largest element in the array
int findSecondMax(int arr[], int size, int max)
{
    int secondMax = arr[0];
    for (int i = 1; i < size; i++)
    {
        if (arr[i] > secondMax && arr[i] < max)
            secondMax = arr[i];
    }
    return secondMax;
}

// Function to find the second smallest element in the array
int findSecondMin(int arr[], int size, int min)
{
    int secondMin = arr[0];
    for (int i = 1; i < size; i++)
    {
        if (arr[i] < secondMin && arr[i] > min)
            secondMin = arr[i];
    }
    return secondMin;
}

// Function to insert an element at the beginning of an array
void insertAtBeginning(int arr[], int size, int newElement)
{
    for (int i = size - 1; i > 0; i--)
    {
        arr[i] = arr[i - 1];
    }
    arr[0] = newElement;
    printf("New array after insertion: ");
    for (int i = 0; i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Function to search for an element in an array
void searchElement(int arr[], int size)
{
    int searchElement;
    printf("Enter the element to search: ");
    scanf("%d", &searchElement);
    int found = 0;
    for (int i = 0; i < size; i++)
    {
        if (arr[i] == searchElement)
        {
            found = 1;
            break;
        }
    }
    if (found == 1)
        printf("%d is found in the array\n", searchElement);
    else
        printf("%d is not found in the array\n", searchElement);
}

// Function to sort array elements in ascending order
void sortArray(int arr[], int size)
{
    for (int i = 0; i < size - 1; i++)
    {
        for (int j = i + 1; j < size; j++)
        {
            if (arr[i] > arr[j])
            {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
    printf("Sorted array: ");
    for (int i = 0; i < size; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");
}
