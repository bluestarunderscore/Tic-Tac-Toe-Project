import socket
import pickle
import random
import PySimpleGUI as ui
###############################################################
# Tic Tac Toe for CS361 Winter 2024
# run with "python tic_tac_toe.py" in command line, or double-
# click the file.
#
###############################################################

###############################################################
# GLOBAL VARIABLES
#
###############################################################

# Global font variables
title_font = ("Times New Roman", 26)
default_font = ("Arial", 12)
larger_font = ("Arial", 18)

# Global option variables
is_large_font = 0
is_high_contrast = 0

# Global default font
main_font = default_font

###############################################################
# GENERAL HELPER FUNCTIONS
# - This section is for functions that don't supply a complete
#   functionality for a page.
#
###############################################################
def toggle_font():
    global is_large_font
    global main_font
    if is_large_font == 0:
        is_large_font = 1
        main_font = larger_font
    else:
        is_large_font = 0
        main_font = default_font

def get_opponent_turn(op_w):
    if len(op_w) == 0:
        print("CLIENT: Draw detected")
        return -1
    return_value = random.choice(op_w)
    print("CLIENT: Opponent played board key", return_value[0],return_value[1])
    op_w.remove(return_value)
    return return_value
    
        
#############################################################
# LAYOUT CREATIONS
#
#
#############################################################
def create_main_layout():
    # Create the main menu layout
    main_menu_layout = [[ui.Text('Tic-Tac-Toe', font = title_font)],
              [ui.Button('New Game', font = main_font)],
              [ui.Button('Load Game', font = main_font)],
              [ui.Button('Tutorial', font = main_font)],
              [ui.Button('Options', font = main_font)],
              [ui.Button('Exit Game', font = main_font)]]
    return main_menu_layout

def create_options_layout():
    # Create the options menu layout
    options_layout = [[ui.Button('Large Font Size', font = main_font)],
                   [ui.Button('High Contrast', font = main_font)],
                   [ui.Button('Apply Changes', font = main_font)],
                   [ui.Button('Back to Main Menu', font = main_font)]]
    return options_layout

def create_game_layout():
    # Create the layout of the game board.
    # Board Coordinates:
    #   00 01 02
    #   10 11 12
    #   20 21 22
    game_layout = [[ui.Button('', font = main_font, size=(6,3), key='00'), ui.Button('', font = main_font, size=(6,3), key='01'), ui.Button('', font = main_font, size=(6,3), key='02')],
               [ui.Button('', font = main_font, size=(6,3), key='10'), ui.Button('', font = main_font, size=(6,3), key='11'), ui.Button('', font = main_font, size=(6,3), key='12')],
               [ui.Button('', font = main_font, size=(6,3), key='20'), ui.Button('', font = main_font, size=(6,3), key='21'), ui.Button('', font = main_font, size=(6,3), key='22')],
               [ui.Button('Save', font = main_font, size=(6,1)), ui.Button('Load', font = main_font, size=(6,1)), ui.Button('Quit', font = main_font, size=(6,1))]]
    return game_layout

#############################################################
# WINDOW CREATIONS
#
#
#############################################################

def create_main_window():
    main_menu_layout = create_main_layout()
    main_window = ui.Window('Tic-Tac-Toe', main_menu_layout, size = (600,400), element_justification = 'c', finalize = True)
    return main_window

def create_options_window():
    options_layout = create_options_layout()
    options_window = ui.Window('Tic-Tac-Toe - Options', options_layout, size = (600,400), element_justification = 'c', finalize = True)
    return options_window

def create_game_window():
    game_layout = create_game_layout()
    game_window = ui.Window('Tic-Tac-Toe - In Play', game_layout, size = (600,400), element_justification = 'c', finalize = True)
    return game_window

# TODO: Microservice
def save_game(player_1_score, player_2_score, board):
    print("test.")

def load_game():
    print("test 2.")


# Very convoluted way of checking game winnability.
# Returns true if winning condition is present on the board, otherwise false.
def is_winning_board(board, is_opponent_turn):
    print("CLIENT: Checking if winning board")
    row_0 = board[0][0] != 'N' and board[0][0] == board[0][1] and board[0][0] == board[0][2]
    row_1 = board[1][0] != 'N' and board[1][0] == board[1][1] and board[1][0] == board[1][2]
    row_2 = board[2][0] != 'N' and board[2][0] == board[2][1] and board[2][0] == board[2][2]
    
    col_0 = board[0][0] != 'N' and board[0][0] == board[1][0] and board[0][0] == board[2][0]
    col_1 = board[0][1] != 'N' and board[0][1] == board[1][1] and board[0][1] == board[2][1]
    col_2 = board[0][2] != 'N' and board[0][2] == board[1][2] and board[0][2] == board[2][2]
    
    diag_down = board[0][0] != 'N' and board[0][0] == board[1][1] and board[0][0] == board[2][2]
    diag_up = board[2][0] != 'N' and board[2][0] == board[1][1] and board[2][0] == board[0][2]

    if row_0 or row_1 or row_2 or col_0 or col_1 or col_2 or diag_down or diag_up:
        print("CLIENT: Winning board detected for internal player", is_opponent_turn)
        return True
    else:
        #print("CLIENT: Game not finished, continuing...")
        return False
    
#############################################################
# MENU LOGIC
#
#
#############################################################

