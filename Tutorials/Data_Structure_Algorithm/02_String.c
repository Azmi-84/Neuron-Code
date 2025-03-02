#include <stdio.h>
#include <string.h>

int main()
{
    // Read a string from user
    char str[100];
    printf("Enter a string: ");
    fgets(str, sizeof(str), stdin); // Read string from user. Difference between printf and fgets is that fgets reads the whole line, including spaces.
    printf("You entered: %s\n", str);

    // Print the string in reverse
    printf("Reverse of the string: ");
    // int len;
    // for (len = 0; str[len] != '\0'; len++)
    // {
    // }
    // int len = (int)(strchr(str, '\0') - str);
    int len = strlen(str);
    for (int i = len - 2; i >= 0; i--)
    {
        printf("%c", str[i]);
    }
    printf("\n");

    // // Separate the individual words from the string
    // printf("Individual words from the string: ");
    // int i = 0;
    // while (str[i] != '\0')
    // {
    //     printf("%c ", str[i]);
    //     i++;
    // }
    // printf("\n");

    // // Separate the individual words from the string and print them in reverse
    // printf("Individual words from the string in reverse: ");
    // i = len - 2;
    // while (i >= 0)
    // {
    //     printf("%c ", str[i]);
    //     i--;
    // }
    // printf("\n");

    // Compare two strings
    char str1[100], str2[100];
    printf("Enter first string: ");
    fgets(str1, sizeof(str1), stdin);
    printf("Enter second string: ");
    fgets(str2, sizeof(str2), stdin);

    // Remove trailing newlines manually
    int i;
    for (i = 0; str1[i] != '\n' && str1[i] != '\0'; i++);
    str1[i] = '\0';
    
    for (i = 0; str2[i] != '\n' && str2[i] != '\0'; i++);
    str2[i] = '\0';

    // Compare strings manually
    i = 0;
    int equal = 1;
    while (str1[i] != '\0' || str2[i] != '\0') {
        if (str1[i] != str2[i]) {
            equal = 0;
            break;
        }
        i++;
    }

    if (equal) {
        printf("Strings are equal\n");
    } else {
        printf("Strings are not equal\n");
    }

    return 0;
}