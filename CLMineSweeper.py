"""
LICENSING


Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from random import randint, choice
import os
if os.name == 'nt':
    os.system('color')

os.system("cls" if os.name == "nt" else "clear")

class Tile:
    def __init__(self, x, y, state="empty", role="empty"):
        self.x = x
        self.y = y
        self.state = state # states can be: flag, covered and empty or the matching value of role
        self.role = role
        self.eightNeighbours = {
            "up-center":(x, y-1),
            "up-right":(x+1, y-1),
            "middle-right":(x+1, y),
            "down-right":(x+1, y+1),
            "down-center":(x, y+1),
            "down-left":(x-1, y+1),
            "middle-left":(x-1, y),
            "up-left":(x-1, y-1)
            }
        self.neighbours = ((x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1))
        self.mineNeighboursAmount = 0

    def reveal(self):
            self.state = self.role
    
    def calculateMineNeighborsAmount(self, RoleLUT):
        mineNeighboursAmountFn = 0
        for neighbor in self.neighbours:
            if RoleLUT[neighbor] == "mine":
                mineNeighboursAmountFn += 1

        self.mineNeighboursAmount = mineNeighboursAmountFn

    def mark(self):
        self.state = "flag"



def colorize(text, rgb):
            if not rgb:
                return text
                
            r, g, b = rgb
            return f"\033[38;2;{r};{g};{b}m{text}\033[0m"



class Display:
    def __init__(self, width=10, height=10, coordinateHelp=True, rowLineSymbol="-", coloumnLineSymbol="|", coveredTile="#", emptyTile=" ", mineTile="¤", flagTile="ł", numberTileSet=[" ", "1", "2", "3", "4", "5", "6", "7", "8"], data=[], numberTiles=True, coveredTileColor = (188,188,188), flagTileColor=(252, 207, 27) ,mineTileColor = (206, 78, 80), numberTilesSetColors = [None, (22, 175, 252), (9, 249, 181), (189, 249, 9), (249, 197, 9), (249, 121, 9), (249, 49, 9), (221, 9, 249), (252, 100, 191)], gridColor=(133, 133, 133)):
        
        self.width = width
        self.height = height
        
        self.coordinateHelp = coordinateHelp

        self.rowLineSymbol = colorize(rowLineSymbol, gridColor)
        self.coloumnLineSymbol = colorize(coloumnLineSymbol, gridColor)

        self.coveredTile = colorize(coveredTile, coveredTileColor)
        self.emptyTile = emptyTile
        self.mineTile = colorize(mineTile, mineTileColor)
        self.flagTile = colorize(flagTile, flagTileColor)

        self.numberTileSet = []
        for i in range(len(numberTileSet)):
            coloredNum = colorize(numberTileSet[i], numberTilesSetColors[i])
            self.numberTileSet.append(coloredNum)

        self.data = data

        self.numberTiles = numberTiles
        
        self.coveredTileColor = coveredTileColor
        self.flagTileColor = flagTileColor
        self.mineTileColor = mineTileColor
        self.numberTilesSetColors = numberTilesSetColors
        self.gridColor = gridColor


    
    def Render(self):
        renderRows = []
        stateLUT = GenerateStateLUT(self.data) # generating Loo Up Table everytime when the function gets called, so it updates automatically.
        numLUT = GenerateNumberLUT(self.data)

        if self.coordinateHelp:
            row = (" "*(len(str(self.height-1)))) + self.coloumnLineSymbol
            for num in range(self.width):
                row += str(num) + self.coloumnLineSymbol
            renderRows.append(row)

        for y in range(self.height):
            if self.coordinateHelp:
                row = self.rowLineSymbol*((self.width*2)+(len(str(self.height-1))*2)) + "\n"
                row += " "*(len(str(self.height-1))-len(str(y))) + str(y) + self.coloumnLineSymbol
            else:
                row = self.rowLineSymbol*(self.width*2) + "\n"
                
            for x in range(self.width):

                if stateLUT.get((x, y)) == "empty":
                    if self.numberTiles:
                        row += self.numberTileSet[numLUT.get((x, y))]
                    else:                    
                        row += self.emptyTile

                elif stateLUT.get((x, y)) == "mine":
                    row += self.mineTile
                elif stateLUT.get((x, y)) == "flag":
                    row += self.flagTile
                elif stateLUT.get((x, y)) == "covered":
                    row += self.coveredTile
                row += self.coloumnLineSymbol
            renderRows.append(row)

        if self.coordinateHelp:
                row = self.rowLineSymbol*((self.width*2)+(len(str(y))*2))
        else:
                row = self.rowLineSymbol*(self.width*2) + "\n"

        renderRows.append(row)
        
        for line in renderRows:
            print(line)

        return renderRows



def GenerateBoard(width, height, chanceMin=0, chanceMax=15, chanceGoal=(1, 1), initialState="covered", initialRole="empty", immediateReveal=False, emptyBoard=False):
    generatedBoard = []
    state = initialState
    for y in range(height):
        for x in range(width):
            if not(emptyBoard):
                
                role = initialRole
                chosenState = randint(chanceMin, chanceMax)
                if chosenState in chanceGoal:
                    role = "mine"
                if immediateReveal:
                    state = role
            else:
                role = "empty"
                state = "empty" \
                ""
            generatedBoard.append(Tile(x, y, state=state, role=role))
    
    # fixing invalid neighbours (removing them from both the associated tuples and the corresponding key:value pairs.)
    horizontalConstraint = range(width)
    verticalConstraint = range(height)
    keys = ("up-center", "up-right", "middle-right", "down-right", "down-center", "down-left", "middle-left", "up-left")
    for tile in generatedBoard:
        eightNeighbours = dict(tile.eightNeighbours)
        simplyNeighbours = list(tile.neighbours)

        for index, neighbour in enumerate(simplyNeighbours):
            if not((neighbour[0] in horizontalConstraint) and (neighbour[1] in verticalConstraint)):
                eightNeighbours.pop(keys[index])
                simplyNeighbours[index] = None
        tile.eightNeighbours = eightNeighbours
        simplyNeighbours = [n for n in simplyNeighbours if n is not None]
        tile.neighbours = simplyNeighbours
    
    # prep for number display values
    for tile in generatedBoard:
        tile.calculateMineNeighborsAmount(GenerateRoleLUT(generatedBoard))

    return generatedBoard



def GenerateStateLUT(tiles):
    tilesLUT = {}
    for tile in tiles:
        tilesLUT[(tile.x, tile.y)] = tile.state
    return tilesLUT

def GenerateRoleLUT(tiles):
    tilesLUT = {}
    for tile in tiles:
        tilesLUT[(tile.x, tile.y)] = tile.role
    return tilesLUT

def GenerateNumberLUT(tiles):
    tilesLUT = {}
    for tile in tiles:
        tilesLUT[(tile.x, tile.y)] = tile.mineNeighboursAmount
    return tilesLUT

def GenerateObjLUT(tiles):
    return {(t.x, t.y): t for t in tiles}



def RevealWave(tiles, selectedTile, objectLUT=None, waveMode="floodfill"): 
          
    if waveMode == "legacy":

        targetTile = selectedTile
        found = True

        if isinstance(selectedTile, tuple):
            found = False
            for tile in tiles:
                if selectedTile[0] == tile.x and selectedTile[1] == tile.y:
                    targetTile = tile
                    found = True
        if found:
            if targetTile.role == "mine":
                return

            targetTile.reveal()

            nextTile = choice(targetTile.neighbours)
            
            for wild in tiles:
                
                if (wild.x, wild.y) == nextTile and wild.state == "covered":
                
                    RevealWave(tiles, wild)
                    
                if (wild.x, wild.y) in targetTile.neighbours and wild.role != "mine":
                    wild.reveal()
            else:
                return
        
    elif waveMode == "floodfill":

        if objectLUT is None:
            objectLUT = GenerateObjLUT(tiles)
            
        if isinstance(selectedTile, tuple):
            selectedTile = objectLUT.get(selectedTile)
            if selectedTile is None:
                print("Coordinates out of bounds.")
                return

        if not isinstance(selectedTile, Tile):
            return

        
        if selectedTile.role == "mine" or selectedTile.state != "covered":
            return
        
        selectedTile.reveal()
        
        if selectedTile.mineNeighboursAmount > 0:
            return
            
        for neighbor_coords in selectedTile.neighbours:
            neighbor_tile = objectLUT.get(neighbor_coords)
            if neighbor_tile:
                
                RevealWave(tiles, neighbor_tile, objectLUT)



def WinLoseCondition(tiles, selectedTile, action):

    targetTile = selectedTile

    if targetTile.role == "mine" and action != "flag":
        return 'lost'
    
    minesFound = 0
    maxMines = 0
    for tile in tiles:
        if tile.role == "mine":
            maxMines += 1
        
        if tile.state == "flag":
            if tile.role == "mine":
                minesFound += 1
            if tile.role == "empty":
                minesFound -= 1

    if minesFound == maxMines:
        return 'win'
        
    return None



def userInput(text="[{}]:", symbol="MineSweeper", promptColor = (252, 235, 83)):
    return input(colorize(text.format(symbol), promptColor))


# Primary game logic
def Main(width, height, chanceMin, chanceMax, chanceGoal):
    
    # Initializing game with an initial board
    board = GenerateBoard(width, height, initialState="covered", chanceMin=chanceMin, chanceMax=chanceMax, chanceGoal=chanceGoal)
    display = Display(width, height, data=board)
    condition = None
    isFirstTurn = True

    # welcome screen

    print(colorize("""
