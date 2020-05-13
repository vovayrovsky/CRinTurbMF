#include <stdio.h>

struct Pair {
    int count;
    double sum;
    };

int main()
    {
if (argc < 2)
        {
        printf ("No input file\n");
        return 0;
        }

    char fname[256] = "";
    strcat(strcpy (fname, argv[1]), "diff.txt");

    FILE* fin  = fopen (argv[1], "r");
    FILE* fout = fopen (fname, "w");

    if (fin == NULL)
        {
        printf ("Input file doesn't exist\n");
        return 0;
        }

    printf ("started\n");

    return 0;
    }
