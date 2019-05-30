################################################################################
#
# Name: Edward (Ted) Marozzi
# Student Number: 910193
# Date last modified: 21/05/2019
# Description: A simplified gui black jack game, open and read "README.txt"
#   for more the rules. This program was created for the mini project in
#   COMP10003 (Media Computation) at the University of Melbourne.
#
# Images sourced from https://opengameart.org/
#
################################################################################
#
# Features to be added:
#   1) Red reset button sitting opposite the hold button +1 symmetry.
#   2) A log file that automatically logs the overall number of player/dealer 
#       wins/losses.
#   3) Add classes for cards, player and dealer, this will shorten the excessive 
#       amounts of parameters passed into each function.

################################################################################
#
# Graphical objects required
from graphics import Image, GraphWin, Point, Rectangle, Text, update, color_rgb\
as colour_rgb
from os import listdir
# Used to randomise card selection
import random
# Used to kill program if no interaction after 300 seconds, prevents getting
#   stuck into an unwanted infinite loop if user forgets to close program.
import time
#
################################################################################
#
# Parameters to adjust to ensure the code works on your machine.
# Please adjust these values if the program is slow or if the window is the
#   wrong size
#
################################################################################

def parameters():
    MOVEMENT_SPEED = 1.5  # Default = 1.5
    SCALING = 1  # Default = 1, not recommended less than 0.8 or greater than 1
    # consider changing your os scaling settings.

    return MOVEMENT_SPEED, SCALING

################################################################################
# Functions responsible for graphics
################################################################################

# Creates the graphics window, which is accessed but not modified by any
#   functions
def create_window():
    width = int(1920*SCALING)
    height = int(1080*SCALING)

    # Create game window
    win = GraphWin("Black Jack", width, height, autoflush=False)
    win.setBackground(colour_rgb(135, 206, 250))
    return win


# Sets up the graphics
def set_up_graphics(num_player_wins, num_ai_wins, player_total, ai_total,
                    player_total_text, ai_total_text):
    deck = draw_deck()
    draw_deck_border(deck)
    draw_hold_button()

    update_total_val(player_total_text, player_total, "human")
    update_total_val(ai_total_text, ai_total, "ai")

    draw_title()
    player_wins_text(num_player_wins)
    ai_wins_text(num_ai_wins)

    return deck


# Undraws everything in the graphics window
def clear(WIN):
    for item in WIN.items[:]:
        item.undraw()


# Draws a border around the deck
def draw_deck_border(deck):

    # Abritatry value to gives a nice spacing.
    deck_border = 10

    deck_width = deck.getWidth()
    deck_height = deck.getHeight()

    # Goes to middle of screen and minus' deck width minus border
    border_top_left = Point(WIN.getWidth()/2 - deck_width/2 - deck_border,
                            WIN.getHeight()*5/19 - deck_height/2 - deck_border)

    border_bottom_right = Point(WIN.getWidth()/2 + deck_width/2 + deck_border,
                            WIN.getHeight()*5/19 + deck_height/2 + deck_border)

    # Draws and styles it!
    deck_border = Rectangle(border_top_left, border_bottom_right)
    deck_border.setOutline("black")
    deck_border.setWidth(5)
    deck_border.draw(WIN)


def draw_deck():
    # This is the back of the deck
    deck = Image(Point(WIN.getWidth()/2, WIN.getHeight()*5/19),
                 "images/deck.png")
    deck.draw(WIN)
    return deck


def draw_title():
    # Can change window dimentions and should still fit as we are scaling here.
    title = Text(Point(WIN.getWidth()/2, WIN.getHeight()/20),
                 "Simple Black Jack")
    title.setFace("helvetica")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor(colour_rgb(255, 100,  0))
    title.draw(WIN)


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
    rand_card.draw(WIN)

    # Reads the string on the card name to obtain the value
    val = get_card_val(rand_card_dir)

    return rand_card, val

# Moves cards down, some support for scaling.
def move_card_down():

    border = 190

    back_of_card = Image(
        Point(WIN.getWidth()/2, WIN.getHeight()/4), "images/deck.png")
    back_of_card.draw(WIN)

    # Moves card down
    while back_of_card.getAnchor().getY() < WIN.getHeight() - border:
        back_of_card.move(0, MOVEMENT_SPEED)
        update()

    return back_of_card

