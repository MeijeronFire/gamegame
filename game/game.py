import uuid

class Game:
    state = {
        "playerAmount" : 0,
        "playerNames" : [],
        "players" : [
        
        ]
    }
    def genPlayer(self, name: str) -> bool | int:
        """
        genPlayer: safe interface for adding to the players in the
        state of the game
        
        :return: Returns false if it has failed, uuid of player generated on succes.
        :rtype: bool | int
        """
        if name in self.state["playerNames"]:
            print(f"{name} is already mentioned!")
            return False

        self.state["playerNames"].append(name)

        player_uuid = str(uuid.uuid4())
        self.state['players'].append({
            'playerNum' : self.state["playerAmount"],
            'displayName': name,
            'uuid' : player_uuid
        })
        self.state["playerAmount"] += 1 # increment the amount of players
        
        return player_uuid