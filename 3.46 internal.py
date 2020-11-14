from tkinter import *
from tkinter import ttk
from random import randint


# create the GUI class
class GUI:
    # create variables
    def __init__(self):
        self.root = Tk()
        self.root.resizable(0, 0)
        self.menu = MenuScreen(self.root)
        self.root.mainloop()


# create the game's Menu screen
class MenuScreen:
    # create variables
    def __init__(self, root):
        self.root = root
        self.frame = Frame(self.root)
        self.title = ttk.Label(self.frame, text="Game")
        self.play_button = ttk.Button(self.frame, text="Play", command=self.play_button)
        self.instructions = ttk.Label(self.frame, text="use the arrow keys to move left and right, avoid the red"
                                                       " squares")
        self.pack()

    # create a function that packs everything in the menu screen
    def pack(self):
        self.title.pack()
        self.instructions.pack()
        self.play_button.pack()
        self.frame.pack()

    # unpack everything to make space for Game Screen
    def unpack(self):
        self.frame.destroy()

    # play button instruction to call on unpack function
    def play_button(self):
        self.unpack()
        GameScreen(self.root)


#  create game screen
class GameScreen:
    # create the variables
    def __init__(self, root):
        self.root = root
        self.height = 600
        self.width = 600
        self.canvas = Canvas(self.root, height=self.height, width=self.width)
        self.frame = ttk.Frame(self.root)
        self.ship = Ship(self.canvas, self.width/2)
        self.enemy = []
        self.create()
        self.quit_button = ttk.Button(self.frame, text="quit", command=exit)
        self.end_game = False
        self.pack()
        self.movement()
        self.right = None
        self.root.bind_all('<KeyPress>', lambda event: self.on_keypress(event))

    # create a function to move the ship
    def movement(self):
        if not self.end_game:
            # check if the player is at the edge of the canvas, if so then stop them
            if self.ship.get_coords()[0] <= 0 and not self.right:
                pass
            elif self.ship.get_coords()[2] >= self.width and self.right:
                pass
            # if the ship is not at the edge of the screen then continue to move the ship
            else:
                self.ship.move()
            # if the last enemy has fallen a certain distance then create another one
            if self.canvas.coords(self.enemy[-1].enemy)[1] > 125:
                self.create()
            # for every enemy in the list move them
            for baddie in self.enemy:
                baddie.move()
            # call on out(to delete the enemies), collision(to check if the game is ended) and update the canvas
            self.out()
            self.collision()
            self.canvas.after(15, self.movement)

    # make a function to change the velocity of the ship when buttons are pressed
    def on_keypress(self, event):
        # if the player presses the right arrow key move the ship to the right at vel of 7
        if event.keysym == "Right":
            self.ship.x_vel = 7
            self.right = True
        # if the player presses the left arrow key move the ship left with vel 7
        if event.keysym == "Left":
            self.ship.x_vel = -7
            self.right = False

    # create a function to check for collisions
    def collision(self):
        # check for any overlaps on the canvas
        for i in self.enemy:
            if self.ship.ship in self.canvas.find_overlapping(*i.get_coords()):
                # if there is an overlap then end the game
                self.end_game = True
                print("dead")
                self.reset()
                break

    # create a function to delete the enemies as they exit the canvas
    def out(self):
        print(self.enemy)
        # look for enemies at the boundary or are passing the boundary
        if self.canvas.coords(self.enemy[0].enemy)[3] > 700:
            # if there is then delete them from the canvas and the list
            self.canvas.delete(self.enemy[0].enemy)
            self.enemy.remove(self.enemy[0])
            print("delete enemy")

    # pack buttons and canvas and frame
    def pack(self):
        self.quit_button.pack()
        self.canvas.pack()
        self.frame.pack()

    # create a function to destroy everything upon game quit and calls on the menu screen again
    def reset(self):
        self.canvas.destroy()
        self.frame.destroy()
        MenuScreen(self.root)

    # call the create enemy function and add to the enemy list
    def create(self):
        self.enemy.append(Enemy(self.canvas))


#  create a class for the player ship
class Ship:
    # create variables
    def __init__(self, parent, x):
        self.x = x
        self.y = 500
        self.x_vel = 0
        self.canvas = parent
        self.height = 20
        self.width = 20
        self.ship = parent.create_rectangle(x, self.y, x + self.width, self.y + self.height, fill="Blue")

    # move the ship by x velocity.
    def move(self):
        # if the absolute value of the x_vel of the ship is greater than 0 then move it
        if abs(self.x_vel) > 0:
            self.canvas.move(self.ship, self.x_vel, 0)

    # return the co-ordinates of the ship
    def get_coords(self):
        return self.canvas.coords(self.ship)


# create a class for the enemies
class Enemy:
    # create variables
    def __init__(self, canvas):
        self.canvas = canvas
        self.y = 0
        self.x_vel = 0
        self.y_vel = 3
        self.x = randint(0, 550)
        self.height = 50
        self.width = 50
        self.enemy = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="Red")

    # create a movement function for the enemies
    def move(self):
        self.canvas.move(self.enemy, self.x_vel, self.y_vel)

    # create a function to get the coords of the enemy object
    def get_coords(self):
        return self.canvas.coords(self.enemy)


# running the program
run = GUI()
