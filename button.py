import notion_helper
import printer_helper
import time
import random
from gpiozero import LED, Button

button = Button(4)
led = LED(2)
power_switch = LED(17)


def is_button_pressed():
    return False


def get_task_as_image():
    return None


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


if __name__ == "__main__":
    print("running button loop")
    print("Button pressed!")
    while True:
        led.on()
        if button.wait_for_press():
            led.off()
            printer_helper.switch_printer(power_switch)
            task = get_random_task()
            printer_helper.print_task(task)
            printer_helper.switch_printer(power_switch)
        time.sleep(1)
