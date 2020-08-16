# Welcome to my Simple Black Jack game!

Just navigate to the source folder
(910193-Blackjack) and run black_jack.py!

<img src="https://github.com/ted-marozzi/black-jack/blob/master/preview/preview.png?raw=true" alt="Preview" width="600">

Be sure to adjust the MOVEMENT_SPEED and SCALING parameters in the top of
the source code to configure the game to your machine.

The game is designed to be played in a best of five format/first
to three format. The goal is to get beat the dealer. In order to 
do this you must obtain a score higher than the dealers score, 
while staying below or equal to 21.

Rules:
1) To begin click on the deck to draw a card,
   (be careful not to double click, this will draw two cards) 
   your total card value is displayed in the upper left corner.
	
2) You must now decide to either click the hold button or to draw again.

3) If you draw again and your total score is over 21 you automatically
   lose that round, unless the last card you drew was an ace, if you
   draw an ace that makes you bust, then aces value is defaulted to 1.
	
4) Once you are happy with your score press the hold button and the 
   dealer will begin to play. If the dealer obtains a the same score as you,
   you draw. If the dealer goes over 21 you win. If the gets better than 
   your score but less than or equal to 21 you loss.

5) Once five games are played the window will automatically close it self.
	
6) Good Luck and have fun!

Card Values:
ace = 11 or 1 (If 11 makes you go bust, then the value is defaulted to 1).
two to ten = face value of the card.
jack, queen, king = 10
