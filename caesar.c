#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>


//function will need to have a command line function
int main(int argc, string argv[])
{
    //make sure that there are two arguments
    if (argc != 2)
    {
        printf("Error, input one command line argument!\n");
        return 1;
    }
//make sure that second argument is a digit
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
        }

    }
//create a variable that changes the string in the second argument to an integer
    int k = atoi(argv[1]);

//get string from user
    string s = get_string("plaintext: ");
//where the resultant string will print
    printf("ciphertext: ");
    //for loop that will check if alpha
    //Within loop if upper case, woill take the letter and then add a value to it which
    //can be frind by doing k mod 26
    //Futhermore if it goes outside of the ASCII letter range bring it back to the original of 64 and then add the difference
    //do the same thing for the lowercase letters
    //if not letter then just keep the same thing there
    //finally print a new line and return 0 to end program
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isalpha(s[i]))
        {
            if (isupper(s[i]))
            {
                int c = s[i] + (k % 26);
                if (c > 90)
                {
                    c = c % 90 + 64;
                }
                printf("%c", c);
            }
            else if (islower(s[i]))
            {
                int c = s[i] + (k % 26);
                // printf("first %i\n", c);
                if (c > 122)
                {
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


