import os
import random
import time


#######################################################################################################
# CUSTOM ENCODED FILE PARSER
#######################################################################################################

def read_encoded_file(file_path):
    """Reads the contents of the encoded file and returns a list of lines."""
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()

    return lines

def filter_lines(lines):
    """Filters out empty lines and lines starting with '#' from a list of lines and returns the filtered list."""
    ret_lines = []
    for line in lines:
        if line.strip() != '' and line[0] != '#':
            ret_lines.append(line[:-1])
    return ret_lines


def extract_sections(lines):
    """Extracts sections from the lines based on the '$$$' delimiter and returns a dictionary of sections."""
    current_section = ''
    current_section_first_idx = None
    sections = {}

    for i in range(len(lines)):
        if lines[i][:4] == '$$$ ':
            if current_section_first_idx is None:
                current_section = lines[i][4:]
                current_section_first_idx = i + 1
            else:
                sections[current_section] = lines[current_section_first_idx:i]
                current_section = lines[i][4:]
                current_section_first_idx = i + 1
        if i == len(lines) - 1 and current_section_first_idx is not None:
            sections[current_section] = lines[current_section_first_idx:]

    return sections


def parse_encoded_file(file_path):
    """Parses the encoded file and returns its sections as a dictionary."""
    file_lines = read_encoded_file(file_path)
    file_lines = filter_lines(file_lines)
    sections = extract_sections(file_lines)
    return sections

def get_section_data(file_path, section_title, return_list=False, return_str=False):
    """Retrieves a specific section from the parsed encoded file and returns it in the specified format. """
    parsed_data = parse_encoded_file(file_path)
    section = None
    try:
        section = parsed_data[section_title]
    except KeyError:
        raise KeyError('{} Section Unavailable in Encoded File'.format(section_title))

    if return_list and not return_str:
        return section
    elif return_str and not return_list:
        return '\n'.join(section)
    else:
        if not return_list and not return_str:
            raise TypeError('Return type has not been specified.')
        elif return_str and return_list:
            raise TypeError('Can only return list or str types, not both.')
        
#######################################################################################################
# UTILS
#######################################################################################################

def clear_screen():
    if os.name == 'nt':
        # for Windows
        os.system('cls')
    else:
        # for macOS and Linux
        os.system('clear')


def my_input(_prompt):
    """(Similar to) Overloading built-in input(__prompt) function to account for quit command"""
    user_input = input(_prompt)
    if user_input.lower() == 'quit':
        exit()
    return user_input


def get_input(prompt, target_type, int_range=None):
    """
    target types: 2

    type : 'int' -> takes input converts to int and does error handling for it.
                    if int_range is specified then does error handing for that too.

                    range[0] = minimum int value;
                    range[1] = maximum int value;

                    returns integer

    type : 'bool' -> takes input and gives output for yes or no question

                    returns bool
    """

    if target_type == 'bool':
        while True:
            _input = my_input('\n' + prompt).lower()

            positive_responses = ['yes', 'y']
            negative_responses = ['no', 'n']

            if _input in positive_responses:
                return True
            elif _input in negative_responses:
                return False
            else:
                print('ERROR: Invalid input. Please enter one of the below responses')
                print('       Positive responses:', ' or '.join(positive_responses))
                print('       Negative responses:', ' or '.join(negative_responses))
    elif target_type == 'int':
        while True:
            _input = my_input('\n'+prompt).lower()

            try:
                ret_int = int(_input)
                if int_range is None:
                    return ret_int
                elif int_range[0] <= ret_int <= int_range[1]:
                    return ret_int
                else:
                    print('ERROR: Invalid Input. Enter a number from {} to {}'.format(int_range[0], int_range[1]))
                    continue
            except ValueError:
                print('ERROR: Invalid Input. Enter a number from {} to {}'.format(int_range[0], int_range[1]))
                continue

    else:
        raise Exception(target_type + ' Target Type not Registered')


def wrap_text(text, wrap_length):
    """
    text: text to be wrapped

    wrap_length: max number of chars per line

    takes in a long sting and converts it to a list of short strings with wrap_length parameter
    also makes sure that no word is cutoff in the middle

    returns: list of wrapped lines
    """

    wrapped_lines = []
    current_line = ''

    words = text.split(' ')  # separates words

    for word in words:
        if len(current_line) + len(word) <= wrap_length:
            current_line += word + ' '
        else:
            wrapped_lines.append(current_line.rstrip())
            current_line = word + ' '

    wrapped_lines.append(current_line.rstrip())  # Adds the last remaining words at the end

    return wrapped_lines

#######################################################################################################
# CONSTANTS
#######################################################################################################

# File Paths (ie. fp_.... where fp indicates file path)
fp_encoded_file = r'C:\Users\nikil\Desktop\Project 01 - Celestial Mark v1\src\Assets\EncodedFile.txt'
fp_save_file = r'C:\Users\nikil\Desktop\Project 01 - Celestial Mark v1\src\Assets\save_file.dat'

