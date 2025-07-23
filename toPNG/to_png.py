from PIL import Image
import os

# directories
input_dir = r"input"
output_dir = r"output"
os.makedirs(output_dir, exist_ok=True)

# create if not exist
os.makedirs(output_dir, exist_ok=True)

# extensions
valid_extensions = ('.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp', '.png')

for filename in os.listdir(input_dir):
    if filename.lower().endswith(valid_extensions):
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, base_name + '.png')

        try:
            with Image.open(input_path) as img:
                # P does not exist -> RGB
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(output_path, 'PNG')
                print(f"Converted: {filename} -> {base_name}.png")
        except Exception as e:
            print(f"Failed to convert {filename}: {e}")
