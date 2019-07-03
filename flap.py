# Oscar Saharoy 2018

import pygame, random, sys, os
from pygame import freetype

pygame.init()

info = pygame.display.Info()

x_res = info.current_h // 2  # Width of display
y_res = info.current_h // 2  # Height of display

SP    = info.current_h // 50 # measurement unit - about 30 pixels on 1440p monitor but scales to others

frmrt = 16 # delay between frames in ms

# Palette
white = (255, 255, 255)
black = (  0,   0,   0)
brick = (160,  50,  40)

class Flappy(object):

	def __init__(self):

		self.surface = pygame.display.set_mode((x_res,y_res)) # initialise window for drawing

		# Set title and favicon
		icon = pygame.image.load(r'assets/flappy.png')
		pygame.display.set_icon(icon)

		pygame.display.set_caption(' Flap.py')

		self.build()


	def build(self):

		# clear screen
		self.surface.fill(white) 

		# initialise game variables
		self.birdvel = 0
		self.bars    = []
		self.tick    = 0
		self.score   = 0
		self.limit   = False

		# Create 'bird' rectangle
		self.bird    = pygame.Rect(SP*3,SP*3,SP*2,SP*2)

		# Initialising fonts
		self.bigfont = pygame.freetype.SysFont('Verdana', x_res//2, bold=True)
		self.smlfont = pygame.freetype.SysFont('Verdana', SP, bold=True)

		self.makebar()

		while True:

			# test for exit request
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# if self.step raises an exception, call self.restart and continue with self.step on the next loop around
			try:
				self.step()
			except:
				self.restart()

	def step(self):

		# Increment self.tick each cycle
		self.tick    += 1

		# Increase bird's downward velocity to simulate gravity
		self.birdvel += SP/60

		# Set bird's velocity to simulate a jump if space is pressed
		if pygame.key.get_pressed()[pygame.K_SPACE]:
			self.birdvel = -SP/3

		# Move the bird by self.birdvel
		self.bird.move_ip(0,self.birdvel)

		# clear screen
		self.surface.fill(white) 

		# draw bird and score within it
		pygame.draw.rect(self.surface, black, self.bird)
		pygame.draw.rect(self.surface, brick, self.bird.inflate(-SP/2,-SP/2))
		self.smlfont.render_to(self.surface,self.bird.inflate(-SP/1.6,-SP/1.6),str(self.score),fgcolor=white)

		# Move each bar along the screen; speed increases as self.tick increases
		for bar in self.bars:
			bar.move_ip(-6-self.tick//100,0)

			# Draw bar
			pygame.draw.rect(self.surface, black, bar)
			pygame.draw.rect(self.surface, brick, bar.inflate(-SP/2,-SP/2))

		# update screen
		pygame.display.flip()

		# Position of first and last bars
		first = self.bars[0].left
		last  = self.bars[-1].left

		# If the last bar is halfway along the screen, create a new one
		if last < x_res/3:
			self.makebar()

		# If the first bar is in line with the bird, increment self.score
		if first < self.bird.left and not self.limit:
			self.score += 1

			# Prevents this block from executing more than once per bar
			self.limit  = True

		
		# If the first bar is off the screen, delete it
		if first < -SP*4:
			self.bars  = self.bars[2:]

			# Reset self.limit to allow score to increase again
			self.limit = False
		

		# True if the bird touches a bar
		collision = (self.bird.collidelist(self.bars) != -1) 

		# If the bird goes off the screen, restart
		if self.bird.bottom > y_res or self.bird.top < 0:
			raise Exception()

		# If the bird hits a bar, restart
		elif collision:
			raise Exception()

		# Otherwise call short delay before next step
		else:
			pygame.time.wait(frmrt)


	def makebar(self):

		# Select random height for opening on bar
		r1 = random.uniform(SP*4,y_res-SP*14)
		r2 = r1 + SP*10 - self.tick/10

		thickness = SP*4

		c1 = [x_res, -10, thickness, r1+10      ]
		c2 = [x_res, r2,  thickness, y_res-r2+10]

		# Create bars
		self.bars += [pygame.Rect(*c1), pygame.Rect(*c2)]

	def restart(self):

		# Flashes red background and score up on screen
		self.surface.fill(brick)
		self.bigfont.render_to(self.surface,(SP*4,SP*8),str(self.score),fgcolor=white)
		self.smlfont.render_to(self.surface,(SP*14,y_res-SP*2),'Space to jump',fgcolor=white)

		# refresh screen
		pygame.display.flip() 

		# Start game again after delay
		pygame.time.wait(200)
		self.build()

Flappy()
