from pdf2image import convert_from_path
import os
import zipfile

def pdf_to_cbr(pdf_path, output_name="output.cbr"):
    temp_dir = "comic_images"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        print("Converting PDF to images...")
        images = convert_from_path(pdf_path, thread_count=4)
        print(f"Total pages converted: {len(images)}")
    except Exception as e:
        print("PDF to image conversion failed:", e)
        return

    for i, img in enumerate(images):
        img_path = os.path.join(temp_dir, f"{i:03}.jpg")
        print(f"Saving page {i + 1} to {img_path}")
        img.save(img_path, "JPEG")

    print("Creating .cbr archive...")
    with zipfile.ZipFile("temp.zip", "w") as zipf:
        for fname in sorted(os.listdir(temp_dir)):
            zipf.write(os.path.join(temp_dir, fname), arcname=fname)

    os.rename("temp.zip", output_name)
    print(f"Saved as {output_name}")

    # Optional cleanup:
    # import shutil
    # shutil.rmtree(temp_dir)

# Example usage
pdf_to_cbr("Shuna's Journey (Hayao Miyazaki) (2022).pdf", "Shuna's Journey.cbr")
