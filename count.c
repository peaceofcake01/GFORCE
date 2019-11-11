#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>

typedef unsigned char BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./count INPUT\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Could not open file.\n");
        return 1;
    }
// initialize count at 0
    int count = 0;
    while (true)
    {
        BYTE b;
        // read through the file one byte at a time
        fread(&b, 1, 1, file);
        // if the character is represented by one byte then when you see that one byte raise count by 1
        if ((b >= 0x00) & (b <= 0x7F))
        {
            count++;
        }
        //if character is represented by two bytes then when you see the first unique byte that
        //represents a character, just raise count by 1 when you see that first byte
        else if ((b >= 0xC2) & (b <= 0xDF))
        {
            count++;
        }
        //if character is represented by three bytes then when you see the first unique byte that
        //represents a character, just raise count by 1 when you see that first byte
        else if ((b >= 0xE0) & (b <= 0xEF))
        {
            count++;
        }
        //if character is represented by four bytes then when you see the first unique byte that
        //represents a character, just raise count by 1 when you see that first byte
        else if ((b >= 0xF0) & (b <= 0xFF))
        {
            count++;
        }
        // We are not adding the range of bytes that are continuation blocks
        // Just by having the first element of each byte sequence we can count the total number of characters
        if (feof(file))
        {
            break;
        }

    }


    printf("Number of characters: %i\n", count);
}