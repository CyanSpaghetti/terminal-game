import pygame
import sys, os
from parser import Parser

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 800, 600
        self.FONT_SIZE = 20
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.CYAN = (0, 255,255)
        self.PURPLE = (255,0,255)
        self.YELLOW = (255,255,0)
        self.WHITE = (255, 255, 255)
        self.commandHistory_FILE = "commandHistory.txt"
        self.prefix = 'user@computer:~$ '
        # Parser
        self.parser = Parser()

        # Create the Pygame window
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Terminal Screen')

        # Font and text-related setup
        self.customFont = os.getcwd() + '/fonts/Perfect DOS VGA 437.ttf'
        self.font = pygame.font.Font(self.customFont, self.FONT_SIZE)
        self.textLines = [('', self.BLUE)]  # Start with an empty line and prompt color
        self.inputText = ''
        self.inputColor = self.WHITE

        # Command history
        self.commandHistory = []
        self.historyIndex = 0
        self.LoadCommandHistory()

    def DisplayText(self):
        self.screen.fill(self.BLACK)
        y = 0
        for text, color in self.textLines:
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (10, y))
            y += self.FONT_SIZE + 2
        pygame.display.flip()

    def ProcessInput(self, command):
        if command.lower() in ["exit", "quit"]: # Quit the game
            self.SaveCommandHistory()
            self.quit()
        elif command.lower() in ["cls", "clear"]:
            self.textLines = [('', self.BLUE)]  # Clear the screen
            self.inputText = ''
            return ''
        elif command.strip() != '':
            return f'{self.parser.Parse(command.lower())}' # Anything else you want to do to the text
        return ''

    def quit(self):
        pygame.quit()
        sys.exit()

    def AddText(self, text, color):
        self.textLines.append((text, color))

    def SaveCommandHistory(self):
        with open(self.commandHistory_FILE, 'w') as file:
            file.write('\n'.join(self.commandHistory))

    def LoadCommandHistory(self):
        try:
            with open(self.commandHistory_FILE, 'r') as file:
                self.commandHistory = file.read().splitlines()
        except FileNotFoundError:
            pass

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.SaveCommandHistory()
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        processed_command = self.ProcessInput(self.inputText)
                        if processed_command:
                            self.textLines.pop()  # Remove the empty input line
                            self.AddText(f'{self.prefix} {self.inputText}', self.inputColor)  # Display input
                            
                            # Check for color change with prefixes (e,s,p,y,c)
                            match(processed_command[0]):
                                case 'e':
                                    self.AddText(processed_command[1:len(processed_command)], self.RED)  # Display processed output
                                case 's':
                                    self.AddText(processed_command[1:len(processed_command)], self.BLUE)  # Display processed output
                                case 'p':
                                    self.AddText(processed_command[1:len(processed_command)], self.PURPLE)  # Display processed output
                                case 'y':
                                    self.AddText(processed_command[1:len(processed_command)], self.YELLOW)  # Display processed output
                                case 'c':
                                    self.AddText(processed_command[1:len(processed_command)], self.CYAN)  # Display processed output
                                case _:
                                    self.AddText(processed_command, self.GREEN)  # Display processed output
                            
                            self.commandHistory.append(self.inputText)  # Add command to history
                            self.SaveCommandHistory()
                            self.historyIndex = len(self.commandHistory)
                            self.AddText('', self.BLUE)  # New line for next input prompt
                            self.inputText = ''
                        else:
                            self.AddText(f'{self.prefix} ', self.BLUE)  # New line for next input prompt without processing
                    elif event.key == pygame.K_BACKSPACE:
                        self.inputText = self.inputText[:-1]
                    elif event.key == pygame.K_UP:
                        if self.historyIndex > 0:
                            self.historyIndex -= 1
                            self.inputText = self.commandHistory[self.historyIndex]
                    elif event.key == pygame.K_DOWN:
                        if self.historyIndex < len(self.commandHistory) - 1:
                            self.historyIndex += 1
                            self.inputText = self.commandHistory[self.historyIndex]
                        elif self.historyIndex == len(self.commandHistory) - 1:
                            self.historyIndex += 1
                            self.inputText = ''
                    else:
                        self.inputText += event.unicode

            self.textLines[-1] = (f'{self.prefix} {self.inputText}', self.inputColor)  # Update input line
            self.DisplayText()

        self.SaveCommandHistory()
        self.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
