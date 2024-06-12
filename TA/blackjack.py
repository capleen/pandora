from ursina import *
import random
from menu_blackjack import create_menu

app = Ursina()

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [f'{rank} of {suit}' for suit in suits for rank in ranks] # Bikin variabel rank buat ambil nilai, suit buat warna
random.shuffle(deck)

tangan_pemain = []
tangan_bandar = []
ent_tangan_pemain = []
ent_tangan_bandar = []
game_over = False

def bagi_kartu(deck, hand):
    card = deck.pop()
    hand.append(card)
    return card

def hitung_total_nilai_tangan(hand):
    nilai = 0
    ada_as = False
    for card in hand:
        rank = card.split()[0]
        if rank.isdigit():
            nilai += int(rank)
        elif rank in ['Jack', 'Queen', 'King']:
            nilai += 10
        elif rank == 'Ace':
            ada_as = True
            nilai += 11
    if ada_as and nilai > 21:
        nilai -= 10
    return nilai

def reset_game():
    global deck, tangan_pemain, tangan_bandar, ent_tangan_pemain, ent_tangan_bandar, game_over
    deck = [f'{rank} of {suit}' for suit in suits for rank in ranks]
    random.shuffle(deck)
    
    tangan_pemain = []
    tangan_bandar = []
    
    for entity in ent_tangan_pemain + ent_tangan_bandar:
        destroy(entity)
    
    ent_tangan_pemain = []
    ent_tangan_bandar = []
    
    bagi_kartu(deck, tangan_pemain)
    bagi_kartu(deck, tangan_bandar)
    bagi_kartu(deck, tangan_pemain)
    bagi_kartu(deck, tangan_bandar)
    
    for i, card in enumerate(tangan_pemain):
        card_entity = create_card_entity(card, position=(-1 + i * 1.2, -2))
        card_entity.texture = card_entity.face_texture
        ent_tangan_pemain.append(card_entity)
    
    for i, card in enumerate(tangan_bandar):
        if i == 0:
            card_entity = create_card_entity(card, position=(-1 + i * 1.2, 2))
            card_entity.texture = card_entity.face_texture
            ent_tangan_bandar.append(card_entity)
        else:
            card_entity = create_card_entity(card, position=(-1 + i * 1.2, 2))
            card_entity.texture = card_entity.back_texture
            ent_tangan_bandar.append(card_entity)
    
    message_text.enabled = False
    button_restart.enabled = False
    
    update_nilai_tangan_pemain()
    update_nilai_tangan_bandar()
    nilai_tangan_bandar.enabled = False
    game_over = False

def create_card_entity(card, position):
    rank, _, suit = card.partition(' of ')
    card_image = f'cards/{rank}_of_{suit}.png'.lower()
    card_entity = Entity(model='quad', texture='cards/back.png', position=position, scale=(1, 1.5))
    card_entity.face_texture = load_texture(card_image)
    card_entity.back_texture = load_texture('cards/back.png')
    card_entity.double_sided = True
    return card_entity

def update_nilai_tangan_pemain():
    nilai_tangan_pemain.text = f'Total Nilai: {hitung_total_nilai_tangan(tangan_pemain)}'

def update_nilai_tangan_bandar():
    nilai_tangan_bandar.text = f'Total Nilai: {hitung_total_nilai_tangan(tangan_bandar)}'
    nilai_tangan_bandar.enabled = True

def start_game():
    menu.enabled = False
    reset_game()
    background.enabled = True
    nilai_tangan_pemain.enabled = True
    nilai_tangan_bandar.enabled = True
    message_text.enabled = False

def show_instructions():
    instructions_text.enabled = True

def exit_game():
    application.quit()

def input(key):
    global game_over
    if menu.enabled or game_over:
        return
    if key == 'h':
        card = bagi_kartu(deck, tangan_pemain)
        card_entity = create_card_entity(card, position=(-1 + len(tangan_pemain) * 1.2, -2))
        card_entity.texture = card_entity.face_texture
        ent_tangan_pemain.append(card_entity)
        flip_card(card_entity)
        update_nilai_tangan_pemain()
        if hitung_total_nilai_tangan(tangan_pemain) > 21:
            message_text.text = 'Kamu Kalah!'
            message_text.enabled = True
            nilai_tangan_bandar.enabled = True
            button_restart.enabled = True
            game_over = True

    if key == 's':
        flip_card(ent_tangan_bandar[1])
        while hitung_total_nilai_tangan(tangan_bandar) < 17:
            card = bagi_kartu(deck, tangan_bandar)
            card_entity = create_card_entity(card, position=(-1 + len(tangan_bandar) * 1.2, 2))
            card_entity.texture = card_entity.face_texture
            ent_tangan_bandar.append(card_entity)
            update_nilai_tangan_bandar()
            flip_card(card_entity)
        player_nilai = hitung_total_nilai_tangan(tangan_pemain)
        dealer_nilai = hitung_total_nilai_tangan(tangan_bandar)
        if dealer_nilai > 21 or player_nilai > dealer_nilai:
            message_text.text = 'Kamu Menang!'
            nilai_tangan_bandar.enabled = True
        elif dealer_nilai > player_nilai:
            message_text.text = 'Bandar Menang!'
            nilai_tangan_bandar.enabled = True
        else:
            message_text.text = 'Seri!'
        message_text.enabled = True
        button_restart.enabled = True
        nilai_tangan_bandar.enabled = True
        game_over = True

    if key == 'q':
        application.quit()
    
    if key == 'escape':
        application.quit()

def flip_card(card_entity):
    card_entity.texture = card_entity.back_texture
    card_entity.animate_rotation_y(180, duration=0.5, curve=curve.linear, interrupt=True)
    invoke(set_texture_after_flip, card_entity, delay=0.5)

def set_texture_after_flip(card_entity):
    card_entity.scale_x *= -1
    card_entity.texture = card_entity.face_texture

message_text = Text(text='', position=(0, 0), origin=(0, 0), scale=2, color=color.white, enabled=False)
instructions_text = Text(text='Tutorial :\n\nTekan H untuk Hit\n\nTekan S untuk Stand\n\nTekan Q/Esc untuk Keluar Game', position=(0.55, -0.1), origin=(0, 0), scale=1.5, color=color.white, enabled=False)

background = Entity(
    model='quad',
    texture='cards/background.jpg',
    scale=(window.aspect_ratio * 12, 12),
    position=(0, 0, 10),
    enabled=False
)

nilai_tangan_pemain = Text(text=f'Total Nilai: {hitung_total_nilai_tangan(tangan_pemain)}',
                              position=(-0.7, -0.25),
                              scale=2,
                              color=color.white,
                              enabled=False)

nilai_tangan_bandar = Text(text=f'Total Nilai: {hitung_total_nilai_tangan(tangan_bandar)}',
                              position=(-0.7, 0.25),
                              scale=2,
                              color=color.white,
                              enabled=False)

button_restart = Button(text='Main Lagi', position=(0.7, 0), scale=0.18, color=color.azure, enabled=False)
button_restart.on_click = reset_game

menu = create_menu(start_game, show_instructions, exit_game)

app.run()