from pygame.time import get_ticks # Import function to get the current time in milliseconds since Pygame started

class Timer:
	def __init__(self, duration, func = None, repeat = False):
		self.duration = duration # Set how long the timer should run (in milliseconds)
		self.func = func # Optional function to call when the timer finishes
		self.start_time = 0 # Stores the time when the timer started
		self.active = False # Indicates if the timer is currently active
		self.repeat = repeat # Determines if the timer should restart automatically after finishing

	def activate(self):
	# Start the timer by setting it to active and recording the current time
		self.active = True 
		self.start_time = get_ticks()

	def deactivate(self):
	# Stop the timer and reset the start time
		self.active = False
		self.start_time = 0
		if self.repeat:
		# If repeating is enabled, reactivate the timer automatically
			self.activate()

	def update(self):
		current_time = get_ticks() # Check how much time has passed since the timer was activated
		if current_time - self.start_time >= self.duration:
			# If the elapsed time is greater than or equal to the duration
			if self.func and self.start_time != 0:
			# If a function is assigned and the timer was started properly, call the function
				self.func()
			self.deactivate()  # Deactivate the timer