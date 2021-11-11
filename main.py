import PySimpleGUI as sg
import pandas as pd
from CardFunctions import CardFunctions


def pop_win():
    pop_out = [
        [],
        [sg.Combo(languages, default_value='Pick a Language', k='lang_1', size=(16, 1))],
        [sg.Text("To")],
        [sg.Combo(languages, default_value='Pick a Language', k='lang_2', size=(16, 1))],
        [sg.Button("Generate", size=(20, 2), k='I have chosen')]
    ]
    w_pop = sg.Window("", layout=pop_out, finalize=True, margins=(10, 10), element_justification='center',
                      disable_close=True, disable_minimize=True, modal=True)
    while True:
        event, values = w_pop.read()
        if event == 'I have chosen':
            if values['lang_1'] == 'Pick a Language' or values['lang_2'] == 'Pick a Language':
                sg.Popup("Data Error", title="")
                w_pop.make_modal()
            elif values['lang_2'] == values['lang_1']:
                sg.Popup("Values must be different", title="")
                w_pop.make_modal()
            else:
                w_pop.close()
                return values


def generate_dict(f_languages):
    v_1 = f_languages['lang_1']
    v_2 = f_languages['lang_2']
    file_name = f"./resources/dictionary_{v_1} to {v_2}.csv"
    try:
        dictionary = pd.read_csv(file_name)
    except FileNotFoundError:
        sg.popup("Saved file not found, using generic word list.")
        dictionary = pd.read_csv('./resources/R_Dictionary.csv')
    else:
        sg.popup("Loaded previous word list.")

    if v_1 == 'Chinese' or v_2 == 'Chinese':
        cards = dictionary.loc[:, [v_1, v_2, 'Pingying']]
    else:
        cards = dictionary.loc[:,[v_1, v_2]]
    cards = cards.sample(frac=1)
    cards = cards.values.tolist()
    return [[v_1, v_2], cards]

def mouse_function(event):
    # window.write_event_value(event, {'Hello': 15})
    f_canvas.flip_card()

sg.theme("LightGreen")
bg_color = "#B1DDC6"

pairs = []

frame_1 = [[sg.Canvas(size=(700, 480), background_color=bg_color, k='-t_canvas-')]]
languages = ['English','French','Spanish','German','Chinese']
# t_french = sg.Tab("French", [[]], k="-french-")
# t_spanish = sg.Tab("Spanish", [[]], k="-spanish-")
# t_german = sg.Tab("German", [[]], k="-german-")
# t_chinese = sg.Tab("Chinese", [[]], k="-chinese-")

layout = [
    # [sg.TabGroup([[t_french], [t_spanish], [t_german], [t_chinese]], size=(700, 400), background_color=bg_color, tab_background_color=bg_color)],
    [sg.Frame("", frame_1, expand_x=True, element_justification='center', border_width=0, background_color=bg_color)],
    [sg.Button(image_filename="./resources/wrong.png", border_width=0, k='-wrong-'), sg.Text("", size=(15, 10), background_color=bg_color), sg.Button(image_filename="./resources/right.png", border_width=0, k='-right-')],
    [sg.Button("Pick Language", k='-language_select-',size=(20,2)), sg.Button("Save Progress", size=(18,2), k='-save-'), sg.Text("", expand_x=True, background_color=bg_color), sg.Button("Exit", size=(14, 2))]
]
window = sg.Window("Flash Cards: Language", layout=layout, element_justification='center', finalize=True, size=(800, 780), background_color=bg_color, margins=(20, 20))
f_canvas = CardFunctions(window['-t_canvas-'].tk_canvas)


# t_chinese.select()
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == '-language_select-':
        # f_canvas.unbind("<Button-1>", mouse_function)
        pairs = generate_dict(pop_win())
        f_canvas.kanvas.bind("<Button-1>", mouse_function)
        f_canvas.send_deck(pairs)
        f_canvas.get_card()
    if not pairs == []:
        if event == '-wrong-':
            f_canvas.return_to_deck()
            f_canvas.get_card()
        if event == '-right-':
            f_canvas.deck_size -= 1
            f_canvas.get_card()
        if event == '-save-':
            save_pandas = pd.DataFrame(f_canvas.flash_deck[1], columns=f_canvas.flash_deck[0])
            save_pandas.to_csv(f"./resources/dictionary_{f_canvas.flash_deck[0][0]} to {f_canvas.flash_deck[0][1]}.csv", index=False)
            sg.popup("Saved")
        # window.write_event_value('To Be Done', {'Languages': (lang_select['lang_1'], lang_select['lang_2'])})
        # sg.AddToReturnList()

window.close()
