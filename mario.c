#include <cs50.h>
#include <stdio.h>
//introduce function that will be called in the main
int get_positive_int(void);

int main(void)
//introduce n and prompt user for positive integer until the number is between 1 and 8
{
    int n;
    do
    {
        n = get_positive_int();
    }
    while (n < 1 || n > 8);
//first for loop that notes that based on the number of n place that many rows, everything inside of this loop should be done over and over again   
    for (int rows = 1; rows <= n; rows++)
    {
//on each row place spaces on the row based on n minus the row number, horizontal number of spaces
        for (int dots = 0; dots < n - rows; dots++)
        {
            printf(" ");
        }
        //for the remaining part of the row place hashtags, notice that as you start in row 1 you only have one hashtag, on row 7 you have 7 so you can keep adding hashtags based on the number of row you are on
        for (int hashtag = 0; hashtag < rows; hashtag++)
        {
            printf("#");
        }
        //move the line forward after competing each row
        printf("\n");
    }
       
}
        
//prompt user for a positive integer

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

    
