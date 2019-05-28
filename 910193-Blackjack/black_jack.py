################################################################################
# Name: Edward (Ted) Marozzi
# Student Number: 910193
# Date last modified: 21/05/2019
# Description: A simplified gui black jack game, open and read "README.txt"
#   for more the rules. This program was created for the mini project in
#   COMP10003 (Media Computation) at the University of Melbourne.
#
# Images sourced from https://opengameart.org/
################################################################################

# Graphical objects required
from graphics import Image, GraphWin, Point, Rectangle, Text, color_rgb as colour_rgb
from os import listdir
# Used to randomise card selection
import random
# Used to kill program if no interaction after 300 seconds, prevents getting
#   stuck into an unwanted infinite loop if user forgets to close program.
import time
################################################################################
# Parameters to adjust to ensure the code works on your machine.
# Please adjust these values if the program is slow or if the window is the
#   wrong size
################################################################################
def parameters():
    MOVEMENT_SPEED = 1.5  # Default = 1.5
    SCALING = 1 # Default = 1, not recommended less than 0.95 consider changing
                #    your os scaling settings.

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
    win = GraphWin("Black Jack", width, height)
    win.setBackground(colour_rgb(135, 206, 250))
    return win


# Draws a border around the deck
def draw_deck_border(deck):

    # Abritatry value to gives a nice spacing.
    deck_border = 10

    deck_width = deck.getWidth()
    deck_height = deck.getHeight()

    # Goes to middle of screen and minus' deck width minus border
    border_top_left = (Point(WIN.getWidth()/2 - deck_width/2 - deck_border,
                             WIN.getHeight()/4 - deck_height/2 - deck_border))

    border_bottom_right = (Point(WIN.getWidth()/2 + deck_width/2 + deck_border,
                                 WIN.getHeight()/4 + deck_height/2 + deck_border))

    # Draws and styles it!
    deck_border = Rectangle(border_top_left, border_bottom_right)
    deck_border.setOutline("black")
    deck_border.setWidth(5)
    deck_border.draw(WIN)


def draw_deck():
    # This is the back of the deck
    deck = Image(Point(WIN.getWidth()/2, WIN.getHeight()/4), "images/deck.png")
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


def move_card_down(player):

    border = 150
    back_of_card = Image(
        Point(WIN.getWidth()/2, WIN.getHeight()/4), "images/deck.png")
    back_of_card.draw(WIN)

    # Moves card down depeneding on who is playing
    if player == "ai":
        while back_of_card.getAnchor().getY() < WIN.getHeight() - border - 300:
            back_of_card.move(0, MOVEMENT_SPEED)
    elif player == "human":
        while back_of_card.getAnchor().getY() < WIN.getHeight() - border:
            back_of_card.move(0, MOVEMENT_SPEED)

    return back_of_card


def move_card_across(cards_in_hand, rand_card):

    border = 160
    # Moves card across using the number of cards as an interger multipier,
    #   an if statment is used to direct the card left or right depending on
    #   which half of the screen it needs to be

    if rand_card.getAnchor().getX() >= cards_in_hand * border:
        while rand_card.getAnchor().getX() > cards_in_hand * border:
            rand_card.move(-MOVEMENT_SPEED, 0)
    else:
        while rand_card.getAnchor().getX() < cards_in_hand * border:
            rand_card.move(MOVEMENT_SPEED, 0)


