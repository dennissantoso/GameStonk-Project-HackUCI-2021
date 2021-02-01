import pygame
import random
from math import ceil

# Game constants
width = 800
height = 600

# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GameSTONK TO THE MOON Simulator")

# Loading images
icon = pygame.image.load('gamestonk.png')
pygame.display.set_icon(icon)
screen.fill((255,255,255))

#
runInstance = True
run_menu = True
run_game = False
click = False
# Initializing some variables

# Determining general trend of stonks
stonks_go_up = True
chance_of_crashing = 1200
each_frame_increase = 4

# Stock price
stock_price = 10
stocks_owned = 0
cash = 1000

# Slow down increase
stock_inc_counter = 0

# Setting up font
myfont = pygame.font.SysFont("monospace", 50)
gameStopFont = pygame.font.SysFont("Impact", 50)

#Loading images
gameBG = pygame.image.load('gameBG.png')
gameBGPositionX = 0
gameBGPositionY = 0

gameOver = pygame.image.load('gameOver.png')
gameOverPositionX = 0
gameOverPositionY = 0

wsbImg = pygame.image.load('wallstreetbets.png')
wsbPositionX = -50
wsbPositionY = 250

tylerImg = pygame.image.load('tyler.png')
tylerPositionX = wsbPositionX
tylerPositionY = wsbPositionY   

start_buttonX = 312
start_buttonY = 315

buttonWidth = 200
buttonHeight = 75

start_button = pygame.transform.scale(pygame.image.load('start.png'), (buttonWidth, buttonHeight))

exit_button = pygame.transform.scale(pygame.image.load('exit.png'), (buttonWidth,buttonHeight))

exit_buttonX = 312
exit_buttonY = 425

menu = pygame.image.load('main_menu.png')
menuPositionX = 0
menuPositionY = 0

restart_button = pygame.image.load('restart.png')
restartX = 312
restartY = 315


# music player
pygame.mixer.music.load('CoffinDance.mp3')
pygame.mixer.music.play(-1)

explosion = False
# For hitmarker sound
hitloaded = False

# For color of text
increasing = True

# Random quote
listOfQuotes = ["HOLD THE LINE",
    "GME TO THE MOON", "DIAMOND HANDS", "IF U/DFV HOLDS I HOLD", "I LIKE THIS STOCK", "IF HE'S IN IM IN!"]

selectedQuote = random.choice(listOfQuotes)

# Sounds
hit_channel = 0
hit_sound = pygame.mixer.Sound('hitmarker.ogg')

# Resetting game
def reset_game():
    pass

#Defining images
def menuImages():
    screen.blit(menu, (menuPositionX, menuPositionY))
    screen.blit(start_button, (start_buttonX, start_buttonY))
    screen.blit(exit_button, (exit_buttonX, exit_buttonY))
def gameImages():
    screen.blit(gameBG, (gameBGPositionX, gameBGPositionY))
    screen.blit(wsbImg, (wsbPositionX, wsbPositionY))

def gameOverScreen():
    global cash, explosion, stocks_owned
    screen.blit(gameOver, (gameOverPositionX, gameOverPositionY))

    

    stock_color = (0, 255, 0) if cash >= 1000 else (255, 0, 0)
    shareCounter = myfont.render(f'SHARES: {stocks_owned:.2f}', 1, stock_color)
    moneyCounter = myfont.render(f'BUYING POWER: {cash:.2f}', 1, stock_color)
    share_rect = shareCounter.get_rect(center=((width / 2), (250)))
    money_rect = moneyCounter.get_rect(center=((width / 2), (height / 2)))
    screen.blit(shareCounter, share_rect)
    screen.blit(moneyCounter, money_rect)
    if not explosion:
        explosion = True
        pygame.mixer.music.load('explosion.mp3')
        pygame.mixer.music.play()
            

    
# For stock graph
stock_history = []
time = 0



# Graph boundaries
graph_x = 310
graph_y = 300
# Maybe if time passes 800, then win
graph_width = 490
graph_height = 300

def scale_price(highest, current):
    global graph_y, graph_height
    return int(graph_y + (graph_height - ((current / highest) * graph_height)))

def scale_time(highest, current):
    global graph_x, graph_width
    return round(graph_x + ((current / highest) * graph_width))

def drawGraph():
    global screen, stock_history, graph_height, time
    step = ceil(len(stock_history) / 400)
    for i in range(0, len(stock_history) - step, step):
        # Draw line between this point and the next point
        stock_color = (0, 255, 0) if increasing else (255, 0, 0)
        high = max(stock_history, key=lambda x: x[1])[1]
        if high < 100:
            high = 100
        high_x = time
        if high_x < 800:
            high_x = 800
        x = scale_time(high_x, stock_history[i][0])
        x_2 = scale_time(high_x, stock_history[i + step][0])
        price = scale_price(high, stock_history[i][1])
        price2 = scale_price(high, stock_history[i + step][1])
        pygame.draw.line(screen, stock_color, (x, price), (x_2, price2), 3)

    