# Moves cards left and right, some scaling support.
def move_card_across(cards_in_hand, rand_card, player):

    border = 160
    # Moves card across using the number of cards as an interger multipier,
    #   an if statment is used to direct the card left or right depending on
    #   which half of the screen the card needs to go.
    if player == "human":
        while rand_card.getAnchor().getX() > cards_in_hand * border:
            rand_card.move(-MOVEMENT_SPEED, 0)
            update()
    elif player == "ai":
        while rand_card.getAnchor().getX() < WIN.getWidth() - \
                cards_in_hand * border:
            rand_card.move(MOVEMENT_SPEED, 0)
            update()

    update()


# Sets up the scores text to be later updated, player parameter determines who
#   which text is being initialised.
def set_value_of_cards(player):
    if player == "ai":
        total_text = Text(Point(WIN.getWidth()*9/11, WIN.getHeight()*2/12),
                          "Value of dealer's cards:\n0")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("red")
        total_text.draw(WIN)
    elif player == "human":
        total_text = Text(Point(WIN.getWidth()*2/11, WIN.getHeight()*2/12),
                          "Value of your cards:\n0")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("green")
        total_text.draw(WIN)
    return total_text


# Draws the hold button
def draw_hold_button():
    # hold button points
    hold_a = Point(WIN.getWidth()*2/11 - 100, WIN.getHeight()*3/12)
    hold_b = Point(hold_a.getX() + 200, hold_a.getY() + 100)

    hold_button = Rectangle(hold_a, hold_b)

    hold_button.setFill("green")
    hold_button.setOutline("black")
    hold_button.setWidth(5)

    # Obtains the center point of the hold button
    center_hold_button = Point(0.5*(hold_a.getX() + hold_b.getX()),
                               0.5*(hold_a.getY() + hold_b.getY()))

    # Text class
    hold_text = Text(center_hold_button, "Hold")

    # Style the text
    hold_text.setFace("helvetica")
    hold_text.setSize(26)
    hold_text.setStyle("bold")
    hold_text.setTextColor("black")

    hold_button.draw(WIN)
    hold_text.draw(WIN)

    return hold_a, hold_b


# Creates the text for the number of dealer wins
def ai_wins_text(num_ai_wins):
    ai_wins_point = Point(WIN.getWidth()*9/11, WIN.getHeight()*5/12)
    ai_wins_text = Text(ai_wins_point, "Dealer wins:\n" + str(num_ai_wins))

    ai_wins_text.setFace("helvetica")
    ai_wins_text.setSize(26)
    ai_wins_text.setStyle("bold")
    ai_wins_text.setTextColor("red")

    ai_wins_text.draw(WIN)


# Creates the text for the number of dealer wins
def player_wins_text(num_player_wins):
    player_wins_point = Point(WIN.getWidth()*2/11, WIN.getHeight()*5/12)
    player_wins_text = (Text(player_wins_point, "Player wins:\n" +
                             str(num_player_wins)))

    player_wins_text.setFace("helvetica")
    player_wins_text.setSize(26)
    player_wins_text.setStyle("bold")
    player_wins_text.setTextColor("green")

    player_wins_text.draw(WIN)


# Updates the scores after each game
def update_wins_text(player_wins_text, num_player_wins, ai_wins_text,
                         num_ai_wins):
    ai_wins_text.setText("Dealer wins:\n" + str(num_ai_wins))
    player_wins_text.setText("Player wins:\n" + str(num_player_wins))


# Used to style some text a couple of times
def style_text(text):
    text.setFace("helvetica")
    text.setSize(30)
    text.setStyle("bold")

    return text


# Game finished text
def game_over(winner):
    center = Point(WIN.getWidth()/2, WIN.getHeight()/2)
    if winner == "human":
        
        game_over_text = Text(center, "Game Over!")
        thanks_text = Text(center, " \n\n\n\n\nCongratulations you won!\n\n"
                            + "Click to play again otherwise this window will"     
                            + " terminate in 10 seconds")
        style_text(game_over_text)
        style_text(thanks_text)
        game_over_text.setSize(36)
        thanks_text.setTextColor("green")
        game_over_text.setTextColor("green")
        thanks_text.setTextColor("green")
        game_over_text.draw(WIN)
        thanks_text.draw(WIN)

    elif winner == "ai":

        game_over_text = Text(center, "Game Over!")
        thanks_text = Text(center, " \n\n\n\n\nYou lost!\n\n"
                              + "Click to play again otherwise this window"
                              +" will terminate in 10 seconds")
        style_text(game_over_text)
        game_over_text.setSize(36)
        style_text(thanks_text)
        
        thanks_text.setTextColor("red")
        game_over_text.setTextColor("red")
        thanks_text.setTextColor("red")
        game_over_text.draw(WIN)
        thanks_text.draw(WIN)



