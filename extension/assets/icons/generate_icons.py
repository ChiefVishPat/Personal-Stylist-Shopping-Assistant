#!/usr/bin/env python3
"""
Simple script to generate placeholder PNG icons for Chrome extension.
Run this script to create the required icon files.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    
    sizes = [16, 48, 128]
    bg_color = (102, 126, 234)  # #667eea
    text_color = (255, 255, 255)  # white
    
    for size in sizes:
        # Create image with gradient background
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw a simple "T" in the center
        font_size = size // 2
        try:
            # Try to use a system font
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            # Fall back to default font
            font = ImageFont.load_default()
        
        text = "T"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        position = ((size - text_width) // 2, (size - text_height) // 2 - bbox[1])
        draw.text(position, text, fill=text_color, font=font)
        
        # Save
        img.save(f'icon{size}.png')
        print(f"Created icon{size}.png")
    
    print("\nAll icons created successfully!")
    
except ImportError:
    print("PIL/Pillow not installed.")
    print("Install with: pip3 install Pillow")
    print("\nOr manually create these files:")
    print("- icon16.png (16x16 pixels)")
    print("- icon48.png (48x48 pixels)")
    print("- icon128.png (128x128 pixels)")

