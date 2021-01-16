import random
import tkinter


def load_images(card_images):
    suits = ['heart', 'club', 'diamond', 'spade']
    face_cards = ['jack', 'queen', 'king']
    if tkinter.TkVersion >= 8.6:
        extension = 'ppm'
    else:
        extension = 'png'

    # for each suit (loop all 52 cards), retrieve the image for the cards
    for suit in suits:
        # first the number cards 1 to 10
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((card, image,))
        # next the face cards
        for card in face_cards:  # this will loop all face cards
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            card_images.append((10, image,))


def _deal_card(frame):
    # pop the next card off the top of the deck
    next_card = deck.pop(0)  # deck is defined as list(cards)
    deck.append(next_card)  # you want to put the pulled card back into the deck to re-use
    # add the image to a Label and display the label into card frame
    tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
    # now return the card's face value
    return next_card


def score_hand(hand):
    # calculate the total score of all cards in the list
    # only one ace can have the value 11, and this will reduce to 1 if the hand would bust
    score = 0
    ace = False
    for next_card in hand:
        card_value = next_card[0]
        if card_value == 1 and not ace:
            ace = True
            card_value = 11
        score += card_value
        # if we would bust, check if there is an ace and subtract 10 if that's the case
        if score > 21 and ace:
            score -= 10
            ace = False
    return score


def deal_dealer():
    global dealer_win_count
    global player_win_count
    dealer_score = score_hand(dealer_hand)  # call score_hand function and store inside dealer_score, dealer_hand = []
    while 0 < dealer_score < 17:  # as long as dealer_score is between 0 & 17
        dealer_hand.append(_deal_card(dealer_card_frame))  # pop next card on dealer card frame
        dealer_score = score_hand(dealer_hand)  # count dealer card value from dealer_hand list
        dealer_score_label.set(dealer_score)  # print dealer_score on card frame grid

    player_score = score_hand(player_hand)  # player_hand = []
    if player_score > 21:
        result_text.set("Dealer wins!")
        dealer_win_count += 1
        dealer_won_label.set(dealer_win_count)
    elif dealer_score > 21 or dealer_score < player_score:
        result_text.set("Player wins!")
        player_win_count += 1
        player_won_label.set(player_win_count)
    elif dealer_score > player_score:
        result_text.set("Dealer wins!")
        dealer_win_count += 1
        dealer_won_label.set(dealer_win_count)
    else:
        result_text.set("Draw!")


def deal_player():
    global dealer_win_count
    player_hand.append(_deal_card(player_card_frame))  # pop next card on player card frame until
    # bust or when you decide to stop
    player_score = score_hand(player_hand)  # count player card value from player_hand list
    player_score_label.set(player_score)  # print player_score on card frame grid
    if player_score > 21:   # if player_score is greater than 21, print on top of result box
        result_text.set("Dealer wins!")
        dealer_win_count += 1
        dealer_won_label.set(dealer_win_count)
    # global player_score
    # global player_ace
    # card_value = deal_card(player_card_frame)[0]
    # if card_value == 1 and not player_ace:
    #     player_ace = True
    #     card_value = 11
    # player_score += card_value
    # if player_score > 21 and player_ace:
    #     player_score -= 10
    #     player_ace = False
    # player_score_label.set(player_score)
    # if player_score > 21:
    #     result_text.set("Dealer wins!")
    # print(locals())


def initial_deal():
    deal_player()
    dealer_hand.append(_deal_card(dealer_card_frame))
    dealer_score_label.set(score_hand(dealer_hand))
    deal_player()