# When player goes bust
def player_bust_text(deck, num_player_wins, num_ai_wins, player_total):
    center = Point(WIN.getWidth()/2, WIN.getHeight()/2)

    bust_text = Text(
        center, "You went bust!\nClick anywhere to play again")
    bust_text = style_text(bust_text)
    bust_text.setTextColor("red")

    bust_text.draw(WIN)
    WIN.getMouse()
    bust_text.undraw()


# Updates the value of each players cards
def update_total_val(total_text, total_val, player):

    if player == "ai":
        total_text.setText(
            "Value of dealer's cards:\n" + str(total_val))
    else:
        total_text.setText("Value of your cards:\n" + str(total_val))

    return total_text


################################################################################
# Functions responsible for black jack game mechanics
################################################################################


# Put all images directorys into a list
def create_card_list():
    card_images = listdir("./images/card_images")
    images_dir = "./images/card_images/"

    card_images = [images_dir + card for card in card_images]

    # Unsure if this is necessasry, but is a good safety measure
    card_images = sorted(card_images)
    return card_images


# Checks if deck was clicked on returns bool
def is_deck_clicked_on(click_point, deck):
    x_min = deck.getAnchor().getX() - deck.getWidth()/2
    x_max = deck.getAnchor().getX() + deck.getWidth()/2

    y_min = deck.getAnchor().getY() - deck.getHeight()/2
    y_max = deck.getAnchor().getY() + deck.getHeight()/2

    top_left = Point(x_min, y_min)
    bottom_right = Point(x_max, y_max)

    # This return is a bool
    return is_button_clicked(click_point, top_left, bottom_right)


# Can be used to check if a rectangle is clicked on
def is_button_clicked(click_point, point_a, point_b):

    if (click_point.getX() >= point_a.getX()
        and click_point.getX() <= point_b.getX()
        and click_point.getY() >= point_a.getY()
            and click_point.getY() <= point_b.getY()):

        return True

    return False


# Extracts the value of the card of of the directory string
def get_card_val(rand_card_dir):

    # Cards 2 to 10 assigned.
    for i in range(2, 11):
        if str(i) in rand_card_dir:
            rand_card_val = i
    # Ace, jack, queen, king
    if "ace" in rand_card_dir:
        rand_card_val = 11
    elif ("jack" in rand_card_dir or "queen" in rand_card_dir or
            "king" in rand_card_dir):
        rand_card_val = 10

    return rand_card_val


# If drawing an ace takes the score over 21 it is defaulted to 1 instead of 11
def ace_correction(total_val, val):
    if val == 11 and total_val > 21:
        return total_val - 10
    return total_val


# When a card is clicked this function runs, revealling and moving a card
def card_clicked(click_point, cards_in_hand, total_text, total_val, deck,
                    card_images):

    if click_point != None and is_deck_clicked_on(click_point, deck) == True:

        back_of_card = move_card_down()
        rand_card, val = reveal_card(card_images, back_of_card)

        cards_in_hand += 1

        move_card_across(cards_in_hand, rand_card, "human")
        total_val = total_val + val

        total_val = ace_correction(total_val, val)

        total_text = update_total_val(total_text, total_val, "human")

    return cards_in_hand, total_val


# Determines and displayes winner
def determine_winner(center, total_text, player_total, ai_total, deck,
                     num_player_wins, num_ai_wins, player_total_text, 
                     ai_total_text):

    if ai_total > player_total and ai_total <= 21:  # Loss case
        lost_text = Text(center, "You Lost\nClick anywhere to play again.")

        lost_text = style_text(lost_text)
        lost_text.setTextColor("red")

        lost_text.draw(WIN)
        WIN.getMouse()
        lost_text.undraw()
        total_text.undraw()

        return False
    elif player_total == ai_total:  # Draw case
        draw_text = Text(center, "You drew\nClick anywhere to play again.")
        draw_text = style_text(draw_text)
        draw_text.draw(WIN)

        WIN.getMouse()
        draw_text.undraw()
        total_text.undraw()
        return
    else:  # Won case
        won_text = Text(center, "You won!\nClick anywhere to play again.")
        won_text = style_text(won_text)
        won_text.setTextColor("green")

        won_text.draw(WIN)
        WIN.getMouse()
        won_text.undraw()
        total_text.undraw()
        return True


