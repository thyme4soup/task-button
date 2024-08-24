import notion_helper
import printer_helper
import time
import random


def is_button_pressed():
    return False


def get_task_as_image():
    return None


def get_random_task():
    db = notion_helper.get_database_object()
    items = []
    while True:
        items.extend(
            [
                notion_helper.unwrap_notion_prop(result["properties"]["Name"])
                for result in db["results"]
            ]
        )
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
    print(get_random_task())

    while True:
        if is_button_pressed():
            print("Button pressed!")
            task = get_random_task()
            print(task)
        time.sleep(1)
