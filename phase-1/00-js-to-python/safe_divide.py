print('Enter numerator: ')
n=input()
print('Enter denominator: ')
d=input()
try:
    print(f'Result: {int(n)/int(d)}')
except ZeroDivisionError:
    print(f'Error: Cannot divide by zero.')
except ValueError:
    print(f'Error: Please enter valid numbers.')