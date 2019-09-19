#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int main (void){
    // prompt user for string
      string s = get_string("Text:  ");
      // create variable
      float letters = 0;

//Find l
for (int i = 0; i < strlen(s); i++)
{
    if (isalpha(s[i]))
    {
        letters++;
    }
}
printf("Letters: %f\n", letters);


    float words = 0;
    bool flag = false;


//Find l
for (int i = 0; i < strlen(s); i++)
{

    if (isalpha(s[i]) && !flag)
    {
        flag = true;
        words++;
    }else if(s[i]==' ')
    {
        flag = false;
    }


}
printf("Words: %f\n", words);



    float sentences = 0;

for (int i = 0; i < strlen(s); i++)
{
    if (s[i]=='.' || s[i]=='?' || s[i] =='!')
    {
        sentences++;
    }

}

printf("Sentences: %f\n", sentences);

float L = 100.0 * letters/words;
float S = 100.0 * sentences/words;

printf("L: %f\n", L);
printf("S: %f\n", S);


//Find initial grade level estimation
   float initialgrade = 0.0588 * L - 0.296 * S - 15.8;
// Round the grade level
printf("initialgrade: %f\n", initialgrade);

int finalgrade= round(initialgrade);

printf("finalgrade: %i\n", finalgrade);
//If else statement saying that if grade ends up being larger than 16 then print grade 16+, if grade is less than 1 print before grade 1

    if (finalgrade>16)
    {
    printf("Grade 16+\n");
    }

    else if (finalgrade<1)
    {
        printf("Before Grade 1...\n");
    }
    else
    {
        printf("Grade %i\n", finalgrade);
    }

}



