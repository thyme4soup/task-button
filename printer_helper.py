import notion_helper
from PIL import Image, ImageDraw
import qrcode
import os

image_path = "images/out.png"
image_width = 384


# get a task and turn it into an image
def get_task_as_image(task):
    title = notion_helper.unwrap_notion_prop(task["properties"]["Name"])
    url = task["url"]

    # create an image with the title and url
    # using PIL
    image = Image.new("RGB", (image_width, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), title, fill="black")
    draw.text((10, 30), url, fill="black")
    # add a QR code of the url
    # using the qrcode library
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    image.paste(qr_image, (image_width - 64, 0))

    # save the image to the image_path
    image.save(image_path)
    # return the image_path
    return image_path


def print_task(task):
    image_path = get_task_as_image(task)
    # print the image
    print(f"Printing {image_path}")
    command = f"./print.py {image_path} -d GB02 -b none > /dev/null &"
    success = os.system(command)
    print(f"Printed {image_path} with success {success}")
