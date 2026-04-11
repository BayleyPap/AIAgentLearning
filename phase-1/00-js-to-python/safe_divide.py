n = input("Enter numerator: ")
d = input("Enter denominator: ")
try:
    print(f"Result: {int(n) / int(d)}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero.")
except ValueError:
    print("Error: Please enter valid numbers.")
