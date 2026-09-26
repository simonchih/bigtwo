"""Native high-resolution card and UI artwork for the Emerald Crown theme."""
from pathlib import Path
import math
import pygame

ROOT = Path(__file__).resolve().parent
GOLD = (225, 189, 108)
IVORY = (250, 243, 224)
INK = (25, 35, 31)
RED = (177, 35, 43)


def font(size, serif=False):
    if serif:
        path = pygame.font.match_font('georgia,timesnewroman,dejavuserif')
    else:
        path = pygame.font.match_font('microsoftjhenghei,notosanscjk,wenquanyizenhei')
    return pygame.font.Font(path or str(ROOT / 'FreeSansBold.ttf'), size)


def suit(surface, kind, center, size, color):
    x, y = center
    r = size
    if kind == 1:
        pygame.draw.polygon(surface, color, [(x, y-r), (x+r*.72, y), (x, y+r), (x-r*.72, y)])
    elif kind == 2:
        pygame.draw.circle(surface, color, (int(x-r*.42), int(y-r*.3)), int(r*.57))
        pygame.draw.circle(surface, color, (int(x+r*.42), int(y-r*.3)), int(r*.57))
        pygame.draw.polygon(surface, color, [(x-r*.95, y-r*.1), (x+r*.95, y-r*.1), (x, y+r)])
    elif kind == 3:
        pygame.draw.polygon(surface, color, [(x, y-r), (x-r*.93, y+r*.1), (x+r*.93, y+r*.1)])
        for dx in (-.43, .43):
            pygame.draw.circle(surface, color, (int(x+dx*r), int(y+r*.14)), int(r*.51))
        pygame.draw.polygon(surface, color, [(x, y), (x-r*.37, y+r), (x+r*.37, y+r)])
    else:
        for dx, dy in ((0, -.5), (-.48, .15), (.48, .15)):
            pygame.draw.circle(surface, color, (int(x+dx*r), int(y+dy*r)), int(r*.52))
        pygame.draw.polygon(surface, color, [(x, y), (x-r*.36, y+r), (x+r*.36, y+r)])


def crown(surface, center, width, color=GOLD):
    x, y = center
    w = width
    points = [(x-w*.5,y-w*.25), (x-w*.27,y-w*.07), (x,y-w*.43),
              (x+w*.27,y-w*.07), (x+w*.5,y-w*.25), (x+w*.35,y+w*.22), (x-w*.35,y+w*.22)]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.line(surface, (255,237,171), (x-w*.32,y+w*.3), (x+w*.32,y+w*.3), max(1,int(w*.055)))


def card_art(rank, kind):
    # Code-native artwork is rendered at 3x for crisp edges and exact indices.
    s = pygame.Surface((288, 408), pygame.SRCALPHA)
    pygame.draw.rect(s, (180,151,95), (2,2,284,404), border_radius=23)
    pygame.draw.rect(s, IVORY, (5,5,278,398), border_radius=21)
    for y in range(10,398):
        t = y/408
        color = (int(255-12*t), int(252-16*t), int(240-24*t))
        pygame.draw.line(s, color, (15,y), (272,y))
    pygame.draw.rect(s, (225,207,166), (15,15,258,378), 2, border_radius=16)
    pygame.draw.rect(s, (255,253,242), (20,20,248,368), 2, border_radius=14)
    color = RED if kind in (1,2) else INK
    label = {1:'A',11:'J',12:'Q',13:'K'}.get(rank,str(rank))
    index = pygame.Surface((66,117),pygame.SRCALPHA)
    text = font(65 if rank != 10 else 52,True).render(label,True,color)
    index.blit(text,text.get_rect(center=(33,39)))
    suit(index,kind,(33,91),19,color)
    s.blit(index,(19,14))
    s.blit(pygame.transform.rotate(index,180),(203,277))
    if rank in (11,12,13):
        pygame.draw.polygon(s,(229,213,176),[(144,115),(211,204),(144,293),(77,204)],3)
        crown(s,(144,152),63)
        suit(s,kind,(144,223),46,color)
    else:
        suit(s,kind,(144,209),62,color)
    return s


def panel(surface, rect, fill=(9,39,31), border=GOLD, radius=14):
    pygame.draw.rect(surface,fill,rect,border_radius=radius)
    pygame.draw.rect(surface,border,rect,1,border_radius=radius)
