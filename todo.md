Rank Action then pick best action (instead of all scores -> Random best

---
Clue stall should be seen as stall. 
Add a way to look at previous player state and that it impacts clue reading (DDA/stall)

---
Handle Strikes
handle playerTimes (ignore)
---
Tests
    ClueFinder
        find_stall_clues
---
~~Create a GameLogger that output all visible action to a json like object~~
~~At the end of the game -> Save to file (player name + game id?)~~
Add a boolean to game (forced_action) default False, when False, you replace the action with the forced_action 
(Has to be sent)
Create  a Game Builder service that take the json as input and build the game up to the turn N. Then unlock the brain.
It will allow testing in all ways. 
---