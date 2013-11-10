# Implementation of classic arcade game Pong

import simpleguitk as simplegui
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
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [2,0]
paddle1_pos = HALF_PAD_HEIGHT * 2 
paddle2_pos = HALF_PAD_HEIGHT * 2
paddle1_vel = 0
paddle2_vel = 0
acc = 3 #ball acceleration
key_acc = 0 #paddle acceleration
score_left = 0
score_right = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    
    global ball_pos, ball_vel, acc, key_acc # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    acc = 1
    key_acc = 0 
    ball_vel = [2, 0]
    if direction == "RIGHT":
        ball_vel[1] += random.randrange(60,180)/60
    elif direction == "LEFT":
        ball_vel[0] += -random.randrange(120,240)/60
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score_left, score_right  # these are ints
    if score_left < score_right:
        spawn_ball("RIGHT")
    else:
        spawn_ball("LEFT")
    score_left = 0
    score_right = 0
    paddle1_vel = 0
    paddle2_vel = 0

def draw(c):
    global score_left, score_right, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel, acc
 
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_text(str(score_left), (WIDTH/4, HEIGHT/8), 42, 'white')
    c.draw_text(str(score_right), (WIDTH/1.35, HEIGHT/8), 42, 'White')
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH or ball_pos[0] >=(WIDTH - 1) - (BALL_RADIUS+PAD_WIDTH):
        ball_vel[0] = - ball_vel[0]
        
    elif ball_pos[1] <= BALL_RADIUS+PAD_WIDTH or ball_pos[1] >= (HEIGHT - 1) - (BALL_RADIUS+PAD_WIDTH):
        ball_vel[1] = - ball_vel[1]
      
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    
    if paddle1_pos >= 0 and paddle1_pos+PAD_HEIGHT <= HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos >= 0 and paddle2_pos+PAD_HEIGHT <= HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    c.draw_line([PAD_WIDTH, paddle1_pos],[PAD_WIDTH, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, 'Red')
    c.draw_line([WIDTH - PAD_WIDTH, paddle2_pos],[WIDTH - PAD_WIDTH, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, 'Red')

    # draw scores
    
     
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH and (ball_pos[1] > paddle1_pos+PAD_HEIGHT or ball_pos[1] < paddle1_pos) : 
        score_right +=1
        spawn_ball("RIGHT")
        acc = 1
        
    elif ball_pos[0] >=(WIDTH - 1) - (BALL_RADIUS+PAD_WIDTH) and (ball_pos[1] > paddle2_pos+PAD_HEIGHT or ball_pos[1] < paddle2_pos) :
        score_left +=1
        spawn_ball("LEFT")
        acc = 1
    elif ball_pos[0] <= BALL_RADIUS+PAD_WIDTH and (ball_pos[1] > paddle1_pos-HALF_PAD_HEIGHT or ball_pos[1] < paddle1_pos+HALF_PAD_HEIGHT) : 
        acc += float(acc/10)
        ball_vel[0] += acc
        
    elif ball_pos[0] >=(WIDTH - 1) - (BALL_RADIUS+PAD_WIDTH) and (ball_pos[1] > paddle2_pos-HALF_PAD_HEIGHT or ball_pos[1] < paddle2_pos+HALF_PAD_HEIGHT) :
        acc +=float(acc/10)
        ball_vel[1] += acc 
        
        
        
def keydown(key):
    global paddle1_vel, paddle2_vel,acc, key_acc,paddle1_pos,paddle2_pos
    if key == simplegui.KEY_MAP['up'] :
        if paddle2_pos+PAD_HEIGHT > HEIGHT:
            paddle2_pos-=1
        key_acc+=1
        paddle2_vel = -(paddle2_vel+key_acc)
    elif key == simplegui.KEY_MAP['down']:
        if paddle2_pos < 0:
            paddle2_pos+=1
        key_acc+=1
        paddle2_vel = -(paddle2_vel-key_acc)
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['W']:
        if paddle1_pos+PAD_HEIGHT > HEIGHT: 
            paddle1_pos-=1
        key_acc+=1
        paddle1_vel = -(paddle1_vel+key_acc)
    elif key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['S']:        
        if paddle1_pos < 0:
            paddle1_pos+=1
        key_acc+=1
        paddle1_vel =-(paddle1_vel-key_acc)
   
                                
   
def keyup(key):
    global paddle1_vel, paddle2_vel, key_acc
    paddle1_vel = 0
    paddle2_vel = 0
   # key_acc = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)



# start frame
new_game()
frame.start()
