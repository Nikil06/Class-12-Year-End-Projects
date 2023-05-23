from Utilities.Constants import *


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
