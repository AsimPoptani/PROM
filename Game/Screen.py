import sys # Todo: remove Debug only
import serial
class Screen:
    # def __str__(self):
    #     for x in range(24):
    #         for y in range(80):
    #             print(str(self.screen[y][x])).replace(self.ESC.encode("utf-8"),"Escape ")
    #         print("\n")

    def __init__(self):
            # This holds colours
        self.colours = {
            'Black': '40m',
            'Red': '41m',
            'Green': '42m',
            'Yellow': '43m',
            'Blue': '44m',
            'Magenta': '45m',
            'Cyan': '46m',
            'White': '47m',
            'BrightBlack': '40;1m',
            'BrightRed': '41;1m',
            'BrightGreen': '42;1m',
            'BrightYellow': '43;1m',
            'BrightBlue': '44;1m',
            'BrightMagenta': '45;1m',
            'BrightCyan': '46;1m',
            'BrightWhite': '47;1m',
        }
        # This holds numbers 0 - 9
        self.numbers = {
            '0':
                ["###",
                 "# #",
                 "# #",
                 "# #",
                 "###",],
            '1':
                [" # ",
                 "## ",
                 " # ",
                 " # ",
                 "###", ],
            '2':
                ["## ",
                 "  #",
                 " # ",
                 "#  ",
                 "###", ],
            '3':
                ["###",
                 "  #",
                 "###",
                 "  #",
                 "###", ],
            '4':
                ["# #",
                 "# #",
                 "###",
                 "  #",
                 "  #", ],
            '5':
                ["###",
                 "#  ",
                 "###",
                 "  #",
                 "###", ],
            '6':
                ["###",
                 "#  ",
                 "###",
                 "# #",
                 "###", ],
            '7':
                ["###",
                 "  #",
                 "  #",
                 "  #",
                 "  #", ],
            '8':
                ["###",
                 "# #",
                 "###",
                 "# #",
                 "###",],
            '9':
                ["###",
                 "# #",
                 "###",
                 "  #",
                 "  #", ],
            'clear':
                [
                    '###',
                    '###',
                    '###',
                    '###',
                    '###'
                ]


       }
        # This holds ESC sequence
        self.ESC = '\u001B['
        # Create a serial port
        self.serialPort = serial.Serial("/dev/ttyAMA0", 115200)
        # defines a matrix of the board
        self.screen=[[None for y in range(23)] for x in range(80)]
        #defines the old screen
        self.oldScreen=[[None for y  in range(23)] for x in range(80)]
        #switch off the cursor
        self.serialPort.write('\u001B[?25l'.encode("utf-8"))
        #Sets the background to black
        for y in range(23):
            for x in range(80):
                self.setColourAtLocation(x,y,"Black")



 # Moves cursor to the location specified
    def _cursorTo(self, x, y):
        #move the cursor on the screen to location x,y
        return self.ESC +  str(y) + ';'  + str(x) + 'H'



    # Set colour at location
    def setColourAtLocation(self, x, y, colour):

        try:
            self.screen[x][y]=self._cursorTo(x, y+1) + self.ESC + self.colours[colour] + " "

        except Exception:
            pass



    # Set character at location
    def _setCharacterAtLocation(self, x, y, char):
        #Set the location of the cursor and the character in that cell

        if char.isalpha() and len(char) == 1:
            return self._cursorTo(x, y) + self.ESC + char

        else:
            raise ValueError(
                'Did not pass a char!'
            )


    def update(self):
        xCount=-1
        for x in self.screen:
            xCount+=1
            yCount=-1
            if not(x == self.oldScreen[xCount]):
                for y in x:
                    yCount+=1
                    if not (y == self.oldScreen[xCount][yCount]):
                        #write to serial
                        self.serialPort.write(y.encode("utf-8"))
                        #sys.stdout.write(y)
        self.oldScreen=[row[:] for row in self.screen]
