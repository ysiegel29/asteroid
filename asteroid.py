import random
import math
# import pgzrun

WIDTH = 1000  # Screen width
HEIGHT = 600  # Screen height
centre_x = WIDTH/2
centre_y = HEIGHT/2
starlocations = []

for i in range(0, 600):
    starlocations.append((random.randint(0, WIDTH), random.randint(0, HEIGHT)))

class RockClass:
    def __init__(self):
        self.size = 0
        self.quadrant_list = []
        self.quadrant = ""
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.image = 'rock'
        self.actor = Actor(self.image, self.position)

    def reset(self):
        self.size = 3 
        self.image = 'rock'
        self.quadrant_list = ["left", "right", "top", "down"]
        self.quadrant = random.choice(self.quadrant_list)
        if self.quadrant == "left":
            self.position = [-10, random.randint(0, HEIGHT)]
            self.velocity = [random.randint(20, 70)/10, random.randint(-40, 40)/10]
        elif self.quadrant == "right":
            self.position = [WIDTH + 10, random.randint(0, HEIGHT)]
            self.velocity = [random.randint(-70, -20)/10, random.randint(-40, 40)/10]
        elif self.quadrant == "top":
            self.position = [random.randint(0, WIDTH), -10]
            self.velocity = [random.randint(-70, 40)/10, random.randint(20, 70)/10]
        elif self.quadrant == "down":
            self.position = [random.randint(0, WIDTH), HEIGHT + 10]
            self.velocity = [random.randint(-40, 40)/10, random.randint(-70, -20)/10]  
        self.actor = Actor(self.image, self.position)

    def update_physics(self):
        for axis in range(0, 2):
            self.position[axis] += self.velocity[axis]
            self.actor = Actor(self.image, self.position)
        if self.position[1] < -10 or self.position[1] > HEIGHT + 10 or self.position[0] < -10 or self.position[0] > WIDTH + 10:
            self.reset()

    def rock_is_hit(self):
        self.image = 'rock_destroyed'
        self.velocity = (0, 0)
        clock.schedule(self.reset, 0.3)

class ShipClass:
    booster_power = 0.2  # Power of the ship's thrusters
    rotate_speed = 5  # How fast the ship rotates in degrees per frame
    
    def __init__(self):
        self.size = 20
        self.angle = 0  # The angle the ship is facing 0 - 360 degrees
        self.booster = False  # True if the player is firing their booster
        self.position = [0, 0]  # The x and y coordinates of the players ship
        self.velocity = [0, 0]  # The x and y velocity of the players ship
        self.acceleration = [0, 0]  # The x and y acceleration of the players ship
        self.laserCharged = True  # True if lasdr is charged
        self.laserFiring = False  # True if the player fire laser
        self.rect = Rect((self.position[0] - 20, self.position[1] - 20), (20, 20))
        self.rectlaser = Rect(self.position, (-100, -100))
        self.laserdotlist = []

    def reset(self):
        self.position = [centre_x, centre_y]  # Always start at the same spot
        self.velocity = [1, 0]  # But with some initial speed
        self.acceleration = [0, 0]  # No initial acceleration (except gravity of course)
        self.angle = random.randint(0, 360)  # And pointing in a random direction
        self.laserCharged = True
        self.laserFiring = False

    def rotate(self, direction):
        if direction == "left":
            self.angle += ShipClass.rotate_speed
        elif direction == "right":
            self.angle -= ShipClass.rotate_speed
        if self.angle > 360:  # Remember than adding or subtracting 360 degrees does not change the angle
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def booster_on(self):
        self.booster = True
        self.acceleration[0] = ShipClass.booster_power * math.sin(math.radians(self.angle + 180))
        self.acceleration[1] = ShipClass.booster_power * math.cos(math.radians(self.angle + 180))

    def booster_off(self):
        self.booster = False
        self.acceleration[0] = 0
        self.acceleration[1] = 0
    
    def laser_firing(self):
        self.laserFiring = True
        for i in range(0, 100):
            self.laserdotlist.append((self.position[0] + 10 * i * math.sin(math.radians(self.angle + 180)), self.position[1] + 10 * i * math.cos(math.radians(self.angle + 180))))
        clock.schedule(self.laserFiringEnd, 0.1)
        clock.schedule(self.laserChargingComplete, 0.7)
        self.laserCharged = False
    
    def laser_target(self):
        is_hitr = False
        is_hitr1 = False
        is_hitr2 = False
        for i in range(0, len(self.laserdotlist)):
            is_hitr += game.rock.actor.collidepoint(game.ship.laserdotlist[i])
            is_hitr1 += game.rock1.actor.collidepoint(game.ship.laserdotlist[i])
            is_hitr2 += game.rock2.actor.collidepoint(game.ship.laserdotlist[i])
        return (is_hitr, is_hitr1, is_hitr2)

    def laserChargingComplete(self):
        self.laserCharged = True  

    def laserFiringEnd(self):
        self.laserdotlist.clear()

    def update_physics(self):
        for axis in range(0, 2):
            self.velocity[axis] += self.acceleration[axis]
            self.position[axis] += self.velocity[axis]
        self.rect = Rect((self.position[0] - 22, self.position[1] - 22), (44, 44))

    def get_out_of_bounds(self):
        if self.position[1] < 0 or self.position[1] >= HEIGHT or self.position[0] <= 0 or self.position[0] >= WIDTH:
            return True
        return False

