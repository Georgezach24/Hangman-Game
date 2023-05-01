import pygame
import os
import Words
import random
import Button

# BASIC SCREEN - GAME INFO
WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 80

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ASSETS LOADING
PAUSE_BUTTON = pygame.image.load(
    os.path.join("Assets", "pause.png"))
SPACE = pygame.image.load(
    os.path.join("Assets", "space.png"))
BLANK = pygame.image.load(
    os.path.join("Assets" , "letters" , "dis.png"))

PLAY_AGAIN_BUTTON = pygame.image.load(
    os.path.join("Assets" , "PLAY_AGAIN.png"))
EXIT_BUTTON = pygame.image.load(
    os.path.join("Assets" , "EXIT.png"))
NEW_GAME_BUTTON = pygame.image.load(
    os.path.join("Assets" , "NEW_GAME.png"))

YOU_LOST = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets" , "YOU_LOST_TXT.png")) , (950 , 200) )
YOU_WON = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets" , "YOU_WON.png")) , (950 , 200) )



LETTER_IMAGES = {}
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for letter in LETTERS:
    filename = f"L_{letter}.png"
    path = os.path.join("Assets", "letters", filename)
    image = pygame.image.load(path)
    LETTER_IMAGES[letter] = image


def words_picker():
    words = []
    with open(os.path.join("List", "words.txt"), "r", encoding='UTF-8') as f:
        for line in f:
            words.append(line.strip().upper())

    randomWord = random.choice(words)

    return randomWord


def drawMainScreen(wordlist, buttons, guessed):
    i = 50
    WIN.fill(BLACK)

    for letter in wordlist:
        if guessed[letter]:
            WIN.blit(LETTER_IMAGES[letter], (50 + i, HEIGHT - SPACE.get_height() *1.5))
        else:
            WIN.blit(SPACE, (50 + i, HEIGHT - SPACE.get_height()))
        i += 100

    for button in buttons:
        WIN.blit(button["image"], button["rect"])

    pygame.display.update()

def LostScreen():
    run = True
    clock = pygame.time.Clock()
    b1 = Button.Button(WIDTH//2 - PLAY_AGAIN_BUTTON.get_width() // 2 , 200 , PLAY_AGAIN_BUTTON, 1)
    b2 = Button.Button(WIDTH//2 - EXIT_BUTTON.get_width() // 2 , HEIGHT - 300, EXIT_BUTTON, 1)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        WIN.fill(BLACK)
        WIN.blit(YOU_LOST, (WIDTH//2 - YOU_LOST.get_width()//2 , 0))
        
        if b1.draw(WIN):
            MainScreen()
        
        if b2.draw(WIN):
            pygame.quit()
        
        pygame.display.update()
    
def WinScreen():
    run = True
    clock = pygame.time.Clock()
    b1 = Button.Button(WIDTH//2 - PLAY_AGAIN_BUTTON.get_width() // 2 , 200 , PLAY_AGAIN_BUTTON, 1)
    b2 = Button.Button(WIDTH//2 - EXIT_BUTTON.get_width() // 2 , HEIGHT - 300, EXIT_BUTTON, 1)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        WIN.fill(BLACK)
        WIN.blit(YOU_WON, (WIDTH//2 - YOU_WON.get_width()//2 , 0))
        
        if b1.draw(WIN):
            MainScreen()
        
        if b2.draw(WIN):
            pygame.quit()
        
        pygame.display.update()    

def RestartMenu():
    run = True
    clock = pygame.time.Clock()
    b1 = Button.Button(WIDTH//2 - NEW_GAME_BUTTON.get_width() // 2 , 200 , NEW_GAME_BUTTON, 1)
    b2 = Button.Button(WIDTH//2 - EXIT_BUTTON.get_width() // 2 , HEIGHT - 300, EXIT_BUTTON, 1)
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        WIN.fill(BLACK)
        
        if b1.draw(WIN):
            MainScreen()
        
        if b2.draw(WIN):
            pygame.quit()
        
        pygame.display.update()


def MainScreen():
    run = True
    clock = pygame.time.Clock()
    rnd_choise = words_picker()
    word = Words.Word(rnd_choise)
    w = word.word_to_letter()
    guessed = {letter: False for letter in rnd_choise}
    guess_cnt = 0
    pause = Button.Button(0, 0, PAUSE_BUTTON, 1)

    # Button settings
    button_size = SPACE.get_width()
    gap = 0
    top_left_x = WIDTH - (10 * button_size + 11 * gap)
    top_left_y = gap

    # Create buttons and add them to the list
    buttons = []
    for i, letter in enumerate(LETTERS):
        col = i % 10
        row = i // 10
        x = top_left_x + col * (button_size + gap)
        y = top_left_y + row * (button_size + gap)
        rect = pygame.Rect(x, y, button_size, button_size)
        buttons.append({"rect": rect,"image": LETTER_IMAGES[letter] , "letter": letter})
    

    drawMainScreen(w, buttons, guessed)

    while run:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    if button["rect"].collidepoint(x, y):
                        letter = button["letter"]
                        if letter in rnd_choise:
                            guessed[letter] = True
                            button["image"] = BLANK
                        else:
                            button["image"] = BLANK
                            guess_cnt += 1
                
                if guess_cnt == 7:
                    LostScreen()
        
                    pygame.display.update()
                else:
                    drawMainScreen(w, buttons, guessed)
            
        
        if pause.draw(WIN):
            RestartMenu()

        if all(guessed.values()):
            WinScreen()
            
            
        pygame.display.update()

if __name__ == "__main__":
    MainScreen()
