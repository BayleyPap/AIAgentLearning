import random

def get_answer(answer_number):
    match answer_number:
        case 1:
            return 'It is certain'
        case 2:
            return 'It is decidedly so'
        case 3:
            return 'Yes'
        case 4:
            return 'Reply hazy try again'
        case 5:
            return 'Ask again later'
        case 6:
            return 'Concentrate and ask again'
        case 7:
            return 'My reply is no'
        case 8:
            return 'Outlook not so good'
        case 9:
            return 'Very doubtful'

print('Ask a yes or no question:')
input('>')
r = random.randint(1,9)
fortune = get_answer(r)
print(fortune)