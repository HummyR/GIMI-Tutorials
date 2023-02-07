# USAGE INSTRUCTIONS to mass disable/enable mods in mod folder: 

# 1) create shortcut of .py (right click -> "Create Shortcut")
# 2) right click on shortcut -> properties
# 3) prefix "Target:" with "python" so it runs the .py as an argument into the python command
# 4) Drag and drop files you want to modify onto shortcut
# 5) press any key to confirm selection


import sys
import os

droppedFile = sys.argv[1:]
for file in droppedFile:
    print(os.path.basename(file))


input("\nPress any key to confirm selection. Close console to cancel.")

#case insensitive replace from https://stackoverflow.com/a/4773614 by rsmoothly

def insensitivereplace(old, new, text):
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(new) 
    return text

for file in droppedFile:
    directory = os.path.dirname(file)
    filename = os.path.basename(file)
    if "disabled_" in file.lower():
        try:
            os.rename(file, os.path.join(directory, insensitivereplace("disabled_", "", filename)))
            print(insensitivereplace("disabled_", "", filename))
        except PermissionError:
            print("Operation not permitted for file: " + file)
        except OSError as error:
            print(error)
            print("Error in file:" + file)
            
    elif "disabled" in file.lower():
        try:
            os.rename(file, os.path.join(directory, insensitivereplace("disabled", "", filename)))
            print(insensitivereplace("disabled", "", filename))
        except PermissionError:
            print("Operation not permitted for file: " + file)
        except OSError as error:
            print(error)
            print("Error in file:" + file)
            
    else:
        try:
            os.rename(file, os.path.join(directory, "DISABLED_" + filename))
            print("DISABLED_"+filename)
        except PermissionError:
            print("Operation not permitted for file: " + file)
        except OSError as error:
            print(error)
            print("Error in file:" + file)
        
   
input("\nFinished.")

# HummyR#8131 
# https://discord.gg/agmg
