import os
from PIL import Image, ImageDraw, ImageFont

def generate_assets():
    # Make sure assets directory exists
    os.makedirs("assets", exist_ok=True)
    
    # 1. Generate logo.png (256x256)
    logo_size = (256, 256)
    logo = Image.new("RGBA", logo_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    
    # Draw a beautiful futuristic glowing circle
    draw.ellipse([20, 20, 236, 236], fill=(15, 23, 42, 230), outline=(99, 102, 241), width=6)
    draw.ellipse([35, 35, 221, 221], fill=(15, 23, 42, 0), outline=(167, 139, 250), width=2)
    
    # Draw stylized geometric shapes representing "Smart Campus AI"
    # An abstract S and C representation
    draw.arc([60, 60, 196, 196], start=135, end=315, fill=(99, 102, 241), width=10)
    draw.arc([75, 75, 181, 181], start=315, end=135, fill=(167, 139, 250), width=10)
    
    # Small glowing AI core in center
    draw.ellipse([110, 110, 146, 146], fill=(99, 102, 241))
    draw.ellipse([118, 118, 138, 138], fill=(255, 255, 255))
    
    logo.save("assets/logo.png", "PNG")
    print("Generated assets/logo.png successfully.")
    
    # 2. Generate background.jpg (1280x720) - a dark violet-indigo gradient
    bg_size = (1280, 720)
    bg = Image.new("RGB", bg_size)
    draw_bg = ImageDraw.Draw(bg)
    
    # Render a smooth gradient
    for y in range(bg_size[1]):
        # Interpolate between deep dark slate blue and dark indigo
        r = int(15 + (15 * (y / bg_size[1])))
        g = int(23 + (5 * (y / bg_size[1])))
        b = int(42 + (20 * (y / bg_size[1])))
        draw_bg.line([(0, y), (bg_size[0], y)], fill=(r, g, b))
        
    bg.save("assets/background.jpg", "JPEG")
    print("Generated assets/background.jpg successfully.")

if __name__ == "__main__":
    generate_assets()
