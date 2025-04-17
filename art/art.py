from PIL import Image, ImageDraw, ImageFont
import io
import os

def create_image_from_ascii(ascii_art, color_map, pixel_size=10):
    # Split the ASCII art into lines
    lines = ascii_art.strip().split('\n')
    width = len(lines[0]) * pixel_size
    height = len(lines) * pixel_size

    # Create a new image with a white background
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)

    # Draw each character as a colored rectangle
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in color_map:
                draw.rectangle(
                    [x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size],
                    fill=color_map[char]
                )

    return image

# Define the color map
color_map = {
    '.': (173, 216, 230),  # Light Blue (sky)
    ',': (70, 130, 180),   # Medium Blue
    ':': (0, 0, 139),      # Dark Blue
    '~': (144, 238, 144),  # Light Green (grass)
    '^': (60, 179, 113),   # Medium Green
    '*': (0, 100, 0),      # Dark Green
    '+': (210, 180, 140),  # Light Brown (earth)
    '=': (165, 42, 42),    # Medium Brown
    '(': (101, 67, 33),    # Dark Brown
    '{': (211, 211, 211),  # Light Gray (rocks)
    '[': (128, 128, 128),  # Medium Gray
    ']': (105, 105, 105),  # Dark Gray
    '}': (255, 255, 224),  # Light Yellow (sun)
    ')': (255, 255, 0),    # Bright Yellow
    '#': (255, 165, 0),    # Light Orange
    '&': (255, 140, 0),    # Dark Orange
    '%': (255, 99, 71),    # Light Red
    '$': (139, 0, 0),      # Dark Red
    '@': (255, 255, 255),  # White
    '8': (0, 0, 0)         # Black
}

# Process all .txt files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'r') as file:
            ascii_art = file.read()
        
        # Create the image
        image = create_image_from_ascii(ascii_art, color_map)
        
        # Save the image with the same name as the text file, but with .png extension
        output_filename = os.path.splitext(filename)[0] + '.png'
        image.save(output_filename)
        print(f"Image saved as {output_filename}")
