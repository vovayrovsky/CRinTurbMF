#include "stdio.h"
#include "string.h"

//input file format: '#id\tL\tD_x\tD_y\tmu\tX\tY\tZ\tdl\n'
//output format: '#L\tD_x\tD_y\n'

const double light_v = 299792458; //m/s
const double pc = 3.086e+16; //m

int main(int argc, char** argv)
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
        printf ("Input file doesn't exists\n");
        return 0;
        }
    printf ("started\n");

    fprintf (fout, "#L\tD_x\tD_y\n");

    double L = 0.0, x = 0.0, y = 0.0, z = 0.0;

    char str_buf [1024] = "";

    fscanf(fin, "%[^\n]\n", str_buf);

    while (!feof(fin))
        {
        fscanf(fin, "%[^\n]\n", str_buf);

        int scanned = sscanf(str_buf, "%*d\t%lg\t%*lg\t%*lg\t%*lg\t%lg\t%lg\t%lg\t%*lg", &L, &x, &y, &z);

        if (L == 0.)
            continue;

        double diff_x = x*x * pc * pc/(2. * L / light_v);
        double diff_y = y*y * pc * pc/(2. * L / light_v);

        fprintf (fout, "%lg\t%lg\t%lg\n", L, diff_x, diff_y);
        }

    fclose (fin);
    fclose (fout);

    return 0;
    }
