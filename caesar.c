#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>



    int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Error, input one command line argument!\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if(!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
        }




    }

   int k = atoi(argv[1]);



    string s = get_string("plaintext: ");
    printf("ciphertext:  ");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isalpha(s[i]))
        {
            if(isupper(s[i]))
            {
                char c = s[i] + (k % 26);
                if(c > 90){
                 c = c % 90 + 64;
                }
                printf("%c", c);
            }
             else
            {
                char c = (s[i] + (k % 26));
                if(c>122){
                     c = c % 122 + 96;
                }
                printf("%c", c);
            }
        }
        else
        {
            char c = s[i];
            printf("%c", c);
        }
    }

    printf("\n");
    return 0;
    }


