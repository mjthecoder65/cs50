#include<cs50.h>
#include<stdio.h>

int main(void)
{
    // Prompting a user to enter height of the mario piramid
    int h =  get_int("Height: ");

    // checking if the value entered ranges between 1 and 8
    if (h < 1 || h > 8)
    {
        while (true)
        {
            h = get_int("Height: ");
            if (h >= 1 && h <= 8)
            {
                break;
            }
        }
    }
    // Printing the mario piramid
    for (int i = 1; i <= h ; i++)
    {
        for (int j = 1; j <= h - i; j++)
        {
            printf(" ");
        }

        for (int m = 1; m <= i; m++)
        {
            printf("#");
        }
        printf("\n");
    }
    // end

}