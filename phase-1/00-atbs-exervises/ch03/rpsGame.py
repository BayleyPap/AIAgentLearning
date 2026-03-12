import random, sys

print('ROCK, PAPER, SCISSORS')

wins = 0
losses = 0
ties = 0 

while True:
    print('%s Wins, %s Losses, %s Ties' % (wins,losses,ties))
    while True:
        print('Enter your move: (r)ock (p)aper (s)cissors or (q)uit')
        player_move = input('>')
        if player_move == 'q':
            sys.exit()
        if player_move == 'r' or player_move == 'p' or player_move =='s':
            break
        print('Type one of r,p,s or q.')

    if player_move == 'r':
        print('ROCK versus...')
    elif player_move == 'p':
        print('PAPER versus...')
    elif player_move == 's':
        print('SCISSORS versus...')

    move_number = random.randint(1,3)
    if move_number == 1:
        computer_move = 'r'
        print('ROCK')
    elif move_number == 2:
        computer_move = 'p'
        print('PAPER')
    elif move_number == 3:
        computer_move = 's'
        print('SCISSORS')

    if player_move == computer_move:
        print('It is a tie!')
        ties = ties + 1
    elif player_move == 'r' and computer_move == 's':
        print('you win!')
        wins = wins + 1
    elif player_move == 's' and computer_move == 'r':
        print('you win!')
        wins = wins + 1
    elif player_move == 's' and computer_move == 'p':
        print('you win!')
        wins = wins + 1
    elif player_move == 'r' and computer_move == 'p':
        print('you lose!')
        losses = losses + 1
    elif player_move == 'p' and computer_move == 's':
        print('you lose!')
        losses = losses + 1
    elif player_move == 's' and computer_move == 'r':
        print('you lose!')
        losses = losses + 1