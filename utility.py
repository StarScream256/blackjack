import os
import sys

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_terminal():
    input('Press any key to continue ...')

def delete_prevline():
    print("\033[F\033[K", end="")

def end_program(text = 'Program finished'):
    print(text)
    sys.exit(0)
