# THE GAME IS STILL UNDER DEVELOPMENT (ITS INCOMPLETE), THE MENU IS NOT ALIGNED AS LAST MINUTE CHANGES WERE MADE AND THE 'GRAB' PART OF THE - 
# - GAME IS NOT DEVELOPED YET 
# SCORES AREN'T ASSIGNED AND WHENEVER THE BALL IS INSIDE THE GOAL, THE SCORE HAS TO BE UPDATED AND THE BALL MUST BE PLACED IN THE CENTRE AGAIN
# LOGGING IS CURRENTLY DONE IN THE TERMINAL. A SEPARATE LOG FILE WILL HAVE TO BE MADE.
# THE PICTURES ARE ALL PUT IN THE SAME FOLDER AS THE GAME FILE AND A CUSTOM FONT CAN BE ASSIGNED. MENU PAGE CONSISTS OF 2 IMAGES.
# PARDON ME FOR THE RECKLESS ASSIGNMENT OF VARIABLES, ASK IN THE COMMENTS IF FURTHER EXPLANATIONS ARE REQUIRED REGARDING THE FUNCTIONS.
# FEEL FREE TO DEVELOP THIS FURTHER IN ANY WAY. - A V -


# ------------------------------------------------------------ THE BEGINNING----------------------------------------------------------------#

import pygame, sys
import math
pygame.init()
pygame.font.init()
import pdb

# THIS IS THE LOGGER (NOT SET UP AND ASSIGNED YET)
# log_format = "%(pathname)s : %(levelname)s : %(asctime)s : %(message)s"
# logging.basicConfig(filename = "**ENTER YOUR FILE PATH**", level = logging.NOTSET, format = log_format, filemode = 'w' )
# logger = logging.getLogger()

window = pygame.display.set_mode((1050, 600))      # HERE WE SET UP THE GAME WINDOW
pygame.display.set_caption("GAME")
ball = pygame.image.load("ball.png")

def printText(text, size, color):           # USER DEFINED FUCNTION FOR PRINTING LETTERS ONTO THE WINDOW
	font = pygame.font.SysFont('brookeshappell10', size)
	text = font.render(text, True, color)
	return text

def borders():    # GAME BACkGROUND AND STUFF
	pygame.draw.line(window, (200, 200, 200), (50, 150), (50, 450), 3)                              
	pygame.draw.line(window, (200, 200, 200), (950 + 50, 150), (950 + 50, 450), 3)
	pygame.draw.line(window, (200, 200, 200), (950 + 50, 150), (1000 + 50, 150), 3)
	pygame.draw.line(window, (200, 200, 200), (0, 150), (50, 150), 3)
	pygame.draw.line(window, (200, 200, 200), (950 + 50, 450), (1000 + 50, 450), 3)
	pygame.draw.line(window, (200, 200, 200), (0, 450), (50, 450), 3)
	pygame.draw.line(window, (200, 200, 200), (500 + 25, 0), (500 + 25, 600), 3)
	pygame.draw.circle(window, (200, 200, 200), (500 + 25, 300), 30, 3)
	pygame.draw.line(window, (200, 200, 200), (50, 0), (50, 600), 1)
	pygame.draw.line(window, (200, 200, 200), (1000, 0), (1000, 600), 1)



class player(object):        # PLAYER CLASS
	def __init__(self, x, y, team, color, number):     
		self.team = team # 1 or 2
		self.color = color # RGB tuple
		self.x = x
		self.y = y
		self.radius = 30
		self.number = number # player number 1 or 2 for reach color
		self.hasBall = False
		self.grab = True
		self.shoot = False
		self.preX = -1
		self.preY = -1
		self.X = -1
		self.Y = -1	
		self.flag = False
	def draw(self):
		pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, 5)


class sphere(object):     # BALL CLASS
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.radius = 20		
		self.team = 0
		self.count = [-1, -1, -1, -1]	
		self.hit_count = [0, 0, 0, 0]
	def draw(self):
		pygame.draw.circle(window, (1, 1, 1), (self.x, self.y), self.radius, 0)
		window.blit(ball, (self.x - 20, self.y - 20))
			
