import uuid

class Game:
    def __add__(self, second):
        return "bro I don't even know you lowkey cooked"

    state = {
        "playerAmount" : 0,
        "playerNames" : []
    }

    playerData = {
        "players" : {}
    }

    def _isPlayer(self, uuid: str) -> bool:
        return uuid in self.playerData["players"].keys()

    def genPlayer(self, name: str) -> bool | str:
        """
        genPlayer: safe interface for adding to the players in the
        state of the game
        
        :return: Returns false if it has failed, uuid of player 
        generated on succes.
        :rtype: bool | int
        """
        if name in self.state["playerNames"]:
            print(f"{name} is already mentioned!")
            return False

        self.state["playerNames"].append(name)

        
        # add entry of player id in playerstate thingie
        player_uuid = str(uuid.uuid4())
        self.playerData['players'][player_uuid] = {
            'playerNum' : self.state["playerAmount"],
            'displayName': name
        }
        self.state["playerAmount"] += 1 # increment the amount of players
        
        return player_uuid

    def delPlayer(self, uuid: str) -> bool:
        """
        delPlayer: interface to delete players that have disconnected
        completely.
        
        :rtype: None
        """
        
        # first find the playername mapped to the uuid. Names are also
        # unique, but we don't want to be able to delete players by
        # using a publicly available key, for if we want to use this
        # as an interface for deregistering or smth. Best practice idk

        if not self._isPlayer(uuid):
            return False
        name = self.playerData["players"][uuid]['displayName']
        self.playerData["players"].pop(uuid)
        self.state["playerNames"].remove(name)
        self.state["playerAmount"] -= 1
        return True

    def getState(self) -> dict:
        return self.state
