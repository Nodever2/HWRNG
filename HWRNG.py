'''
Created on Sep 18, 2021
Updated on Sep 26, 2021
@author: Nodever2
'''

'''##########################################
############ Beginning of config ############
##########################################'''
ConfigMaxHumansPerGame = 6#Default: 6. Will change to default if not set to an int between 1 and 6 (inclusive).
#If ConfigForceHumanAlliance is set to 1, this needs to be an int between 1 and 3 (inclusive). It will be forced to 3 if too high.
ConfigAlternateHumanTeamAssignmentAlgorithm = 0#if this is set to 1, players will be assigned to teams differently:
#BY DEFAULT, players have a 50/50 chance of being assigned to each team.
#WITH THIS VARIABLE SET TO 1, players will have an equal chance of being placed in each open slot.
#This would mean that the algorithm would be more biased towards having teams with roughly equal amount of humans on each team.
#This option does nothing if ConfigForceHumanAlliance is set to 1 or -1.
ConfigForceHumanAlliance = 0#Default: 0. If set to 1, this option will force the generator to place all humans on a team against AIs.
#WARNING: THIS FORCES ConfigMaxHumansPerGame TO BE BETWEEN 1-3!!!!!
#Bonus: You can also set this to -1 to force humans to be on opposing teams (team 1 will have majority of odd # of players per team).
'''##########################################
############### End of config ###############
##########################################'''

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
    Blood_Gultch = 1#1v1
    Chasms = 2
    Pirth_Outskirts = 3
    Release = 4
    Tundra = 5
    Barrens = 6
    Blood_River = 7
    Beasleys_Plateau = 8#2v2
    Crevice = 9
    The_Docks = 10
    Labyrinth = 11
    Repository = 12
    Terminal_Moraine = 13
    Memorial_Basin = 14
    Exile = 15#3v3
    Fort_Deen = 16
    Frozen_Valley = 17
    Glacial_Ravine = 18

'''
* HWError: function that displays error/warning message and terminates program if needed.
* @param str errormsg: A string, the error message to be displayed.
* @param int isError: 1 if error and program should be terminated, 0 if warning.
'''
def HWerror(errormsg, isError):
    if (not(isinstance(isError, int)) or (isError < 0) or (isError > 1)):
        print("Error or warning encountered. Invalid error flag, should be 1 if error, 0 if warning. Terminating.")
        isError = 1
    if (isinstance(errormsg, str)):
        print(errormsg)
    else:
        print("Error or warning encountered. Invalid error message.")
    if (isError == 1):
        print()
        input("Press enter to close...")
        exit()


'''##########################################
############ Beginning of script ############
##########################################'''
#STEP 1: INPUT    
pcInput = input("How many players? ")

#STEP 2: INITIALIZATION OF CORE VARIABLES
#        AND ERROR CHECKING ON CONFIG AND INPUT
try:
    humanCount = int(pcInput)
except ValueError:
    HWerror("Unexpected input. Terminating.", 1)

if (humanCount <= 0):
    HWerror("Unexpected input. Terminating.", 1)

if (not(isinstance(ConfigAlternateHumanTeamAssignmentAlgorithm,int))):
    ConfigAlternateHumanTeamAssignmentAlgorithm = 0
    HWerror("Config Error: Alternate Team Assignment Algorithm option is not an integer. Setting to default " + str(ConfigAlternateHumanTeamAssignmentAlgorithm) + ".", 0)

if (ConfigAlternateHumanTeamAssignmentAlgorithm < 0 or ConfigAlternateHumanTeamAssignmentAlgorithm > 1):
    ConfigAlternateHumanTeamAssignmentAlgorithm = 0
    HWerror("Config Error: Alternate Team Assignment Algorithm is not within the valid range. Setting to default " + str(ConfigAlternateHumanTeamAssignmentAlgorithm) + ".", 0)

if (not(isinstance(ConfigMaxHumansPerGame,int))):
    ConfigMaxHumansPerGame = 6
    HWerror("Config Error: Max Humans Per Game is not an integer. Setting to " + str(ConfigMaxHumansPerGame) + ".", 0)