# Extract Data From Encoded File (ie. pd()... where pd indicates parsed data)
pd_menu_page      = get_section_data(fp_encoded_file, 'MENU',          return_str=True)
pd_game_board_ui  = get_section_data(fp_encoded_file, 'GAME BOARD UI', return_str=True)
pd_credits        = get_section_data(fp_encoded_file, 'CREDITS',       return_str=True)
pd_lore_header    = get_section_data(fp_encoded_file, 'LORE HEADER',   return_str=True)

pd_quotes     = get_section_data(fp_encoded_file, 'QUOTES',          return_list=True)
pd_lore_paras = get_section_data(fp_encoded_file, 'LORE STORY', return_list=True)

# _______________________________________________________________________________________________
pages = ('menu', 'one player mode', 'two player mode', 'lore', 'credits', 'quit')
back_to_menu_prompt = '\nPress Enter to get beck to Main Menu...'
bold_sep_line  = ' ============================================================================ '
empty_sep_line = '|                                                                            |'
get_move_prompt = '{}, please enter the position of cell of your choice : '
# _______________________________________________________________________________________________
large_num = int( 1e15)
small_num = int(-1e15)
# _______________________________________________________________________________________________
WIN_COMBINATIONS = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                    (1, 4, 7), (2, 5, 8), (3, 6, 9),
                    (1, 5, 9), (3, 5, 7))


#######################################################################################################
# MENU PAGE
#######################################################################################################

menu_prompt = 'ENTER THE NUMBER BESIDE PAGE YOU WOULD LIKE TO ENTER : '
menu_prompt_range = [1, 5]


# ______________________PRIVATE METHODS______________________
def get_random_quote():
    quotes = pd_quotes
    return random.choice(quotes)


# ______________________PUBLIC METHODS_______________________

def menu_page():
    placeholder_spaces = ' ' * 30
    formatted_quote = [placeholder_spaces] * 9
    quote = get_random_quote()

    wrapped_quote = wrap_text(quote, 30)

    for i in range(len(formatted_quote)):
        if i < len(wrapped_quote):
            formatted_quote[i] = wrapped_quote[i] + ' ' * (30 - len(wrapped_quote[i]))

    menu_page_str = pd_menu_page.format(formatted_quote[0], formatted_quote[1], formatted_quote[2],
                                         formatted_quote[3], formatted_quote[4], formatted_quote[5],
                                         formatted_quote[6], formatted_quote[7], formatted_quote[8])
    print(menu_page_str)
    nav_page = get_input(menu_prompt, 'int', menu_prompt_range)

    return pages[nav_page]

#######################################################################################################
# GAME
#######################################################################################################

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

#######################################################################################################
# LORE PAGE
#######################################################################################################

lore_wrap_len = 70

# ______________________PRIVATE METHODS______________________

def format_para(para):
    wrapped_lines = wrap_text(para, lore_wrap_len)
    for i in range(len(wrapped_lines)):
        wrapped_lines[i] = '|   ' + wrapped_lines[i] + (lore_wrap_len - len(wrapped_lines[i])) * ' ' + '   |'
    return '\n'.join(wrapped_lines)

# ______________________PUBLIC METHODS_______________________


def lore_page():

    header = pd_lore_header
    print(header)

    paragraphs = pd_lore_paras
    formatted_paragraphs = []
    need_back_to_menu_prompt = True

    for para in paragraphs:
        formatted_paragraphs.append(format_para(para))

    for i in range(len(formatted_paragraphs)):

        print(formatted_paragraphs[i])

        if i == len(formatted_paragraphs) - 2:
            break

        user_input = my_input('')

        if user_input == '':
            continue
        elif user_input == 's':
            print('\n\n'.join(formatted_paragraphs[i + 1:]))
            break
        elif user_input == 'm':
            need_back_to_menu_prompt = False
            break

    print(empty_sep_line)
    print(bold_sep_line)

    return need_back_to_menu_prompt

#######################################################################################################
# CREDITS PAGE
#######################################################################################################

# ______________________PUBLIC METHODS_______________________

def credits_page():
    print(pd_credits)

#######################################################################################################
# RUN GAME
#######################################################################################################

current_page = pages[0]


def navigate_to_menu(ask_for_menu_prompt=True):
    global current_page
    if ask_for_menu_prompt:
        input(back_to_menu_prompt)
    clear_screen()
    current_page = pages[0]


def run_game():
    global current_page

    current_page = pages[0]
    running = True

    while running:
        if current_page != pages[0]:
            time.sleep(.25)
            clear_screen()

        if current_page == pages[0]:
            current_page = menu_page()
        elif current_page == pages[1]:
            game_page(pages[1])
            navigate_to_menu()
        elif current_page == pages[2]:
            game_page(pages[2])
            navigate_to_menu()
        elif current_page == pages[3]:
            need_back_to_menu_prompt = lore_page()
            navigate_to_menu(need_back_to_menu_prompt)
        elif current_page == pages[4]:
            credits_page()
            navigate_to_menu()
        elif current_page == pages[5]:
            print('Ending Program...')
            running = False


run_game()
