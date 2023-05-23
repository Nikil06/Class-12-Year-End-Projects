from Utilities.Constants import *
import random

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
