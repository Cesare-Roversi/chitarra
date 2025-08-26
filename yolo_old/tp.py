from PIL import Image, ImageDraw, ImageFont
import os
import random

output_dir = "digits_images"
os.makedirs(output_dir, exist_ok=True)

fonts = ["ARIALBD.TTF", "arial.ttf"]  # Add paths to your fonts
image_size = (128, 128)
digits = [str(i) for i in range(31)]

for i in range(1000):  # Number of images to generate
    digit = random.choice(digits)
    font_path = random.choice(fonts)
    font_size = random.randint(50, 100)
    font = ImageFont.truetype(font_path, font_size)

    img = Image.new("RGB", image_size, (255, 255, 255))
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), digit, font=font) #solo per sapere la larghezza
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = random.randint(0, image_size[0] - w)
    y = random.randint(0, image_size[1] - h)
    draw.text((x, y), digit, fill=(0, 0, 0), font=font)


    #*Draw lines
    ascent, descent = font.getmetrics()
    baseline = y + (descent+ascent)/2 #boh
    print(f"y {y}, ascent {ascent}, descent {descent} ")#! ????

    line1_end_x = x-4
    line1_y = baseline
    line2_start_x = x+w+4
    line2_y = line1_y

    # Draw left horizontal line
    draw.line([(0, line1_y), (line1_end_x, line1_y)], fill=(0, 0, 0), width=2)
    # Draw right horizontal line
    draw.line([(line2_start_x, line2_y), (image_size[0], line2_y)], fill=(0, 0, 0), width=2)

    #*Draw arches
    arc_height = 40
    arc_width = arc_height * 3
    
    # Position the arc to start from the left side of the number
    arc_right_x = x +w/2  # Same as line1_end_x
    arc_center_y = y - 10      # Top of the number
    
    # Draw an inverted arc (like a mountain or sad face)
    rand = random.random()
    if rand < 0.25:
        draw.arc([(arc_right_x - arc_width, arc_center_y), 
                  (arc_right_x, arc_center_y + arc_height)], 
                 start=180, end=360, fill=(0, 0, 0), width=4)
    
    if rand > 0.25 and rand < 0.5:
        draw.arc([(arc_right_x, arc_center_y), 
                  (arc_right_x + arc_width, arc_center_y + arc_height)], 
                 start=180, end=360, fill=(0, 0, 0), width=4)


    #*INFO X TRAIN
    center_num_x = x + (w / 2)
    center_num_y = baseline
    # draw.ellipse([(center_num_x - 2, baseline-2), (center_num_x + 2, baseline+2)], fill="red")
    # draw.ellipse([(center_num_x - 2, y-2), (center_num_x + 2, y+2)], fill="green")
    # draw.ellipse([(center_num_x - 2, y+descent-2), (center_num_x + 2, y+descent+2)], fill="red")
    # draw.ellipse([(center_num_x - 2, y+ascent-2), (center_num_x + 2, y+ascent+2)], fill="blue")
    # draw.ellipse([(x - 2, baseline -2), (x + 2, baseline +2)], fill="blue")
    # draw.ellipse([(x+w - 2, baseline -2), (x+w + 2, baseline +2)], fill="blue")

    x_center_norm = center_num_x / image_size[0]
    y_center_norm = center_num_y / image_size[1]
    bbox_width_norm = w/image_size[0]
    bbox_height_norm = (ascent-descent) / image_size[1]

    ttt = "train"
    
    label_path = os.path.join("dataset", "labels", ttt, f"{i}_{digit}.txt")
    with open(label_path, "w") as f:
        f.write(f"{digit} {x_center_norm:.6f} {y_center_norm:.6f} {bbox_width_norm} {bbox_height_norm}")

    # img.show()

    images_path = os.path.join("dataset", "images", ttt, f"{i}_{digit}.png")
    img.save(images_path)
