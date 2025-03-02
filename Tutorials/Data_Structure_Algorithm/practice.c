#include <stdio.h>

// There is have two methods for passing an array in a function.
// 1. Call by value
// 2. Call by reference

void getStudentID(int arr[9])
{
    // int len = sizeof(arr) / sizeof(arr[0]);

    // if (len != 9)
    // {
    //     printf("Invalid ID");
    // }

    return;
}

int main()
{
    int math = 0, phy = 0, chem = 0;

    // printf("Marks of Math: ");
    // scanf("%d", &math);
    // printf("Marks of Physics: ");
    // scanf("%d", &phy);
    // printf("Marks of Chemistry: ");
    // scanf("%d", &chem);

    if (math >= 65 && phy >= 55 && chem >= 50 && (math + phy + chem) >= 190 && (math + phy) >= 140)
    {
        // printf("Eligible\n");
    }
    else
    {
        // printf("Not eligible\n");
    }

    int arr[9];
    printf("Enter 10 Student IDs (space-separated): ");
    for (int i = 0; i < 8; i++)
    {
        scanf("%d", &arr[i]);
    }

    int len = sizeof(arr) / sizeof(arr[0]);

    if (len != 9)
    {
        printf("Invalid ID");
    }

    getStudentID(arr);
}