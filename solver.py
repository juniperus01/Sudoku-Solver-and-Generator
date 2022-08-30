import pygame
# Default Sudoku Board.
from generator import *
pygame.init()

# Total window
screen = pygame.display.set_mode((500, 600)) # (width,height)
# Title
pygame.display.set_caption("SUDOKU")

x = 0
y = 0
dif = 500 / 9
val = 0
d = {}

# Load test fonts for future use
# This will always return a valid Font object, and will fallback on the builtin pygame
#font if the given font is not found.

font1 = pygame.font.SysFont("palatinolinotypebolditalicttf", 30)
font2 = pygame.font.SysFont("ptmonottc", 25)
font3 = pygame.font.SysFont("ptmonottc", 15)
font5 = pygame.font.SysFont("palatinolinotypebolditalicttf", 35)
font6 = pygame.font.SysFont("palatinolinotypebolditalicttf", 25)

background = pygame.image.load("bg8.jpeg")
background = pygame.transform.scale(background, (500, 600))
bg = pygame.image.load("bg9.jpeg")
bg = pygame.transform.scale(bg, (500, 600))

# creates an object to help track time
clock = pygame.time.Clock()


def createGen(t):
    global genModQ
    solve_sudoku()
    remove_nos(t)
    genModQ = {}
    for i in range(9):
        for j in range(9):
            genModQ[(i, j)] = [matrix[i][j], matrix[i][j]]

# to find location of the first empty cell in the matrix
def find_empty():
    for i in range(9):
        for j in range(9):
            if genModQ[(i, j)][1] == 0:
                return i, j # row, col
    return False

def get_cord(px, py):
    global x, y
    x = int(px // dif)
    y = int(py // dif)

# Highlight the cell selected
def draw_box():
    pygame.draw.rect(screen, (255, 0, 0), (x * dif, y * dif, dif, dif), 6)

def draw():
# Draw the lines
    for i in range(9):
        for j in range(9):
            if genModQ[(j, i)][1] != 0:
                # Fill blue color in already numbered grid
                if genModQ[(j, i)][0] == 0:
                    pygame.draw.rect(screen, (40, 137, 210), (i * dif, j * dif, dif + 1, dif + 1))
                else:
                    pygame.draw.rect(screen, (8, 34, 125), (i * dif, j * dif, dif + 1, dif + 1))

                # Fill gird with default numbers specified
                # This creates a new Surface with the specified text rendered on it.
                text1 = font1.render(str(genModQ[(j, i)][1]), 1, (254, 190, 16))
                # (text,antialias,colour)
                # antialias (boolean) if true, the characters will have smooth edges
                screen.blit(text1, (i * dif + 15, j * dif + 15))
                # screen is the canvas name, text1 is the surface
            if d[(j, i)] != [] and type(d[(j, i)]) != tuple:
                 notes(j, i, d[(j, i)])
        for i in range(10):
            if i % 3 == 0:
                thick = 7
            else:
                thick = 1
            pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
            pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)

# creating dictionary for notes
def create_notesdict(genModQ):

    global d
    d = {}
    for i in range(0, 9):
        for j in range(0, 9):
            if genModQ[(i, j)][0] != 0:
                d[(i, j)] = ()
            else:
                d[(i, j)] = []

def notes(y, x, v):

    numsize = 500 // 27
    cellsize = 500 // 9
    for i in v:
        num_x, num_y = 0, 0
        num_x = (i - 1) % 3  # 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
        if i <= 3:
            num_y = 0
        elif i > 6:
            num_y = 2
        else:
            num_y = 1
        exact_x = ((x) * cellsize + num_x * numsize) + 7
        exact_y = ((y) * cellsize + num_y * numsize) + 4
        te = font3.render(str(i), 1, (0, 0, 0))
        screen.blit(te, (exact_x, exact_y))

# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid key", 1, (255, 0, 0))
    screen.blit(text1, (5, 558))

# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[(it, i)][1] == val:
            return False
        if m[(j, it)][1] == val:
            return False
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[(j, i)][1] == val:
                return False
        return True

# Display instruction for the game
def instruction():
    text1 = font3.render("NUMBER PRESSED AFTER ENTER KEY WILL BE DISPLAYED", 1, (0, 0, 0))
    text2 = font3.render("YOU CAN MAKE NOTES TOO", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))

    screen.blit(text2, (20, 540))

