import os
import sys
import time
import inspect

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_terminal():
    input('Press enter to continue ...')

def delete_prevline():
    print("\033[F\033[K", end="")

def end_program(text = 'Program finished'):
    print(text)
    sys.exit(0)

def sleep_terminal(t):
    '''
    Delay terminal

    Args:
        t (int): number of seconds to sleep
    '''
    time.sleep(t)

def debug(expression, purposes=''):
    caller_frame = inspect.getouterframes(inspect.currentframe())[1]
    file_path = caller_frame.filename
    file_name = os.path.basename(file_path)
    line_number = caller_frame.lineno

    default_purposes = f"debug request from {file_name} at line {line_number}"
    print("\033[96m{}\033[00m".format(f"DEBUG : {default_purposes if purposes == '' or not purposes else f'{purposes} ({file_name}:{line_number})'}"))
    print("\033[96m{}\033[00m".format('-' * len(str(expression))))
    print(expression)
    print("\033[96m{}\033[00m".format('-' * len(str(expression))))

# def pretty_print_dict(dict):
#     pretty_dict = ''
#     for key, value in dict

