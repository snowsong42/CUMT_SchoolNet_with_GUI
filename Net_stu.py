import pyautogui as pg
pg.hotkey('win','d',interval=0)
pg.moveTo(39, 292)
pg.click(x=39, y=292,clicks=1,interval=0,duration=0, button='left')
pg.press('enter',presses=1,interval=0.2)

pg.write("http://10.2.5.251/",interval=0)
pg.press('enter',presses=2,interval=0.2)
pg.PAUSE = 1.0

pg.moveTo(1379, 343)
pg.click(x=1379, y=343,clicks=2,interval=0.3,duration=0, button='left')
pg.write("06245011",interval=0)
pg.press('tab',presses=1,interval=0)
pg.write("Snowsong_42",interval=0)

pg.click(x=1437 , y=481,clicks=1,interval=0,duration=0, button='left')
pg.click(x=1440 , y=586,clicks=1,interval=0,duration=0, button='left')
pg.click(x=1452 , y=533,clicks=1,interval=0,duration=0, button='left')