#include <stdio.h>
#include <stdlib.h> 

/**
 * This program demonstrates fundamental array operations and algorithms
 * commonly used in data analysis and scientific computing.
 *
 * Arrays are crucial data structures for representing:
 *  - Material composition data
 *  - Experimental measurements
 *  - Simulation results
 *  - Crystallographic information
 */

int main()
{
    // ===== BASIC ARRAY OPERATIONS =====

    // Initialize a fixed-size array to store 5 elements
    int arr[5];
    printf("Enter 5 elements: \n");
    for (int i = 0; i < 5; i++)
    {
        printf("Enter element %d: ", i + 1);
        scanf("%d", &arr[i]);
    }

    // Classify elements as even or odd
    // In materials science, this could represent categorizing materials by specific properties
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

    // Calculate sum of even numbers (useful for statistical analysis of data subsets)
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

    // Calculate sum of odd numbers
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

    // ===== STATISTICAL ANALYSIS =====

    // Find maximum value - O(n) time complexity
    // Useful for identifying peak values in experimental data
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

    // Find minimum value - O(n) time complexity
    // Important for identifying threshold values or base cases
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

    // Find second largest number - outlier identification in datasets
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

    // Find second smallest number
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

    // ===== ARRAY MANIPULATION TECHNIQUES =====

    /*
     * Note on array size manipulation in C:
     * Fixed arrays cannot be resized after declaration
     * Options:
     * 1. Create new array and copy elements
     * 2. Use dynamic memory allocation (malloc/realloc/free)
     * 3. Shift elements within existing bounds
     */

    printf("Insert an element at the beginning: ");

    // METHOD 1: Insert element at beginning (without dynamic allocation)
    // This shifts all elements right and places new element at index 0
    // Time complexity: O(n) for shifting n elements
    int newElement;
    printf("Enter the new element: ");
    scanf("%d", &newElement);
    for (int i = 4; i > 0; i--)
    {
        arr[i] = arr[i - 1]; // Shift each element one position right
    }
    arr[0] = newElement;
    printf("New array: ");
    for (int i = 0; i < 5; i++)
    {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // METHOD 2: Insert element at beginning using dynamic memory allocation
    // This creates a larger array to accommodate the new element
    // Allocate memory for 6 integers - sizeof(int) ensures correct size on different platforms
    int *newArr = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr[i + 1] = arr[i]; // Copy with offset of 1 position
    }

    printf("Enter the new element: ");
    scanf("%d", &newArr[0]);

    printf("New array: ");
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", newArr[i]);
    }
    printf("\n");

    free(newArr); // Release allocated memory to prevent memory leaks

    // Insert element at the end of array using dynamic memory allocation
    int *newArr2 = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr2[i] = arr[i]; // Copy original elements
    }

    printf("Enter the new element: ");
    scanf("%d", &newArr2[5]); // Add new element at the end

    printf("New array: ");
    for (int i = 0; i < 6; i++)
    {
        printf("%d ", newArr2[i]);
    }
    printf("\n");

    free(newArr2); // Free memory

    // Insert element at specific position
    // This is useful when adding new data points at precise locations in datasets
    int *newArr3 = (int *)malloc((6) * sizeof(int));
    for (int i = 0; i < 5; i++)
    {
        newArr3[i] = arr[i]; // Copy original array
    }

    int position;
    printf("Enter the position: ");
    scanf("%d", &position);

    // Validate user input to prevent buffer overflows or invalid memory access
    if (position < 0 || position > 5)
    {
        printf("Invalid position. Position should be between 0 and 5\n");
        free(newArr3);
        return 1;
    }

    // Shift elements to make space for new element
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

    // ===== DATA ANALYSIS ALGORITHMS =====

    // Frequency analysis: Count occurrences of each unique element
    // Important in materials science for analyzing distribution of properties/measurements
    // Time complexity: O(n²) - more efficient algorithms exist using hash maps
    printf("Frequency of each element: \n");
    for (int i = 0; i < 6; i++)
    {
        int count = 1; // Start with 1 (counting current element)
        int alreadyCounted = 0;

        // Check if this element was already counted in previous iterations
        for (int k = 0; k < i; k++)
        {
            if (newArr3[i] == newArr3[k])
            {
                alreadyCounted = 1;
                break; // Element already counted, no need to continue
            }
        }

        // Skip if already counted to avoid duplicate output
        if (alreadyCounted == 1)
        {
            continue;
        }

        // Count additional occurrences in the rest of the array
        for (int j = i + 1; j < 6; j++)
        {
            if (newArr3[i] == newArr3[j])
            {
                count++;
            }
        }
        printf("%d occurs %d times\n", newArr3[i], count);
    }

    // Find and print unique elements (elements with frequency = 1)
    // This algorithm identifies distinct values in your dataset
    printf("Unique elements: ");
    for (int i = 0; i < 6; i++)
    {
        int isUnique = 1;
        // Check if element appears elsewhere in array
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
            printf("%d ", newArr3[i]);
        }
    }
    printf("\n");

    // Separate even and odd elements into different arrays
    // This demonstrates data classification/categorization
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

    // ===== SEARCH ALGORITHMS =====

    // Linear search - O(n) time complexity
    // Used to find specific data points in datasets
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
            break; // Element found, exit loop early
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

    // ===== SORTING ALGORITHMS =====

    // Bubble sort implementation - O(n²) time complexity
    // Sorting is fundamental to data analysis and visualization
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
        // Bubble sort in ascending order
        for (int i = 0; i < 6; i++)
        {
            for (int j = i + 1; j < 6; j++)
            {
                if (newArr4[i] > newArr4[j])
                {
                    // Swap elements using temporary variable
                    int temp = newArr4[i];
                    newArr4[i] = newArr4[j];
                    newArr4[j] = temp;
                }
            }
        }
    }
    else if (choice == 2)
    {
        // Bubble sort in descending order
        for (int i = 0; i < 6; i++)
        {
            for (int j = i + 1; j < 6; j++)
            {
                if (newArr4[i] < newArr4[j])
                {
                    // Swap elements
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

    // ===== MATRIX OPERATIONS =====
    /*
     * Matrices are essential in materials science for:
     * - Stress-strain calculations
     * - Crystallographic transformations
     * - Finite element analysis
     * - Image processing in microstructure analysis
     */

    // Matrix addition - element-wise addition of corresponding elements
    // Time complexity: O(n×m) where n,m are dimensions
    int matrix1[2][2] = {{1, 2}, {3, 4}};
    int matrix2[2][2] = {{5, 6}, {7, 8}};
    int sumMatrix[2][2];

    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            sumMatrix[i][j] = matrix1[i][j] + matrix2[i][j];
        }
    }

    printf("Sum of two matrices: \n");
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            printf("%d ", sumMatrix[i][j]);
        }
        printf("\n");
    }

    // Scalar multiplication - multiply each element by scalar value
    // Used in scaling transformations and unit conversions
    int scalar = 2;
    int scalarMatrix[2][2];

    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            scalarMatrix[i][j] = scalar * matrix1[i][j];
        }
    }

    printf("Scalar multiplication of a matrix: \n");
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            printf("%d ", scalarMatrix[i][j]);
        }
        printf("\n");
    }

    // Matrix multiplication - follows mathematical rules for matrix product
    // Critical for coordinate transformations and solving systems of equations
    // Time complexity: O(n³) for naive implementation
    int matrix3[2][2] = {{1, 2}, {3, 4}};
    int matrix4[2][2] = {{5, 6}, {7, 8}};
    int productMatrix[2][2];

    for (int i = 0; i < 2; i++) // Iterating through the rows of the first matrix
    {
        for (int j = 0; j < 2; j++) // Iterating through the columns of the second matrix
        {
            productMatrix[i][j] = 0; // Initialize result cell to zero
            // Calculate dot product of row i from matrix1 and column j from matrix2
            for (int k = 0; k < 2; k++)
            {
                productMatrix[i][j] += matrix3[i][k] * matrix4[k][j];
            }
        }
    }

    printf("Product of two matrices: \n");
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            printf("%d ", productMatrix[i][j]);
        }
        printf("\n");
    }

    // Matrix equality comparison
    // Used to verify transformation results or compare experimental vs. theoretical data
    int matrix5[2][2] = {{1, 2}, {3, 4}};
    int matrix6[2][2] = {{1, 2}, {3, 4}};

    int equal = 1; // Assume equal until proven otherwise
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            if (matrix5[i][j] != matrix6[i][j])
            {
                equal = 0; // Set flag to false if any elements differ
                break;
            }
        }
    }

    if (equal == 1)
    {
        printf("Two matrices are equal\n");
    }
    else
    {
        printf("Two matrices are not equal\n");
    }

    // Calculate sum of main diagonal (trace)
    // The trace has special significance in linear transformations and eigenvalue problems
    int matrix7[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};

    int mainDiagonalSum = 0;

    for (int i = 0; i < 3; i++)
    {
        mainDiagonalSum += matrix7[i][i]; // Elements where row index equals column index
    }

    printf("Sum of the main diagonal matrix is: %d\n", mainDiagonalSum);

    // Calculate sum of minor diagonal
    // Important in analyzing symmetry properties and structural relationships
    int minorDiagonalSum = 0;

    for (int i = 0; i < 3; i++)
    {
        int j = 2 - i; // Column index for minor diagonal elements
        if (j >= 0 && j < 3)
        {
            minorDiagonalSum += matrix7[i][j];
        }
    }

    printf("The sum of the minor diagonal is: %d\n", minorDiagonalSum);

    // Calculate row and column sums
    // Useful for analyzing distributions and verifying conservation properties
    int n = 3; // Matrix dimension

    // Calculate and print row sums
    printf("\nRow sums:\n");
    for (int i = 0; i < n; i++)
    {
        int rowSum = 0;
        for (int j = 0; j < n; j++)
        {
            rowSum += matrix7[i][j];
        }
        printf("Row %d sum: %d\n", i + 1, rowSum);
    }

    // Calculate and print column sums
    printf("\nColumn sums:\n");
    for (int j = 0; j < n; j++)
    {
        int colSum = 0;
        for (int i = 0; i < n; i++)
        {
            colSum += matrix7[i][j];
        }
        printf("Column %d sum: %d\n", j + 1, colSum);
    }

    // Merging two array in a single sorted array

    int newArray5[] = {1, 23, 3, 25, 12};
    int newArray6[] = {34, 12, 10, 121, 1212};

    int size1 = sizeof(newArray5) / sizeof(newArray5[0]);
    int size2 = sizeof(newArray6) / sizeof(newArray6[0]);
    int mergeArraySize = size1 + size2;

    int *mergeArray = (int *)malloc((mergeArraySize) * sizeof(int));

    // Copy elements from first array
    for (int i = 0; i < size1; i++)
    {
        mergeArray[i] = newArray5[i];
    }

    for (int i = 0; i < size2; i++)
    {
        mergeArray[size1 + i] = newArray6[i];
    }

    // Sort the merged array
    for (int i = 0; i < mergeArraySize - 1; i++)
    {
        for (int j = 1; j < mergeArraySize; j++)
        {
            if (mergeArray[i] > mergeArray[j])
            {
                int temp = mergeArray[j];
                mergeArray[i] = mergeArray[j];
                mergeArray[j] = temp;
            }
        }
    }

    // Print the merged array
    printf("\nMerged and sorted array: ");
    for (int i = 0; i < mergeArraySize; i++)
    {
        printf("%d ", mergeArray[i]);
    }
    printf("\n");

    // Free allocated memory before exiting
    free(newArr3);
    free(evenArr);
    free(oddArr);
    free(newArr4);
    free(mergeArray);

    return 0;
}