maxHumans = 6    
if (ConfigMaxHumansPerGame >= 1 and ConfigMaxHumansPerGame <= 6):
    maxHumans = ConfigMaxHumansPerGame
else:
    HWerror("Config Warning: Max Humans Per Game is outside the allowed range. Using " + str(maxHumans) + " instead.", 0)

if (not(isinstance(ConfigForceHumanAlliance,int))):
    ConfigForceHumanAlliance = 0
    HWerror("Config Error: Force Human Alliance is not an integer. Setting to " + str(ConfigForceHumanAlliance) + ".", 0)
    
if (ConfigForceHumanAlliance == 1):
    if (ConfigMaxHumansPerGame > 3):
        maxHumans = 3
        HWerror("Config Warning: Force Human Alliance is " + str(ConfigForceHumanAlliance) + ", but Max Humans Per Game is too high. Setting Max Humans Per Game to " + str(maxHumans) + ".", 0)
            
elif (ConfigForceHumanAlliance != 0 and ConfigForceHumanAlliance != -1):
    ConfigForceHumanAlliance = 0
    HWerror("Config Warning: Force Human Alliance is outside the allowed range. Using " + str(ConfigForceHumanAlliance) + " instead.", 0)
    
if(ConfigAlternateHumanTeamAssignmentAlgorithm != 0 and ConfigForceHumanAlliance != 0):
    ConfigAlternateHumanTeamAssignmentAlgorithm = 0
    HWerror("Config Warning: Alternate Team Assignment Algorithm is nonzero, but Force Human Alliance is " + str(ConfigForceHumanAlliance) + ". Setting Alternate Team Assignment Algorithm to " + str(ConfigAlternateHumanTeamAssignmentAlgorithm) + ".", 0)
    

numGamesLeft = int(math.ceil(humanCount/maxHumans))#pre-calculated, later used to determine how many humans in each game
remainingUnallocatedHumans = humanCount#keeps track of how many players there are left to allocate
iteration = 0#this is used to display game #
currentHumanIndex = 0#global index into randomizedHumanArray

#STEP 3: RANDOMIZE THE PLAYER ORDER
#This algorithm uses the Fisher-Yates shuffle. See https://bost.ocks.org/mike/shuffle/ for more info.
randomizedHumanArray = [(i+1) for i in range(humanCount)]
for i in range(humanCount):
    randomEntry = random.randint(i,humanCount-1)
    temp = randomizedHumanArray[i]
    randomizedHumanArray[i] = randomizedHumanArray[randomEntry]
    randomizedHumanArray[randomEntry] = temp
    
