## 3.0+ Character Shader Fix

For fixing green reflections and broken outlines colors on 3.0+ characters. Please credit https://discord.gg/agmg if you use this code. Updated for 4.0

Add the corresponding sections to your ini:


```ini
; Variables -----------------------

[Constants]
global $CharacterIB
;0=none, 1=head, 2=body, 3=dress, 4=extra, etc.

[Present]
post $CharacterIB = 0
[ResourceRefHeadDiffuse]
[ResourceRefHeadLightMap]
[ResourceRefBodyDiffuse]
[ResourceRefBodyLightMap]
[ResourceRefDressDiffuse]
[ResourceRefDressLightMap]
[ResourceRefExtraDiffuse]
[ResourceRefExtraLightMap]

; ShaderOverride ---------------------------

[ShaderRegexCharReflection]
shader_model = ps_5_0
run = CommandListReflectionTexture
[ShaderRegexCharReflection.pattern]
mul r\d+\.\w+, r\d+\.\w+,[^.]*\.\w+\n
mad o\d+\.\w+, r\d+\.\w+, cb\d+\[\d+\]\.\w+, r\d+\.\w+\n
mov o\d+\.\w+, l\(\d+\.\d+\)\n

[ShaderRegexCharOutline]
shader_model = ps_5_0
run = CommandListOutline
[ShaderRegexCharOutline.pattern]
ne r\d\.\w+, l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\), -?cb\d\[\d+\]\.\w+\n
add r\d\.\w+, v\d\.\w+, l\(-?\d*\.?\d+\)\n
lt r\d\.\w+, r\d\.\w+, l\(-?\d*\.?\d+\)\n
and r\d\.\w+, r\d\.\w+, r\d\.\w+\n
discard_nz r\d\.\w+\n
ne r\d\.\w+, l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\), -?cb\d\[\d+\]\.\w+\n
if_nz[\s\S]+^endif\n
sample_indexable\(texture\dd\)\(float,float,float,float\) r\d\.\w+, v\d\.\w+, t\d\.\w+, s\d\n
eq r\d\.\w+, -?cb\d\[\d+\]\.\w+, l\(-?\d*\.?\d+\)\n
add r\d\.\w+, r\d\.\w+, -?cb\d\[\d+\]\.\w+\n
lt r\d\.\w+, r\d\.\w+, l\(-?\d*\.?\d+\)\n
and r\d\.\w+, r\d\.\w+, r\d\.\w+\n
discard_nz r\d\.\w+\n
(?:(?:ne r\d\.\w+, l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\), -?cb\d\[\d+\]\.\w+\n)+(?:or r\d\.\w+, r\d\.\w+, r\d\.\w+\n)*)+
if_nz[\s\S]+^endif\n
ne r\d\.\w+, l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\), -?cb\d\[\d+\]\.\w+\n
mul r\d\.\w+, -?cb\d\[\d+\]\.\w+, l\(-?\d*\.?\d+\)\n
movc o\d\.\w+, r\d\.\w+, r\d\.\w+, r\d\.\w+\n
mad o\d\.\w+, v\d\.\w+, l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\), l\(-?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+, -?\d*\.?\d+\)\n
(?:mov o\d\.\w+, l\(-?\d*\.?\d+\)\n
mov o\d\.\w+, r\d\.\w+\n)+
(?:mov o\d\.\w+, -?cb\d\[\d+\]\.\w+\n
mov o\d\.\w+, l\(-?\d*\.?\d+\)\n)+

; OPTIONAL: shader hash for reflection. replace this incase regex does not work.
;[ShaderOverrideReflectionTexture]
;hash=26eb354bad491b6f
;allow_duplicate_hash=overrule
;run=CommandListReflectionTexture

; OPTIONAL: shader hash for outline. replace this incase regex does not work.
;[ShaderOverrideOutlineTexture]
;hash=c72470bbf959ff35
;allow_duplicate_hash=overrule
;run=CommandListOutline

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

[CommandListOutline]
if $CharacterIB != 0
    if $CharacterIB == 1
        ps-t1 = copy ResourceRefHeadLightMap
    else if $CharacterIB == 2
        ps-t1 = copy ResourceRefBodyLightMap
    else if $CharacterIB == 3
        ps-t1 = copy ResourceRefDressLightMap
    else if $CharacterIB == 4
        ps-t1 = copy ResourceRefExtraLightMap
    endif
drawindexed=auto
$CharacterIB = 0
endif
```

Add these lines to the end of the corresponding [TextureOverride] section
```ini
[TextureOverrideCharacterHead]
$CharacterIB = 1
ResourceRefHeadDiffuse = reference ps-t1
ResourceRefHeadLightMap = reference ps-t2

[TextureOverrideCharacterBody]
$CharacterIB = 2
ResourceRefBodyDiffuse = reference ps-t1
ResourceRefBodyLightMap = reference ps-t2

[TextureOverrideCharacterDress]
$CharacterIB = 3
ResourceRefDressDiffuse = reference ps-t1
ResourceRefDressLightMap = reference ps-t2

[TextureOverrideCharacterExtra]
$CharacterIB = 4
ResourceRefExtraDiffuse = reference ps-t1
ResourceRefExtraLightMap = reference ps-t2
```

If you use Scaramouche/Wanderer or any other character that has special object parts with shared IB hashes, please include their hash and set the $CharacterIB variable to the appropriate value for your mod ($CharacterIB = 0 if you did not want to modify that special object part).
```ini
[TextureOverrideWandererHatIB]
hash = 99be9547
$CharacterIB = 0
; this is Wanderer's normal hat IB
[TextureOverrideWandererHat2IB]
hash = 676cc015
$CharacterIB = 0
; this is Wanderer's hat IB while flying
```
Credits to Discord users HummyR#8131, Modder4869#4818, and Takoyaki#0697.
Also huge thanks to 3dmigoto developers.
