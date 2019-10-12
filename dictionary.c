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
    //Start on first element of linked list
    //pointer to node

    node *cursor;
    int n = hash(word);
    cursor = table [n];
    //while statement that will compare the word of the dictionary to what cursor is pointing to
    while (cursor != NULL)
    {
        if (strcasecmp(cursor -> word, word) == 0)
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
    return tolower(word[0]) - 'a';
}

int counter = 0;
char buffer[LENGTH + 1];
int x = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{

    //Take new node and put it inside hash table
    node *list = NULL;
    FILE *DICT = fopen(dictionary, "r");
    while (fscanf(DICT, "%s", buffer) != EOF)
    {
        if (DICT == NULL)
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

    fclose(DICT);
    return true;
}

//first argument is pointer, want to read line by line ,fscanf(pointer, percent s, buffer)

// Returns number of words in dictionary if loaded else 0 if not yet loaded

unsigned int size(void)
{
    if (counter != 0)
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
    for (int n = 0; n < 26; n++)
    {
        pt = table[n];
        while (pt != NULL)
        {
            node *temp = pt;
            pt = pt -> next;
            free(temp);
        }

    }

    return true;
}

