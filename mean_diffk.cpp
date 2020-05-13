#include <stdio.h>
#include <string.h>

#include <crpropa/Units.h>

using namespace crpropa;

//input file format: '#id\tL\tD_x\tD_y\tmu\tX\tY\tZ\tdl\n'
//output format: '#L\tD_x\tD_y\n'

struct Element {
    int count;
    double Dx_sum;
    double Dy_sum;

        Element():
            count(0),
            Dx_sum(0.),
            Dy_sum(0.)
            {}
    };

unsigned FindPos (unsigned steps, double max_len, double L);

int main (int argc, char** argv)
    {
    if (argc < 2)
        {
        printf ("No input file\n");
        return 0;
        }

    char fname[256] = "";
    strcat(strcpy (fname, argv[1]), "meandiff.txt");

    FILE* fin  = fopen (argv[1], "r");
    FILE* fout = fopen (fname, "w");

    if (fin == NULL)
        {
        printf ("Input file doesn't exist\n");
        return 0;
        }

    printf ("started\n");

    double max_len = 50 * pc;
    double step =  10 * au;

    if (argc >=3)
        {
        if (sscanf (argv[2], "%lg", &max_len) < 1)
            {
            printf ("Wrong 2 parameter (max_len) value. Using default\n ");
            max_len = 1;
            }

        max_len *= pc;
        }
    if (argc >= 4)
        {
        if (sscanf (argv[3], "%lg", &step) < 1)
            {
            printf ("Wrong 2 parameter (max_len) value. Using default\n ");
            step = 10;
            }

        step *= au;
        }

    unsigned steps = unsigned(max_len/step) + 1;

    printf ("\nmax_len = %lg pc\nstep = %lg au\nsteps = %u\n", max_len / pc, max_len/double(steps)/au, steps);

    fprintf (fout, "#L\tD_x\tD_y\n");

    double L = 0.0, Dx = 0.0, Dy = 0.0;

    char str_buf [1024] = "";

    fscanf(fin, "%[^\n]\n", str_buf);

    Element* array = new Element[steps];

    printf ("Starting cycle\n");

    while (!feof(fin))
        {
        fscanf(fin, "%[^\n]\n", str_buf);

        int scanned = sscanf(str_buf, "%*d\t%lg\t%lg\t%lg\t%*lg\t%*lg\t%*lg\t%*lg\t%*lg", &L, &Dx, &Dy);

        if (FindPos(steps, max_len, L) >= steps)
            {
            printf ("Bad value %u with %u, %lg, %lg\n", FindPos(steps, max_len, L),
                                                        steps, max_len / pc, L / pc);

            delete array;
            return 1;
            }

        array [FindPos(steps, max_len, L)].count++;
        array [FindPos(steps, max_len, L)].Dx_sum += Dx;
        array [FindPos(steps, max_len, L)].Dy_sum += Dy;
        }

    for (unsigned i = 0; i < steps; i++)
        {
        if (array[i].count == 0)
            continue;

        array[i].Dx_sum /= array[i].count;
        array[i].Dy_sum /= array[i].count;

        fprintf (fout, "%lg\t%lg\t%lg\n", double(i) * max_len / double(steps), array[i].Dx_sum
                                                                             , array[i].Dy_sum);
        }

    delete array;

    fclose (fin);
    fclose (fout);

    return 0;
    }

unsigned FindPos (unsigned steps, double max_len, double L)
    {
    return L / max_len * steps;
    }
