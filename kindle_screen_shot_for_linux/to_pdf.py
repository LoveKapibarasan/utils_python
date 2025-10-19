from PIL import Image
import os
import re

# Ask for the base folder
base_dir = input("Enter the folder path that contains image subfolders: ").strip()

# Ask how to sort image files
sort_mode = input("Sorting mode? (l = lexicographical [default], n = numerical): ").strip().lower()
if sort_mode not in ('n', 'l', ''):
    print("❌ Invalid choice. Defaulting to lexicographical sort.")
    sort_mode = 'l'

# Supported extensions
extensions = ('.png', '.jpg', '.jpeg')

# Helper: extract numeric part from filename
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

print(f"DEBUG: base_dir = {base_dir}")
print(f"DEBUG: subfolders = {os.listdir(base_dir)}")


# Process each subfolder
for subfolder in sorted(os.listdir(base_dir)):
    subfolder_path = os.path.join(base_dir, subfolder)

    # ❌ Skip if not a directory
    if not os.path.isdir(subfolder_path):
        continue

    # Get all image files
    image_files = [
        f for f in os.listdir(subfolder_path)
        if f.lower().endswith(extensions)
    ]

    if not image_files:
        print(f"⏭️ Skipping '{subfolder}' — no image files found.")
        continue

    # Sort based on user choice
    if sort_mode == 'n':
        image_files.sort(key=extract_number)
    else:
        image_files.sort()  # lexicographical

    image_paths = [os.path.join(subfolder_path, f) for f in image_files]

    # 🖼 Convert to RGB
    image_list = []
    for path in image_paths:
        try:
            img = Image.open(path).convert("RGB")
            image_list.append(img)
        except Exception as e:
            print(f"⚠️ Could not open {path}: {e}")

    # Save to PDF
    if image_list:
        output_path = os.path.join(subfolder_path, f"{subfolder}.pdf")
        image_list[0].save(output_path, save_all=True, append_images=image_list[1:])
        print(f"✅ Created PDF: {output_path}")
    else:
        print(f"❌ No valid images to convert in '{subfolder}'.")
