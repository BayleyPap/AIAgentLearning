my_pets = ['Zophie', 'Pooka', 'Fat-tail']
print('Enter a pet name:')
name = input()
if name not in my_pets:
    print(f'I do not have a pet named {name}')
else:
    print(f'{name} is my pet.')