playing_tyler = False

def play_tyler():
    global playing_tyler, hitloaded
    if not playing_tyler:
        playing_tyler = True
        pygame.mixer.music.load('tyler1 scream.mp3')
        hitloaded = False
        pygame.mixer.music.play(start = 4.5, loops=0)

def buy_stock():
    global cash, stocks_owned, stock_price
    if cash >= stock_price:
        cash -= stock_price
        stocks_owned += 1

def sell_stock():
    global cash, stocks_owned, stock_price
    if stocks_owned >= 1:
        cash += stock_price
        stocks_owned -= 1

gameMusicPlaying = False
def gameMusic():
    global gameMusicPlaying
    if not gameMusicPlaying:
        gameMusicPlaying = True
        pygame.mixer.music.load('gameMusic.mp3')
        pygame.mixer.music.play(-1, start = 48)

def game():
    # Calculating stock price
    global stock_price, stonks_go_up, stock_inc_counter, screen, increasing, time, stock_history, selectedQuote

    gameMusic()

    stock_history.append((time, stock_price))
    time += 1

    # Every half a second
    if random.randint(1,300) == 1:
        stonks_go_up = False
    
    # Calling my diamond hand wsb
    gameImages()

    if stonks_go_up:
        if stock_inc_counter == 10:
            temp = stock_price
            stock_price += each_frame_increase + random.randint(-800, 800)/100
            if stock_price > temp:
                increasing = True
            else:
                increasing = False
            stock_inc_counter = 0
        stock_inc_counter += 1
    if stonks_go_up == False:
        increasing = False
        stock_price -= random.randint(1,20) 
        if not playing_tyler:
            play_tyler()
        screen.blit(tylerImg, (tylerPositionX, tylerPositionY))

    

    drawGraph()
    
    
    if stock_price <= 0:
        stock_price = 0
        # Show game over screen here
        gameOverScreen()
        pygame.display.update()

    #Graphics

    # Display text
    # stock_price <= 0 means Game Over
    if stock_price > 0:
        stock_color = (0, 255, 0) if increasing else (255, 0, 0)
        label = myfont.render(f'GME PRICE: {stock_price:.2f}', 1, stock_color)
        screen.blit(label, (0, 50))
        
        quotes = myfont.render(f'{selectedQuote}', 1, (0,255,0))
        quotes_rect = quotes.get_rect(center=((width / 2), (25)))
        screen.blit(quotes, quotes_rect)
            
        stockCounter = myfont.render(f'SHARES: {stocks_owned}', 1, (255,255,255))
        screen.blit(stockCounter, (0,100))
        
        moneyCounter = myfont.render(f'BUYING POWER: {cash:.2f}', 1, (255,255,255))
        screen.blit(moneyCounter, (0,150))

    pygame.display.update()

#Main menu
def menu_run():
    global click, runInstance, run_game, run_menu, mx, my, start_button, exit_button, buttonWidth, buttonHeight, hit_channel
    
    # Check main menu displaying
    menuImages()
    
    start = pygame.Rect(start_buttonX, start_buttonY, buttonWidth, buttonHeight)
    exitb = pygame.Rect(exit_buttonX, exit_buttonY, buttonWidth, buttonHeight)

    pygame.display.update()

    if start.collidepoint ((mx, my)):
        if click:
            run_game = True
            run_menu = False
            pygame.mixer.music.fadeout(1500)

    if exitb.collidepoint ((mx, my)):
        if click:
            pygame.mixer.Channel(hit_channel).play(pygame.mixer.Sound('hitmarker.ogg'))
            pygame.mixer.Channel(hit_channel).stop()
            runInstance = False
            
while runInstance:
    # 20 Frames per second (1000ms / 50ms == 20)
    pygame.time.delay(50)

    # Handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runInstance = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
        if event.type == pygame.MOUSEBUTTONUP:
            click = False

    # Getting mouse position
    mx, my = pygame.mouse.get_pos()
    
    # Handling key presses
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        # Buying stonks
        pygame.mixer.Channel(hit_channel).play(hit_sound)
        # if not hitloaded and not playing_tyler:
        #     pygame.mixer.Channel(hit_channel).load('hitmarker.mp3')
        #     hitloaded = True
        # if not playing_tyler:
        #     pygame.mixer.Channel(hit_channel).play(0)
        buy_stock()
    if keys[pygame.K_DOWN]:
        # Selling stonks
        pygame.mixer.Channel(hit_channel).play(hit_sound)
        # if not hitloaded and not playing_tyler:
        #     pygame.mixer.Channel(hit_channel).play(pygame.mixer.Sound('hitmarker.mp3'))
        #     hitloaded = True
        # if not playing_tyler:
        #     pygame.mixer.Channel(hit_channel).play(0)
        sell_stock()

    # Deciding to run menu or game    
    if run_menu:
        menu_run()
    elif run_game:
        game()

pygame.quit()
