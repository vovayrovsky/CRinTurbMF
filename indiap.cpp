#include "stdio.h"
#include "string.h"
//file format: '#id\tL\tD_x\tD_y\tmu\tX\tY\tZ\tdl\n'

const double pc = 3.086e+16; //m

int main(int argc, char** argv)
    {
    if (argc < 2)
        {
        printf ("No input file\n");
        return 0;
        }

    char fname[256] = "";
    strcat(strcpy (fname, argv[1]), "indiap.txt");

    FILE* fin  = fopen (argv[1], "r");
    FILE* fout = fopen (fname, "w");

    if (fin == NULL)
        {
        printf ("Input file doesn't exist\n");
        return 0;
        }

    printf ("start\n");

    char str_buf[1024] = "";

    fscanf  (fin, "%[^\n]\n", str_buf);
    fprintf (fout, "%s\n", str_buf);

    double diap = 3. * pc;
    double delta = 0.0001 * pc;
    double L = 0.;

    while (!feof(fin))
        {
        fscanf(fin, "%[^\n]\n", str_buf);

        int scanned = sscanf(str_buf, "%*d\t%lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg", &L);

        if (diap - delta < L && L < diap + delta)
            {
            fprintf (fout, "%s\n", str_buf);
            }
        }

    fclose (fin);
    fclose (fout);

    return 0;
    }
