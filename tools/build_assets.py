"""Export native card/UI artwork and replace every legacy image in Image.

The generated table/back originals and supplied icon remain lossless PNGs.
Pillow is used only as an encoder for legacy GIF/JPEG/ICO compatibility.
"""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
from PIL import Image
from theme import ROOT, card_art, GOLD, IVORY, panel, font, suit


def save(surface,path):
    im = Image.frombytes('RGBA',surface.get_size(),pygame.image.tobytes(surface,'RGBA'))
    if path.suffix.lower() in ('.jpg','.gif'):
        im = im.convert('RGB')
    if path.suffix == '.ico':
        im.save(path,bitmap_format="bmp",sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
    else:
        im.save(path)


def build():
    pygame.init()
    pygame.display.set_mode((1,1))
    folder = ROOT/'Image'
    table = pygame.image.load(str(folder/'table.png'))
    back = pygame.image.load(str(folder/'card_back.png'))
    icon = pygame.image.load(str(folder/'simpybigtwo_default.png'))
    for path in list(folder.iterdir()):
        if path.suffix.lower() not in ('.gif','.jpg','.ico'):
            continue
        name = path.stem
        if len(name)==3 and name[:2].isdigit() and name[-1] in 'cdhs':
            art = card_art(int(name[:2]),'cdhs'.index(name[-1]))
            save(art,folder/(name+'.png'))
        elif name.startswith('back'):
            art = pygame.transform.smoothscale(back,(96,136))
        elif name.startswith(('shadow','xshadow')) or name == 'shade':
            art = pygame.Surface((96,136),pygame.SRCALPHA)
            for inset in range(12):
                pygame.draw.rect(art,(5+inset,23+inset,17+inset),(inset,inset,96-2*inset,136-2*inset),border_radius=12)
        elif name.startswith(('bottom','l0')):
            art = pygame.Surface((96,136),pygame.SRCALPHA)
            art.fill((9,48,36))
            pygame.draw.rect(art,GOLD,(3,3,90,130),2,border_radius=12)
            suit(art,3,(48,68),19,GOLD)
        elif name == 'pass':
            art = pygame.Surface((128,48)); panel(art,art.get_rect())
            label=font(23).render('PASS',True,IVORY)
            art.blit(label,label.get_rect(center=(64,24)))
        elif path.suffix=='.ico':
            art=pygame.transform.smoothscale(icon,(256,256))
        else:
            art=pygame.transform.smoothscale(table,(1280,720))
        save(art,path)
    pygame.quit()
    print('Rebuilt all 124 original image assets; exported 52 high-resolution PNG cards.')


if __name__=='__main__':
    build()

