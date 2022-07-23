"""
Functions return True if a cheat is detected
"""

# import sys

# def perform_quit():
#     print("Found cheat. Quitting...")

#     with open("ib.cfg", "w") as f:
#         f.write("1")
#     with open("../ib.cfg", "w") as f:
#         f.write("1")
    
#     sys.exit(1)

def check_jump_height(jump_height: int, valid_jump_height: int):
    if jump_height != valid_jump_height:
        return True

def check_speed(speed: int):
    if speed not in [3, 7]:
        return True

def check_health(health: int):
    if health > 150:
        return True