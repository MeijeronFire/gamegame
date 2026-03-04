from game.uber import Game
from pprint import pprint
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
		pprint(self.uber.state)
	
	def do_printplayerdata(self, arg):
		"""
		usage: printstate
		
		prints current state of game
		"""
		pprint(self.uber.playerData)

	def do_kick(self, uuid: str):
		"""
		usage: kick <uuid>

		kicks a player by a UUID
		"""
		name = self.uber.playerData["players"][uuid]["displayName"]
		print(f"kicking {name}")
		if self.uber.delPlayer(uuid):
			print("succes")
		else:
			print('failure')
