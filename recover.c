#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    FILE *img;

    int counter = -1;

    if(f == NULL)
    {
        printf("Need a Readable File\n");
        return 1;
    }
    char x[8];
//Check that *f
    unsigned char buffer[512];
    while(fread(buffer, 1, 512, f) == 512)
    {

        if (buffer[0] == 0xff  && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            if(counter != -1)
            {
                fclose(img);
            }
            counter++;
            sprintf(x, "%03i.jpg", counter);
            img = fopen(x, "w+");
        }
        if (counter!=-1)
        {
            fwrite(buffer, 1, 512, img);
        }

    }
    fclose(img);
    fclose(f);
}


    //If Represents a JPEG File- write 000.jpg and write

        //        Create JPG with name ###.jpg starting from 000.jpg
        //how to get filename to be going up on JPEG



        //Write first file

        //fwrite(pointer to bytes written,512, number ,File *f= JPEG)

        //if second or third JPEG- close the


//         else if ((buffer[0] != 0xff || buffer[1] != oxd8 && buffer[2] != 0xff && (buffer[3]& 0xf0) != 0xe0)

//         {


//         }
//     }
//     }while fread ( ) >0
// }

//   fread(data, size, number, inptr-file you will read from)
//     //want to read from memory file

//     fread(buffer, 512 BYTE, number, FILE *f = fopen(argv[1], "r"))
// //repeat somr process until you reach the end of the card

//  typedef unsigned char BYTE;

//     fread(y, 1, 512, FILE *f = fopen(argv[1], "r"))