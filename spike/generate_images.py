import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/jiaen/Agy/AI Bootcamp/spike"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try fonts
FONT_PATH = "/System/Library/Fonts/Noteworthy.ttc"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"

def create_notebook_background(width=600, height=400, line_spacing=45, margin_x=80):
    # Off-white paper background
    img = Image.new("RGB", (width, height), (252, 252, 250))
    draw = ImageDraw.Draw(img)
    
    # Draw faint horizontal blue ruled lines
    for y in range(line_spacing, height, line_spacing):
        draw.line([(0, y), (width, y)], fill=(210, 225, 240), width=1)
        
    # Draw vertical red margin line
    draw.line([(margin_x, 0), (margin_x, height)], fill=(240, 180, 180), width=2)
    
    return img

def render_sample1():
    # Sample 1 (Correct):
    # Solve 3(x - 4) = 15
    # Line 1: 3x - 12 = 15
    # Line 2: 3x = 27
    # Line 3: x = 9
    img = create_notebook_background(width=640, height=360, line_spacing=45, margin_x=70)
    draw = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.truetype(FONT_PATH, 28)
        font_body = ImageFont.truetype(FONT_PATH, 32)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        
    ink_color = (25, 35, 75) # Dark ballpoint blue ink
    
    lines = [
        ("Solve  3(x - 4) = 15", font_header, 35, 100),
        ("3x - 12 = 15", font_body, 80, 120),
        ("3x = 27", font_body, 125, 120),
        ("x = 9", font_body, 170, 120),
    ]
    
    for text, font, y, x in lines:
        # Add slight natural jitter
        jx = x + random.randint(-1, 1)
        jy = y + random.randint(-1, 1)
        draw.text((jx, jy), text, fill=ink_color, font=font)
        
    path = os.path.join(OUTPUT_DIR, "sample1_correct.png")
    img.save(path)
    print(f"Saved {path}")

def render_sample2():
    # Sample 2 (Classic Sign/Transposition Error):
    # Solve 2(x + 3) = 14
    # Line 1: 2x + 6 = 14
    # Line 2: 2x = 14 + 6
    # Line 3: 2x = 20
    # Line 4: x = 10
    img = create_notebook_background(width=640, height=400, line_spacing=45, margin_x=70)
    draw = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.truetype(FONT_PATH, 28)
        font_body = ImageFont.truetype(FONT_PATH, 32)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        
    ink_color = (20, 25, 60)
    
    lines = [
        ("Solve  2(x + 3) = 14", font_header, 35, 100),
        ("2x + 6 = 14", font_body, 80, 120),
        ("2x = 14 + 6", font_body, 125, 120),
        ("2x = 20", font_body, 170, 120),
        ("x = 10", font_body, 215, 120),
    ]
    
    for text, font, y, x in lines:
        jx = x + random.randint(-1, 1)
        jy = y + random.randint(-1, 1)
        draw.text((jx, jy), text, fill=ink_color, font=font)
        
    path = os.path.join(OUTPUT_DIR, "sample2_sign_error.png")
    img.save(path)
    print(f"Saved {path}")

def render_sample3():
    # Sample 3 (Common Algebraic Misconception):
    # Expand and simplify:
    # (x + 3)^2 = x^2 + 9
    img = create_notebook_background(width=640, height=320, line_spacing=45, margin_x=70)
    draw = ImageDraw.Draw(img)
    
    try:
        font_header = ImageFont.truetype(FONT_PATH, 28)
        font_body = ImageFont.truetype(FONT_PATH, 32)
        font_super = ImageFont.truetype(FONT_PATH, 22)
    except Exception:
        font_header = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_super = ImageFont.load_default()
        
    ink_color = (25, 30, 70)
    
    # Header
    draw.text((100, 35), "Expand and simplify:", fill=ink_color, font=font_header)
    
    # Equation line: (x + 3)^2 = x^2 + 9
    # Render with genuine superscripts
    base_y = 100
    cur_x = 120
    
    # "(x + 3)"
    draw.text((cur_x, base_y), "(x + 3)", fill=ink_color, font=font_body)
    bbox = font_body.getbbox("(x + 3)")
    cur_x += (bbox[2] - bbox[0]) + 2
    
    # "^2"
    draw.text((cur_x, base_y - 10), "2", fill=ink_color, font=font_super)
    bbox_s = font_super.getbbox("2")
    cur_x += (bbox_s[2] - bbox_s[0]) + 6
    
    # " = x"
    draw.text((cur_x, base_y), " = x", fill=ink_color, font=font_body)
    bbox2 = font_body.getbbox(" = x")
    cur_x += (bbox2[2] - bbox2[0]) + 1
    
    # "^2"
    draw.text((cur_x, base_y - 10), "2", fill=ink_color, font=font_super)
    bbox_s2 = font_super.getbbox("2")
    cur_x += (bbox_s2[2] - bbox_s2[0]) + 6
    
    # " + 9"
    draw.text((cur_x, base_y), " + 9", fill=ink_color, font=font_body)
    
    path = os.path.join(OUTPUT_DIR, "sample3_misconception.png")
    img.save(path)
    print(f"Saved {path}")

if __name__ == "__main__":
    render_sample1()
    render_sample2()
    render_sample3()