def dist(x1, y1, x2, y2):      # RETURNS DISTANCE BETWEEN TWO COORDINATES ON A PLANE
	return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def angle(x1, y1, x2, y2):    # RETURNS ANGLE OF 2ND COORDINATES WITH RESPECT TO THE 1ST
	
	if x1 - x2 != 0:
		if x1 >= x2 and y1 < y2:
			return abs(math.degrees(math.atan((y1 - y2)/(x1 - x2))))
		if x1 < x2 and y1 <= y2:
			return 180 - abs(math.degrees(math.atan((y1 - y2)/(x1 - x2))))
		if x1 <= x2 and y1 > y2:
			return 180 + abs(math.degrees(math.atan((y1 - y2)/(x1 - x2))))
		if x1 > x2 and y1 >= y2:
			return 360 - abs(math.degrees(math.atan((y1 - y2)/(x1 - x2))))
	elif y1 < y2: return 90
	elif y1 > y2: return 270

initial_pos_x = [200, 200, 850, 850, 525]
initial_pos_y = [150, 450, 150, 450, 300]
owen = -1
ang = -1
save_x1, save_y1, save_x2, save_y2 = -2, -2, -2, -2
dummy = True
reds = [player(initial_pos_x[0], initial_pos_y[0], 1, (220, 10, 10), 1), player(initial_pos_x[1], initial_pos_y[1], 1, (220, 10, 10), 2)]
blues = [player(initial_pos_x[2], initial_pos_y[2], 2, (10, 110, 200), 1), player(initial_pos_x[3], initial_pos_y[3], 2, (10, 110, 200), 2)]
p = reds + blues + [sphere(initial_pos_x[4], initial_pos_y[4])] # THIS LIST CONTAINS FOUR PLAYER OBJECTS AND THE BALL OBJECT
up, down, left, right = False, False, False, False
prevx = [-1, -1, -1, -1]
prevy = [-1, -1, -1, -1]
normal_meta = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] # THIS IS SOLELY FOR LOGGING, JUST STORES SOME PARAMETER VALUES 
point_r = 0
point_b = 0
owen_stores_data = [-1]


def spaceCheck(cur, p, up, down, left, right):	 # FUCNTION TO AVOID THE OVERLAPPING OF CIRCLES (COLLISION OF PLAYERS)
		array_of_dist = [-1, -1, -1, -1]
		hit = False
		for j in range(0, 4):
			if j == cur: continue
			else:
				array_of_dist[j] = dist(p[cur].x, p[cur].y, p[j].x, p[j].y)	
				if array_of_dist[j] <= 60 and array_of_dist[j] > 0:
					hit = True
					index = j
					if normal_meta[4][j] == 0:
						print(cur, " touched : ", j)
						normal_meta[4][j] += 1

					break
				else: normal_meta[4][j] = 0

		if hit == True:
			if up == True:
				if dist(p[cur].x, p[cur].y - 10, p[index].x, p[index].y) > 60:
					p[cur].y -= 3
			elif down == True:
				if dist(p[cur].x, p[cur].y + 10, p[index].x, p[index].y) > 60:
					p[cur].y += 3
			elif left == True:
				if dist(p[cur].x - 10, p[cur].y, p[index].x, p[index].y) > 60:
					p[cur].x -= 3
			elif right == True:
				if dist(p[cur].x + 10, p[cur].y, p[index].x, p[index].y) > 60:
					p[cur].x += 3

		if hit == False:
			if up == True: p[cur].y -= 3
			if down == True: p[cur].y += 3
			if left == True: p[cur].x -= 3
			if right == True: p[cur].x += 3

	
