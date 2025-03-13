#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define NUM_MOVIES 5
#define MAX_TITLE_LENGTH 100

typedef struct
{
    char title[MAX_TITLE_LENGTH];
    int year;
} Movie;

int compareMovies(const void *a, const void *b)
{
    Movie *movieA = (Movie *)a;
    Movie *movieB = (Movie *)b;

    if (movieA->year != movieB->year)
    {
        return movieA->year - movieB->year;
    }
    return strcmp(movieA->title, movieB->title);
}

int main()
{
    // Movie movies[NUM_MOVIES];

    // for (int i = 0; i < NUM_MOVIES; i++)
    // {
    //     printf("Enter title of movie %d: ", i + 1);
    //     getchar();
    //     fgets(movies[i].title, MAX_TITLE_LENGTH, stdin);
    //     movies[i].title[strcspn(movies[i].title, "\n")] = 0;

    //     printf("Enter release year of movie %d: ", i + 1);
    //     scanf("%d", &movies[i].year);
    // }

    // qsort(movies, NUM_MOVIES, sizeof(Movie), compareMovies);

    // printf("\nSorted Movies:\n");
    // for (int i = 0; i < NUM_MOVIES; i++)
    // {
    //     printf("%s (%d)\n", movies[i].title, movies[i].year);
    // }

    // char DNA_SEQUENCE[100];
    // int gene_count = 0;
    // int i; // Declare loop variable outside the for loop

    // printf("DNA Sequence: ");
    // fgets(DNA_SEQUENCE, sizeof(DNA_SEQUENCE), stdin);
    // DNA_SEQUENCE[strcspn(DNA_SEQUENCE, "\n")] = 0;

    // for (i = 0; i < strlen(DNA_SEQUENCE); i++)
    // {
    //     if (DNA_SEQUENCE[i] >= 'A' && DNA_SEQUENCE[i] <= 'Z')
    //     {
    //         if (gene_count > 0)
    //         {
    //             printf("-");
    //         }
    //         gene_count++;
    //     }
    //     printf("%c", DNA_SEQUENCE[i]);
    // }

    char input[100], output[100];
    int specialChar = 0, k = 0;

    printf("Input: ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;

    printf("%d", strlen(input));

    for (int i = 0; i < strlen(input); i++)
    {
        if (isalnum(input[i]))
        {
            output[k++] = input[i];
        }
        else
        {
            specialChar++;
        }
    }
    output[k] = '\0';

    return 0;
}
