from pdf2image import convert_from_path
import os
import zipfile
import shutil
from pdf2image.pdf2image import pdfinfo_from_path
from PIL import Image

# Suppress warnings in case you're working with a HIGH quality PDF
Image.MAX_IMAGE_PIXELS = None

def get_num_pages(pdf_path):
    info = pdfinfo_from_path(pdf_path)
    return info["Pages"]

def pdf_to_cbr(pdf_path, output_name="output.cbr"):
    temp_dir = "comic_images"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        print("Converting PDF to images (one page at a time)...")
        for i in range(1, get_num_pages(pdf_path) + 1):
            try:
                image = convert_from_path(pdf_path, thread_count=1, first_page=i, last_page=i)[0]
                img_path = os.path.join(temp_dir, f"{i:03}.jpg")
                print(f"Saving page {i} to {img_path}")
                image.save(img_path, "JPEG")
            except Exception as e:
                print(f"Failed to convert page {i}: {e}")
    except Exception as e:
        print("PDF to image conversion failed:", e)
        return

    print("Creating .cbr archive...")
    with zipfile.ZipFile("temp.zip", "w") as zipf:
        for fname in sorted(os.listdir(temp_dir)):
            zipf.write(os.path.join(temp_dir, fname), arcname=fname)

    os.rename("temp.zip", output_name)
    print(f"Saved as {output_name}")

    print("Cleaning up temporary images...")
    shutil.rmtree(temp_dir)
    print("Done!")

# Example usage
pdf_to_cbr("Shuna's Journey (Hayao Miyazaki) (2022).pdf", "Shuna's Journey.cbr")