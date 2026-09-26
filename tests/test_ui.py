import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
import pygame
from main import App
from game import Game
from theme import ROOT

class UITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=App(7)
    @classmethod
    def tearDownClass(cls):pygame.quit()

    def test_assets(self):
        for path in (ROOT/'Image').iterdir():
            if path.suffix in ('.png','.gif','.jpg','.ico'):
                self.assertGreater(pygame.image.load(str(path)).get_width(),0,path.name)

    def test_interaction_and_round(self):
        a=self.app
        seed=next(i for i in range(30) if Game(i).turn==0)
        a.reset(seed);a.deal_age=2;a.draw()
        a.event(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=(a.hitboxes[0][1].x+10,530)))
        self.assertEqual(len(a.selected),1)
        a.event(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_h))
        self.assertTrue(a.game.legal(tuple(a.selected)))
        a.event(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_RETURN))
        self.assertFalse(a.game.opening)
        self.assertTrue(a.flights)
        a.draw()
        for _ in range(300):
            if a.game.winner is not None:break
            a.ai_due=0;a.update(.05,autoplay=True);a.draw()
        self.assertIsNotNone(a.game.winner)
        pygame.image.save(a.canvas,str(ROOT/'art/victory.png'))
        a.event(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_r))
        self.assertIsNone(a.game.winner)
        self.assertEqual(len(a.game.hands[0]),13)
        a.event(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_F1))
        turn=a.game.turn;a.update(3);self.assertEqual(a.game.turn,turn)
        a.draw();pygame.image.save(a.canvas,str(ROOT/'art/rules.png'))
        a.event(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_ESCAPE))
        self.assertFalse(a.help)
        a.screen=pygame.display.set_mode((960,600),pygame.RESIZABLE);a.draw()
        self.assertAlmostEqual(a.mouse_position((480,300))[0],640)
        self.assertAlmostEqual(a.mouse_position((480,300))[1],360)
        a.event(pygame.event.Event(pygame.QUIT))
        self.assertFalse(a.running)

if __name__=='__main__':unittest.main()
