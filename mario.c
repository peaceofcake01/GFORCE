#include <cs50.h>
#include <stdio.h>

int get_positive_int(void);

int main(void)
{
   int n;
    do
    {
        n = get_positive_int();
    }
    while (n < 1 || n > 8);
       
    for (int rows = 1; rows <= n; rows++)
    {
        for (int dots = 0; dots < n-rows; dots++)
        {
            printf(" ");
        }
        for (int hashtag = 0; hashtag < rows; hashtag++)
        {
            printf("#");
        }
         printf("\n");
        }
       
    }
        


int get_positive_int(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1);
    return n;
   
}

    
