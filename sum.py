def sum_of_even_numbers(n):
    """
    Calculates the sum of all positive even numbers up to n (inclusive)
    using a while loop and also prints each odd number.
    """
    i = 1
    even_sum = 0
    even_numbers = []
    while i <= n:
        if i % 2 == 0:
            even_sum += i
            even_numbers.append(i)
        i += 1
    return even_sum, even_numbers

# Get input from the user
n = int(input("Enter a positive integer: "))

# Calculate the sum of odd numbers and get the list of odd numbers
total_sum, even_list = sum_of_even_numbers(n)

# Print the results
print("Even numbers:", even_list)
print("Sum of Even numbers:", total_sum)
#if _name_ == "_main_":