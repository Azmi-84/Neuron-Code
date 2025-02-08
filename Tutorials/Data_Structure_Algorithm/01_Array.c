#include <stdio.h>

int main()
{
    int arr[5];
    printf("Enter 5 elements: \n");
    for (int i = 0; i < 5; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &arr[i]);
    }

    for (int i = 0; i < 5; i++)
    {
        if (arr[i] % 2 == 0)
        {
            printf("%d is even\n", arr[i]);
        }
        else
        {
            printf("%d is odd\n", arr[i]);
        }
    }

    printf("Sum of all even numbers: ");
    int evenSum = 0;
    for (int i = 0; i < 5; i++)
    {
        if (arr[i] % 2 == 0)
        {
            evenSum += arr[i];
        }
    }
    printf("%d\n", evenSum);

    printf("Sum of all odd numbers: ");
    int oddSum = 0;
    for (int i = 0; i < 5; i++)
    {
        if (arr[i] % 2 != 0)
        {
            oddSum += arr[i];
        }
    }
    printf("%d\n", oddSum);

    printf("Maximum number: ");
    int max = arr[0];
    for (int i = 1; i < 5; i++)
    {
        if (arr[i] > max)
        {
            max = arr[i];
        }
    }
    printf("%d\n", max);

    printf("Minimum number: ");
    int min = arr[0];
    for (int i = 1; i < 5; i++)
    {
        if (arr[i] < min)
        {
            min = arr[i];
        }
    }
    printf("%d\n", min);

    printf("Second largest number: ");
    int secondMax = arr[0];
    for (int i = 1; i < 5; i++)
    {
        if (arr[i] > secondMax && arr[i] < max)
        {
            secondMax = arr[i];
        }
    }
    printf("%d\n", secondMax);

    printf("Second smallest number: ");
    int secondMin = arr[0];
    for (int i = 1; i < 5; i++)
    {
        if (arr[i] < secondMin && arr[i] > min)
        {
            secondMin = arr[i];
        }
    }
    printf("%d\n", secondMin);

    printf("Insert an element at the beginning: "); // Insert an element at the beginning and few things we have to remember that in C we can't increase the size of an array when it declared. So, one way we can do is to create a new array and copy all the elements from the old array to the new array and then insert the new element at the beginning. Another way is to use dynamic memory allocation, where we have to involve malloc() and free() functions. These two functions are used to allocate and deallocate memory dynamically. We can also use realloc() function to increase the size of an array. But realloc() function is used to increase the size of an array, not to insert an element at the beginning. So, we can use realloc() function to increase the size of an array and then shift all the elements to the right and then insert the new element at the beginning.

    // The following code is to insert an element at the beginning of an array without using realloc() function.
    int newElement;
    printf("Enter the new element: ");
    scanf("%d", &newElement);
    for (int i = 4; i > 0; i--)
    {
        arr[i] = arr[i - 1];
    }
    arr[0] = newElement;
    printf("New array: ");
    for (int i = 0; i < 5; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // The following code is to insert an element at the beginning of an array using realloc() function. So,let's create a new array and copy all the elements from the old array to the new array and then insert the new element at the beginning.

    int *newArr = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr[i + 1] = arr[i];
    }

    printf("Enter the new element: ");
    scanf("%d", &newArr[0]);

    printf("New array: ");
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", newArr[i]);
    }
    printf("\n");

    free(newArr);

    //  The following code is to insert an element at the end of an array using realloc() function. So, let's create a new array and copy all the elements from the old array to the new array and then insert the new element at the end.

    int *newArr2 = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr2[i] = arr[i];
    }

    printf("Enter the new element: ");
    scanf("%d", &newArr2[5]);

    printf("New array: ");
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", newArr2[i]);
    }
    printf("\n");

    free(newArr2);

    // Insert an element at a specific position: Let's create a new array and copy all the elements from the old array to the new array and then insert the new element at a specific position.

    int *newArr3 = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr3[i] = arr[i];
    }

    int position;
    printf("Enter the position: ");
    scanf("%d", &position);

    if (position < 0 || position > 5)
    {
        printf("Invalid position. Position should be between 0 and 5\n");
        free(newArr3);
        return 1;
    }

    // Shift all the elements to the right starting from the position to insert the new element
    for (int i = 5; i > position; i--)
    {
        newArr3[i] = newArr3[i - 1];
    }

    printf("Enter the new element: ");
    scanf("%d", &newArr3[position]);

    printf("New array: ");
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", newArr3[i]);
    }
    printf("\n");

    // Counting frequency of each element in an array

    printf("Frequency of each element: \n");
    for (int i = 0; i < 6; i++)
    {
        int count = 1;
        int alreadyCounted = 0;
        for (int k = 0; k < i; k++)
        {
            if (newArr3[i] == newArr3[k])
            {
                alreadyCounted = 1;
                break;
            }
        }

        if (alreadyCounted == 1)
        {
            continue;
        }

        for (int j = i + 1; j < 6; j++)
        {
            if (newArr3[i] == newArr3[j])
            {
                count++;
            }
        }
        printf("%d occurs %d times\n", newArr3[i], count);
    }

    // https://codeforwin.org/c-programming/array-programming-exercises-and

    // Printing all unique elements in an array

    printf("Unique elements: ");
    for (int i = 0; i < 6; i++)
    {
        int isUnique = 1;
        for (int j = 0; j < i; j++)
        {
            if (newArr3[i] == newArr3[j])
            {
                isUnique = 0;
                break;
            }
        }
        if (isUnique == 1)
        {
            printf("Unique elements: %d ", newArr3[i]);
        }
    }
    printf("\n");

    //  Putting even and odd elements of array in two separate array.

    printf("Putting even and odd elements of array in two separate array.\n");
    int *evenArr = (int *)malloc(6 * sizeof(int));
    int *oddArr = (int *)malloc(6 * sizeof(int));

    int evenIndex = 0;
    int oddIndex = 0;
    for (int i = 0; i < 6; i++)
    {
        if (newArr3[i] % 2 == 0)
        {
            evenArr[evenIndex] = newArr3[i];
            evenIndex++;
        }
        else
        {
            oddArr[oddIndex] = newArr3[i];
            oddIndex++;
        }
    }

    printf("Even array: ");
    for (int i = 0; i < evenIndex; i++)
    {
        printf("%d ", evenArr[i]);
    }

    printf("\n");

    printf("Odd array: ");
    for (int i = 0; i < oddIndex; i++)
    {
        printf("%d ", oddArr[i]);
    }

    printf("\n");

    // Searching an element in an array.

    printf("Searching an element in an array.\n");
    int searchElement;
    printf("Enter the element to search: ");
    scanf("%d", &searchElement);

    int found = 0;
    for (int i = 0; i < 6; i++)
    {
        if (newArr3[i] == searchElement)
        {
            found = 1;
            break;
        }
    }

    if (found == 1)
    {
        printf("%d is found in the array\n", searchElement);
    }
    else
    {
        printf("%d is not found in the array\n", searchElement);
    }

    // Sorting array elements in ascending or descending order.

    printf("Sorting array elements in ascending or descending order.\n");
    int *newArr4 = (int *)malloc(6 * sizeof(int));
    for (int i = 0; i < 6; i++)
    {
        newArr4[i] = newArr3[i];
    }

    int choice;
    printf("Enter 1 to sort in ascending order and 2 to sort in descending order: ");
    scanf("%d", &choice);

    if (choice == 1)
    {
        for (int i = 0; i < 6; i++)
        {
            for (int j = i + 1; j < 6; j++)
            {
                if (newArr4[i] > newArr4[j])
                {
                    int temp = newArr4[i];
                    newArr4[i] = newArr4[j];
                    newArr4[j] = temp;
                }
            }
        }
    }
    else if (choice == 2)
    {
        for (int i = 0; i < 6; i++)
        {
            for (int j = i + 1; j < 6; j++)
            {
                if (newArr4[i] < newArr4[j])
                {
                    int temp = newArr4[i];
                    newArr4[i] = newArr4[j];
                    newArr4[j] = temp;
                }
            }
        }
    }
    else
    {
        printf("Invalid choice\n");
        free(newArr4);
        return 1;
    }

    return 0;
}