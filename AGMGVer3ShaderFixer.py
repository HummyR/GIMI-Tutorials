import os
import re
import sys

path = getattr(sys, '_MEIPASS', os.getcwd())
full_path = path+"\\data"
data_path = full_path+"\\DISABLED_Shaders.ini"

def main():
    
    print("\nAnime Game 3.0+ Shader Fixer\n")
    
    print("Be sure to use mods generated from GIMI importer plugin.\n\n")
    
    try:
        input("Press enter to continue\n")
    except:
        raw_input("Press enter to continue")
    
    
    with open(data_path, "r") as f:
        print("Initializing...\n")  
        Shadercode = f.read()
             

    ModifiedFiles = []
    for root, dir, files in os.walk("."):
        if "disabled" in root.lower():
            continue
        for file in files:
            if "disabled" in file.lower():
                continue
            if os.path.splitext(file)[1] == ".ini":
                ModifiedFiles.append(file)
            
                print(file)

                with open(file, "r") as f:
                    Corecode = f.read()
                    Newcode = Corecode
                    ObjectPart = ['Head', 'Body', 'Dress', 'Extra']
                    
                    for i in range(len(ObjectPart)):
                        OPIterate = ObjectPart[i]
                        TOIndex = re.search('\[TextureOverride\w+' + OPIterate + '\]\n', Newcode)
                        
                        if TOIndex == None:
                            continue
                            
                        x = TOIndex.end()
                        Newcode = Newcode[:x] + '$CharacterIB = ' + str(i+1) + '\nResourceRef' + OPIterate + 'Diffuse = reference ps-t1' + '\nResourceRef' + OPIterate + 'LightMap = reference ps-t2\n'  + Newcode[x:]

                    result = Newcode 
                    result += "\n\n; Version 1.0.0 AGMG Tool Developer Version 3 Shader Fixer\n\n"
                    result += Shadercode
                        
                    with open("DISABLED_"+file, "w") as f:
                        f.write(Corecode)                       
                    
                    with open(file, "w") as f:
                        f.write(result)
                        print("Writing shader fix to " + file + " Completed.\n")
                    
    undo = input("Undo operation? [y] \nDo not modify file names while you are checking. \nExit if you are done.\n")
        
    if undo == "y":
        print("\n")
        for modded in ModifiedFiles:
            if os.path.exists(modded):
                with open(modded, "w") as f:
                    f.write(Corecode)
                    os.remove("DISABLED_" + modded)
                    print("Undo complete")
            else:
                print("The file does not exist")

            
             


if __name__ == "__main__":
    main()
