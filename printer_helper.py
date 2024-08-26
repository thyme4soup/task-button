import notion_helper
from PIL import Image, ImageDraw, ImageFont
import qrcode
import cv2
import os
import time

image_path = "images/out.png"
# create images folder if it doesn't exist
os.makedirs("images", exist_ok=True)
image_width = 384


def switch_printer(power_switch):
    print("Toggling printer")
    power_switch.on()
    time.sleep(2)
    power_switch.off()
    time.sleep(5)


# get a task and turn it into an image
def get_task_as_image(task):
    title = notion_helper.unwrap_notion_prop(task["properties"]["Name"])
    url = task["url"]

    # create a QR code of the url
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2,
    )
    qr.add_data(url)
    qr.make()
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Use the full width of the image for title
    fontsize = 1
    font_path = os.path.join(cv2.__path__[0], "qt", "fonts", "DejaVuSans.ttf")
    font = ImageFont.truetype(font_path, size=fontsize)
    while font.getsize(title)[0] < image_width - 10:
        fontsize += 1
        font = ImageFont.truetype(font_path, size=fontsize)
    fontsize -= 2  # decrement just in case
    font = ImageFont.truetype(font_path, size=fontsize)

    # create an image with the title and url qr code
    # using PIL
    image = Image.new(
        "RGB", (image_width, qr_image.size[1] + fontsize + 10), (255, 255, 255)
    )
    draw = ImageDraw.Draw(image)
    draw.text((10, 5), title, fill="black", font=font)
    image.paste(qr_image, (image_width // 2 - qr_image.size[0] // 2, fontsize + 10))

    # save the image to the image_path
    image.save(image_path)
    # return the image_path
    return image_path


def print_task(task):
    image_path = get_task_as_image(task)
    # print the image
    print(f"Printing {image_path}")
    command = f"../catprinter/print.py {image_path} -d GB02 -b none -t"
    for i in range(3):
        if os.system(command) == 0:
            return True
        else:
            print("Failed to print")
    print("Failed to print after 3 attempts")
    return False
