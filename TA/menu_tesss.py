from ursina import *

def create_text_with_border(parent, text, position, scale, text_color, border_color, border_thickness=0.05):
    # Create border texts
    offsets = [
        (border_thickness, 0),
        (-border_thickness, 0),
        (0, border_thickness),
        (0, -border_thickness),
        (border_thickness, border_thickness),
        (-border_thickness, -border_thickness),
        (border_thickness, -border_thickness),
        (-border_thickness, border_thickness)
    ]
    for offset in offsets:
        Text(parent=parent, text=text, position=(position[0] + offset[0], position[1] + offset[1]), 
             origin=(0, 0), scale=scale, color=border_color)

    # Create main text
    Text(parent=parent, text=text, position=position, origin=(0, 0), scale=scale, color=text_color)

def create_menu(start_game, show_instructions, exit_game):
    menu = Entity(enabled=True)
    menu_bg = Entity(parent=menu, model='quad', texture='cards/menu_bg', scale=(window.aspect_ratio * 8.5, 8.5), z=1)

    create_text_with_border(parent=menu, text='BlackJack', position=(0, 3), scale=25, text_color=color.white, border_color=color.black)

    def create_button(text, position, on_click):
        button = Button(parent=menu, text=text, position=position, scale=(3.25, 1.5), color=color.clear, on_click=on_click)
        button.text_entity.color = color.azure  # Set the text color separately
        button.text_entity.scale *= 1.5  # Increase text size if needed
        return button

    start_button = create_button('Start Game', (0, 0), start_game)
    instructions_button = create_button('Instructions', (0, -1.5), show_instructions)
    exit_button = create_button('Exit', (0, -3), exit_game)

    return menu