Command Line Minesweeper program made by EndlessCODEON101010
Licensed under MIT License          
""", (110, 110, 110)))

    print(colorize(f"""




  ░██████  ░██         ░███     ░███ ░██                                                                                                       
 ░██   ░██ ░██         ░████   ░████                                                                                                            
░██        ░██         ░██░██ ░██░██ ░██░████████   ░███████   ░███████  ░██    ░██    ░██  ░███████   ░███████  ░████████   ░███████  ░██░████ 
░██        ░██         ░██ ░████ ░██ ░██░██    ░██ ░██    ░██ ░██        ░██    ░██    ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░██    ░██ ░███     
░██        ░██         ░██  ░██  ░██ ░██░██    ░██ ░█████████  ░███████   ░██  ░████  ░██  ░█████████ ░█████████ ░██    ░██ ░█████████ ░██      
 ░██   ░██ ░██         ░██       ░██ ░██░██    ░██ ░██               ░██   ░██░██ ░██░██   ░██        ░██        ░███   ░██ ░██        ░██      
  ░██████  ░██████████ ░██       ░██ ░██░██    ░██  ░███████   ░███████     ░███   ░███     ░███████   ░███████  ░██░█████   ░███████  ░██      
                                                                                                                 ░██                            
                                                                                                                 ░██
                   
