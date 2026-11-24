#!/usr/bin/env python3
# Regenerates the static "SG Print" fonts from the Schibsted Grotesk variable font.
# Same method used for the printed file (Oct 2026). Requires: pip install fonttools
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
for w, name in [(400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (800, 'ExtraBold')]:
    f = TTFont('SchibstedGrotesk[wght].ttf')
    instancer.instantiateVariableFont(f, {'wght': w}, inplace=True)
    for rec in f['name'].names:
        if rec.nameID in (1, 16): rec.string = 'SG Print'
        if rec.nameID in (2, 17): rec.string = name
        if rec.nameID == 4: rec.string = 'SG Print ' + name
        if rec.nameID == 6: rec.string = 'SGPrint-' + name
    f['OS/2'].usWeightClass = w
    f.save(f'SGPrint-{name}.ttf')
print('ok')