class GameClass:
    def __init__(self):
        self.time = 0  # Time spent playing in seconds
        self.score = 0  # Player's score
        self.highscore = 0
        self.game_speed = 30  # How fast the game should run in frames per second
        self.time_elapsed = 0.  # Time since the last frame was changed
        self.game_on = False  # True if the game is being played
        self.game_message = "PI   LANDER\nPRESS S TO START"  # Start of game message
        self.ship = ShipClass()  # Make a object of the ShipClass type
        self.rock = RockClass()  # Make a object of the ShipClass type
        self.rock1 = RockClass()  # Make a object of the ShipClass type
        self.rock2 = RockClass()  # Make a object of the ShipClass type
        self.reset()  # Start the game with a fresh ship
        self.gameOver = False

    def reset(self):
        self.time = 0.
        self.score = 0
        self.ship.reset()
        self.rock.reset()
        self.rock1.reset()
        self.rock2.reset()
        self.gameOver = False
   
game = GameClass()

def draw():
    screen.fill("black")
    game.rock.actor.draw()
    game.rock1.actor.draw()
    game.rock2.actor.draw()
    
    for i in range(0, len(starlocations)):
        screen.draw.line(starlocations[i], starlocations[i], "pink")
    
    if not game.game_on:
        screen.draw.text(game.game_message, center=(WIDTH/2, HEIGHT/5), align="center")

    screen.draw.text("SCORE: " + str(round(game.score)), (10, 10), color="white", background="black")
    screen.draw.text("HIGH SCORE: " + str(round(game.highscore)), (10, 25), color="white", background="black")
    
    if game.ship.laserCharged:
        screen.draw.circle(game.ship.position, game.ship.size, "yellow") 
    else:
        screen.draw.circle(game.ship.position, game.ship.size, "red")

    sin_angle = math.sin(math.radians(game.ship.angle - 45))  # Legs are drawn 45 degrees either side of the ship's angle
    cos_angle = math.cos(math.radians(game.ship.angle - 45))
    screen.draw.line(game.ship.position, (game.ship.position[0] + (sin_angle*game.ship.size*2), game.ship.position[1] + (cos_angle*game.ship.size*2)), "yellow")
    sin_angle = math.sin(math.radians(game.ship.angle + 45))
    cos_angle = math.cos(math.radians(game.ship.angle + 45))
    screen.draw.line(game.ship.position, (game.ship.position[0] + (sin_angle*game.ship.size*2), game.ship.position[1] + (cos_angle*game.ship.size*2)), "yellow")

    if game.ship.booster:
        sin_angle = math.sin(math.radians(game.ship.angle))  # Booster is drawn at the same angle as the ship, just under it
        cos_angle = math.cos(math.radians(game.ship.angle))
        screen.draw.filled_circle((game.ship.position[0] + (sin_angle*game.ship.size*2), game.ship.position[1] + (cos_angle*game.ship.size*2)), game.ship.size, "orange")

    if game.ship.laserFiring:
        for i in range(0, len(game.ship.laserdotlist)):
            screen.draw.filled_circle(game.ship.laserdotlist[i], 1, "yellow")

    if game.gameOver:
        for i in range(20, -5, -5):
            screen.draw.filled_rect(Rect((centre_x-(100+i), centre_y-(30+i)), (200+(i*2), 80+(i*2))), (200-(i*8), 0, 0))
        screen.draw.text("GAME OVER!", center=(centre_x, centre_y))
        screen.draw.text("(S to RESTART)", center=(centre_x, centre_y+20))

def update(deltatime):
    game.time_elapsed += deltatime
    if game.time_elapsed < 1/game.game_speed:
        return  # A 30th of a second has not passed yet
    game.time_elapsed -= 1/game.game_speed

    if keyboard.s and not game.game_on:
        game.game_on = True
        game.reset()
    elif not game.game_on:
        return

    if not game.gameOver:
        game.time += deltatime
        game.ship.update_physics()
        game.rock.update_physics()
        game.rock1.update_physics()
        game.rock2.update_physics()
    else:
        if keyboard.s:
            game.reset()

    if keyboard.left and not game.gameOver:  
        game.ship.rotate("left")
    elif keyboard.right and not game.gameOver:
        game.ship.rotate("right")

    if keyboard.space and not game.gameOver:  # Fire boosters 
        game.ship.booster_on()
        sounds.thruster.play(0, 300)
    else:
        game.ship.booster_off()

    if keyboard.c and game.ship.laserCharged and not game.gameOver:  # Fire laser 
        game.ship.laser_firing()
        game.ship.laserCharged = False
        sounds.laser.play(0, 300)
        if game.ship.laser_target()[0]:
            sounds.crash.play(0, 300)
            game.score = game.score + 1
            game.rock.rock_is_hit()
        elif game.ship.laser_target()[1]:
            sounds.crash.play(0, 300)
            game.score = game.score + 1
            game.rock1.rock_is_hit()
        elif game.ship.laser_target()[2]:
            sounds.crash.play(0, 300)
            game.score = game.score + 1
            game.rock2.rock_is_hit()

    collision = game.rock.actor.colliderect(game.ship.rect)
    collision += game.rock1.actor.colliderect(game.ship.rect)
    collision += game.rock2.actor.colliderect(game.ship.rect)

    if collision or game.ship.position[1] < -100 or game.ship.position[1] > HEIGHT + 100 or game.ship.position[0] < -100 or game.ship.position[0] > WIDTH + 100:
        game.gameOver = True
        if game.score > game.highscore:
            game.highscore = game.score

# pgzrun.go()
