#include "stdio.h"
#include "string.h"
//file format: '#id\tL\tD_x\tD_y\tmu\tX\tY\tZ\tdl\n'

int main(int argc, char** argv)
    {
    if (argc < 2)
        {
        printf ("No input file\n");
        return 0;
        }

    char fname[256] = "";
    strcat(strcpy (fname, argv[1]), "last.txt");

    FILE* fin  = fopen (argv[1], "r");
    FILE* fout = fopen (fname, "w");

    if (fin == NULL)
        {
        printf ("Input file doesn't exists\n");
        return 0;
        }

    char str_buf [2][1024] = {"", ""};
    int count = 0;

    double prevL = 0;
    double L = 0;

    printf ("start\n");

    fscanf  (fin, "%[^\n]\n", str_buf[0]);
    fprintf (fout, "%s\n", str_buf[0]);

    //printf ("buf[0]: %s\n"
    //        "buf[1]: %s\n\n",
    //        str_buf[0], str_buf[1]);

    fscanf  (fin, "%[^\n]\n", str_buf[1]);
    sscanf(str_buf[1], "%*d\t%lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg", &prevL);

    int particles = 0;
    int lines = 0;
    while (!feof(fin))
        {
        count = (count + 1) % 2;

        fscanf(fin, "%[^\n]\n", str_buf[count]);

        int scanned = sscanf(str_buf[count], "%*d\t%lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg", &L);

        //printf ("scanned: %d\tlines: %d\r", scanned, lines);

        if (L < prevL)
            {
            particles++;
            printf ("New particle! L: %lg Now: %d\n", prevL, particles);
            fprintf (fout, "%s\n", str_buf[(count + 1)%2]);
            }

        prevL = L;
        lines++;
        }

    particles++;
    printf ("New particle! L: %lg Now: %d\n", prevL, particles);
    fprintf (fout, "%s\n", str_buf[(count + 1)%2]);

    fclose (fin);
    fclose (fout);

    return 0;
    }
