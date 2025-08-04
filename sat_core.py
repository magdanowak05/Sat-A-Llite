from PIL import Image, ImageDraw, ImageFont
import os
import re

def extract_datetime(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2})[ _](\d{6})', filename)
    if match:
        date_part = match.group(1)
        time_raw = match.group(2)
        time_part = f"{time_raw[:2]}:{time_raw[2:4]}:{time_raw[4:]}"
        return f"{date_part} {time_part}"
    return "Brak daty"

def generate_collage(image_paths, sat_model, orbit, output_path):
    if len(image_paths) != 4:
        raise ValueError("Musisz podać dokładnie 4 obrazy.")

    images = [Image.open(path).convert("RGB") for path in image_paths]
    base_size = images[0].size
    images = [img.resize(base_size) for img in images]

    w, h = base_size
    half_w, half_h = w // 2, h // 2

    crops = [
        images[0].crop((0, 0, half_w, half_h)),           # lewy górny
        images[1].crop((half_w, 0, w, half_h)),           # prawy górny
        images[2].crop((0, half_h, half_w, h)),           # lewy dolny
        images[3].crop((half_w, half_h, w, h))            # prawy dolny
    ]

    collage = Image.new("RGB", base_size)
    collage.paste(crops[0], (0, 0))
    collage.paste(crops[1], (half_w, 0))
    collage.paste(crops[2], (0, half_h))
    collage.paste(crops[3], (half_w, half_h))

    draw = ImageDraw.Draw(collage)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    positions = [
        (10, 10),
        (half_w + 10, 10),
        (10, half_h + 10),
        (half_w + 10, half_h + 10)
    ]

    for pos, path in zip(positions, image_paths):
        dt = extract_datetime(os.path.basename(path))
        draw.text(pos, dt, font=font, fill=(255, 255, 0))

    collage.save(output_path)
    return output_path
