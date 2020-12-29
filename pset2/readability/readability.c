#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include<ctype.h>
#include<math.h>

float readability(string text);

int main(void)
{
    string text = get_string("Text: ");
    float grade = readability(text);
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int)round(grade));
    }
}

float readability(string text)
{
    int sentences = 0, words = 1, letters = 0;
    int n = strlen(text);
    float L = 0, S = 0, index = 0;

    for (int i = 0; i < n ; i++)
    {
        // Counting the number of sentenses
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
        // Counting the number of words
        if (text[i] == ' ')
        {
            words++;
        }
        // Checking if the character is alphabet
        if (isalpha(text[i]))
        {
            letters++;
        }

    }
    // computing for L
    L = (letters * 100) / (float) words;
    // computing for S
    S = (sentences * 100)  / (float) words;

    // Computing for Index
    index = (0.0588 * L) - (0.296 * S) - 15.8;

    return index;

}