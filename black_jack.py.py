from graphics import Image, GraphWin, Point, Rectangle, Text, color_rgb
from os import listdir
import random
import time

###############################################################################
# Functions responsible for graphics
###############################################################################

def create_window():
    width = 1920
    height = 1080
    # Create game window
    win = GraphWin("Black Jack", width, height)
    win.setBackground(color_rgb(135,206,250))
    return (win, width, height)

def draw_deck_border(deck):
    # Put all images directorys into a list
    deck_box_border = 10

    deck_width = deck.getWidth()
    deck_height = deck.getHeight()
    border_top_left = Point(width/2 - deck_width/2 - deck_box_border,\
        height/4 - deck_height/2 - deck_box_border)

    border_bottom_right = Point(width/2 + deck_width/2 + deck_box_border,\
        height/4 + deck_height/2 + deck_box_border)
    
    deck_border = Rectangle(border_top_left, border_bottom_right)
    deck_border.setOutline("black")
    deck_border.setWidth(5)
    deck_border.draw(win)

def draw_deck(width, height):

    deck = Image(Point(width/2, height/4), "deck.png")
    deck.draw(win)
    return deck

def draw_title(width, height, win):
    title = Text(Point(width/2, height/20), "Simplified Black Jack")
    title.setFace("helvetica")
    title.setSize(36)
    title.setStyle("bold")
    title.setTextColor("black")
    title.draw(win)

    read_me = Text(Point(width/2, height/12), "{Read 'README.md' for rules}")
    read_me.setFace("helvetica")
    read_me.setSize(15)
    read_me.setTextColor("black")
    read_me.draw(win)


def reveal_card(card_images, back_of_card):
    rand_card_dir = random.choice(card_images)
    #need to delete card from list
    card_images.remove(rand_card_dir)
    rand_card = Image(back_of_card.getAnchor(), rand_card_dir)

    back_of_card.undraw()
    rand_card.draw(win)

    val = get_card_val(rand_card_dir)

    return (rand_card, val)

def move_card_down(height, player):
    border = 150
    back_of_card = Image(Point(width/2, height/4), "deck.png")
    back_of_card.draw(win)

    # Moves card down to the border

    if player == "ai":
        while back_of_card.getAnchor().getY() < height - border - 300:
            back_of_card.move(0, 1)
    else:
        while back_of_card.getAnchor().getY() < height - border:
            back_of_card.move(0, 1)

    return back_of_card


def move_card_across(cards_in_hand, rand_card):

    border = 160

    if rand_card.getAnchor().getX() >= cards_in_hand * border:
        while rand_card.getAnchor().getX() > cards_in_hand * border:
            rand_card.move(-1,0)
    else:
        while rand_card.getAnchor().getX() < cards_in_hand * border:
            rand_card.move(1,0)

