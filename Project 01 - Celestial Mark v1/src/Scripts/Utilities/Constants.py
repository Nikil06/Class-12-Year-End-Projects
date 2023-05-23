import CustomEncodedFileParser as parser
from Utils import *

# File Paths (ie. fp_.... where fp indicates file path)
fp_encoded_file = r'C:\Users\nikil\Desktop\Project 01 - Celestial Mark v1\src\Assets\EncodedFile.txt'
fp_save_file = r'C:\Users\nikil\Desktop\Project 01 - Celestial Mark v1\src\Assets\save_file.dat'

# Extract Data From Encoded File (ie. pd()... where pd indicates parsed data)
pd_menu_page      = parser.get_section_data(fp_encoded_file, 'MENU',          return_str=True)
pd_game_board_ui  = parser.get_section_data(fp_encoded_file, 'GAME BOARD UI', return_str=True)
pd_credits        = parser.get_section_data(fp_encoded_file, 'CREDITS',       return_str=True)
pd_lore_header    = parser.get_section_data(fp_encoded_file, 'LORE HEADER',   return_str=True)

pd_quotes     = parser.get_section_data(fp_encoded_file, 'QUOTES',          return_list=True)
pd_lore_paras = parser.get_section_data(fp_encoded_file, 'LORE STORY', return_list=True)

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