def interact_ball(p, owen_stores_data):   # GRABBING AND SHOOTING THE BALL
	o = False
	for i in range(0, 4):
		if p[i].grab == True:
			if dist(p[i].x, p[i].y, p[4].x, p[4].y) < 50:
				p[i].hasBall = True
				p[4].x = p[i].x
				p[4].y = p[i].y
				p[i].flag = True
			# else: p[i].flag = False
		
		if p[i].shoot == True:
			if p[i].hasBall == True:			
				# print("has the ball and shoot is enabled")
				p[i].grab = False
				if normal_meta[3][i] == 0:
					print(i, " shot the ball")
					owen_stores_data[0] = i
					normal_meta[3][i] += 1

				
				# print("grab right after shooting ", p[i].grab)
				
				if p[4].count[i] < 100:
					p[4].count[i] += 1
					# print(p[4].count[i])
					
					if p[4].x + p[4].radius < 1050 and p[4].x - p[4].radius > 0 and p[4].y + p[4].radius < 600 and p[4].y - p[4].radius > 0 : 						 
						# print("entering the ball iteration conditional block")
						if p[i].preX > p[i].X:
							if p[i].preY > p[i].Y:
								p[4].x -= 4
								p[4].y -= 4								
							elif p[i].preY < p[i].Y:
								p[4].x -= 4
								p[4].y += 4
							else: p[4].x -= 4
						elif p[i].preX < p[i].X:
							if p[i].preY > p[i].Y:
								p[4].x += 4
								p[4].y -= 4
							elif p[i].preY < p[i].Y:
								p[4].x += 4
								p[4].y += 4
							else: p[4].x += 4
						elif p[i].preX == p[i].X:
							if p[i].preY > p[i].Y: p[4].y -= 4
							elif p[i].preY < p[i].Y: p[4].y += 4
							elif p[i].preY == p[i].Y: pass
						# print("ball is successfully being shot")							
					
					if dist(p[4].x, p[4].y, p[i].x, p[i].y) > 50:						
						p[i].grab = True
						p[i].flag = False
						if normal_meta[2][i] == 0:
							print("ball out of :", i)
							normal_meta[2][i] += 1
						
						# print(p[i].flag ," : is the flag after ball goes out of : ", i)
						# print("grab after going out ", p[i].grab)																			
						for m in range(0, 4):
							if dist(p[4].x, p[4].y, p[m].x, p[m].y) < 50:
								if i == m:
									continue
								else:
									p[i].shoot = False
									p[m].hasBall = True
									p[i].hasBall = False
									p[4].count[i] = 0
									print("this one has the ball : ", m)
									print(" this one lost the ball ", i)	
						# pdb.set_trace()
					else: normal_meta[2][i] = 0							
				else: o = True
			if o == True:		
				p[i].shoot = False
				p[i].grab = True
				# print("final grab of : ", i, "is :", p[i].grab)
				p[i].hasBall = False					
				p[4].count[i] = 0
				p[i].flag = False	
				# print("shoot is over , count  = ", p[4].count[i])
				o = False
		else: normal_meta[3][i] = 0

def tackle(p, dummy, save_x1, save_y1, save_x2, save_y2, ang, owen, normal_meta ,owen_stores_data):  # TACKLE BETWEEN PLAYERS AND THE BALL IS LOST
	
	con = -1

	for v in range(0, 4):
		if p[v].flag == True:
			con = v
			# owen = 1
			if normal_meta[0][v] == 0:
				print("this has the ball :", con)
				normal_meta[0][v] += 1
		else: normal_meta[0][v] = 0
	if con != -1:
		for f in range(0, 4):
			# print(p[f].flag)
			if con != f:
				# if owen == 1:
				if dist(p[f].x, p[f].y, p[con].x, p[con].y) <= 60:
					if normal_meta[1][f] == 0:
						print("this :", f, " hit :", con)
						normal_meta[1][f] += 1

					if dummy == True:
						save_x1, save_y1, save_x2, save_y2 = p[f].x, p[f].y, p[con].x, p[con].y
						dummy = False
				else: normal_meta[1][f] = 0	
				if p[con].flag == True and dummy == False:

					ang = angle(save_x1, save_y1, save_x2, save_y2)
					# print(ang)	
					
					if p[4].hit_count[con] <= 60:
						p[4].hit_count[con] += 1
						p[con].grab = False
						if p[4].x + p[4].radius < 1000 and p[4].x - p[4].radius > 0 and p[4].y + p[4].radius < 600 and p[4].y - p[4].radius > 0:
							if (ang <= 22.5 and ang > 0.0) or (ang <= 360.0 and ang > 337.5):
								p[4].x -= 2
							if ang > 22.5 and ang <= 67.5:
								p[4].x -= 2
								p[4].y += 2
							if ang > 67.5 and ang <= 112.5:
								p[4].y += 2
							if ang > 112.5 and ang <= 157.5:
								p[4].x += 2
								p[4].y += 2
							if ang > 157.5 and ang <= 202.5:
								p[4].x += 2
							if ang > 202.5 and ang <= 247.5:
								p[4].x += 2
								p[4].y -= 2
							if ang > 247.5 and ang <= 292.5:
								p[4].y -= 2
							if ang > 292.5 and ang <= 337.5:
								p[4].x -= 2
								p[4].y -= 2
							# print(p[4].hit_count[con])
						
						if dist(p[con].x, p[con].y, p[4].x, p[4].y) > 50:
							# owen = 0
							p[con].grab = True
							for m in range(0, 4):
								if dist(p[4].x, p[4].y, p[m].x, p[m].y) < 50:
									if con == m:
										continue
									else:
										p[con].flag = False
										p[4].hit_count[con] = 0
										dummy = True
										# p[m].flag = True
					else: 			
						dummy = True
						p[con].grab = True
						p[4].hit_count[con] = 0
						p[con].flag = False
						# print(" ends the move and flag ", p[con].flag, " out of the whjole tinf this one ", con)

