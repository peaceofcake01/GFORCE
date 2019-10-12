// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdlib.h>



// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table (26 buckets)
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
//******* Check this number need it to be total going thfrough dictionary

bool check(const char *word)
{
    //Start on first element of linked list?
    //pointer to node

    node *cursor;
    int n = hash(word);
    cursor = table [n];
        while(cursor != NULL)
        {

            if(strcasecmp(cursor -> word, word) == 0)
            {
                return true;
            }

        cursor = cursor -> next;

        }
    return false;

}

//hash word to obtain hash value
//

// Hashes word to a number
//Just want to convert string into number
unsigned int hash(const char *word)
{
    return tolower(word[0])-'a';
}

int counter = 0;
char buffer[LENGTH + 1];
int x=0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    //Take new node and put it inside hash table
     node *list = NULL;
     FILE *f = fopen(dictionary, "r");
     while (fscanf(f, "%s", buffer) != EOF)
     {
        if (f == NULL)
        {
            printf("Need a Readable File\n");
            return false;
        }



    //Hash the word - give it hash key-  0,1 , 2,
    //table

        x = hash(buffer);

        list = table[x];

        node *n = malloc(sizeof(node));
        strcpy(n->word, buffer);
        n->next = NULL;

    //add new node to head
        n->next = list;
        table[x] = n;

        counter++;


        }
        return true;
}

    //first argument is pointer, want to read line by line ,fscanf(pointer, percent s, buffer)


    //Linked lists- every node has value and pointer to next node


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(counter!=0)
    {
        return counter;
    }
    else
    {
        return 0;
    }

}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node *pt;
    for(int n=0; n<26; n++)
    {
       pt= table[n];
       while(pt != NULL)
       {
        node *temp = pt;
        pt = pt ->next;
        free (temp);
       }

    }

    return true;
}


// linked list is a string dangling off a  cliff

// Only pointer if you free any of the top then you lose it

// How to free a linked list- can have pointer



// Can go recursively

// //Free
    // node *ptr = list;
    // while (ptr != NULL)
    //     {
    //         node *tmp = ptr;
    //         ptr = ptr->next;
    //         free(tmp);


// when test small.txt small.txt



//or can use
    // node *n=malloc
    // fsan(ptr,"%s", n -> word)
    //Take buffer


// TODO

    //dictionary- words on each line

    //Function is taking in a string
    //use


    //Store in Hashtable
    //Hashtable is an array of linked list
    //Hash function assigns number to every input
    //Create different Buckets

    //A bucket for all words with letter A
    //B bucket for all with b

    //Hash function takes a words as an input
    //Outputs number corresponding to bucket it was put in

    // //  node *n = malloc(sizeof(node));
    // n->word = 25;
    // n->next = NULL

   // strcpy(n->word, buffer)