import uuid

class Game:
    state = {
        "playerAmount" : 0,
        "playerNames" : []
    }

    playerData = {
        "players" : [

        ]
    }

    def genPlayer(self, name: str) -> bool | str:
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
        self.playerData['players'].append({
            player_uuid : {
                'playerNum' : self.state["playerAmount"],
                'displayName': name,
            }
        })
        self.state["playerAmount"] += 1 # increment the amount of players
        
        return player_uuid

    def delPlayer(self, uuid: str) -> None:
        """
        delPlayer: interface to delete players that have disconnected
        completely.
        
        :rtype: None
        """
        # first find the playername mapped to the uuid. Names are also
        # unique, but we don't want to be able to delete players by
        # using a publicly available key, for if we want 

    def getState(self) -> dict:
        return self.state