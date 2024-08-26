import notion_helper
import printer_helper
import time
import random
import threading
import math
from gpiozero import LED, Button, PWMLED

button = Button(4)
led = PWMLED(2)
power_switch = LED(17)
last_button_press = time.gmtime(0)


def should_button_flash():
    # check if we're in productive hours (7pm-10pm pacific) and last button press was more than 12 hours ago
    now = time.localtime()
    print(now)
    if now.tm_hour < 3 or now.tm_hour > 6:
        return False
    if time.mktime(now) - time.mktime(last_button_press) < 43200:
        return False
    return True


def get_random_task():
    db = notion_helper.get_database_object()
    items = []
    while True:
        items.extend([result for result in db["results"]])
        if db["has_more"]:
            time.sleep(0.1)
            db = notion_helper.get_database_object(start_cursor=db["next_cursor"])
        else:
            break

    if (len(items)) > 0:
        print(f"Picking from {len(items)} items")
        return random.choice(items)
    else:
        print("No items found")
        return None


def glow_led(e):
    x = 0
    print("glowing led")
    while not e.is_set():
        led.value = -1 * math.cos(x) * 0.5 + 0.5
        time.sleep(0.01)
        x = min(x + 0.01, 1000000000)
    print("stopping led")
    led.value = 0


if __name__ == "__main__":
    print("running button loop")
    print("Button pressed!")
    e = None
    t = None

    while True:
        if should_button_flash() and not (t and t.is_alive()):
            e = threading.Event()
            t = threading.Thread(name="button-light", target=glow_led, args=(e,))
            t.start()
        if button.wait_for_press(timeout=5):
            if e:
                e.set()
            led.off()
            printer_helper.switch_printer(power_switch)
            task = get_random_task()
            if printer_helper.print_task(task):
                last_button_press = time.localtime()
            printer_helper.switch_printer(power_switch)
