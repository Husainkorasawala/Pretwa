import pygame
import sys
from game import *

pygame.init()

buttonSound = pygame.mixer.Sound("buttonSound.mp3")
gameSound = pygame.mixer.Sound("gameSound.mp3")


red = pygame.image.load("red.png")
green = pygame.image.load("green.png")


def drawBeads():
    for i in range(1, 20):
        if game.boardState[i] == State.RED:
            screen.blit(red, (game.coordinates[i]))
        elif game.boardState[i] == State.GREEN:
            screen.blit(green, (game.coordinates[i]))

game = Game()
inMenu = True
inWarning = False
inInstructions = False
screen = pygame.display.set_mode((600, 650))  # Here we open the window
# We set what will be displayed on the bar
pygame.display.set_caption("Pretwa - The game")

while True:
    if inMenu:
        backgroundImage = pygame.image.load("PretwaMenu.png")
        for event in pygame.event.get():  # catches some events, you just have to distinguish that
            # e.g. each click is a separate event
            # but clicking and holding is just one more event

            if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                sys.exit(0)  # if so, it turns off the popup
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('Mouse position: {}'.format(event.pos))
                if (event.pos[0] >= 116) and (event.pos[0] <= 486) and (event.pos[1] >= 326) and (event.pos[1] <= 428):
                    buttonSound.play()
                    inMenu = False
                    game = Game()
                    backgroundImage = pygame.image.load("PretwaBoard.png")
                elif (event.pos[0] >= 116) and (event.pos[0] <= 486) and (event.pos[1] >= 464) and (event.pos[1] <= 556):
                    buttonSound.play()
                    inMenu = False
                    inInstructions = True
                    backgroundImage = pygame.image.load("PretwaInstructions.png")

    elif inWarning:
        backgroundImage = pygame.image.load("PretwaWarning.png")
        for event in pygame.event.get():  # catches some events, you just have to distinguish that
            # e.g. each click is a separate event
            # but clicking and holding is just one more event
            if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                sys.exit(0)  # if so, it turns off the popup
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('Mouse position: {}'.format(event.pos))
                if (event.pos[0] >= 341) and (event.pos[0] <= 480) and (event.pos[1] >= 332) and (event.pos[1] <= 382):
                    buttonSound.play()
                    inWarning = False
                    backgroundImage = pygame.image.load("PretwaBoard.png")
                elif (event.pos[0] >= 120) and (event.pos[0] <= 257) and (event.pos[1] >= 332) and (event.pos[1] <= 382):
                    buttonSound.play()
                    inWarning = False
                    inMenu=True

    elif inInstructions:
        backgroundImage = pygame.image.load("PretwaInstructions.png")
        for event in pygame.event.get():  # catches some events, you just have to distinguish that
            # e.g. each click is a separate event
            # but clicking and holding is just one more event
            if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                sys.exit(0)  # if so, it turns off the popup
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('Mouse position: {}'.format(event.pos))
                if (event.pos[0] >= 20) and (event.pos[0] <= 168) and (event.pos[1] >= 550) and (event.pos[1] <= 600):
                    buttonSound.play()
                    inMenu = True
                    inInstructions = False
                    backgroundImage = pygame.image.load("PretwaMenu.png")

    elif game.redWins == False and game.greenWins == False:
        for event in pygame.event.get():  # catches some events, you just have to distinguish that
            # e.g. each click is a separate event
            # but clicking and holding is just one more event
            if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                sys.exit(0)                 # if so, it turns off the popup

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                inWarning= True
                backgroundImage = pygame.image.load("PretwaWarning.png")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameSound.play()
                print('Mouse position: {}'.format(event.pos))
                objectIndex = game.isIntersection(event.pos)

                if objectIndex != None:
                    print('Position on board: {}'.format(objectIndex))
                    screen.blit(red, (game.coordinates[2]))

                    game.addToMovePositions(objectIndex)
                    print("Positions: {}".format(game.movePositions))
                    drawBeads()

 
        if game.redTurn:
            backgroundImage = pygame.image.load(
                "PretwaRedTurn.png")
        else:
            backgroundImage = pygame.image.load(
                "PretwaGreenTurn.png")
        drawBeads()
    
    else:
        if game.greenWins:
            backgroundImage = pygame.image.load(
                "PretwaGreenWins.png")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                    sys.exit(0)  # if so, it turns off the popup
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    inMenu = True
        elif game.redWins:
            backgroundImage = pygame.image.load("PretwaRedWins.png")
            for event in pygame.event.get():  # catches some events, you just have to distinguish that
                # e.g. each click is a separate event
                # but clicking and holding is just one more event
                if event.type == pygame.QUIT:  # checks to see if this event was clicking an X
                    sys.exit(0)  # if so, it turns off the popup
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_KP_ENTER:
                    inMenu = True

    pygame.display.flip()  # displays what we drew
    screen.blit(backgroundImage, [0, 0]) # draws surface on a surface meaning draws the given image on the surface form coordinates given as (0, 0)