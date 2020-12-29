from cs50 import get_float

# Promping user to enter change in dollar
dollar = get_float("Change owed: ")

# Reprompting user if enters a wrong input
while dollar < 0:
    dollar = get_float("Change owned: ")

# Converting dollar to cents
cents = int(dollar * 100)
count = 0

# Findin minimum number of coing to returned as change
while cents > 0:
    if cents >= 25:
        cents -= 25
        count += 1
    elif cents >= 10:
        cents -= 10
        count += 1
    elif cents >= 5:
        cents -= 5
        count += 1
    else:
        cents -= 1
        count += 1

# printing the results
print(count)
