from PIL import Image, ImageDraw, ImageFont

def make_icon(size, path):
    img = Image.new("RGB", (size, size), "#1e293b")
    draw = ImageDraw.Draw(img)
    # gradient-ish background using two tones (simple radial approx via ellipse)
    for r in range(size, 0, -4):
        t = r / size
        color = (
            int(30 + (220 - 30) * (1 - t)),
            int(41 + (90 - 41) * (1 - t)),
            int(59 + (60 - 59) * (1 - t)),
        )
        bbox = [(size - r) / 2, (size - r) / 2, (size + r) / 2, (size + r) / 2]
        draw.ellipse(bbox, fill=color)

    text = "CC"
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size * 0.38))
    except Exception:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - w) / 2 - bbox[0], (size - h) / 2 - bbox[1]), text, fill="white", font=font)
    img.save(path)

make_icon(192, "/tmp/carecap/webapp/icon-192.png")
make_icon(512, "/tmp/carecap/webapp/icon-512.png")
print("done")
