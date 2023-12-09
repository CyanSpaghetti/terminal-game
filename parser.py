import pygame, os, sys

class Parser:
    def __init__(self):
        self.debug = True # Set to false when you're done making the final version
    def Parse(self, command : str) -> str:
        if not self.debug:
            match(command): # return with prefixes to change color (e = red, s = blue, p, y, c)
                case "boot":
                    return "BOOTING SYSTEM"
                case _:
                    return f'eCOMMAND NOT RECOGNIZED'
        else:
            match(command):
                case "boot":
                    return "BOOTING SYSTEM"
                
                # debugging commands
                case "red":
                    return "eRED"
                case "yellow":
                    return "yYELLOW"
                case "blue":
                    return "sBLUE"
                case "cyan":
                    return "cCYAN"
                case "green":
                    return "GREEN"
                case "purple":
                    return "pPURPLE"
                
                # wildcard
                case _:
                    return f'eCOMMAND NOT RECOGNIZED'