def init_scores_text(player):
    if player == "ai":
        total_text = Text(Point(width*5/6, height/10), "Current value of dealer's cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("black")
        total_text.draw(win)
    else:
        total_text = Text(Point(width/6, height/10), "Current value of your cards:\n")
        total_text.setFace("helvetica")
        total_text.setSize(30)
        total_text.setStyle("bold")
        total_text.setTextColor("black")
        total_text.draw(win)
    return total_text

###############################################################################
# Functions responsible for black jack game mechanics
###############################################################################

# Put all images directorys into a list
def create_card_list():
    card_images = listdir("./card_images")
    images_dir = "./card_images/"
    card_images = [images_dir + card for card in card_images]
    card_images = sorted(card_images)
    return card_images

def clicked_on_deck(deck, click_point):
    x_min = deck.getAnchor().getX() - deck.getWidth()/2
    x_max = deck.getAnchor().getX() + deck.getWidth()/2

    y_min = deck.getAnchor().getY() - deck.getHeight()/2
    y_max = deck.getAnchor().getY() + deck.getHeight()/2

    if (click_point.getX() >= x_min and
        click_point.getX() <= x_max and
        click_point.getY() >= y_min and
        click_point.getY() <= y_max):
        return True
    
    return False

def get_card_val(rand_card_dir):
    for i in range(2, 11):
        if str(i) in rand_card_dir:
            rand_card_val = i
    
    if "ace" in rand_card_dir:
        rand_card_val = 11
    elif "jack" in rand_card_dir or "queen" in rand_card_dir or "king" in rand_card_dir:
        rand_card_val = 10

    return rand_card_val


def update_total_val(total_text, total_val, player):
    if player == "ai":
        total_text.setText("Current value of dealer's cards:\n" + str(total_val))
    else:     
        total_text.setText("Current value of your cards:\n" + str(total_val))
    
    return total_text



def is_button_clicked(click_point, point_a, point_b):

    if (click_point.getX() >= point_a.getX()
        and click_point.getX() <= point_b.getX()
        and click_point.getY() >= point_a.getY()
        and click_point.getY() <= point_b.getY()):

        return True

    return False

def card_clicked(click_point, cards_in_hand, total_text, total_val, deck, card_images, width, height):
    
    if click_point != None and clicked_on_deck(deck, click_point) == True:
    
        back_of_card = move_card_down(height, "human")
        rand_card, val = reveal_card(card_images, back_of_card)
        
        cards_in_hand += 1
        
        move_card_across(cards_in_hand, rand_card)
        total_val = total_val + val
        if total_val > 21 and val == 11:
            
            total_val = total_val - 10
        
        total_text = update_total_val(total_text, total_val, "player")

    return cards_in_hand, total_val


def draw_hold_button(width, height):
    hold_a = Point(width/6 - 100, 200)

    hold_b = Point(hold_a.getX() + 200, hold_a.getY() + 100)

    hold_button = Rectangle(hold_a, hold_b)

    hold_button.setFill("green")
    hold_button.setOutline("black")
    hold_button.setWidth(5)

    center_hold_button = Point(0.5*(hold_a.getX() + hold_b.getX()),\
        0.5*(hold_a.getY() + hold_b.getY()) )

    hold_text = Text(center_hold_button, "Hold")


    hold_text.setFace("helvetica")
    hold_text.setSize(26)
    hold_text.setStyle("bold")
    hold_text.setTextColor("black")
    

    hold_button.draw(win)
    hold_text.draw(win)

    return hold_a, hold_b
    
def player_loop(deck, card_images, width, height):

    hold_a, hold_b = draw_hold_button(width, height)

    total_val = 0
    cards_in_hand = 0

    total_text = init_scores_text("human")

    time_since_click = time.time()

    while True:
        
        # time out value
        if time.time() - time_since_click > 300:
            total_val = None
            return total_val

        # Gets click
        click_point = win.checkMouse()

        # Hold button
        if click_point != None\
            and is_button_clicked(click_point, hold_a, hold_b) == True\
            and total_val != 0:
            return total_val
        
        # Reset timer
        if click_point != None:
            time_since_click = time.time()

        
        if total_val > 21:
            center = Point(width/2, height/2)
            bust_text = Text(center, "You went bust!\nClick anywhere to play again")
            bust_text = style_text(bust_text)
            bust_text.setTextColor("red")
            
            bust_text.draw(win)
            win.getMouse()
            bust_text.undraw()
            
            total_val = False
            
            return total_val
 
        cards_in_hand, total_val = card_clicked(click_point, cards_in_hand,\
            total_text, total_val, deck, card_images, width, height)

    total_text.undraw()
    

def ai_loop(deck, card_images, width, height, player_val):
    ai_val = 0
    cards_in_hand = 0

    total_text = init_scores_text("ai")

    if player_val == False:
        return False

    while ai_val < 21 and ai_val <= player_val:
        
        back_of_card = move_card_down(height, "ai")
        rand_card, val = reveal_card(card_images, back_of_card)
        
        cards_in_hand += 1
        
        move_card_across(cards_in_hand, rand_card)
        ai_val = ai_val + val

        if ai_val > 21 and val == 1:
            ai_val = ai_val - 10

        
        total_text = update_total_val(total_text, ai_val, "ai")


        

        if ai_val >= 15 and ai_val == player_val:
            break
         


    center = Point(width/2, height/2)

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



def clear(win):
    for item in win.items[:]:
        item.undraw()
    
   

def init_ai_wins_text(num_ai_wins):
    ai_wins_point = Point(width*5/6, height/3 + 50)
    ai_wins_text = Text(ai_wins_point, "Dealer wins:\n" + str(num_ai_wins))

    ai_wins_text.setFace("helvetica")
    ai_wins_text.setSize(26)
    ai_wins_text.setStyle("bold")
    ai_wins_text.setTextColor("red")

    ai_wins_text.draw(win)

def init_player_wins_text(num_player_wins):
    player_wins_point = Point(width/6, height/3 + 50)
    player_wins_text = Text(player_wins_point, "Player wins:\n" + str(num_player_wins))

    player_wins_text.setFace("helvetica")
    player_wins_text.setSize(26)
    player_wins_text.setStyle("bold")
    player_wins_text.setTextColor("green")

    player_wins_text.draw(win)


def update_wins_text(player_wins_text, num_player_wins, ai_wins_text, num_ai_wins):
    ai_wins_text.setText("Dealer wins:\n" + str(num_ai_wins))
    player_wins_text.setText("Player wins:\n"+ str(num_player_wins))


def style_text(text):

    text.setFace("helvetica")
    text.setSize(30)
    text.setStyle("bold")

    return text

def best_of_five(num_player_wins, num_ai_wins):

    while num_ai_wins + num_player_wins < 5:    
        card_images = create_card_list()
        deck = draw_deck(width, height)
        draw_deck_border(deck)

        draw_title(width, height, win)
        init_scores_text("ai")

        player_val = player_loop(deck, card_images, width, height)

        if player_val ==  None:
            break

        did_player_win = ai_loop(deck, card_images, width, height, player_val)

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
    
# Create window
win, width, height = create_window()
# Set scores to 0 - 0
num_ai_wins = 0
num_player_wins = 0

# Initialise win count text to be updated as scores change
init_player_wins_text(num_player_wins)
init_ai_wins_text(num_ai_wins)

# Start the best of five game loops
best_of_five(num_player_wins, num_ai_wins)

# Enables users to see the final score after the 5 games are played
win.getMouse()

