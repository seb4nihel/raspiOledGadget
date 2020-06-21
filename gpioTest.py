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

async def button_ctl(btn1, btn2, stop_event):
    while True:
        if (btn1.is_pressed and btn2.is_pressed):
            stop_event.set()
        else:
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    # Instance class and start async stuff
    #buttonHandler = ButtonHandler(21, shutdown())
    loop = asyncio.get_event_loop()
    #loop.create_task(buttonHandler)
    shutdown_btn1 = Button(21)
    shutdown_btn2 = Button(16)
    event = asyncio.Event()
    loop.create_task(button_ctl(shutdown_btn1, shutdown_btn2, event))
    loop.create_task(main_loop(event))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('stopping programm')
    finally:
        loop.close()