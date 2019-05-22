###############################################################################
# Name: Edward (Ted) Marozzi
# Student Number: 910193
# Date last modified: 21/05/2019
# Description: A simplified gui black jack game, open and read "README.md"
#   for more the rules. This program was created for the mini project in
#   COMP10003 (Media Computation).
###############################################################################

# Graphical objects required
from graphics import Image, GraphWin, Point, Rectangle, Text, color_rgb
from os import listdir
# Used to randomise card selection
import random
# Used to kill program if no interaction after 300 seconds, prevents getting
#   stuck into an unwanted infinite loop
import time

###############################################################################
# Functions responsible for graphics
###############################################################################

# Creates the graphics window, which is accessed but not modified by any
#   functions
def create_window():
    width = 1920
    height = 1080
   
    # Create game window
    win = GraphWin("Black Jack", width, height)
    win.setBackground(color_rgb(135, 206, 250))
    return win

# Draws a border around the deck
def draw_deck_border(deck):

    # Abritatry value to gives a nice spacing.
    deck_border = 10


    deck_width = deck.getWidth()
    deck_height = deck.getHeight()
    
    # Goes to middle of screen and minus' deck width minus border
    border_top_left = (Point(win.getWidth()/2 - deck_width/2 - deck_border,
                             win.getHeight()/4 - deck_height/2 - deck_border))

    border_bottom_right = (Point(win.getWidth()/2 + deck_width/2 + deck_border,
                                 win.getHeight()/4 + deck_height/2 + deck_border))

    # Draws and styles it!
    deck_border = Rectangle(border_top_left, border_bottom_right)
    deck_border.setOutline("black")
    deck_border.setWidth(5)
    deck_border.draw(win)


def draw_deck():
    # This is the back of the deck
    deck = Image(Point(win.getWidth()/2, win.getHeight()/4), "deck.png")
    deck.draw(win)
    return deck


def draw_title():

    # Can change window dimentions and should still fit as we are scaling here.
    title = Text(Point(win.getWidth()/2, win.getHeight()/20),
                 "Simple Black Jack")
    title.setFace("helvetica")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor(color_rgb(255, 100,  0))
    title.draw(win)

# Uses the random.choice() method to pick a rand card from a list and 
#   draw the image
def reveal_card(card_images, back_of_card):

    # Card images is a list of the relative directorys on all 52 cards.
    rand_card_dir = random.choice(card_images)

    # Deletes the card once revealed, this simulates a real deck much better.
    card_images.remove(rand_card_dir)

    
    rand_card = Image(back_of_card.getAnchor(), rand_card_dir)

    # Replaces back of deck image with the random card picked
    back_of_card.undraw()
    rand_card.draw(win)

    val = get_card_val(rand_card_dir)

    return rand_card, val


def move_card_down(player):
    border = 150
    back_of_card = Image(
        Point(win.getWidth()/2, win.getHeight()/4), "deck.png")
    back_of_card.draw(win)

    # Moves card down depeneding on who is playing
    if player == "ai":
        while back_of_card.getAnchor().getY() < win.getHeight() - border - 300:
            back_of_card.move(0, 1)
    elif player == "human":
        while back_of_card.getAnchor().getY() < win.getHeight() - border:
            back_of_card.move(0, 1)

    return back_of_card


def move_card_across(cards_in_hand, rand_card):

    border = 160
    # Moves card across using the number of cards as an interger multipier,
    #   an if statment is used to direct the card left or right depending on 
    #   which half of the screen it needs to be
 
    if rand_card.getAnchor().getX() >= cards_in_hand * border:
        while rand_card.getAnchor().getX() > cards_in_hand * border:
            rand_card.move(-1, 0)
    else:
        while rand_card.getAnchor().getX() < cards_in_hand * border:
            rand_card.move(1, 0)

