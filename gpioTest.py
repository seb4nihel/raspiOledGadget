import asyncio
from gpiozero import Button
from subprocess import call

async def main_loop(shutdown_event):
    while True:
        print("main loop")
        if shutdown_event.is_set():
            print("gotcha!")
            shutdown_event.clear()
            call("sudo shutdown now --poweroff", shell=True)
        await asyncio.sleep(5)

async def button_ctl(OledButtons, stop_event):
    while True:
        if (OledButtons.key1.is_pressed and OledButtons.key3.is_pressed):
            stop_event.set()
        else:
            await asyncio.sleep(0.1)
        
class OledButtons:
    def __init__(self, key1 = 21, key2 = 20, key3 = 16, jup = 6, jdown = 19, jleft = 5, jright = 26, jpress = 13):
        self.key1 = Button(key1)
        self.key2 = Button(key2)
        self.key3 = Button(key3)
        self.jup = Button(jup)
        self.jdown = Button(jdown)
        self.jleft = Button(jleft)
        self.jright = Button(jright)
        self.jpress = Button(jpress)

if __name__ == "__main__":
    oledBtns = OledButtons()
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    loop.create_task(button_ctl(oledBtns, event))
    loop.create_task(main_loop(event))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('stopping programm')
    finally:
        loop.close()