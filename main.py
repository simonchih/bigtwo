"""Emerald Crown Big Two. Run with Python 3.10+ and pygame-ce."""
import argparse
import math
import os
from pathlib import Path
import random
import pygame
from game import Game, NAMES, classify
from theme import ROOT, GOLD, IVORY, crown, font, panel, suit

SIZE = (1280, 720)
PLAYERS = ['你', '東家', '北家', '西家']


class App:
    def __init__(self, seed=None):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
        pygame.display.set_caption('大老二 · EMERALD CROWN')
        self.canvas = pygame.Surface(SIZE)
        self.clock = pygame.time.Clock()
        self.fonts = {n: font(n) for n in (13,15,17,19,22,28,38,52)}
        self.title_font = font(30,True)
        def load(name,size):
            return pygame.transform.smoothscale(pygame.image.load(str(ROOT/'Image'/name)).convert_alpha(),size)
        self.background = load('table.png',SIZE)
        self.icon = load('simpybigtwo_default.png',(58,58))
        pygame.display.set_icon(self.icon)
        self.back = load('card_back.png',(54,76))
        self.cards = {}
        for c in range(52):
            rank = (c//4+1)%13+1
            self.cards[c] = load(f'{rank:02d}{"cdhs"[c%4]}.png',(96,136))
        self.shadow = pygame.Surface((108,148),pygame.SRCALPHA)
        for i in range(6):
            pygame.draw.rect(self.shadow,(0,0,0,8+i*5),(i,i,108-2*i,148-2*i),border_radius=13)
        self.buttons = {'hint':pygame.Rect(431,656,125,40),'pass':pygame.Rect(570,656,125,40),
                        'play':pygame.Rect(709,656,150,40),'restart':pygame.Rect(1030,48,112,35),
                        'help':pygame.Rect(1151,48,65,35)}
        self.running = True
        self.help = False
        self.particles = []
        self.flights = []
        self.elapsed = 0
        self.reset(seed)

    def reset(self,seed=None):
        self.game = Game(seed)
        self.selected = set()
        self.lifts = {}
        self.hitboxes = []
        self.flights.clear()
        self.particles.clear()
        self.ai_due = 1.2
        self.deal_age = 0
        self.message = '持有梅花 3 的玩家先出牌'
        self.message_time = 4
        self.winner_age = 0

    def text(self,text,pos,size=19,color=IVORY,center=False):
        image=self.fonts[size].render(text,True,color)
        self.canvas.blit(image,image.get_rect(center=pos) if center else pos)

    def notify(self,message):
        self.message=message
        self.message_time=3

    def burst(self,position,count=24):
        for _ in range(count):
            angle=random.uniform(0,math.tau)
            speed=random.uniform(35,170)
            self.particles.append([float(position[0]),float(position[1]),math.cos(angle)*speed,
                                   math.sin(angle)*speed,random.uniform(.5,1.3),random.choice([GOLD,IVORY,(112,206,165)])])

    def play(self,cards):
        actor=self.game.turn
        origins={c:rect.topleft for c,rect in self.hitboxes}
        if not self.game.play(cards):
            self.notify('首手必須包含梅花 3' if self.game.opening else '牌型不合法，或無法壓過桌面的牌')
            return
        target_x=640-(96+(len(cards)-1)*49)/2
        for i,c in enumerate(self.game.table):
            source=origins.get(c,(592,520)) if actor==0 else {1:(1095,312),2:(613,149),3:(90,312)}[actor]
            self.flights.append([c,source,(target_x+i*49,300),0])
        self.selected.clear()
        self.burst((640,365))
        self.notify(f'{PLAYERS[actor]}出了{NAMES[classify(cards)[0]]}')
        self.ai_due=.95
        if self.game.winner is not None:self.burst((640,290),110)

    def pass_turn(self):
        actor=self.game.turn
        if self.game.pass_turn():
            self.selected.clear()
            self.notify(f'{PLAYERS[actor]}略過' if self.game.table else f'{PLAYERS[self.game.turn]}重新領牌')
            self.ai_due=.85
        else:self.notify('領牌時不能略過，請選擇牌出牌')

    def action(self,action):
        if action=='restart':
            self.reset()
            return
        if action=='help':
            self.help=not self.help
            return
        if self.help or self.game.winner is not None or self.game.turn!=0:return
        if action=='hint':
            self.selected=set(self.game.suggest())
            if not self.selected:self.notify('目前沒有可出的牌，可以略過')
        elif action=='pass':self.pass_turn()
        elif action=='play':self.play(sorted(self.selected))

    def mouse_position(self,pos):
        w,h=self.screen.get_size()
        scale=min(w/SIZE[0],h/SIZE[1])
        return ((pos[0]-(w-SIZE[0]*scale)/2)/scale,(pos[1]-(h-SIZE[1]*scale)/2)/scale)

    def event(self,event):
        if event.type==pygame.QUIT:self.running=False
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                if self.help:self.help=False
                else:self.running=False
            else:
                keymap={pygame.K_RETURN:'play',pygame.K_SPACE:'pass',pygame.K_h:'hint',pygame.K_r:'restart',pygame.K_F1:'help'}
                if event.key in keymap:self.action(keymap[event.key])
        elif event.type==pygame.MOUSEBUTTONDOWN:
            p=self.mouse_position(event.pos)
            if self.help:
                self.help=False
                return
            if event.button==3:self.action('play' if self.selected else 'pass')
            elif event.button==1:
                for action,rect in self.buttons.items():
                    if rect.collidepoint(p):
                        self.action(action)
                        return
                if self.game.turn==0 and self.game.winner is None:
                    for c,rect in reversed(self.hitboxes):
                        if rect.collidepoint(p):
                            if c in self.selected:self.selected.remove(c)
                            else:self.selected.add(c)
                            self.burst((rect.centerx,rect.top),7)
                            break

    def update(self,dt,autoplay=False):
        self.elapsed+=dt
        if self.help:return
        self.deal_age+=dt
        self.message_time=max(0,self.message_time-dt)
        for c in self.game.hands[0]:
            target=25 if c in self.selected else 0
            self.lifts[c]=self.lifts.get(c,0)+(target-self.lifts.get(c,0))*min(1,dt*16)
        for flight in self.flights:flight[3]+=dt
        self.flights=[f for f in self.flights if f[3]<.42]
        for p in self.particles:
            p[0]+=p[2]*dt;p[1]+=p[3]*dt;p[3]+=100*dt;p[4]-=dt
        self.particles=[p for p in self.particles if p[4]>0]
        if self.game.winner is not None:
            self.winner_age+=dt
            if self.winner_age<4 and random.random()<dt*9:
                self.burst((random.randint(260,1020),random.randint(170,350)),12)
            return
        self.ai_due-=dt
        if (self.game.turn!=0 or autoplay) and self.ai_due<=0:
            cards=self.game.suggest()
            if cards:self.play(cards)
            else:self.pass_turn()

    def opponent(self,player,x,y):
        active=self.game.turn==player and self.game.winner is None
        panel(self.canvas,pygame.Rect(x,y,136,63),border=GOLD if active else (49,95,73))
        if active:pygame.draw.circle(self.canvas,GOLD,(x+17,y+19),4+int(math.sin(self.elapsed*4)>0))
        self.text(PLAYERS[player],(x+30,y+7),19)
        self.text(f'{len(self.game.hands[player]):02d} 張手牌',(x+30,y+34),15,(169,196,172))
        if player in self.game.passed:self.text('PASS',(x+102,y+17),13,GOLD,True)

    def draw(self):
        s=self.canvas
        s.blit(self.background,(0,0))
        veil=pygame.Surface(SIZE,pygame.SRCALPHA)
        pygame.draw.ellipse(veil,(3,32,23,92),(222,219,836,262))
        pygame.draw.ellipse(veil,(222,184,99,65),(222,219,836,262),1)
        s.blit(veil,(0,0))
        s.blit(self.icon,(51,42))
        s.blit(self.title_font.render('EMERALD CROWN',True,IVORY),(124,44))
        self.text('大 老 二   /   T A I W A N   B I G   T W O',(126,80),13,GOLD)
        self.opponent(2,572,93)
        self.opponent(1,1060,247)
        self.opponent(3,84,247)
        for p in (1,2,3):
            hand=self.game.hands[p]
            for i in range(len(hand)):
                if p==2:pos=(640-(54+(len(hand)-1)*19)/2+i*19,167)
                else:pos=((1101 if p==1 else 125),324+i*5)
                if self.deal_age>i*.035:s.blit(self.back,pos)
        if not self.game.table:
            crown(s,(640,320),72,(165,143,81))
            self.text('EMERALD  CROWN',(640,378),19,(145,173,133),True)
            self.text('梅花 3 先出' if self.game.opening else '新一輪 · 自由領牌',(640,407),15,GOLD,True)
        else:
            cards=self.game.table
            self.text(f'{PLAYERS[self.game.owner]}  /  {NAMES[classify(cards)[0]]}',(640,270),17,GOLD,True)
            x=640-(96+(len(cards)-1)*49)/2
            flying={f[0] for f in self.flights}
            for i,c in enumerate(cards):
                if c not in flying:
                    s.blit(self.shadow,(x+i*49-3,303))
                    s.blit(self.cards[c],(x+i*49,300))
        for c,start,end,age in self.flights:
            t=1-(1-min(1,age/.42))**3
            pos=(start[0]+(end[0]-start[0])*t,start[1]+(end[1]-start[1])*t-45*math.sin(t*math.pi))
            s.blit(self.shadow,(pos[0]-3,pos[1]+3));s.blit(self.cards[c],pos)
        status=self.message if self.message_time else ('輪到你了 · 點選手牌，再按出牌' if self.game.turn==0 else f'{PLAYERS[self.game.turn]}正在思考…')
        self.text(status,(640,467),17,IVORY,True)
        hand=self.game.hands[0]
        self.text(f'你的手牌  /  {len(hand):02d}',(72,532),19,GOLD)
        self.text('已選擇 '+str(len(self.selected))+' 張',(72,562),15,(163,195,174))
        if 0 in self.game.passed:self.text('本輪已略過',(72,588),15,GOLD)
        self.hitboxes=[]
        step=44
        x=640-(96+(len(hand)-1)*step)/2
        mouse=self.mouse_position(pygame.mouse.get_pos())
        for i,c in enumerate(hand):
            y=510-self.lifts.get(c,0)+max(0,1-(self.deal_age-i*.035)/.4)*190
            rect=pygame.Rect(x+i*step,y,96,136)
            if c in self.selected:pygame.draw.rect(s,GOLD,rect.inflate(6,6),border_radius=10)
            s.blit(self.shadow,(rect.x-3,rect.y+3));s.blit(self.cards[c],rect)
            self.hitboxes.append((c,rect))
        labels={'hint':'提示  H','pass':'略過  Space','play':'出牌  Enter','restart':'重新開局  R','help':'規則'}
        for name,rect in self.buttons.items():
            enabled=name in ('restart','help') or (self.game.turn==0 and self.game.winner is None and not self.help)
            if name=='play':enabled=enabled and self.game.legal(tuple(self.selected))
            if name=='pass':enabled=enabled and bool(self.game.table)
            primary=name=='play' and enabled
            fill=(224,187,104) if primary else ((25,75,53) if enabled and rect.collidepoint(mouse) else (9,40,30))
            panel(s,rect,fill,GOLD if enabled else (48,82,61),9)
            self.text(labels[name],rect.center,15,(21,42,29) if primary else (IVORY if enabled else (115,140,120)),True)
        self.text('左鍵選牌 · 右鍵出牌 / 略過',(77,662),13,(168,192,161))
        for kind in range(4):
            suit(s,kind,(1052+kind*43,671),6,GOLD)
            if kind<3:self.text('<',(1070+kind*43,661),15,GOLD)
        if self.game.winner is not None:self.draw_winner()
        fx=pygame.Surface(SIZE,pygame.SRCALPHA)
        for x,y,vx,vy,life,color in self.particles:
            pygame.draw.circle(fx,(*color,min(255,int(life*255))),(int(x),int(y)),2 if life<.6 else 3)
        s.blit(fx,(0,0))
        if self.help:self.draw_help()
        w,h=self.screen.get_size()
        scale=min(w/1280,h/720)
        size=(max(1,int(1280*scale)),max(1,int(720*scale)))
        self.screen.fill((4,18,13))
        self.screen.blit(pygame.transform.smoothscale(s,size),((w-size[0])//2,(h-size[1])//2))
        pygame.display.flip()

    def overlay(self,rect):
        shade=pygame.Surface(SIZE,pygame.SRCALPHA);shade.fill((0,12,8,185))
        self.canvas.blit(shade,(0,0));panel(self.canvas,pygame.Rect(rect),border=GOLD,radius=22)

    def draw_winner(self):
        self.overlay((405,227,470,250))
        crown(self.canvas,(640,283),66)
        self.text('你贏了！' if self.game.winner==0 else f'{PLAYERS[self.game.winner]}獲勝',(640,343),38,GOLD,True)
        self.text('本局結束 · 按 R 或右上角重新開局',(640,414),17,IVORY,True)

    def draw_help(self):
        self.overlay((284,131,712,459))
        self.text('台灣大老二 · 遊戲規則',(640,178),28,GOLD,True)
        lines=['牌序：3 < 4 < … < K < A < 2；花色：梅花 < 方塊 < 紅心 < 黑桃。',
               '首手必須包含梅花 3，最先出完手牌者獲勝。',
               '可出單張、對子、順子、葫蘆、鐵支、同花順，以及一條龍。',
               '葫蘆與順子不能互壓；鐵支、同花順可壓兩者。不能出三條。',
               '順子 A2345 最小、23456 最大；葫蘆比三張，鐵支比四張。',
               '鐵支與同花順可壓單張、對子；一條龍可壓其他牌型。',
               '略過後退出本輪；其他三家略過，由最後出牌者重新領牌。',
               '左鍵選牌 / Enter 出牌 / Space 略過 / H 提示 / R 重新開局。']
        for i,line in enumerate(lines):self.text(line,(316,226+i*35),17)
        self.text('點擊任意位置或按 Esc 返回',(640,554),15,GOLD,True)

    def run(self,frames=0,autoplay=False,screenshot=None):
        count=0
        while self.running:
            dt=min(self.clock.tick(60)/1000,.05)
            for event in pygame.event.get():self.event(event)
            self.update(dt,autoplay)
            self.draw()
            count+=1
            if frames and count>=frames:break
        if screenshot:
            path=Path(screenshot);path.parent.mkdir(parents=True,exist_ok=True)
            pygame.image.save(self.canvas,str(path))
        pygame.quit()


def main():
    parser=argparse.ArgumentParser(description='Emerald Crown Big Two')
    parser.add_argument('--frames',type=int,default=0,help='Exit after N frames (smoke test)')
    parser.add_argument('--seed',type=int)
    parser.add_argument('--autoplay',action='store_true')
    parser.add_argument('--screenshot')
    parser.add_argument('--headless',action='store_true')
    args=parser.parse_args()
    if args.headless:
        os.environ['SDL_VIDEODRIVER']='dummy'
        os.environ['SDL_AUDIODRIVER']='dummy'
    App(args.seed).run(args.frames,args.autoplay,args.screenshot)


if __name__=='__main__':
    main()
