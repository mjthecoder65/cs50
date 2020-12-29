#include<stdio.h>
#include<math.h>
#include<cs50.h>

int main(void)
{
    int count = 0;
    int n = 0;
    // Asking user to enter changed owned in dollar
    float dollar = get_float("Change owed: ");

    // Ensuring the user enter a proper change value
    while (dollar < 0)
    {
        dollar = get_float("Change owned: ");
    }
    // Converting change(in dollar) to cents
    int cents = round(dollar * 100);

    // Finding the minimum number of coins to be returned as change
    while (cents > 0)
    {
        if (cents >= 25)
        {
            cents -= 25;
            count++;
        }
        else if (cents >= 10)
        {
            cents -= 10;
            count++;
        }
        else if (cents >= 5)
        {
            cents -= 5;
            count++;
        }
        else
        {
            cents -= 1;
            count++;
        }
    }
    // Printing the results which is minimum number of coins for change
    printf("%i\n", count);

}