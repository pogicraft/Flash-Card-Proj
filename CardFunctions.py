import tkinter as tk
from PIL import Image, ImageTk
import random


def draw_card(plate, triple, c_count):
    plate.delete('all')
    print(triple)
    plate.create_image(0, 0, image=triple[0], anchor='nw')
    plate.create_text(350, 130, text=triple[1], font=('Helvetica', 32), justify='center')
    if triple[1] == 'Chinese':
        plate.create_text(350, 210, text=triple[2][1], justify='center', font=('Verdana', 24))
        plate.create_text(350, 260, text=triple[2][0], justify='center', font=('Verdana', 24))
    else:
        plate.create_text(350, 240, text=triple[2], justify='center', font=('Verdana', 24))
    plate.create_text(640, 420, text=f"{c_count}/10000", justify='center', font=('Verdana', 14), anchor='se')
    plate.update()


class CardFunctions:
    def __init__(self, root):
        a = Image.open("./resources/card_front.png")
        b = Image.open("./resources/card_back.png")
        self.card_front = ImageTk.PhotoImage(a)
        self.card_back = ImageTk.PhotoImage(b)
        self.kanvas = root
        self.drawn = {'front': [self.card_front, '', ''], 'back': [self.card_back, '', '']}
        self.current = 'front'
        self.flash_deck = None
        self.c_card = None
        self.deck_size = None

    def get_card(self):
        pop_index = random.randint(0, self.deck_size)
        self.c_card = self.flash_deck[1].pop(pop_index)
        print(self.c_card)
        if self.flash_deck[0][0] == 'Chinese':
            self.drawn['front'] = [self.card_front, self.flash_deck[0][0], [self.c_card[0], self.c_card[2]]]
            self.drawn['back'] = [self.card_back, self.flash_deck[0][1], self.c_card[1]]
        elif self.flash_deck[0][1] == 'Chinese':
            self.drawn['front'] = [self.card_front, self.flash_deck[0][0], self.c_card[0]]
            self.drawn['back'] = [self.card_back, self.flash_deck[0][1], [self.c_card[1], self.c_card[2]]]
        else:
            self.drawn['front'] = [self.card_front, self.flash_deck[0][0], self.c_card[0]]
            self.drawn['back'] = [self.card_back, self.flash_deck[0][1], self.c_card[1]]
        draw_card(self.kanvas, self.drawn[self.current], self.deck_size)
        
    def flip_card(self):
        if self.current == 'front':
            self.current = 'back'
        elif self.current == 'back':
            self.current = 'front'
        
        draw_card(self.kanvas, self.drawn[self.current], self.deck_size)
        
    def send_deck(self, deck):
        self.flash_deck = deck
        self.deck_size = len(self.flash_deck[1])
        
    def return_to_deck(self):
        self.flash_deck[1].append(self.c_card)
        