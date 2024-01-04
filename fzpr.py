#!/usr/bin/env python

from pathlib import Path

import fontforge
from fontforge import font as Font

L_PARENS = '〈《「『【〔〖〘〝（［｛｟'
R_PARENS = '〉》」』】〕〗〙〞）］｝｠'
SHIFT = 0.17  # in em, 我自己测量的


def glyph_h_shift(font: Font, char: str, shift: float) -> None:
    print(f'Shifting char: {char} by {shift}em')
    if ord(char) not in font:
        print(f'Char {char} not found in font')
        return
    glyph = font[ord(char)]
    layer = glyph.foreground
    for curve in layer:
        for point in curve:
            point.x += glyph.width * shift
    glyph.setLayer(layer, 'Fore')


def patch_font(file: Path) -> None:
    print(f'Patching font: {file}')
    font = fontforge.open(file.name)
    print(f'Font name: {font.fullname}')
    font.fontname += '-Patched'
    font.fullname += '-Patched'
    font.familyname += '-Patched'
    for c in L_PARENS:
        glyph_h_shift(font, c, SHIFT)
    for c in R_PARENS:
        glyph_h_shift(font, c, -SHIFT)
    font.generate(f'{file.stem}_Patched.ttf')
    font.close()


if __name__ == '__main__':
    files = 'FZFSK.ttf FZHTK.TTF FZKTK.ttf FZLSK.ttf FZSSK.ttf FZXSSK.ttf FZXBSK.ttf FZXH1K.ttf FZY1K.ttf FZY3K.ttf'
    for fn in files.split():
        patch_font(Path(fn))
