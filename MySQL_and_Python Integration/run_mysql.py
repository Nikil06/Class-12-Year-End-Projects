import sys
import time

from RegalQuill import printc
from RegalQuill.tabulate import Table, TableStyles
import configparser

import mysql.connector as connector


#########################################################################
# HIGH USAGE FUNCTIONS
#########################################################################
def _print(*args, sep=' ', end='\n'):
    printc(*args, sep=sep, end=end, remove_tags=(not print_colours))

def _input(__prompt: str):
    _print(__prompt, end='')
    user_input = input()
    return user_input


def prompt_yes_or_no(__prompt: str, use_modified_input: bool = True):
    positive_prompts = ['y', 'yes']
    negative_prompts = ['n', 'no']

    input_command = input
    if use_modified_input:
        input_command = _input

    while True:
        want_colours = input_command(__prompt).strip().lower()

        if want_colours in ['y', 'yes']:
            return True
        elif want_colours in ['n', 'no']:
            return False
        else:
            print("Invalid Input.",
                  f"\t Positive Prompts : {positive_prompts}",
                  f"\t Negative Prompts : {negative_prompts}",
                  sep='\n')

print_colours = prompt_yes_or_no("Does your terminal support colours? [Y/N] : ", False)
_print()

def log_success(message: str):
    _print(f'[l green]/[+][/l green] {message}')

def log_failure(message: str, exception=None):
    _print(f'[l red]/[!][/l red] {message}')
    if exception is not None:
        _print(f'\n[red]{exception}[/red]')

def exit_program(time_to_exit: float):
    if time_to_exit:
        _print(f'[red]Exiting in {time_to_exit} seconds[/red]')
        time.sleep(time_to_exit)
    sys.exit()

#########################################################################


#########################################################################
# STARTUP FUNCTIONS
#########################################################################
# Get Credentials config.ini
def get_credentials():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        db_host = config.get('Connection', 'HOST')
        db_user = config.get('Connection', 'USER')
        db_password = config.get('Connection', 'PASSWORD')

        log_success('obtained connection credentials')
        return db_host, db_user, db_password
    except Exception as e:
        log_failure('failed to obtain connection credentials', e)
        exit_program(5)

# Get Preferences from config.ini
def get_preferences():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        _db_name = config.get('Preferences', 'DB_NAME')
        _file_path = config.get('Preferences', 'FILE_PATH')
        _comment_marker = config.get('Preferences', 'COMMENT_MARKER')

        log_success('obtained preferences')
        return _db_name, _file_path, _comment_marker
    except Exception as e:
        log_failure('failed to obtain preferences', e)
        exit_program(5)

db_name, file_path, comment_marker = get_preferences()

# Connect with mysql
def get_connection():
    db_host, db_user, db_password = get_credentials()
    try:
        _connection = connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        log_success('connection with mysql has been established')
        return _connection
    except Exception as e:
        log_failure('failed to establish connection with mysql', e)
        exit_program(5)

#########################################################################

#########################################################################
# QUERYING LOGIC
#########################################################################

connection = get_connection()
cursor = connection.cursor()

# Function that runs all the queries to the connection
def run_queries(_queries: list[str]):
    for i, query in enumerate(_queries):
        print()
        i += 1
        _print(f'{i} : [bold, l blue]{query}[reset]')

        try:
            cursor.execute(query)
            log_success(f'{i} was executed successfully')
        except Exception as e:
            log_failure(f"{i} encountered an error in execution", e)
            exit_program(5)

        try:
            results = cursor.fetchall()
            if results:
                rows = results[:]
                cols = [col[0] for col in cursor.description]

                if not cols:
                    cols = None

                table = Table(rows=rows, headers=cols)
                render = table.get_render(TableStyles.SQL_Style)
                render = '\n'.join('\t' + line for line in render.split('\n'))
                print(render)

            else:
                _print('\t', 'fetched result was empty')
        except Exception as e:
            log_failure(f'Error occurred while fetching the results of {i}', e)

def get_queries_from_file():
    with open(file_path) as file:
        lines = file.readlines()

    filtered = []
    for line in lines:
        if line.strip() != '' and not line.startswith(comment_marker):
            filtered.append(line[:-1])

    return filtered


#########################################################################

setup_queries = [f"CREATE DATABASE IF NOT EXISTS {db_name};",
                 f"USE {db_name};"]

queries = get_queries_from_file()

run_queries(setup_queries)
_print('[yellow, crossed]\n'+'x'*75)
run_queries(queries)

connection.close()
_print()
log_success('connection closed successfully')

_input("\n[yellow]Press Enter to Exit : [reset]")
