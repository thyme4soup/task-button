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
    # check if we're in productive hours and last button press
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


def glow_led():
    x = 0
    while not e.is_set():
        led.value = max(math.sin(x), 0)
        time.sleep(0.1)


if __name__ == "__main__":
    print("running button loop")
    print("Button pressed!")
    e = threading.Event()
    t = threading.Thread(name="button-light", target=glow_led, args=(e, 2))

    while True:
        if should_button_flash() and not t.is_alive():
            t.start()
        if button.wait_for_press(timeout=5):
            e.set()
            led.off()
            printer_helper.switch_printer(power_switch)
            task = get_random_task()
            printer_helper.print_task(task)
            printer_helper.switch_printer(power_switch)
