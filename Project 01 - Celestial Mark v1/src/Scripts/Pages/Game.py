from Utilities.Constants import *
import time

# __________________GAMEPLAY IMPLEMENTATION__________________
# Player Structure---------------------------------------
player_one = {}
player_two = {}

current_player = player_one


def switch_player():
    global current_player
    if current_player['identity'] == 'P1':
        current_player = player_two
    elif current_player['identity'] == 'P2':
        current_player = player_one


def add_score(player):
    player['score'] += 1


# Board Structure---------------------------------------
def create_cell(position):
    return {'position': position,
            'state': '-',
            'display str': '[{}]'.format(position)}


def create_board():
    _board = {'cell list': {}, 'P1 cells': [], 'P2 cells': []}
    for i in range(1, 10):
        _cell = create_cell(i)
        _board['cell list'][i] = create_cell(i)
    return _board


board = create_board()


def print_board():
    clear_screen()
    global board
    cell_list = board['cell list']
    display_board = pd_game_board_ui.format(cell_list[1]['display str'], cell_list[2]['display str'],
                                            cell_list[3]['display str'], cell_list[4]['display str'],
                                            cell_list[5]['display str'], cell_list[6]['display str'],
                                            cell_list[7]['display str'], cell_list[8]['display str'],
                                            cell_list[9]['display str'])

    left_spaces = ' ' * int((44 - len(player_one['name'] + player_two['name'])) // 2)
    right_spaces = ' ' * ((44 - len(player_one['name'] + player_two['name'])) - len(left_spaces))
    names = [player_one['name'].upper(), player_two['name'].upper()]
    symbols = [player_one['symbol'], player_two['symbol']]
    scores = [str(player_one['score']).zfill(3), str(player_two['score']).zfill(3)]

    score_line = '|     {} [{}] : {}{}vs{}{} [{}] : {}     |'.format(names[0], symbols[0], scores[0],
                                                                     left_spaces, right_spaces,
                                                                     names[1], symbols[1], scores[1])

    print(display_board)
    print(score_line)
    print(bold_sep_line)


def mark_cell(cell_pos, player, game_board):
    if game_board['cell list'][cell_pos]['state'] != '-':
        pass
    else:
        game_board['cell list'][cell_pos]['state'] = player['identity']
        game_board['cell list'][cell_pos]['display str'] = ' {} '.format(player['symbol'])

        if player['identity'] == player_one['identity']:
            game_board['P1 cells'].append(cell_pos)
        elif player['identity'] == player_two['identity']:
            game_board['P2 cells'].append(cell_pos)


def undo_mark_cell(cell_pos, game_board):
    if game_board['cell list'][cell_pos]['state'] == '-':
        pass
    else:
        game_board['cell list'][cell_pos]['state'] = '-'
        game_board['cell list'][cell_pos]['display str'] = '[{}]'.format(cell_pos)

    if cell_pos in game_board['P1 cells']:
        game_board['P1 cells'].remove(cell_pos)
    elif cell_pos in game_board['P2 cells']:
        game_board['P2 cells'].remove(cell_pos)

    return game_board


def reset_board():
    global board
    board = create_board()


# AI Implementation---------------------------------------
def evaluate(_board):
    winner = None
    for win_combo in WIN_COMBINATIONS:
        if win_combo[0] in _board['P1 cells'] and win_combo[1] in _board['P1 cells'] \
                and win_combo[2] in _board['P1 cells']:
            winner = 'P1'
    for win_combo in WIN_COMBINATIONS:
        if win_combo[0] in _board['P2 cells'] and win_combo[1] in _board['P2 cells'] \
                and win_combo[2] in _board['P2 cells']:
            winner = 'P2'
    
    is_tie = True
    for cell in _board['cell list'].values():
        if cell['state'] != '-':
            is_tie = False
            
    if winner is not None:
        if winner == 'P1':
            return -10
        elif winner == 'P2':
            return +10
    elif is_tie:
        return 0
    else:
        return None
    

def get_best_move(_board):
    best_score = small_num
    best_move = None
    for cell in _board['cell list'].values():
        if cell['state'] == '-':
            mark_cell(cell['position'], player_two, _board)
            score = minimax_algorithm(_board, 0, False)
            _board = undo_mark_cell(cell['position'], _board)
            if score > best_score:
                best_score = score
                best_move = cell['position']
    return best_move


def minimax_algorithm(_board, depth, is_maximizing):
    if evaluate(_board) is not None:
        return evaluate(_board)

    if is_maximizing:
        best_score = small_num
        for cell in _board['cell list'].values():
            if cell['state'] == '-':
                mark_cell(cell['position'], player_two,_board)
                score = minimax_algorithm(_board, depth + 1, False)
                _board = undo_mark_cell(cell['position'], _board)
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = large_num
        for cell in _board['cell list'].values():
            if cell['state'] == '-':
                mark_cell(cell['position'], player_one, _board)
                score = minimax_algorithm(_board, depth + 1, True)
                _board = undo_mark_cell(cell['position'], _board)
                best_score = min(score, best_score)
        return best_score


# Other Functions---------------------------------------
def check_win(player):
    marked_cells = []
    if player['identity'] == player_one['identity']:
        marked_cells = board['P1 cells']
    elif player['identity'] == player_two['identity']:
        marked_cells = board['P2 cells']

    for win_combo in WIN_COMBINATIONS:
        if win_combo[0] in marked_cells and \
                win_combo[1] in marked_cells and \
                win_combo[2] in marked_cells:
            return True
    return False


def check_tie():
    for cell in board['cell list'].values():
        if cell['state'] == '-':
            return False
    return True


def get_move(player):
    if player['is human']:
        move = -4
        while True:
            move_prompt = get_move_prompt.format(player['name'])
            move = get_input(move_prompt, 'int', [1, 9])
            if board['cell list'][move]['state'] == '-':
                break
            else:
                print('ERROR: Position already occupied, please enter a valid move.')
        return move

    else:
        time.sleep(0.75)
        best_move = get_best_move(board)
        return best_move


def play_round():
    while True:
        global current_player

        print_board()

        move = get_move(current_player)

        mark_cell(move, current_player, board)

        if check_win(current_player):
            add_score(current_player)
            print_board()
            print('\n{} Has Won!!!'.format(current_player['name']))
            reset_board()
            break
        elif check_tie():
            print_board()
            print('\nMatch Concluded As Tie')
            reset_board()
            break

        switch_player()


def game_loop(mode):
    global current_player, player_one, player_two

    if mode == pages[1]:
        player_one = {'identity': 'P1', 'is human': True, 'name': 'PLAYER ONE', 'symbol': 'X', 'score': 0}
        player_two = {'identity': 'P2', 'is human': False, 'name': 'COMPUTER', 'symbol': 'O', 'score': 0}
    elif mode == pages[2]:
        player_one = {'identity': 'P1', 'is human': True, 'name': 'PLAYER ONE', 'symbol': 'X', 'score': 0}
        player_two = {'identity': 'P2', 'is human': True, 'name': 'PLAYER TWO', 'symbol': 'O', 'score': 0}

    current_player = player_one

    can_play = True

    while can_play:
        play_round()
        can_play = get_input('Wanna go for another round? [Y/N]: ', 'bool')


# ______________________PUBLIC METHODS_______________________

def game_page(mode):
    if mode == pages[1]:
        game_loop(mode)
    elif mode == pages[2]:
        game_loop(mode)
    else:  # remove later
        raise Exception(f"'{mode}' Game Mode doesn't exist")

game_page('one player mode')
