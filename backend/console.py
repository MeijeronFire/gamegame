from game.uber import Game
import cmd

class Console(cmd.Cmd):
	intro = "Lorem Ipsum Dolor Sit Amet"
	prompt = "[anker] - "
	def __init__(self, game: Game):
		#
		#
		#  THIS IS AN UGLY HACK
		#
		#
		super(Console, self).__init__()
		self.uber = game
		#
		#
		# THIS IS AN UGLY HACK
		#
		#

	def do_hello(self, arg):
		"""
		usage: hello <name>

		name: person to greet
		"""
		print(f"Hello {arg}")
	
	def do_printstate(self, arg):
		"""
		usage: printstate
		
		prints current state of game
		"""
		print(f"{self.uber.state}")
	
	def do_printplayerdata(self, arg):
		"""
		usage: printstate
		
		prints current state of game
		"""
		print(f"{self.uber.playerData}")
