from cs50 import get_int

# A function to print mario piramid
# It takes height as a parameter and print the piramid


def print_mario_piramid(height):
    for x in range(1, height+1):
        print(" " * (height - x) + ("#" * x) + "  " + ("#" * x) + " " * (height - x))


# initializing height with any negative number or zero.
h = -1

while h <= 0 or h > 8:
    # Prompting user to enter piramid's height
    h = get_int("Height: ")

# printing the piramid if user enters a desired valued of height
# The piramid is printed by the print_mario_piramid() function

print_mario_piramid(h)