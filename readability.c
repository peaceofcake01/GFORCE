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
      int letters = 0;

//Find l
for (int i = 0; i < strlen(s); i++)
{
    if (isalpha(s[i]))
    {
        letters++;
    }
}
//printf("Letters: %i\n", letters);


    int words = 0;
    bool flag = true;


//Find l
for (int i = 0; i < strlen(s); i++)
{

    if (isalpha(s[i]) && !flag)
    {
        flag = true;
        words++;
    }else if(!isalpha(s[i]))
    {
        flag = false;
    }


}
//printf("Words: %i\n", words);



    int sentences = 0;

for (int i = 0; i < strlen(s); i++)
{
    if (s[i]=='.' || s[i]=='?' || s[i] =='!')
    {
        sentences++;
    }

}

//printf("Sentences: %i\n", sentences);

float L = 100 * letters/words;
float S = 100 * sentences/words;



//Find initial grade level estimation
   float initialgrade = 0.0588 * L - 0.296 * S - 15.8;
// Round the grade level
   int finalgrade= (int) roundf(initialgrade)
;
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



