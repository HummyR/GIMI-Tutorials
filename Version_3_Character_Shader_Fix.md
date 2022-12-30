## 3.0+ Character Shader Fix

For fixing green reflections and broken outlines colors on 3.0+ characters. Please credit https://discord.gg/agmg if you use this code


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
discard_n\w+ r\d\.\w+\n
lt r\d\.\w+, l\(0\.010000\), r\d\.\w+\n
and r\d\.\w+, r\d\.\w+, r\d\.\w+\n

[ShaderRegexCharOutline]
shader_model = ps_5_0
run = CommandListOutline
[ShaderRegexCharOutline.pattern]
mov o0\.w, l\(0\)\n
mov o1\.xyz, r0\.xyzx\n

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

Credits to Discord users HummyR#8131, Modder4869#4818, and Takoyaki#0697.
Also huge thanks to 3dmigoto developers.
