#include<stdio.h>
#include<cs50.h>

int main(void)
{
    // Asking user to enter name
    string name = get_string("What is your name?\n");
    
    // printing the result
    printf("hello, %s\n", name);

}