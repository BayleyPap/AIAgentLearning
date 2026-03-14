print('Enter a starting number: ',end='')
x = input()
x = int(x)
i = 0
while x != 1:
    i += 1
    print(f'{x}')
    if x % 2 != 0:
        x = x * 3 + 1
    else:
        x = x // 2
print('1')
print(f'Reached 1 in {i} steps.')