from PIL import Image
import os

# Directory containing images
image_dir = "./images"  # Change this to your image folder path

# Supported extensions
extensions = ('.png', '.jpg', '.jpeg')

# Get sorted image files
image_files = sorted(
    [f for f in os.listdir(image_dir) if f.lower().endswith(extensions)]
)

# Full paths to image files
image_paths = [os.path.join(image_dir, f) for f in image_files]

# Convert images to RGB and collect them
image_list = []
for path in image_paths:
    img = Image.open(path).convert("RGB")
    image_list.append(img)

# Save as one PDF
if image_list:
    output_path = os.path.join(image_dir, "output.pdf")
    image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
    print(f"PDF created: {output_path}")
else:
    print("No images found to convert.")
