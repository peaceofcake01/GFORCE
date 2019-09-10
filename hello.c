#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Receive a string which should be a person's name
    string answer = get_string("What is your name?\n");
    //Print hello and the string received previously
    printf("hello, %s\n", answer);
}