run = True
flag1 = 0 # draws box
flag2 = 0 # to solve/check val given
rs = 0 # result
error = 0
raiseerror = 0
frame_count = 0
frame_rate = 60
start_time = 90
front = 1 # to display front end
new = False
# The loop that keeps the window running
while run:
    screen.fill((227, 227, 82))
    # front page block
    if front == 1:
        screen.blit(background, (0, 0))
        text2 = font5.render("PLAY GAME: ", 1, (0, 0, 0))
        screen.blit(text2, (152, 205))
        text3 = font2.render("EASY" , 1, (0, 0, 0))
        screen.blit(text3, (210, 260))
        text4 = font2.render("MEDIUM", 1, (0, 0, 0))
        screen.blit(text4, (210, 295))
        text5 = font2.render("HARD", 1, (0, 0, 0))
        screen.blit(text5, (210, 330))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

        if x > 207 and x < 275 and y >= 260 and y < 290:
            createGen('a')  # creating easy soduku question
            create_notesdict(genModQ)
            front = 0
            continue

        elif x < 207 and x > 303 and y >= 295 and y < 330:
            createGen('b') # creating medium level soduku question
            create_notesdict(genModQ)
            front = 0
            continue

        elif x > 207 and x < 270 and y >= 330 and y < 365:
            createGen('c')# creating hard soduku question
            create_notesdict(genModQ)
            front = 0
            continue

        # if your answer is correct, exit page

        elif rs == 1:
            screen.blit(bg, (0, 0))
            text1 = font5.render( "CORRECT ANS!!", 1, (0, 0, 0))
            screen.blit(text1, (119, 75))
            output_string = "Time: {0: 02}:{1: 02}".format(minutes, seconds)
            text2 = font3.render(output_string, True, (0, 0, 0))
            screen.blit(text2, (192, 225))
            text3 = font6.render( 'play again', True, (0, 0, 0))
            screen.blit(text3, (192, 411))
            text4 = font6.render( 'quit', True, (0, 0, 0))
            screen.blit(text4, (224, 457))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

            if x > 192 and x < 313 and y > 421 and y < 436:
                new = True
                front = 1
                rs = 0
                continue
            elif x > 223 and x < 271 and y > 469 and y < 482:
                run = False
                continue

        # when the game starts :
        else:
            if new:
                frame_count = 0
                total_seconds = 0
                new = False
            screen.fill((255, 255, 255))
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Quit the game window
                if event.type == pygame.QUIT:
                    run = False
                # Get the mouse position to insert number
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag1 = 1
                    x, y = event.pos  # gives the x,y coordinate; unpacking
                    get_cord(x, y)
                # Get the number to be inserted if key pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if x <= 0:
                            x = 0
                    else:
                        x -= 1
                    flag1 = 1
                if event.key == pygame.K_RIGHT:
                    if x >= 8:
                        x = 8
                    else:
                        x += 1
                    flag1 = 1
                if event.key == pygame.K_UP:
                    if y <= 0:
                        y = 0
                    else:
                        y -= 1
                    flag1 = 1
                if event.key == pygame.K_DOWN:
                    if y >= 8:
                        y = 8
                    else:
                        y += 1
                    flag1 = 1
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9
                if event.key == pygame.K_RETURN:
                    flag2 = 1
        if y > 8:
            continue
        if genModQ[(y, x)][0] != 0:
            continue
        if val != 0 and flag2 == 0:
            if val not in d[(y, x)] and type(d[(y, x)]) != tuple:
                d[(y, x)] = d[(y, x)] + [val]
            elif val in d[(y, x)] and type(d[(y, x)]) != tuple:
                l = d[(y, x)]
                l.remove(val)
                d[(y, x)] = l

        elif val != 0 and flag2 == 1:  # if val is not 0 and we pressed enter

            if valid(genModQ, int(x), int(y), val) == True:
                genModQ[(int(y), int(x))][1] = val
                d[(y, x)] = ()
                flag1 = 0
                flag2 = 0
                raiseerror = 0
            else:
                genModQ[(int(y), int(x))][1] = 0
                flag2 = 0
                raise_error2()
                raiseerror = 1
            if not find_empty():
                rs = 1
        if error == 1:
            raise_error1()
        if raiseerror == 1:
            raise_error2()
        draw()
        if flag1 == 1:
            draw_box()
        instruction()
        total_seconds = frame_count // frame_rate
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
        # Use python string formatting to format in leading zeros
        output_string = "Time: {0: 02}:{1: 02}".format(minutes, seconds)
        text = font3.render(output_string, True, (0, 0, 0))
        screen.blit(text, (363, 569))
        frame_count += 1
        # Limit frames per second
        # just sets up how fast game should run or how often while loop should update
        #itself, run through itself.
        clock.tick(frame_rate)
        # timer output
        # Go ahead and update the screen with what we&#39;ve drawn.
        # It allows only a portion of the screen to updated, instead of the entire area
        pygame.display.flip()
        val = 0
        # Update window
        pygame.display.update()
        # Quit pygame window
        pygame.quit()