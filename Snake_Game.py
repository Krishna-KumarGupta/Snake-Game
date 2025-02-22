from tkinter import *
import random

# Game Constants
GAME_WIDTH = 1250
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 30
BODY_PARTS = 5
SNAKE_COLOR = "#2c43db"
FOOD_COLOR = "#FFFF00"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        self.food = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction

    x, y = snake.coordinates[0]

    if direction == "Up":
        y -= SPACE_SIZE
    elif direction == "Down":
        y += SPACE_SIZE
    elif direction == "Left":
        x -= SPACE_SIZE
    elif direction == "Right":
        x += SPACE_SIZE

    # Update snake body
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
    snake.squares.insert(0, square)

    # Check if food is eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")

        # Delete old food
        canvas.delete("food")

        # Create new food
        food.__init__(canvas)  # Reinitialize food
    else:
        # Remove last part of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    
    else:
    # Call next turn
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'Left' and direction != 'Right':
        direction = 'Left'
    elif new_direction == 'Right' and direction != 'Left':
        direction = 'Right'
    elif new_direction == 'Up' and direction != 'Down':
        direction = 'Up'
    elif new_direction == 'Down' and direction != 'Up':
        direction = 'Down'

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("Game Over")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("Game Over")
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game Over")
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Consolas", 70), text=f"Game Over", fill="red", tags="gameover", anchor=CENTER)

# Initialize game window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "Right"

# Score Label
label = Label(window, text="Score: 0", font=("Consolas", 40))
label.pack()

# Canvas for game area
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the window
window.update()
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{int((window.winfo_screenwidth() / 2) - (window.winfo_width() / 2))}+{int((window.winfo_screenheight() / 2) - (window.winfo_height() / 2))}")

# Key bindings
window.bind("<Left>", lambda event: change_direction('Left'))
window.bind("<Right>", lambda event: change_direction('Right'))
window.bind("<Up>", lambda event: change_direction('Up'))
window.bind("<Down>", lambda event: change_direction('Down'))

# Initialize game objects
snake = Snake(canvas)
food = Food(canvas)

next_turn(snake, food)

window.mainloop()
