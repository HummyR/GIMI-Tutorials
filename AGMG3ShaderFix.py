import os
import re
import sys

# Script created by HummyR#8131, Modder4869#4818, and Takoyaki#0697.
# Huge thanks to SilentNightSound#7430 for guiding us.
# Please visit our AGMG discord server https://discord.gg/agmg if you have any questions regarding this.

# open command console and type "python agmg3shaderfix.py" to use
# use this script last after any transparency or merge_mods scripts

def main():
    
    print("\nAnime Game 3.0+ Shader Fixer\n")
    
    print("Be sure to use mods generated from GIMI importer plugin.\nPlease visit our AGMG discord server https://discord.gg/agmg if you have any questions regarding this.")
    print("Source code: https://github.com/HummyR/GIMI-Tutorials/blob/main/Version_3_Character_Shader_Fix.md")
    
    print("\nThese files will be modified:")
    for roote, dir, testfiles in os.walk("."):
        if "disabled" in roote.lower():
            continue
        for fil in testfiles:
            if "disabled" in fil.lower():
                continue
            if os.path.splitext(fil)[1] == ".ini":
                print(os.path.join(roote, fil))
    try:
        input("\nThis will modify all .ini files in this folder and subdirectories. \nRename some with 'disabled' if you dont want that .ini edited. \nPress enter to continue\n")
    except:
        raw_input("\nThis will modify all .ini files in this folder and subdirectories. \nRename some with 'disabled' if you dont want that .ini edited. \nPress enter to continue\n")
    
  
    Shadercode = r"""
; Generated shader fix for 3.0+ GIMI importer characters. Please contact the tool developers at https://discord.gg/agmg if you have any questions.

; Variables -----------------------

[Constants]
global $CharacterIB
;0=none, 1=head, 2=body, 3=dress, 4=extra, etc.

[Present]
post $CharacterIB = 0

[ResourceRefHeadDiffuse]
;[ResourceRefHeadLightMap]
[ResourceRefBodyDiffuse]
;[ResourceRefBodyLightMap]
[ResourceRefDressDiffuse]
;[ResourceRefDressLightMap]
[ResourceRefExtraDiffuse]
;[ResourceRefExtraLightMap]

; ShaderOverride ---------------------------

[ShaderRegexCharReflection]
shader_model = ps_5_0
run = CommandListReflectionTexture
[ShaderRegexCharReflection.pattern]
mul r\d+\.\w+, r\d+\.\w+,[^.]*\.\w+\n
mad o\d+\.\w+, r\d+\.\w+, cb\d+\[\d+\]\.\w+, r\d+\.\w+\n
mov o\d+\.\w+, l\(\d+\.\d+\)\n

;[ShaderRegexCharOutline]
;shader_model = ps_5_0
;run = CommandListOutline
;[ShaderRegexCharOutline.pattern]
;mov o\d+\.\w+, l\(\d+\)\n
;mov o\d+\.\w+, r\d+\.\w+\n
;mov o\d+\.\w+, l\(\d+\.\d+\)
;broken as of version 4.0

; OPTIONAL: If regex match breaks, use a [ShaderOverride] command matching shader hash for reflection then use "run = CommandListOutline" under the command

; CommandList -------------------------

[CommandListReflectionTexture]
if $CharacterIB != 0
    if $CharacterIB == 1
        ps-t0 = copy ResourceRefHeadDiffuse
    else if $CharacterIB == 2
        ps-t0 = copy ResourceRefBodyDiffuse
    else if $CharacterIB == 3
        ps-t0 = copy ResourceRefDressDiffuse
    else if $CharacterIB == 4
        ps-t0 = copy ResourceRefExtraDiffuse    
    endif
drawindexed=auto
$CharacterIB = 0
endif

;[CommandListOutline]
;if $CharacterIB != 0
;    if $CharacterIB == 1
;        ps-t1 = copy ResourceRefHeadLightMap
;    else if $CharacterIB == 2
;        ps-t1 = copy ResourceRefBodyLightMap
;    else if $CharacterIB == 3
;        ps-t1 = copy ResourceRefDressLightMap
;    else if $CharacterIB == 4
;        ps-t1 = copy ResourceRefExtraLightMap
;    endif
;drawindexed=auto
;$CharacterIB = 0
;endif
"""
             

    ModifiedFiles = []
    DISABLED_files = []
    Corecode = []
    for root, dir, files in os.walk("."):
        if "disabled" in root.lower():
            continue
        for file in files:
            if "disabled" in file.lower():
                continue
            if os.path.splitext(file)[1] == ".ini":
                file_path = os.path.join(root, file)
                DISABLED_file_path = os.path.join(root, "DISABLED_" + file)
                
                with open(file_path, "r") as f:
                    Original = f.read()
                    Corecode.append(Original)
                    Newcode = Original
                    ObjectPart = ['Head', 'Body', 'Dress', 'Extra']
                    
                    for i in range(len(ObjectPart)):
                        OPIterate = ObjectPart[i]
                        TO = re.search('\[TextureOverride\w+' + OPIterate + '\]\n', Newcode)
                        if TO == None:
                            continue

                        TOIndex = TO.end()

                        End = Newcode.find('[', TOIndex)

                        Newcode = Newcode[:End] + '$CharacterIB = ' + str(i+1) + '\nResourceRef' + OPIterate + 'Diffuse = reference ps-t1' + '\nResourceRef' + OPIterate + 'LightMap = reference ps-t2\n\n'  + Newcode[End:]
                    ModifiedFiles.append(file_path)
                    DISABLED_files.append(DISABLED_file_path)
                        
                    result = Newcode
                    result += "\n\n; Version 1.0.0 AGMG Tool Developer Version 3 Shader Fixer\n\n"
                    result += Shadercode
                        
                    with open(DISABLED_file_path, "w") as f:
                        f.write(Original)                       
                    
                    with open(file_path, "w") as f:
                        f.write(result)
                        print("Writing shader fix to " + file + " Completed.\n")
                    
    try:
        undo = input("Undo operation? [y] \nDo not modify file names while you are checking. \nExit if you are done.\n")
    except:
        raw_input("Undo operation? [y] \nDo not modify file names while you are checking. \nExit if you are done.\n")
        
    if undo == "y":
        print("\n")
        for modded in range(len(ModifiedFiles)):
        
            mod = ModifiedFiles[modded]
            
            if os.path.exists(mod):
                with open(mod, "w") as f:
                    f.write(Corecode[modded])
                    os.remove(DISABLED_files[modded])
                    print(mod + " undo complete.")
            else:
                print("The file does not exist")


if __name__ == "__main__":
    main()
