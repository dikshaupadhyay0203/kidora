from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image_path: str, text: str):
    """Adds centered, large text with a colored background at the bottom of the image."""
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Create a new image with extra height for the text area
    extra_height = 150
    new_height = height + extra_height
    new_image = Image.new("RGB", (width, new_height), (255, 255, 255))
    new_image.paste(image, (0, 0))

    # Draw text background rectangle with themed color
    draw = ImageDraw.Draw(new_image)
    background_color = (240, 230, 140)  # Soft yellow like a fairy tale book
    draw.rectangle([(0, height), (width, new_height)], fill=background_color)

    # Load a readable, large font
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    # Wrap text nicely
    max_width = width - 40
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    # Center each line
    y_text = height + 10
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x_text = (width - text_width) / 2
        draw.text((x_text, y_text), line, font=font, fill="black")
        y_text += font.getbbox(line)[3] - font.getbbox(line)[1] + 5

    # Save over original
    new_image.save(image_path)

# add_text_to_image("/home/mithun-arulmani/ghostdrive/django/ai_prototype/images/3.png", "A detective duck wearing a detective costume, solving a case in a small town.")
