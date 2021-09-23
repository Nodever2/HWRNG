'''
Created on Sep 18, 2021
Updated on Sep 22, 2021
@author: Nodever2
'''

#NEW UPDATE! YOU CAN CHANGE THESE CONFIG VALUES TO MAKE THE ALGORITHM WORK DIFFERENTLY!
#They all default at -1 meaning the program will automatically determine what they should be.
ConfigMaxPlayersPerGame = 6#Default: 6. Will change to default if not set to an int between 1 and 6 (inclusive).
#todo: cleanup code (ADD FUCNTIONS, REMOVE REPEATED CODE), comments etc. maybe redo variable names? add isInstanceOf or whatever it is for config values.
#and add optional alternate algorhthm for RNGing what team players are on that has an equal chance of all open slots
#also make it so that the names of maps/leaders print with spaces instead of underscores if possible?

import random
import math
from enum import Enum

class HWLeader(Enum):#Enum with all possible leaders in Halo Wars
    INVALID = 0#except this
    The_United_Rebel_Front = 1
    The_Flood_Gravemind = 2
    Sesa_Refumee = 3
    The_Grunt_Rebellion = 4
    Captain_Cutter = 5
    Sergeant_Forge = 6
    Professor_Anders = 7
    Arbiter = 8
    Tartarus = 9
    Prophet_Of_Regret = 10
    
class HWMap(Enum):#Enum with all possible maps in Halo Wars
    INVALID = 0#except this
    BLOOD_GULTCH = 1#1v1
    CHASMS = 2
    PIRTH_OUTSKIRTS = 3
    RELEASE = 4
    TUNDRA = 5
    BARRENS = 6
    BLOOD_RIVER = 7
    BEASLEYS_PLATEAU = 8#2v2
    CREVICE = 9
    THE_DOCKS = 10
    LABYRINTH = 11
    REPOSITORY = 12
    TERMINAL_MORAINE = 13
    MEMORIAL_BASIN = 14
    EXILE = 15#3v3
    FORT_DEEN = 16
    FROZEN_VALLEY = 17
    GLACIAL_RAVINE = 18

pcInput = input("How many players? ")
try:
    playerCount = int(pcInput)
except ValueError:
    print("Unexpected input. Terminating.")
    print()
    input("Press enter to close...")
    exit()
if (playerCount <= 0):
    print("Unexpected input. Terminating.")
    print()
    input("Press enter to close...")
    exit()
remainingUnallocatedHumans = playerCount
maxPlayers = 6
if (ConfigMaxPlayersPerGame >= 1 and ConfigMaxPlayersPerGame <= 6):
    maxPlayers = ConfigMaxPlayersPerGame
else:
    print("Config Warning: Max Players Per Game is outside the allowed range. Using " + str(maxPlayers) + " instead.")
numGamesLeft = int(math.ceil(playerCount/maxPlayers))

iteration = 0
lastGamesHighestPlayerNum = 0
while (remainingUnallocatedHumans > 0):                    #this code supports more than 6 players; it will divide the players evenly between 2 different games if so
    iteration = iteration + 1                                            
    print("===========================")
    print("GAME " + str(iteration) + ": ")
    humansThisGame = -1
    if (remainingUnallocatedHumans > maxPlayers):
        humansThisGame = int(math.ceil(remainingUnallocatedHumans/numGamesLeft))     #amount of players in each game (todoL figure this out before the loop I think)
    else:
        humansThisGame = remainingUnallocatedHumans
    remainingUnallocatedHumans -= humansThisGame
    
    teamSize = -1;                                        #figure out team size (1v1, 2v2, or 3v3)
    if (humansThisGame <= 2):
        teamSize = random.randint(1,3)
    elif (humansThisGame <= 4):
        teamSize = random.randint(2,3)
    else:
        teamSize = 3
    
    print("  This game will be a " + str(teamSize) + "v" + str(teamSize))
    
    mapThisGame = HWMap(0)                                  #randomize map
    if (teamSize == 1):
        mapThisGame = HWMap(random.randint(1,18))
    elif (teamSize == 2):
        mapThisGame = HWMap(random.randint(8,18))
    else:#3v3
        mapThisGame = HWMap(random.randint(15,18))
    print("  MAP: " + str(mapThisGame.name))
    
    rows, cols = (teamSize*2, 2)                                    #initialize the player array according to team size (and thus # of players in game)
    arr = [[0 for i in range(cols)] for j in range(rows)]#array, where index = player number, 1st value = [(player ID) if human, 0 if AI], 2nd value = leader ID [1-10] (note that AIS can never have 1 here)
    for i in range(humansThisGame):                        #assign each player a slot in array. First slots of each team prioritized.
        desiredSlot = random.randint(0,1)*teamSize
        while (arr[desiredSlot][0] != 0):
            desiredSlot = desiredSlot + 1
            if (desiredSlot >= rows):
                desiredSlot = 0
        arr[desiredSlot][0] = (i+1)#player # = (i+1)
    
    for i in range(rows):#RNG each player's leader
        if (arr[i][0] != 0):#if slot is not AI
            arr[i][1] = HWLeader(random.randint(1,10))
        else:
            arr[i][1] = HWLeader(random.randint(2,10))
    
    
    
    print("  TEAM ALPHA:")
    for i in range((int)(rows/2)):#team 1
        if (arr[i][0] != 0):
            if (arr[i][0]+lastGamesHighestPlayerNum < 10):
                print("    Player   " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
            elif(arr[i][0]+lastGamesHighestPlayerNum < 100):
                print("    Player  " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
            else:
                print("    Player " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
        else:
            print("    AI        " + ": " + str(arr[i][1].name))
        
    print("  TEAM BRAVO:")
    for j in range((int)(rows/2)):#team 2
        i = j + (int)(rows/2)
        if (arr[i][0] != 0):
            if (arr[i][0]+lastGamesHighestPlayerNum < 10):
                print("    Player   " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
            elif(arr[i][0]+lastGamesHighestPlayerNum < 100):
                print("    Player  " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
            else:
                print("    Player " + str(arr[i][0]+lastGamesHighestPlayerNum) + ": " + str(arr[i][1].name))
        else:
            print("    AI        " + ": " + str(arr[i][1].name))
    
    numGamesLeft = numGamesLeft - 1
    lastGamesHighestPlayerNum = lastGamesHighestPlayerNum + humansThisGame
    
    
    




print()
input("Press enter to close...")