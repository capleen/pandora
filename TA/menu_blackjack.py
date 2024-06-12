from ursina import *

def create_menu(start_game, show_instructions, exit_game):
    menu = Entity(enabled=True)
    menu_bg = Entity(parent=menu, model='quad', texture='cards/menu_bg', scale=(window.aspect_ratio * 8.5, 8.5), z=1)

    # Text(parent=menu, text='BlackJack', position=(0, 3), origin=(0, 0), scale=25, color=color.white)

    def create_button(text, position, on_click):
        button = Button(parent=menu, text=text, position=position, scale=(3.25, 1.5), color=color.clear, on_click=on_click)
        button.text_entity.color = color.azure
        button.text_entity.scale *= 1.5
        return button

    start_button = create_button('Start Game', (0, 0), start_game)
    instructions_button = create_button('Petunjuk', (0, -1.5), show_instructions)
    exit_button = create_button('Keluar', (0, -3), exit_game)

    return menu
