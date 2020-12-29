#include<stdio.h>
#include<cs50.h>

int add_digits(int number);

int main(void)
{
    // Asking user for credit input
    long int card_number = get_long("Number: ");
    int position = 1, sum1 = 0, sum2 = 0;
    int last_digit = 0;
    // sum1 is the sume of all product of 2 and sum2 is the sum of all numbers
    // not multiplied by 2
    while (card_number > 0)
    {
        if (position % 2 == 0)
        {
            if ((card_number % 10 * 2) > 9)
            {
                sum1 += add_digits(card_number % 10 * 2);
            }
            else
            {
                sum1 += card_number % 10 * 2;
            }
        }
        else
        {
            sum2 += card_number % 10;
        }
        position += 1;
        last_digit = card_number;
        card_number = card_number / 10;
    }

    if (position - 1 < 13 || position - 1 > 16)
    {
        printf("INVALID\n");
    }
    else if ((sum1 + sum2) % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        switch (last_digit)
        {
            case 5:
                printf("MASTERCARD\n");
                break;
            case 3:
                printf("AMEX\n");
                break;
            case 4:
                printf("VISA\n");
                break;
            default:
                printf("Unrecognized card type");
        }
    }
}

int add_digits(int number)
{
    int total = 0;
    while (number > 0)
    {
        total += number % 10;
        number = number / 10;
    }
    return total;
}