import socket
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

# Swap out fonts upon window reload
def toggle_font():
    global is_large_font
    global main_font
    if is_large_font == 0:
        is_large_font = 1
        main_font = larger_font
    else:
        is_large_font = 0
        main_font = default_font
        
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
    game_layout = [[ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3))],
               [ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3))],
               [ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3)), ui.Button('', font = main_font, size=(6,3))],
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
    previous_font = default_font
    
    print('CLIENT: Welcome to the Tic-Tac-Toe logs!')
    title = create_main_window()
    options = None
    game = None
    print('CLIENT: Created main window')

    #Begin main loop.
    while True:
        #Get every window loaded (do this every time to apply font size and (contrast NYI) changes)
        window, event, values = ui.read_all_windows()
        
        # Exiting the game with X
        if event == ui.WIN_CLOSED:
            break

#############################################################
# MAIN MENU
#
#
#############################################################
                
        # Starting a new game
        elif event == 'New Game':
            print('CLIENT: Starting new game')
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
            print('CLIENT: Saving and quitting to title')
            options.close()
            options = None
            title.un_hide()

#############################################################
# GAME MENU
#
#
#############################################################

# NOTE: THIS SECTION IS INCOMPLETE, AND IS NOT PART OF MILESTONE 1'S FEATURE SET.

        # Quit the game and return to the main menu.
        elif event == 'Quit':
            if ui.popup_yes_no('Are you sure you want to quit this game?', font=main_font) == 'Yes':
                print('CLIENT: Saving and quitting to title (Saving NYI)')
                game.close()
                game = None
                title.un_hide()
main_loop()

    
        