def score(point_r, point_b, p, owen_stores_data, normal_meta):   # SCORE FUNCTION (INCOMPLETE)
	# r_score = printText(str(point_r), 20, (10, 10, 10))
	# b_score = printText(str(point_b), 20, (10, 10, 10))

	for s in range(0, 4):
		if p[s].hasBall == True:
			if p[s].shoot == True:	
					if p[4].x - 20 <= 50 and p[4].y >= 150 and p[4].y <= 450: # left RED
						if normal_meta[5][s] == 0:
							point_r += 1
							print("goal by : ", owen_stores_data[0])
							normal_meta[5][s] += 1
					if p[4].x - 20 >= 950 and p[4].y >= 150 and p[4].y <= 450: # right BLUE
						if normal_meta[5][s] == 0:
							point_b += 1
							print("goal by : ", owen_stores_data[0])
							normal_meta[5][s] += 1									
		else: normal_meta[5][s] = 0
	# r_r = point_r
	# b_b = point_b
	# font = pygame.font.SysFont('brookeshappell10', 10)
	# r_score = font.render(str(r_r), True, (10, 10, 10))
	# return r_score, b_score



def updateWindow():        # THIS IS TO UPDATE THE GAME WINDOW CONSTANTLY
	borders()
	p[0].draw()
	p[1].draw()
	p[2].draw()
	p[3].draw()
	p[4].draw()
	# window.blit(r_score, (10, 10))
	pygame.display.update()
	window.fill((10, 90, 10))
	
#-----------------------------------------------------------MENU--------------------------------------------------------------#

opening = True                                                        
ins = False
op_bg = pygame.image.load("this.jpg")
ins_bg = pygame.image.load("instructions.jpg")
click = 0
goal = False
grab = False

def updateIns():
	window.blit(ins_bg, (0,0))

	if click == 2:	
		pygame.draw.rect(window, (0, 255, 123), (660, 400, 285, 100), 4)
	if click == 1:
		pygame.draw.rect(window, (0, 255, 123), (660, 200, 285, 100), 4)
	pygame.display.update()

def updateOpening():
	window.blit(op_bg, (0,0))
	pygame.display.update()

while opening == True:
	pygame.time.Clock().tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()			
	meys = pygame.key.get_pressed()
	if meys[pygame.K_RETURN]:
		ins = True
		break
	updateOpening()

while ins == True:
	pygame.time.Clock().tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
			
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if pos[0] >= 660 and pos[0] <= 945 and pos[1] <= 300 and pos[1] >= 200: # GOAL
				goal = True
				click = 1				
			elif pos[0] >= 660 and pos[0] <= 945 and pos[1] >= 400 and pos[1] <= 500: # GRAB
				click = 2		
			else: click = 0
	if goal == True: break					
	updateIns()


#---------------------------------------------------------GAME LOOP-------------------------------------------------------------#

