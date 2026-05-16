import os
from PIL import Image

base_dir = os.path.join('PetImages')

def clean_fake_formats(directory):
    print("Starting file signature scan (Magic Bytes)...")
    removed = 0
    analyzed = 0
    converted = 0
    
    # Standard hexadecimal signatures for valid formats
    SIGNATURES = {
        b'\xff\xd8\xff': 'JPEG',  # Start of a standard JPEG file
        b'\x89PNG\r\n\x1a\n': 'PNG',
        b'BM': 'BMP',
        b'GIF8': 'GIF'
    }

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                full_path = os.path.join(root, file)
                analyzed += 1
                
                try:
                    # Read the first 8 bytes of the physical file
                    with open(full_path, 'rb') as f:
                        header = f.read(8)
                    
                    # Check if the file starts with a valid signature
                    valid = False
                    for sig in SIGNATURES:
                        if header.startswith(sig):
                            valid = True
                            break
                    
                    # If it doesn't have a valid signature or is empty (0 bytes), delete it
                    if not valid or len(header) == 0:
                        os.remove(full_path)
                        removed += 1
                        continue
                    
                    # Validate and fix the number of channels
                    try:
                        img = Image.open(full_path)
                        img.load()  # Force load to detect corruption
                    except Exception:
                        os.remove(full_path)
                        removed += 1
                        continue
                    
                    # If it's grayscale (1 channel) or RGBA (4 channels), convert to RGB (3 channels)
                    if img.mode == 'L':  # Grayscale
                        img = img.convert('RGB')
                        img.save(full_path)
                        converted += 1
                    elif img.mode == 'RGBA':  # RGBA with transparency
                        img = img.convert('RGB')
                        img.save(full_path)
                        converted += 1
                    elif img.mode not in ('RGB', '1', 'L', 'RGBA'):  # Exotic mode
                        img = img.convert('RGB')
                        img.save(full_path)
                        converted += 1
                    elif img.mode != 'RGB':  # Any other mode
                        img = img.convert('RGB')
                        img.save(full_path)
                        converted += 1
                        
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    if os.path.exists(full_path):
                        os.remove(full_path)
                    removed += 1

    print(f"\n[Scan Completed]")
    print(f"Images analyzed: {analyzed}")
    print(f"Fake or corrupted files deleted: {removed}")
    print(f"Images converted to RGB: {converted}")

# Execute signature-based cleaning on your safe directory
clean_fake_formats(base_dir)