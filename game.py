from tkinter import *
import random
import os
import sys

# Constants
WIDTH = 800
HEIGHT = 700
GAME_SIZE = 25
SNAKE_LENGTH = 3
SNAKE_SPEED = 50
BACKGROUND_COLOR = "#000000"
FOOD_COLOR = '#ff33cc'
SNAKE_COLOR = '#00f2ff'

score = 0
direction = 'down'

# Snake spawn
class Snake:
    def __init__(self):
        self.snake_lenght = SNAKE_LENGTH
        self.coordinates = [[0, 0]] * SNAKE_LENGTH
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill = SNAKE_COLOR, tag = 'snake')
            self.squares.append(square)

# Food spawn
class Food:
    def __init__(self):
        x = random.randint(0, (WIDTH / GAME_SIZE) -1) * GAME_SIZE
        y = random.randint(0, (HEIGHT / GAME_SIZE) -1) * GAME_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill = FOOD_COLOR, tag = 'food')

# Snake movement
def snake_move(snake, food):
    for x, y in snake.coordinates:
        square = canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill=SNAKE_COLOR)
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= GAME_SIZE
    if direction == 'down':
        y += GAME_SIZE
    if direction == 'left':
        x -= GAME_SIZE
    if direction == 'right':
        x += GAME_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill = SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Adds score when snake eats food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f'Score: {score}')
        
        # Makes snake speed faster when score reaches 5 points
        if score % 5 == 0:
            global SNAKE_SPEED
            SNAKE_SPEED -= 1 

        canvas.delete('food')
        food = Food()
    
    else:
        x, y = snake.coordinates[-1]
        square = canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill=BACKGROUND_COLOR)

        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()

    window.after(SNAKE_SPEED, snake_move, snake, food) 
    # window.after() - when it will be ready for proccesing, tkinter will call function and will give arguments

# Snake control
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
        
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# End the game when snake goes out playground
def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True
    elif y < 0 or y >= HEIGHT:
        return True

    # End the game when snake eats itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

#  Clean all game process and displays an inscriptions on the screen when the game ends
def game_over():
    canvas.delete(ALL)
    game_over_text = canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                                        font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

    restart_text = canvas.create_text(canvas.winfo_width()/2, 450, font=('consolas',50), 
                                      text="Play Again", fill="green", tag="restart")
    
    quit_text = canvas.create_text(canvas.winfo_width()/2, 550, font=('consolas',50),  
                                   text="Quit", fill="green", tag="quit")

    # Making inscriptions clickable 
    canvas.tag_bind(restart_text, "<Button-1>", clicked)
    canvas.tag_bind(quit_text, "<Button-1>", close_win)

# Closing game window and starting new game
def clicked(event):
    python = sys.executable # sys.executable - is the path to the Python interpreter
    os.execl(python, python, * sys.argv) #  os.execl() - replace the running process image with the new process

# Close game window if player hit 'quit' button
def close_win(window):
    exit()

# Game Window
window = Tk()
window.title('Snake')
window.iconbitmap('D:\\Python\\images\\icon.ico')
window.resizable(False, False)

# Score Board
label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg = BACKGROUND_COLOR, width = WIDTH, height = HEIGHT)
canvas.pack()

window.update() # runs tasks currently waiting in the queue until it's entirely clear

# Placing game window at the middle of the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Snake control bind key
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

food = Food()
snake = Snake()
snake_move(snake, food)
window.mainloop()







