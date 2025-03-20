from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

def merge_images(image_paths, output_path, layout=(2, 3), padding=10, target_height=1000):
    """
    Merge multiple images into a single image while preserving aspect ratio.
    
    Args:
        image_paths: List of paths to the input images
        output_path: Path where the merged image will be saved
        layout: Tuple of (rows, cols) defining the layout of the merged image
        padding: Padding between images in pixels
        target_height: Target height for normalizing images (higher = better text visibility)
    """
    rows, cols = layout
    
    # Check if we have enough space in the layout
    if len(image_paths) > rows * cols:
        raise ValueError(f"Too many images ({len(image_paths)}) for layout {layout}")
    
    # Load all images
    images = [Image.open(path) for path in image_paths]
    
    # Resize images to the target height while preserving aspect ratio
    resized_images = []
    for img in images:
        aspect_ratio = img.width / img.height
        new_width = int(aspect_ratio * target_height)
        resized_img = img.resize((new_width, target_height), Image.LANCZOS)
        resized_images.append(resized_img)
    
    # Calculate the width of each column and height of each row
    col_widths = [0] * cols
    row_heights = [0] * rows
    
    for i, img in enumerate(resized_images):
        row = i // cols
        col = i % cols
        col_widths[col] = max(col_widths[col], img.width)
        row_heights[row] = max(row_heights[row], img.height)
    
    # Calculate the dimensions of the final image
    total_width = sum(col_widths) + padding * (cols + 1)
    total_height = sum(row_heights) + padding * (rows + 1)
    
    # Create a new blank image
    result_img = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
    
    # Paste each image in its position
    y_offset = padding
    for row in range(rows):
        x_offset = padding
        for col in range(cols):
            idx = row * cols + col
            if idx < len(resized_images):
                img = resized_images[idx]
                # Center the image in its cell
                x_center = x_offset + (col_widths[col] - img.width) // 2
                y_center = y_offset + (row_heights[row] - img.height) // 2
                result_img.paste(img, (x_center, y_center))
            x_offset += col_widths[col] + padding
        y_offset += row_heights[row] + padding
    
    # Save the result with high DPI for better text readability
    result_img.save(output_path, quality=95, dpi=(300, 300))
    print(f"Merged image saved to {output_path}")

if __name__ == "__main__":
    # Example usage - replace with your actual image paths
    # Using paths relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_paths = [
        os.path.join(script_dir, "image1.png"),  # Add your first image filename here
        os.path.join(script_dir, "image2.png"),  # Add your second image filename here
        os.path.join(script_dir, "image3.png"),  # Add your third image filename here
        os.path.join(script_dir, "image4.png"),  # Add your fourth image filename here
        os.path.join(script_dir, "image5.png"),  # Add your fifth image filename here
        os.path.join(script_dir, "image6.png"),  # Add your sixth image filename here
    ]
    output_path = os.path.join(script_dir, "merged_image.jpg")    # Use layout of 2 rows and 3 columns for 6 images
    merge_images(image_paths, output_path, layout=(2, 3))
