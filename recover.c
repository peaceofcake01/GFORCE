#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //check that you are receiving two argument
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open file and define the image
    FILE *f = fopen(argv[1], "r");
    FILE *img;

    int counter = -1;
    //if receive an unopenable file then quit
    if (f == NULL)
    {
        printf("Need a Readable File\n");
        return 1;
    }
    //define name of the jpegs
    char x[8];
    //Check that *f
    unsigned char buffer[512];

    //create a forever loop that checks that buffer is 512 long
    while (fread(buffer, 1, 512, f) == 512)
    {
        //Buffer must start with this to get started
        if (buffer[0] == 0xff  && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if not the first one close the image and create a new file that can be written in
            if (counter != -1)
            {
                fclose(img);
            }
            counter++;
            sprintf(x, "%03i.jpg", counter);
            img = fopen(x, "w+");
        }
        //if it is not the first one then start writing it when you hit the first buffer
        if (counter != -1)
        {
            fwrite(buffer, 1, 512, img);
        }

    }
    fclose(img);
    fclose(f);
}