#STEP 4: ITERATE THROUGH EACH GAME
while (remainingUnallocatedHumans > 0):
    #STEP 4.1: SETUP AND CALCULATE HOW MANY HUMANS THIS GAME WILL HAVE
    print()#print an empty line for aesthetics.
    iteration += 1
    humansThisGame = -1
    if (remainingUnallocatedHumans > maxHumans):
        humansThisGame = int(math.ceil(remainingUnallocatedHumans/numGamesLeft))     #amount of players in each game (todoL figure this out before the loop I think)
    else:
        humansThisGame = remainingUnallocatedHumans
    remainingUnallocatedHumans -= humansThisGame
    
    #STEP 4.2: RANDOMIZE TEAM SIZE (1v1, 2v2, or 3v3)
    minTeamSize = int(math.ceil(humansThisGame/2))
    if (ConfigForceHumanAlliance == 1):
        minTeamSize = humansThisGame
    teamSize = random.randint(minTeamSize,3)
    print("===========================")
    print("GAME " + str(iteration) + ": " + str(teamSize) + "v" + str(teamSize))
    
    #STEP 4.3: RANDOMIZE MAP BASED ON TEAM SIZE
    mapThisGame = HWMap(0)#default: invalid map
    if (teamSize == 1):
        mapThisGame = HWMap(random.randint(1,18))
    elif (teamSize == 2):
        mapThisGame = HWMap(random.randint(8,18))
    else:#3v3
        mapThisGame = HWMap(random.randint(15,18))
    print("  MAP: " + str(mapThisGame.name).replace('_',' '))#Print map. Also remove underscores from map names using str.replace().
    
    #STEP 4.4: RANDOMIZE WHICH TEAM EACH HUMAN IS ON
    rows, cols = (teamSize*2, 2)                                    #initialize the player array according to team size (and thus # of players in game)
    arr = [[0 for i in range(cols)] for j in range(rows)]#array, where index = player number, 1st value = [(human ID) if human, 0 if AI], 2nd value = leader ID [1-10] (note that AIS can never have 1 here)
    #4.4.1: ALGORITHM 1: 50/50 CHANCE OF EACH PLAYER BEING ON EACH TEAM
    if (ConfigAlternateHumanTeamAssignmentAlgorithm == 0):
        for i in range(humansThisGame):                        #assign each human a slot in array.
            if (ConfigForceHumanAlliance == 1):
                desiredSlot = 0
            elif (ConfigForceHumanAlliance == -1):
                desiredSlot = (i%2)*(teamSize)#this still randomizes which team everyone is on since player order is pre-randomized
            else:
                desiredSlot = random.randint(0,1)*teamSize
            while (arr[desiredSlot][0] != 0):#find next open slot after desiredSlot
                desiredSlot += 1
                if (desiredSlot >= rows):
                    desiredSlot = 0
            arr[desiredSlot][0] = randomizedHumanArray[currentHumanIndex]#player # = random human ID (this array is pre-randomized)
            currentHumanIndex += 1
    #4.4.2: ALGORITHM 2: EQUAL CHANCE OF PLAYER BEING PLACED IN ANY OPEN SLOT (bias towards even teams)
    else:#ConfigAlternateHumanTeamAssignmentAlgorithm == 1
        openSlots = teamSize*2
        team1index = 0
        team2index = 0
        for i in range(humansThisGame):
            desiredSlot = -1
            randomNumber = random.randint(team1index,(teamSize*2-1)-team2index)
            if (randomNumber < teamSize):#player is on team 1
                desiredSlot = 0
                team1index += 1
            else:#player is on team 2
                desiredSlot = teamSize
                team2index += 1
            while (arr[desiredSlot][0] != 0):#find next open slot after desiredSlot
                desiredSlot += 1
                if (desiredSlot >= rows):
                    desiredSlot = 0
            arr[desiredSlot][0] = randomizedHumanArray[currentHumanIndex]#player # = random human ID (this array is pre-randomized)
            currentHumanIndex += 1
    
    #STEP 4.5: RANDOMIZE WHICH LEADER EACH PLAYER WILL BE (AIs are players too)
    for i in range(rows):#RNG each player's leader
        if (arr[i][0] != 0):#if a human player is in this slot
            arr[i][1] = HWLeader(random.randint(1,10))
        else:#if an AI player is in this slot (AIs cannot play as the United Rebel Front in this game)
            arr[i][1] = HWLeader(random.randint(2,10))
    
    #STEP 4.6: PRINT RESULTS. FIX SPACING TO DYNAMICALLY RESIZE OUTPUT BASED ON NUMBER OF PLAYERS USING str.rjust(). Also remove underscores from leader names using str.replace().
    for i in range((int)(rows)):
        if (i == 0):
            print("  TEAM ALPHA:")
        elif(i == (int)(rows/2)):
            print("  TEAM BRAVO:")
        if (arr[i][0] != 0):
            print("    Player " + str(arr[i][0]).rjust(len(str(humanCount)),' ') + ": " + str(arr[i][1].name).replace('_',' '))
        else:
            print("    AI     " + str().rjust(len(str(humanCount)),' ') + ": " + str(arr[i][1].name.replace('_',' ')))
   
    #STEP 4.7: FINISH LOOP AND PREPARE VARIABLES FOR NEXT ITERATION.    
    numGamesLeft -= 1
    
#STEP 5: END PROGRAM ONCE LOOP FINISHES
print()
input("Press enter to close...")