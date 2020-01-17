# Implementation of classic arcade game Pong by Nick Togneri

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_vel = [0,0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, speed_counter # these are vectors stored as lists
    speed_counter = 2
    ball_pos = [WIDTH/2 , HEIGHT/2]
    if direction == RIGHT:
        direction = 1
    else:
        direction = -1
    ball_vel = [direction, -random.randrange(1,8)/ 3.1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2  
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    score1 = 0
    score2 = 0
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, HEIGHT, speed_counter
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += (ball_vel[0] * (speed_counter))
    ball_pos[1] += (ball_vel[1] * (speed_counter))
        
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        ball_vel [0] = -ball_vel[0]
        speed_counter *= 1.1
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        ball_vel [0] = -ball_vel[0]
        speed_counter *= 1.1
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel [1] = -ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel [1] = -ball_vel[1]
        
    # draw paddles, update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= (HEIGHT - HALF_PAD_HEIGHT) and paddle1_pos > HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    canvas.draw_line((HALF_PAD_WIDTH-2, paddle1_pos + HALF_PAD_HEIGHT), (HALF_PAD_WIDTH-2, paddle1_pos -HALF_PAD_HEIGHT), 12, 'White')
        
    if paddle2_pos <= (HEIGHT - HALF_PAD_HEIGHT) and paddle2_pos > HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH + 2, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH + 2, paddle2_pos - HALF_PAD_HEIGHT), 12, 'WHITE')
   
    # determine whether paddle and ball collide 
    if (ball_pos[0] - (BALL_RADIUS + 2)) <= PAD_WIDTH:
        if paddle1_pos < (ball_pos[1] - HALF_PAD_HEIGHT) or paddle1_pos > (ball_pos[1] + HALF_PAD_HEIGHT):
            score2 += 1
            spawn_ball(RIGHT)
            
    elif (ball_pos[0] + (BALL_RADIUS)) >= (WIDTH - PAD_WIDTH):
        if paddle2_pos < (ball_pos[1] - HALF_PAD_HEIGHT) or paddle2_pos > (ball_pos[1] + HALF_PAD_HEIGHT):
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), (120, 70), 60, 'Red', 'monospace')
    canvas.draw_text(str(score2), (450, 70), 60, 'Red', 'monospace')
    
    # draw ball
    canvas.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 1, "White", "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel -= 5
        if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
            paddle1_pos += paddle1_vel

    if key == simplegui.KEY_MAP['S']:
        paddle1_vel += 5
        if paddle1_pos <= HALF_PAD_HEIGHT:
            paddle1_pos += paddle1_vel

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 5
        if paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
            paddle2_pos += paddle2_vel

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 5
        if paddle2_pos <= HALF_PAD_HEIGHT:
            paddle2_pos += paddle2_vel

   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['W']:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP['S']:
        paddle1_vel = 0

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def button_handler():
    new_game()
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', button_handler, 80)

# start frame
new_game()
frame.start()