#TODO: Refactor for less "elif" spam (may improve efficiency)
def main_loop():
    
    #Use global variables to allow proper usage.
    global main_font
    global default_font
    global larger_font
    global opponent_whitelist
    opponent_whitelist = ['00','01','02','10','11','12','20','21','22']
    board = [ ['N','N','N'],
              ['N','N','N'],
              ['N','N','N']]

    is_in_game = 0
    is_opponent_turn = 0
    player_1_score = 0
    player_2_score = 0
    previous_font = default_font
    
    # Whitelist for opponent placements
    # Board Coordinates:
    #   00 01 02
    #   10 11 12
    #   20 21 22

    print('CLIENT: Welcome to the Tic-Tac-Toe logs!')
    title = create_main_window()
    options = None
    game = None
    print('CLIENT: Created main window')

    #Begin main loop.
    while True:
        #Get every window loaded (do this every time to apply font size and (contrast NYI) changes)
        window, event, values = ui.read_all_windows()
        #print(event,values)
        #print(board)
            
        # Exiting the game with X
        if event == ui.WIN_CLOSED:
            break

        elif event == 'Quit':
                if ui.popup_yes_no('Are you sure you want to quit this game?', font=main_font) == 'Yes':
                    print('CLIENT: Saving and quitting to title (Saving NYI)')
                    is_in_game = 0
                    game.close()
                    game = None
                    title.un_hide()

#############################################################
# MAIN MENU
#
#
#############################################################
        # Starting a new game
        elif event == 'New Game':
            print('CLIENT: Starting new game')
            is_in_game = 1
            opponent_whitelist = ['00','01','02','10','11','12','20','21','22']
            board = [ ['N','N','N'],
                    ['N','N','N'],
                    ['N','N','N']]
            is_opponent_turn = 0
            title.hide()
            game = create_game_window()
         
        # TODO: Load the game (from either main menu or game board) microservice
        elif event == 'Load Game' or event == 'Load':
            print('CLIENT: Request to load game started...')
            file_name = ui.popup_get_file('Enter the save file name, or browse for it on your computer.', font=main_font)
            if file_name is not None:
                print('CLIENT: Request for', file_name, 'sent to microservice (NYI)')
            else:
                print('CLIENT: Request to load canceled.')

        # Display tutorial
        elif event == 'Tutorial':
            print('CLIENT: Showing tutorial')
            ui.popup('To play tic-tac-toe, click one of the buttons on the 3x3 board to place an X. The opponent (computer) will place an O.',
                     'Try to get three in a row before the enemy does, or force a draw!', font = main_font)

        # Open the options menu
        elif event == 'Options':
            print('CLIENT: Opened the options menu')
            title.hide()
            options = create_options_window()

        # Exit the game, confirming choice first
        elif event == 'Exit Game':
            if ui.popup_yes_no('Are you sure you want to exit the game?', font = main_font) == 'Yes':
                print('CLIENT: Saving and exiting (NYI)')
                exit()

#############################################################
# OPTIONS MENU
#
#
#############################################################

        # Change font size and update in command line log
        elif event == 'Large Font Size':
            toggle_font()
            print(str(is_large_font))

        # Actually apply the changes
        elif event == 'Apply Changes':
            print('CLIENT: Applying setting changes')
            options.close()
            options = None
            title.close()
            title = create_main_window()
            print("CLIENT: Current Font:", main_font)
            #title.un_hide()

        # Return to the main menu without updating
        elif event == 'Back to Main Menu':
            print('CLIENT: Quitting to title')
            options.close()
            options = None
            title.un_hide()

#############################################################
# GAME MENU
#
#
#############################################################

# TODO: Game Logic
        # Track player-pressed buttons and remove them from the list of valid buttons for the computer to play on.
        # Board Coordinates:
        #   00 01 02
        #   10 11 12
        #   20 21 22
        if is_in_game == 1 and is_opponent_turn == 0:
            if event != 'Quit' and event != 'Load' and event != 'Save':
                if event in opponent_whitelist:
                    board[int(event[0])][int(event[1])] = 'X'
                    window[event].update("X")
                    opponent_whitelist.remove(event)
                    if is_in_game and is_winning_board(board, is_opponent_turn):
                        print("Winning board")
                        is_in_game = 0
                    is_opponent_turn = 1

            # Quit the game and return to the main menu.
            if event == 'Quit':
                if ui.popup_yes_no('Are you sure you want to quit this game?', font=main_font) == 'Yes':
                    print('CLIENT: Saving and quitting to title (Saving NYI)')
                    is_in_game = 0
                    game.close()
                    game = None
                    title.un_hide()
        
        if is_in_game == 1 and is_opponent_turn == 1:
            opponent_turn = get_opponent_turn(opponent_whitelist)
            if opponent_turn == -1:
                is_in_game = 0
                print("CLIENT: Draw.")
                is_in_game = 0
                opponent_whitelist = ['00','01','02','10','11','12','20','21','22']
                board = [ ['N','N','N'],
                        ['N','N','N'],
                        ['N','N','N']]
            else:
                board[int(opponent_turn[0])][int(opponent_turn[1])] = 'O'
                window[opponent_turn].update("O")
                if is_in_game and is_winning_board(board, is_opponent_turn):
                        print("Winning board")
                        opponent_whitelist = ['00','01','02','10','11','12','20','21','22']
                        board = [ ['N','N','N'],
                                  ['N','N','N'],
                                  ['N','N','N']]
                        is_in_game = 0
                is_opponent_turn = 0
                window.refresh()

            # Quit the game and return to the main menu.
            if event == 'Quit':
                if ui.popup_yes_no('Are you sure you want to quit this game?', font=main_font) == 'Yes':
                    print('CLIENT: Saving and quitting to title (Saving NYI)')
                    is_in_game = 0
                    game.close()
                    game = None
                    title.un_hide()
        
        

        #window.refresh()
              
main_loop()

    
        
