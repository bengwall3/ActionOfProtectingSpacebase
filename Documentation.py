# Game Programming
# Course ID #: 543
# Username: bluecarneal
# User ID #: 38516
# Challenge Set #: 4

#NOTE: All files must be within the same folder.
'''

Idea Timeline:

Senet:
    An ancient Egyptian board game I made for a project in 3rd grade.  Didn't quite feel like programming a board game,
    though, even though there was Hedgehogs in a Hurry.  I then thought about doing Othello, but as I thought more about it, I
    guess I just thought it got too complicated.

Raindrops:
    I was trying to get an idea of what I could do from scratch, so I made this game where raindrops fell from the
    sky.  I realized that without anything more interesting, dodging raindrops would be boooooooring.

Mario!:
    If I can make raindrops fall from the sky, why not coins?  or Koopa shells?  or mushrooms?  I was able to do this!
    Anyway, I found all the sprites, figured out how to animate Mario, and then I was about to start creating scoring when Scott
    Weiss helped me realize "Oh, that's copyrighted."  There went that idea.  I'll still develop it for personal use, when I have
    the time.

Action of Protecting Spacebase:
    From Mario!, I had about 150 lines of code that I didn't really want to waste.  It worked,
    why get rid of it?  Anyways, I created a new character, background, and everything (wow designing graphics can be time con-
    suming!).  Nothing you see is copyrighted.




Action of Protecting Spacebase Timeline:

    So basically I started with the robot.  I animated him.  Then I made him a background.  After that, I created the buttons and
    menus.  Next was to make the second robot, and make sure the controls worked.  Using separate key variables is a good idea.
    Now I had to make the actual game.  I created the aliens and the power ups.  I found background music and made (one) sound
    effects.  I put it all together, and I had a decent one player game.  Now I needed to mix in the second player.  I decided
    that the best way to do this was not to copy most of the one player gameplay, but to inject "if stage == 'twoplayergame'"
    statements throughout the one player version.  I also added high scores and statistics for one player mode.


Instructions:

STORY:
    Aliens are attacking your moon base!  Fight back with your robot and laser turret while the scientists evacuate to the lunar
    orbting station.  Collect powerups to increase your ammunition, your turret's rate of fire, and to restore your energy.
    Be careful, though.  If you run out of energy, you lose.

ONE PLAYER:
    Control the robot using the arrow keys.  Shoot your robot laser with the space bar, and use the laser turret by clicking on screen.
    You win if all the scientists escape safely.  This mode supports high scores and stats.

TWO PLAYER:
    Player 1 uses the same controls as in single player, but player 2 uses WASD controls, with 'r' to shoot the the
    robot laser.  Each palyer controls the turret for 30 seconds at a time, and possession is noted onscreen.  If you die, you lose.
    if all the scientists evacuate safely, the person with the most points wins!

How it Works:
    Action of Protecting Spacebase (AoPS) runs on Python 3 and Pygame.  It has 11 classes.  Many items are animated.  The
    method I used to animate was to have an animation counter (such as self.animation), and a list of frames to be animated
    (such as self.frames).  Each time the object was updated, it would advance the self.animation counter by 1, looping
    for the number of frames in self.frames.  If I wanted to slow the animation, as I did with the robots, I added a simple
    switch that cut the animation speed in half.  Additionally, instead of having separate left and right frames, I
    made pygame flip the image if necessary, which cuts the number of frames in half.

    Gameplay is governed by what stage you are in, much like the "Hedgehogs in a Hurry" game we did in class.  Other than winning
    or losing a game, you can switch between stages by clicking buttons, which have this really nifty hovering feature.  The title
    page is animated as well.

    The cursor was created by me, and looks really cool.  Please note that on my version of pygame, the line
        cursor_data, cursor_mask = pygame.cursors.compile(cursor_strings, black='X', white='.', xor='o')
    confuses the definition of black and white.  If you can't see the cursor because you have a pygame release that has this
    fixed, please change the definition of black and white, so that it reads
        cursor_data, cursor_mask = pygame.cursors.compile(cursor_strings, black='.', white='X', xor='o')

    Since there are so many images, many of them are processed using loops, which makes for more efficient coding.
    Also, many of the sprites are stored in sprite.Groups, which makes it easier to check all of them at once.

    The function genForm() allows the program to generate a wave of enemies in a pre-created pattern, instead of having
    a continous random onslaught.

    The function processData() takes the data from the end of a game, and writes it to the data.txt file.  You can view
    the results of this if you win a game and then click the stats button.  It also records each score, so that you
    can see the high score list.  The function returns the processed information so that we can display it during the
    oneplayerend and oneplayerstats stages.

    The function play() is an attempt to take recent results and adjust the difficulty of the game accordingly.

    The main loop.  It's quite large.  450 lines.  It uses the stages I mentioned earlier, and basically runs the whole
    program.  I'll give a quick map of the stages.

    First off is mainmenu.  This is the title screen, and has three buttons.  It is also the only animated background.
    There is the instructions button, which leads to the instructions page, the one player button, and the two player button,
    which lead to their respective start pages.

    The maininstructions page is accessed from the mainmenu, and contains the instructions for AoPS (which I have included in
    this document).  This page also has a back button for navigigating back to the title screen.

    The one player and two player start pages each contain a start button, which, if clicked, starts the respective games.

    As I mentioned before, I created oneplayergame first, and then added twoplayergame onto it.  The code would be a bit longer
    if I didn't merge them this way.  Note that I store each player's key seperately.  The main loop creates waves of aliens,
    powerups, etc.  It checks for collisions and deals with them appropriately.  It updates all the sprites and the scoreboard.

    If you win (or lose), you'll be sent to oneplayerend.  If you won, you will have the leaderboard displayed, and if your
    score is on it, it will be highlighted.  If not, you'll still have your ranking displayed.  There is also a button to the
    stats page, which includes your alltime statistics.  You'll also have a chance to hit the replay button.

    If you lost, a simple message appears, but the results are still recorded.  Maybe it's an incentive to win if you aren't able
    to get to those cool-looking stats.

    If you're playing a two player game, the game ends if a robot dies, or if all the scientists are evacuated.  While this mode
    doesn't record scores to a file, it does display who won and the end scores.
    
    Most of the main loop is commented, so you have a general idea of what each part does.

If you have any questions, or errors (which is entirely possible, even after exhaustive testing), please send me (bluecarneal)
a private message on Art of Problem Solving.  If this game makes it to the finals and is "published",  I'll add a discussion thread.

'''