[Press ENTER to begin]
                   
                   
                   """, (0, 206, 247)))
    
    cheat = input()

    if cheat.lower() == "upupdowndownleftrightleftrightbastart":
        try:
            print('[CLMinesweeper] cheat mode accessed')
            validresults = input('valid results for randint?').strip().split()
            veryvalidresults = []
            
            for value in validresults:
                veryvalidresults.append(int(value))

            Main(int(input('grid width?')), int(input('grid height?')), int(input('grid randint min?')), int(input('grid randint max?')), veryvalidresults)
        except:
            print(colorize("[CLMinesweeper] Unexpected error happened while setting up new game", (255, 0, 0)))
        print((colorize("[CLMinesweeper] Exited custom game. Continuing to normal mode.\n", (255, 255, 0))))

    # Master loop
    while condition not in ("win", "lost"):
        display.Render()
        
        try:
            userCommand = userInput(text='[{}] Action (c=click, f=flag) and coords (X Y): ', symbol="Game")
            print() # spacer

            userAction = userCommand.strip().split()
            
            if isFirstTurn and len(userAction) == 2:
                userCommand = "c " + userCommand
                print(colorize(f"[ATTENTION] You left out what action you wanted to do, so the game assumed you wanted to CLICK, so it attached the CLICK action to your initial input: {colorize(f"{userCommand}", (255, 255, 255))}\n{colorize("[ATTENTION] The auto correction system won't take action in further commands from now on to avoid annoyances.\n", (252, 150, 0))}", (252, 150, 0)))
                userAction = userCommand.strip().split()

            
            if userCommand.lower() in ("help", "h"):
                print(colorize("""
