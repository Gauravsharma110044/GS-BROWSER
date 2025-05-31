from PIL import Image, ImageDraw
import os

def create_icon(name, color, size=(32, 32)):
    # Create a new image with a transparent background
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw different icons based on name
    if name == 'back':
        # Draw a back arrow
        points = [(size[0]*0.7, size[1]*0.3), (size[0]*0.3, size[1]*0.5), 
                 (size[0]*0.7, size[1]*0.7)]
        draw.polygon(points, fill=color)
    elif name == 'forward':
        # Draw a forward arrow
        points = [(size[0]*0.3, size[1]*0.3), (size[0]*0.7, size[1]*0.5), 
                 (size[0]*0.3, size[1]*0.7)]
        draw.polygon(points, fill=color)
    elif name == 'reload':
        # Draw a circular arrow
        center = (size[0]/2, size[1]/2)
        radius = min(size) * 0.4
        draw.arc([center[0]-radius, center[1]-radius, 
                 center[0]+radius, center[1]+radius], 
                45, 315, fill=color, width=3)
        # Draw arrow head
        points = [(center[0]+radius*0.7, center[1]-radius*0.3),
                 (center[0]+radius*0.9, center[1]),
                 (center[0]+radius*0.7, center[1]+radius*0.3)]
        draw.polygon(points, fill=color)
    elif name == 'home':
        # Draw a house
        points = [(size[0]*0.5, size[1]*0.2),  # Roof top
                 (size[0]*0.2, size[1]*0.5),   # Left wall
                 (size[0]*0.2, size[1]*0.8),   # Left bottom
                 (size[0]*0.8, size[1]*0.8),   # Right bottom
                 (size[0]*0.8, size[1]*0.5)]   # Right wall
        draw.polygon(points, fill=color)
        # Draw door
        door_points = [(size[0]*0.4, size[1]*0.6),
                      (size[0]*0.4, size[1]*0.8),
                      (size[0]*0.6, size[1]*0.8),
                      (size[0]*0.6, size[1]*0.6)]
        draw.polygon(door_points, fill=color)
    elif name == 'bookmark':
        # Draw a bookmark
        points = [(size[0]*0.3, size[1]*0.2),  # Top left
                 (size[0]*0.7, size[1]*0.2),   # Top right
                 (size[0]*0.7, size[1]*0.8),   # Bottom right
                 (size[0]*0.5, size[1]*0.6),   # Middle point
                 (size[0]*0.3, size[1]*0.8)]   # Bottom left
        draw.polygon(points, fill=color)
    elif name == 'new_tab':
        # Draw a plus sign
        draw.rectangle([(size[0]*0.4, size[1]*0.2), 
                       (size[0]*0.6, size[1]*0.8)], fill=color)
        draw.rectangle([(size[0]*0.2, size[1]*0.4), 
                       (size[0]*0.8, size[1]*0.6)], fill=color)
    elif name == 'app_icon':
        # Draw a simple browser icon
        # Background circle
        draw.ellipse([(2, 2), (size[0]-2, size[1]-2)], 
                    fill=(66, 133, 244))  # Google blue
        # Draw a 'G' in white
        draw.arc([(size[0]*0.2, size[1]*0.2), 
                 (size[0]*0.8, size[1]*0.8)], 
                0, 300, fill='white', width=3)
        # Draw the horizontal line of 'G'
        draw.line([(size[0]*0.5, size[1]*0.5), 
                  (size[0]*0.8, size[1]*0.5)], 
                 fill='white', width=3)
    
    # Create icons directory if it doesn't exist
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # Save the icon
    image.save(f'icons/{name}.png')

def main():
    # Create all necessary icons
    icons = {
        'back': '#666666',
        'forward': '#666666',
        'reload': '#666666',
        'home': '#666666',
        'bookmark': '#666666',
        'new_tab': '#666666',
        'app_icon': None  # Uses custom colors
    }
    
    for name, color in icons.items():
        create_icon(name, color)

if __name__ == '__main__':
    main() 