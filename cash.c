#include <cs50.h>
#include <stdio.h>
//set up function that will be used later
float get_change(void);

//Main Body
int main(void)
{
    //define float n
    float n;
    //initate the get change function and assign n to the received float
    do
    {
        n = get_change();
    }
    while (n < 0);
    //set up variables that will make future steps easier by multiplying the float and making it into an integer
    int newN = n * 100;
    //initialize total coins to 0
    int totalCoins = 0;
    //if the total is more than 25, add 1 to total coins due to the quarter that would take its spot, and subtract 25 from the newN
    while (newN >= 25)
    {
        totalCoins++;
        newN -= 25;
    }
     //if the total is more than 10, add 1 to total coins due to the dime that would take its spot, and subtract 10 from the newN
    while (newN>=10)
    {
        totalCoins = totalCoins+1;
        newN = newN-10;
    }
      //if the total is more than 5, add 1 to total coins due to the nickel that would take its spot, and subtract 5 from the newN
     while (newN>=5)
    {
        totalCoins = totalCoins+1;
        newN = newN-5;
    }
      //if the total is more than 1, add 1 to total coins due to the penny that would take its spot, and subtract 1 from the newN
     while (newN>=1)
    {
        totalCoins = totalCoins+1;
        newN = newN-1;
    }
    //print the integer of minimum total coins that can be found
    printf("%i\n", totalCoins);
    }

//create a function that prompts the user for a float until n is more than 0
float get_change(void)
{
    float n;
    do
    {
        n = get_float("Change Owed?");
        
    }
    while (n < 0);
    return n;
   
}
