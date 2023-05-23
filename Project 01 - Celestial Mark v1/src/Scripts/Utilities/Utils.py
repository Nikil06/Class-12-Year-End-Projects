import os


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
