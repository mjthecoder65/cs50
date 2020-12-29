#include<stdio.h>
#include<cs50.h>
#include<ctype.h>
#include<stdlib.h>
#include<string.h>

bool isDigitsOnly(string str);
// A function to find out if the a string
// is composed of only digits

int main(int args, char **argv)
{
    string plaintext = "";
    // Look up string array container for uppercase letters
    string uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    // Look up string array container for lower case letters
    string lowercase_letters = "abcdefghijklmnopqrstuvwxyz";
    int key = 0, cipherCode = 0;
    char ch;
    // Handling the case when the number of argument is 1 or greater than 2
    if (args  == 2)
    {
        if (!isDigitsOnly(argv[1]))
        {
            printf("Usage: %s key\n", argv[0]);
            return 1;
        }
        // Prompting user to enter a plaintext
        plaintext = get_string("plaintext: ");
        key = atoi(argv[1]);
        for (int index = 0; plaintext[index] != '\0'; index++)
        {
            ch = plaintext[index];
            if (ch >= 'a' && ch <= 'z')
            {
                cipherCode = (ch - 97 + key) % 26;
                plaintext[index] = lowercase_letters[cipherCode];
            }
            else if (ch >= 'A' && ch <= 'Z')
            {
                cipherCode = (ch - 65 + key) % 26;
                plaintext[index] = uppercase_letters[cipherCode];

            }

        }
        // printing out the ciphertext
        printf("ciphertext: %s\n", plaintext);

    }
    else
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

}

// Definining the function isDigitsOnly()
bool isDigitsOnly(string str)
{
    int i = 0;
    while (str[i] != '\0')
    {
        if (!isdigit(str[i]))
        {
            return false;
        }
        i++;
    }
    return true;
}