def new_game():
    global dealer_card_frame
    global player_card_frame
    global dealer_hand
    global player_hand
    dealer_card_frame.destroy()
    dealer_card_frame = tkinter.Frame(card_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)
    player_card_frame.destroy()
    player_card_frame = tkinter.Frame(card_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")
    # create the list to store the dealer's and player's hands
    dealer_hand = []
    player_hand = []

    initial_deal()


def reset_score():
    global dealer_win_count
    global player_win_count
    dealer_win_count = 0
    player_win_count = 0
    dealer_won_label.set(dealer_win_count)
    player_won_label.set(player_win_count)


def shuffle():
    random.shuffle(deck)


def play():
    initial_deal()
    mainWindow.mainloop()


mainWindow = tkinter.Tk()
# Set up the screen and frames for the dealer and player
mainWindow.title("Black Jack")
mainWindow.geometry("640x480")
mainWindow.configure(background='green')
# create result text
result_text = tkinter.StringVar()  # create class StringVar to edit a widget's text
result = tkinter.Label(mainWindow, textvariable=result_text)  # Label implements a display box where you can place text or images
result.grid(row=0, column=0, columnspan=3)  # place display box inside grid with the following dimensions
# create card frame
card_frame = tkinter.Frame(mainWindow, relief="sunken", borderwidth=1, background="green")  # Frame: container letting you organize and group widgets
card_frame.grid(row=1, column=0, sticky='ew', columnspan=3, rowspan=2)  # put card frame inside grid dimensions
# dealer score label
dealer_score_label = tkinter.IntVar()  # create class IntVar to edit a widget's integer (dealer score)
tkinter.Label(card_frame, text="Dealer", background="green", fg="white").grid(row=0, column=0)  # display box for "dealer" within card frame
tkinter.Label(card_frame, textvariable=dealer_score_label, background="green", fg="white").grid(row=1, column=0)  # display box for dealer score within card frame
# embedded frame to hold the card images for dealer
dealer_card_frame = tkinter.Frame(card_frame, background="green")  # create another frame for the dealer card frame within the whole card frame
dealer_card_frame.grid(row=0, column=1, sticky="ew", rowspan=2)  # put dealer card frame (using grid) inside the whole card frame

player_score_label = tkinter.IntVar()  # create class IntVar to edit a widget's integer (player score)
tkinter.Label(card_frame, text="Player", background="green", fg="white").grid(row=2, column=0)  # display box for "player" within card frame
tkinter.Label(card_frame, textvariable=player_score_label, background="green", fg="white").grid(row=3, column=0)  # display box for dealer score within card frame
# embedded frame to hold the card images for player
player_card_frame = tkinter.Frame(card_frame, background="green")  # create another frame for the player card frame within the whole card frame
player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)  # put player card frame (using grid) inside the whole card frame

button_frame = tkinter.Frame(mainWindow)  # create frame (container) for buttons
button_frame.grid(row=3, column=0, columnspan=3, sticky='w')  # add the button frame to grid

dealer_button = tkinter.Button(button_frame, text="Dealer", command=deal_dealer)  # create button for dealer inside button frame
dealer_button.grid(row=0, column=0)  # place dealer button in grid within button frame

player_button = tkinter.Button(button_frame, text="Player", command=deal_player)  # create button for player inside button frame
player_button.grid(row=0, column=1)  # place player button in grid within button frame

restart_button = tkinter.Button(button_frame, text="Play Again!", command=new_game)  # create button for restart game inside button frame
restart_button.grid(row=0, column=2)  # place restart button in grid within button frame

shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)  # create button for shuffling card inside button frame
shuffle_button.grid(row=0, column=3)  # place shuffle button in grid within button frame

count_frame = tkinter.Frame(mainWindow)  # create frame (container) for counting wins
count_frame.grid(row=4, column=0, sticky='w', rowspan=1, columnspan=1)  # add the win count frame to grid

dealer_won_label = tkinter.IntVar()  # create class IntVar to edit a widget's integer (dealer win count)
tkinter.Label(count_frame, text="Dealer Score", background="green", fg="white").grid(row=0, column=0, sticky='ew')  # display box for "Dealer Score" within count_frame
tkinter.Label(count_frame, textvariable=dealer_won_label, background="green", fg="white").grid(row=0, column=1,
                                                                                                       sticky='ew')  # display box for dealer wins within count frame

player_won_label = tkinter.IntVar()  # create class IntVar to edit a widget's integer (player win count)
tkinter.Label(count_frame, text="Player Score", background="green", fg="white").grid(row=1, column=0, sticky='ew')  # display box for "Player Score" within count frame
tkinter.Label(count_frame, textvariable=player_won_label, background="green", fg="white").grid(row=1, column=1,
                                                                                                       sticky='ew')  # display box for player wins within count frame
reset_frame = tkinter.Frame(mainWindow)
reset_frame.grid(row=5, column=0, sticky='w')

reset_score_button = tkinter.Button(reset_frame, text="Reset Score", command=reset_score)
reset_score_button.grid(row=0, sticky='ew')

# load cards
cards = []
load_images(cards)
print(cards)
# create a new deck of cards and shuffle them
deck = list(cards)
random.shuffle(deck)

player_win_count = 0
dealer_win_count = 0
# create the list to store the dealer's and player's hands
dealer_hand = []
player_hand = []

if __name__ == "__main__":
    play()