[HELP] The following command schemes are available (replace x and y with the desired tile's coordinates):
        
       Reveals tile:
        click x y
            c x y

       Flags/Unflags tile:
        flag x y
           f x y

       Winning condition:
            You win, when you successfully flag all the tiles that has mines under it and not flagging tiles which has no mines!

       Losing condition:
            You lose when you click on a tile which has a mine under it.
    

                \n""" ,(0, 255, 0)))
                continue

            if len(userAction) != 3:
                print(colorize("Invalid format. Use: action X Y (e.g., c 0 0)", (255, 100, 100)))
                continue
                
            action = userAction[0].lower()
            x = int(userAction[1])
            y = int(userAction[2])
            
            if not (0 <= x < width and 0 <= y < height):
                print(colorize("Coordinates out of bounds! Try again.", (255, 100, 100)))
                continue
                
        except ValueError:
            print(colorize("Invalid input!", (255, 100, 100)))
            continue
        
        targetIndex = (y * width) + x
        
        # initilitilitilitization
        if isFirstTurn and action in ('c', 'click'):
            # Keep generating until the clicked tile is completely safe (a zero)
            while board[targetIndex].role == "mine" or board[targetIndex].mineNeighboursAmount > 0:
                board = GenerateBoard(width, height, initialState="covered", chanceMin=chanceMin, chanceMax=chanceMax, chanceGoal=chanceGoal)
                display.data = board 
            
            isFirstTurn = False

        # Process the move
        targetTile = board[targetIndex]
        
        if action in ('c', 'click'):
            if targetTile.state == "flag":
                print(colorize("Can't reveal a flagged tile! Unflag it first.", (255, 200, 50)))
                continue
            RevealWave(board, targetTile)
            
        elif action in ('f', 'flag'):
            if targetTile.state == "covered":
                targetTile.mark()
            elif targetTile.state == "flag":
                targetTile.state = "covered" # Un-flag
            else:
                print(colorize("You can't flag an already revealed tile!", (255, 200, 50)))
                continue
        else:
            print(colorize("Unknown action. Use 'c' to click or 'f' to flag.", (255, 100, 100)))
            continue
            
        
        condition = WinLoseCondition(board, targetTile, ('flag' if action.lower() == 'f' else action.lower()))

    # Ending game
    for tile in board:
        tile.reveal()
    
    display.Render()
    
    if condition == 'win':
        print(colorize("\nYippeee! A WIN. Good job!", (9, 249, 181)))
    elif condition == 'lost':
        print(colorize("\nSelected a mine! You lost!", (206, 78, 80)))


if __name__ == "__main__":
    try:
        Main(10, 10, 0, 15, (1, 2, 3))
    except KeyboardInterrupt:
        print(colorize("\n[CLMinesweeper] Program exited upon manual intervention.", (252, 150, 0)))
