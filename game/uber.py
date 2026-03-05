from .game import Game
from random import randint

"""
Woop woop game layer
"""

class Uber(Game):
    # not neccesary for the code, but good for reiterating the layout
    def __init__(self):
        self.state = {
            "playerAmount" : 0,
            "playerNames" : [],
            "playerState" : {
                # to be filled like 'player': ml, ...
            },
            "glasses" : [0, 0, 0, 0, 0, 0],
            "optout": 300
        }
    def _onRegister(self):
        # add most recently added playername 
        self.state['playerNames'][-1]
        self.state["playerState"][self.state['playerNames'][-1]]

    def throw(self) -> int:
        return randint(0, 5) # like throwing a 0-indexed die
    
    def fill(self, glassNr: int, amount: int):
        self.state['glasses'][glassNr] = amount
    
    def drink(self, playerName: str, glassNr: int):
        self.state['playerState'][playerName] += self.state['glasses'][glassNr]
    
    def optOut(self, playerName):
        self.state['playerState'][playerName] += self.state['optout']