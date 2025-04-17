from PIL import Image, ImageDraw, ImageFont
import io
import os
import re

def parse_color(color_string):
    # Extract RGB values from the string
    match = re.search(r'\((\d+),\s*(\d+),\s*(\d+)\)', color_string)
    if match:
        return tuple(map(int, match.groups()))
    return None

def parse_file_content(content):
    lines = content.strip().split('\n')
    title = lines[0].strip()
    color_map = {}
    ascii_art_start = 0

    for i, line in enumerate(lines[2:], 2):  # Start from the third line
        if line.strip() == '':
            ascii_art_start = i + 1
            break
        parts = line.split('-', 1)
        if len(parts) == 2:
            char, color_name = parts[0].strip(), parts[1].strip()
            color = parse_color(color_name)
            if color:
                color_map[char] = color

    ascii_art = '\n'.join(lines[ascii_art_start:])
    return title, color_map, ascii_art

def create_image_from_ascii(ascii_art, color_map, pixel_size=10):
    lines = ascii_art.strip().split('\n')
    width = len(lines[0]) * pixel_size
    height = len(lines) * pixel_size

    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in color_map:
                draw.rectangle(
                    [x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size],
                    fill=color_map[char]
                )

    return image

# Process all .txt files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'r') as file:
            content = file.read()
        
        title, color_map, ascii_art = parse_file_content(content)
        
        # Create the image
        image = create_image_from_ascii(ascii_art, color_map)
        
        # Save the image with the title as the filename
        output_filename = f"{title.replace(' ', '_')}.png"
        image.save(output_filename)
        print(f"Image '{title}' saved as {output_filename}")