# Sets up the scores text to be later updated, player parameter determines who
#   which text is being initialised.
def init_scores_text(player):
    if player == "ai":
        total_text = Text(Point(win.getWidth()*5/6, win.getHeight()/10),
                          "Current value of dealer's cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("red")
        total_text.draw(win)
    else:
        total_text = Text(Point(win.getWidth()/6, win.getHeight()/10),
                          "Current value of your cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("green")
        total_text.draw(win)
    return total_text


def draw_hold_button():
    hold_a = Point(win.getWidth()/6 - 100, 200)

    hold_b = Point(hold_a.getX() + 200, hold_a.getY() + 100)

    hold_button = Rectangle(hold_a, hold_b)

    hold_button.setFill("green")
    hold_button.setOutline("black")
    hold_button.setWidth(5)

    center_hold_button = Point(0.5*(hold_a.getX() + hold_b.getX()),
                               0.5*(hold_a.getY() + hold_b.getY()))

    hold_text = Text(center_hold_button, "Hold")

    hold_text.setFace("helvetica")
    hold_text.setSize(26)
    hold_text.setStyle("bold")
    hold_text.setTextColor("black")

    hold_button.draw(win)
    hold_text.draw(win)

    return hold_a, hold_b


def init_ai_wins_text(num_ai_wins):
    ai_wins_point = Point(win.getWidth()*5/6, win.getHeight()/3 + 50)
    ai_wins_text = Text(ai_wins_point, "Dealer wins:\n" + str(num_ai_wins))

    ai_wins_text.setFace("helvetica")
    ai_wins_text.setSize(26)
    ai_wins_text.setStyle("bold")
    ai_wins_text.setTextColor("red")

    ai_wins_text.draw(win)


def init_player_wins_text(num_player_wins):
    player_wins_point = Point(win.getWidth()/6, win.getHeight()/3 + 50)
    player_wins_text = (Text(player_wins_point, "Player wins:\n" +
                             str(num_player_wins)))

    player_wins_text.setFace("helvetica")
    player_wins_text.setSize(26)
    player_wins_text.setStyle("bold")
    player_wins_text.setTextColor("green")

    player_wins_text.draw(win)


def update_wins_text(player_wins_text, num_player_wins, ai_wins_text, num_ai_wins):
    ai_wins_text.setText("Dealer wins:\n" + str(num_ai_wins))
    player_wins_text.setText("Player wins:\n" + str(num_player_wins))


def style_text(text):

    text.setFace("helvetica")
    text.setSize(30)
    text.setStyle("bold")

    return text


###############################################################################
# Functions responsible for black jack game mechanics
###############################################################################

# Put all images directorys into a list
def create_card_list():
    card_images = listdir("./card_images")
    images_dir = "./card_images/"

    card_images = [images_dir + card for card in card_images]
    # Unsure if this is necessasry, but is a good safety measure
    card_images = sorted(card_images)
    return card_images


def clicked_on_deck(click_point, deck):
    x_min = deck.getAnchor().getX() - deck.getWidth()/2
    x_max = deck.getAnchor().getX() + deck.getWidth()/2

    y_min = deck.getAnchor().getY() - deck.getHeight()/2
    y_max = deck.getAnchor().getY() + deck.getHeight()/2

    top_left = Point(x_min, y_min)
    bottom_right = Point(x_max, y_max)

    return is_button_clicked(click_point, top_left, bottom_right)


def is_button_clicked(click_point, point_a, point_b):

    if (click_point.getX() >= point_a.getX()
        and click_point.getX() <= point_b.getX()
        and click_point.getY() >= point_a.getY()
            and click_point.getY() <= point_b.getY()):

        return True

    return False


def get_card_val(rand_card_dir):
    for i in range(2, 11):
        if str(i) in rand_card_dir:
            rand_card_val = i

    if "ace" in rand_card_dir:
        rand_card_val = 11
    elif ("jack" in rand_card_dir or "queen" in rand_card_dir or
            "king" in rand_card_dir):
        rand_card_val = 10

    return rand_card_val


def update_total_val(total_text, total_val, player):
    if player == "ai":
        total_text.setText(
            "Current value of dealer's cards:\n" + str(total_val))
    else:
        total_text.setText("Current value of your cards:\n" + str(total_val))

    return total_text
# If drawing an ace takes the score over 21 it is defaulted to 1 instead of 11
def ace_correction(total_val, val):
    if val == 11 and total_val > 21:
        return total_val - 10
    return total_val


def card_clicked(click_point, cards_in_hand, total_text, total_val, deck, card_images):

    if click_point != None and clicked_on_deck(click_point, deck) == True:

        back_of_card = move_card_down("human")
        rand_card, val = reveal_card(card_images, back_of_card)

        cards_in_hand += 1

        move_card_across(cards_in_hand, rand_card)
        total_val = total_val + val

        total_val = ace_correction(total_val, val)

        total_text = update_total_val(total_text, total_val, "player")

    return cards_in_hand, total_val


def player_loop(deck, card_images):

    hold_a, hold_b = draw_hold_button()

    total_val = 0
    cards_in_hand = 0

    total_text = init_scores_text("human")

    time_last_clicked = time.time()
    time_since_clicked = None

    while True:
        
        # Gets click
        click_point = win.checkMouse()

        # Sets the time between clicks
        if click_point != None:
            time_since_clicked = time.time() - time_last_clicked

        # Time out after 300 seconds
        if time_since_clicked != None and time_since_clicked > 300:
            total_val = None
            return total_val
  
        # Hold button
        if (click_point != None and
            is_button_clicked(click_point, hold_a, hold_b) == True
                                                and total_val != 0):
            return total_val

        if total_val > 21:
            center = Point(win.getWidth()/2, win.getHeight()/2)
            bust_text = Text(center, "You went bust!\nClick anywhere to play again")
            bust_text = style_text(bust_text)
            bust_text.setTextColor("red")
            
            bust_text.draw(win)
            win.getMouse()
            bust_text.undraw()
            
            total_val = False
            
            return total_val

       
        cards_in_hand, total_val = (card_clicked(click_point, cards_in_hand,
                                                 total_text, total_val, deck, 
                                                                card_images))

    total_text.undraw()



def ai_loop(deck, card_images, player_val):
    ai_val = 0
    cards_in_hand = 0

    total_text = init_scores_text("ai")

    if player_val == False:
        return False

    while ai_val < 21 and ai_val <= player_val:

        back_of_card = move_card_down("ai")
        rand_card, val = reveal_card(card_images, back_of_card)

        cards_in_hand += 1

        move_card_across(cards_in_hand, rand_card)
        ai_val = ai_val + val

        ai_val = ace_correction(ai_val, val)

        if ai_val > 21 and val == 1:
            ai_val = ai_val - 10

        total_text = update_total_val(total_text, ai_val, "ai")

        if ai_val >= 15 and ai_val == player_val:
            break

    center = Point(win.getWidth()/2, win.getHeight()/2)

    did_player_win = determine_winner(center, total_text, player_val, ai_val)

    return did_player_win


def determine_winner(center, total_text, player_val, ai_val):
    if ai_val > player_val and ai_val <= 21:
        lost_text = Text(center, "You Lost\nClick anywhere to play again.")

        lost_text = style_text(lost_text)
        lost_text.setTextColor("red")

        lost_text.draw(win)
        win.getMouse()
        lost_text.undraw()
        total_text.undraw()

        return False
    elif player_val == ai_val:
        draw_text = Text(center, "You drew\nClick anywhere to play again.")
        draw_text = style_text(draw_text)

        draw_text.draw(win)
        win.getMouse()
        draw_text.undraw()
        total_text.undraw()
        return
    else:
        won_text = Text(center, "You won!\nClick anywhere to play again.")
        won_text = style_text(won_text)
        won_text.setTextColor("green")

        won_text.draw(win)
        win.getMouse()
        won_text.undraw()
        total_text.undraw()
        return True

# Undraws everything in the graphics window
def clear(win):
    for item in win.items[:]:
        item.undraw()

# Lets users play five games
def best_of_five(num_player_wins, num_ai_wins):

    while num_ai_wins + num_player_wins < 5:
        card_images = create_card_list()
        deck = draw_deck()
        draw_deck_border(deck)

        draw_title()
        init_scores_text("ai")

        player_val = player_loop(deck, card_images)

        if player_val == None:
            break

        did_player_win = ai_loop(deck, card_images, player_val)

        if did_player_win:
            num_player_wins += 1
        elif not did_player_win:
            num_ai_wins += 1

        clear(win)

        init_player_wins_text(num_player_wins)
        init_ai_wins_text(num_ai_wins)

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    # Create window, 
    win = create_window()

    # Set scores to 0 - 0
    num_ai_wins = 0
    num_player_wins = 0

    # Initialise win count text to be updated as scores change
    init_player_wins_text(num_player_wins)
    init_ai_wins_text(num_ai_wins)

    # Start the best of five game loops
    best_of_five(num_player_wins, num_ai_wins)

    # Enables users to see the final score after the 5 games are played
    for timer in range(0,1):
        time.sleep(10)