# When its the players turn the function loops
def player_loop(deck, card_images, num_player_wins, num_ai_wins, 
                player_total_text, ai_total_text):

    hold_a, hold_b = draw_hold_button()

    player_total = 0
    cards_in_hand = 0

    # Tic is the time of the start of the timer
    tic = time.time()
    # Tock is the time between tic and when toc is defined
    toc = None
    # Several different things break this loop such as a time out or hold button
    #   pressed
    while True:

        # Gets click
        click_point = WIN.checkMouse()

        # Sets the time between clicks
        if click_point != None:
            toc = time.time() - tic

        # Time out after 300 seconds
        if toc != None and toc > 300:
            player_total = None
            return player_total

        # Hold button
        if (click_point != None and
            is_button_clicked(click_point, hold_a, hold_b) == True
                and player_total != 0):
            return player_total

        # If player goes over 21 break loop, they lost
        if player_total > 21:

            player_bust_text(deck, num_player_wins, num_ai_wins, player_total)

            player_total = False

            return player_total

        if player_total == 21:
            WIN.getMouse()
            return player_total

       # Checks if the deck is clicked and executes the card clicked routine
        cards_in_hand, player_total = card_clicked(click_point, cards_in_hand,
                                                    player_total_text, 
                                                    player_total, deck, 
                                                    card_images)
                                                    

    player_total_text.undraw()

# Run when ai is playing


def ai_loop(deck, card_images, player_total, num_player_wins, num_ai_wins, 
            player_total_text, ai_total_text):
    ai_total = 0
    cards_in_hand = 0

    if player_total == False:
        return False

    # While no one has won or lost this loop runs
    while ai_total < 21 and ai_total <= player_total:

        back_of_card = move_card_down()
        rand_card, val = reveal_card(card_images, back_of_card)

        # Use to position the cards
        cards_in_hand += 1

        move_card_across(cards_in_hand, rand_card, "ai")
        ai_total = ai_total + val

        # If an ace drawn makes player/dealer go bust the ace val is converted 
        #   to 1
        ai_total = ace_correction(ai_total, val)

        total_text = update_total_val(ai_total_text, ai_total, "ai")

        # Ai chooses to let game be a draw if equal scores over 14
        if ai_total >= 15 and ai_total == player_total:
            break

    center = Point(WIN.getWidth()/2, WIN.getHeight()/2)

    # Determines winner returns a bool
    did_player_win = determine_winner(center, total_text, player_total, 
                                        ai_total, deck, num_player_wins,
                                        num_ai_wins, player_total_text, 
                                        ai_total_text)

    return did_player_win


# Lets users play best of five rounds per game within this the other two 
#   main functions of the game are called, player_loop and ai_loop
def best_of_five(num_player_wins, num_ai_wins):

    while num_ai_wins < 3 and num_player_wins < 3:
        player_total_text = set_value_of_cards("human")
        ai_total_text = set_value_of_cards("ai")
        player_total = 0
        ai_total = 0
        deck = set_up_graphics(num_player_wins, num_ai_wins,
                               player_total, ai_total, player_total_text, 
                            ai_total_text)

        card_images = create_card_list()

        draw_title()

        deck = draw_deck()

        player_total = player_loop(deck, card_images, num_player_wins, 
                                    num_ai_wins, player_total_text, 
                                    ai_total_text)

        if player_total == None:
            break

        did_player_win = ai_loop(deck, card_images, player_total, 
                                 num_player_wins, num_ai_wins, 
                                 player_total_text, ai_total_text)

        # Updates the scores
        if did_player_win == True:
            num_player_wins += 1
        elif did_player_win == None:
            pass
        elif did_player_win == False:
            num_ai_wins += 1

        clear(WIN)

        player_wins_text(num_player_wins)
        ai_wins_text(num_ai_wins)

    if num_ai_wins > num_player_wins:
        winner = "ai"
    elif num_player_wins > num_ai_wins:
        winner = "human"

    return winner

# Controls the repition of multiple games each game containing a round.
def main():
    play_again = True
    while play_again == True:
        # Set scores to 0 - 0
        num_ai_wins = 0
        num_player_wins = 0

        # Start the best of five game loops
        winner = best_of_five(num_player_wins, num_ai_wins)

        # Draws the text depending on who won
        game_over(winner)

        # 10 second timer to restart
        tic = time.time()
        while time.time() - tic < 10:

            WIN.checkMouse()

            # Gives pc time to register click.
            time.sleep(0.5)
            if WIN.checkMouse() != None:
                play_again = True
                clear(WIN)
                break
            play_again = False


################################################################################
# Main
################################################################################
if __name__ == "__main__":
    # Parameters to be adjusted at the top of program.
    MOVEMENT_SPEED, SCALING = parameters()

    # Create window.
    WIN = create_window()
    main()
    WIN.close()
################################################################################
################################################################################