# Sets up the scores text to be later updated, player parameter determines who
#   which text is being initialised.
def init_scores_text(player):
    if player == "ai":
        total_text = Text(Point(WIN.getWidth()*5/6, WIN.getHeight()/10),
                          "Current value of dealer's cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("red")
        total_text.draw(WIN)
    else:
        total_text = Text(Point(WIN.getWidth()/6, WIN.getHeight()/10),
                          "Current value of your cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("green")
        total_text.draw(WIN)
    return total_text


# Draws the hold button
def draw_hold_button():
    # hold button points
    hold_a = Point(WIN.getWidth()/6 - 100, 200)
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
def init_ai_wins_text(num_ai_wins):
    ai_wins_point = Point(WIN.getWidth()*5/6, WIN.getHeight()/3 + 50)
    ai_wins_text = Text(ai_wins_point, "Dealer wins:\n" + str(num_ai_wins))

    ai_wins_text.setFace("helvetica")
    ai_wins_text.setSize(26)
    ai_wins_text.setStyle("bold")
    ai_wins_text.setTextColor("red")

    ai_wins_text.draw(WIN)


# Creates the text for the number of dealer wins
def init_player_wins_text(num_player_wins):
    player_wins_point = Point(WIN.getWidth()/6, WIN.getHeight()/3 + 50)
    player_wins_text = (Text(player_wins_point, "Player wins:\n" +
                             str(num_player_wins)))

    player_wins_text.setFace("helvetica")
    player_wins_text.setSize(26)
    player_wins_text.setStyle("bold")
    player_wins_text.setTextColor("green")

    player_wins_text.draw(WIN)


# Updates the scores after each game
def update_wins_text(player_wins_text, num_player_wins, ai_wins_text, num_ai_wins):
    ai_wins_text.setText("Dealer wins:\n" + str(num_ai_wins))
    player_wins_text.setText("Player wins:\n" + str(num_player_wins))


# Used to style some text a couple of times
def style_text(text):
    text.setFace("helvetica")
    text.setSize(30)
    text.setStyle("bold")

    return text


def game_over(winner):
    center = Point(WIN.getWidth()/2, WIN.getHeight()/2)
    if winner == "player":
        game_over_text = Text(center, "Game Over!\n\n\n\nCongratulations you won!\n\n"
                              + "Click to play again otherwise this window will terminate in 10 seconds")
        style_text(game_over_text)
        game_over_text.setTextColor("green")
        game_over_text.draw(WIN)
    elif winner == "ai":
        game_over_text = Text(center, "Game Over!\n\n\n\nYou lost!\n\n"
                              + "Click to play again otherwise this window will terminate in 10 seconds")
        style_text(game_over_text)
        game_over_text.setTextColor("red")
        game_over_text.draw(WIN)


###############################################################################
# Functions responsible for black jack game mechanics
###############################################################################

# Put all images directorys into a list
def create_card_list():
    card_images = listdir("./images/card_images")
    images_dir = "./images/card_images/"

    card_images = [images_dir + card for card in card_images]

    # Unsure if this is necessasry, but is a good safety measure
    card_images = sorted(card_images)
    return card_images


# Checks if deck was clicked on returns bool
def clicked_on_deck(click_point, deck):
    x_min = deck.getAnchor().getX() - deck.getWidth()/2
    x_max = deck.getAnchor().getX() + deck.getWidth()/2

    y_min = deck.getAnchor().getY() - deck.getHeight()/2
    y_max = deck.getAnchor().getY() + deck.getHeight()/2

    top_left = Point(x_min, y_min)
    bottom_right = Point(x_max, y_max)

    # Is a bool
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


# Updates the value of each players cards
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


# When a card is clicked this function runs, revealling and moving a card
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

# When its the players turn the function loops


def player_loop(deck, card_images):

    hold_a, hold_b = draw_hold_button()

    total_val = 0
    cards_in_hand = 0

    total_text = init_scores_text("human")

    time_last_clicked = time.time()
    time_since_clicked = None

    # Several different things break this loop such as a time out or hold button
    #   pressed
    while True:

        # Gets click
        click_point = WIN.checkMouse()

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

        # If player goes over 21 break loop, they lost
        if total_val > 21:
            center = Point(WIN.getWidth()/2, WIN.getHeight()/2)
            draw_text_box(center)
            bust_text = Text(
                center, "You went bust!\nClick anywhere to play again")
            bust_text = style_text(bust_text)
            bust_text.setTextColor("red")

            bust_text.draw(WIN)
            WIN.getMouse()
            bust_text.undraw()

            total_val = False

            return total_val

        if total_text == 21:
            return total_val

       # Checks if the deck is clicked and executes the card clicked routine
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

    # While no one has won or lost this loop runs
    while ai_val < 21 and ai_val <= player_val:
        
        back_of_card = move_card_down("ai")
        rand_card, val = reveal_card(card_images, back_of_card)

        # Use to position the cards
        cards_in_hand += 1

        move_card_across(cards_in_hand, rand_card)
        ai_val = ai_val + val

        # If an ace drawn makes player/dealer go bust the ace val is converted to 1
        ai_val = ace_correction(ai_val, val)

        total_text = update_total_val(total_text, ai_val, "ai")

        # Ai chooses to let game be a draw if equal scores over 14
        if ai_val >= 15 and ai_val == player_val:
            break



    center = Point(WIN.getWidth()/2, WIN.getHeight()/2)

    # Determins winner
    did_player_win = determine_winner(center, total_text, player_val, ai_val)

    return did_player_win

def draw_text_box(center):
    top_left = Point(center.getX()-300, center.getY()-80)
    bottom_right = Point(center.getX()+300, center.getY()+ 80)
    text_box = Rectangle(top_left,bottom_right) 
    text_box.setFill(colour_rgb(135, 206, 250))
    text_box.setOutline(colour_rgb(135, 206, 250))
    text_box.draw(WIN)



# Determines and displayes winner
def determine_winner(center, total_text, player_val, ai_val):
    draw_text_box(center)

    if ai_val > player_val and ai_val <= 21: # Loss case
        lost_text = Text(center, "You Lost\nClick anywhere to play again.")

        lost_text = style_text(lost_text)
        lost_text.setTextColor("red")
        
        lost_text.draw(WIN)
        WIN.getMouse()
        lost_text.undraw()
        total_text.undraw()

        return False
    elif player_val == ai_val: # Draw case
        draw_text = Text(center, "You drew\nClick anywhere to play again.")
        draw_text = style_text(draw_text)
        draw_text.draw(WIN)

        WIN.getMouse()
        draw_text.undraw()
        total_text.undraw()
        return
    else: # Won case
        won_text = Text(center, "You won!\nClick anywhere to play again.")
        won_text = style_text(won_text)
        won_text.setTextColor("green")
        
        won_text.draw(WIN)
        WIN.getMouse()
        won_text.undraw()
        total_text.undraw()
        return True


# Undraws everything in the graphics window
def clear(win):
    for item in win.items[:]:
        item.undraw()


# Lets users play five games per round
def best_of_five(num_player_wins, num_ai_wins):

    while num_ai_wins < 3 and num_player_wins < 3:
        card_images = create_card_list()
        deck = draw_deck()
        draw_deck_border(deck)

        draw_title()
        init_scores_text("ai")

        player_val = player_loop(deck, card_images)

        if player_val == None:
            break

        did_player_win = ai_loop(deck, card_images, player_val)

        # Updates the scores
        if did_player_win == True:
            num_player_wins += 1
        elif did_player_win == None:
            pass
        elif did_player_win == False:
            num_ai_wins += 1

        clear(WIN)

        init_player_wins_text(num_player_wins)
        init_ai_wins_text(num_ai_wins)

    if num_ai_wins > num_player_wins:
        winner = "ai"
    elif num_player_wins > num_ai_wins:
        winner = "player"

    return winner


def main():
    play_again = True
    while play_again == True:
        # Set scores to 0 - 0
        num_ai_wins = 0
        num_player_wins = 0

        # Initialise win count text to be updated as scores change
        init_player_wins_text(num_player_wins)
        init_ai_wins_text(num_ai_wins)

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