while True:
	
	pygame.time.Clock().tick(300)       # SETTING UP THE CLOCK RATE
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
	
	prev_x, prev_y = p[0].x, p[0].y
	keys = pygame.key.get_pressed()	
	
	for circ in p:           # LOOP FOR EXECUTING ACTIONS OF EVERY PLAYER
		if circ.team == 1:
			if circ.number == 1:    # 1ST RED PLAYER
				if keys[pygame.K_UP]: 
					if circ.y - circ.radius >= 0:
						up = True
						spaceCheck(0, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 
																
				if keys[pygame.K_DOWN]: 
					if circ.y + circ.radius <= 600:
						down = True
						spaceCheck(0, p, up, down, left, right)
					up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_LEFT]: 					
					if circ.x - circ.radius >= 50:
						left = True
						spaceCheck(0, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_RIGHT]:
					if circ.x + circ.radius <= 1000:
						right = True
						spaceCheck(0, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 

				if keys[pygame.K_SPACE]:
					if p[0].hasBall == True:
						p[0].shoot = True
						if p[4].count[0] == 0:
							p[0].X = p[0].x
							p[0].Y = p[0].y
							p[0].preX = prevx[0]
							p[0].preY = prevy[0]
														
			if circ.number == 2:          # 2ND RED PLAYER
				if keys[pygame.K_KP5]: 				
					if circ.y - circ.radius >= 0:
						up = True
						spaceCheck(1, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 
								
				if keys[pygame.K_KP2]: 
					if circ.y + circ.radius <= 600:
						down = True
						spaceCheck(1, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_KP1]: 				
					if circ.x - circ.radius >= 50:
						left = True
						spaceCheck(1, p, up, down, left, right)
					up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_KP3]:					
					if circ.x + circ.radius <= 1000:
						right = True
						spaceCheck(1, p, up, down, left, right)						
					up, down, left, right = False, False, False, False 
				
				if keys[pygame.K_SPACE]:
					if p[1].hasBall == True:
						p[1].shoot = True
						if p[4].count[1] == 0:
							p[1].X = p[1].x
							p[1].Y = p[1].y
							p[1].preX = prevx[1]
							p[1].preY = prevy[1]
		

		if circ.team == 2:	
			if circ.number == 1:        # 1ST BLUE PLAYER
				if keys[pygame.K_w]: 					
					if circ.y - circ.radius >= 0:
						up = True
						spaceCheck(2, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
								
				if keys[pygame.K_s]: 						
					if circ.y + circ.radius <= 600:
						down = True
						spaceCheck(2, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_a]: 						
					if circ.x - circ.radius >= 50:
						left = True
						spaceCheck(2, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_d]:						
					if circ.x + circ.radius <= 1000:
						right = True
						spaceCheck(2, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
				
				if keys[pygame.K_SPACE]:
					if p[2].hasBall == True:
						p[2].shoot = True
						if p[4].count[2] == 0:
							p[2].X = p[2].x
							p[2].Y = p[2].y
							p[2].preX = prevx[2]
							p[2].preY = prevy[2]
			
			if circ.number == 2:        # 2ND BLUE PLAYER
				if keys[pygame.K_u]: 						
					if circ.y - circ.radius >= 0:
						
						up = True
						spaceCheck(3, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 

								
				if keys[pygame.K_j]: 						
					if circ.y + circ.radius <= 600:

						down = True
						spaceCheck(3, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_h]: 						
					if circ.x - circ.radius >= 50:
						left = True
						spaceCheck(3, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
						
				if keys[pygame.K_k]:						
					if circ.x + circ.radius <= 1000:
						right = True
						spaceCheck(3, p, up, down, left, right)						
				up, down, left, right = False, False, False, False 
				
				if keys[pygame.K_SPACE]:
					if p[3].hasBall == True:
						p[3].shoot = True
						if p[4].count[3] == 0:
							p[3].X = p[3].x
							p[3].Y = p[3].y
							p[3].preX = prevx[3]
							p[3].preY = prevy[3]
			
	interact_ball(p, owen_stores_data)
	tackle(p, dummy, save_x1, save_y1, save_x2, save_y2, ang, owen, normal_meta, owen_stores_data)
	score(point_r, point_b, p, owen_stores_data, normal_meta)
	for i in range(0, 4):      # THIS IS TO ASSIGN CURRENT CYCLE'S PARAMETER VALUES TO VARIBALES FOR USE IN FUNCTIONS IN SUBSEQUENT CYCLES
		prevx[i], prevy[i] = p[i].x, p[i].y
	
	updateWindow()


	



	
	