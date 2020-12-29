from cs50 import get_string

# A function to calculate Colemna-Liau index


def readability(text):
    sentences = 0
    words = 1
    letters = 0

    for i in range(len(text)):
        if text[i] == '!' or text[i] == '.' or text[i] == "?":
            sentences += 1
        if text[i] == ' ' and text[i+1]:
            words += 1
        if text[i].isalpha():
            letters += 1
    L = (letters * 100) / words
    S = (sentences * 100) / words

    index = (0.0588 * L) - (0.296 * S) - 15.8
    return round(index)


# Asking user to enter a piece of text
input_text = get_string("Text: ")
grade = readability(input_text)

# Checking for grade level that can understand the piece of text
if grade >= 16:
    print('Grade 16+')
elif grade < 1:
    print('Before Grade 1')
else:
    print(f'Grade {grade}')