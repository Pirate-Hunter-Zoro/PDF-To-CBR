from pdf2image import convert_from_path
import os
import zipfile

def pdf_to_cbr(pdf_path, output_name="output.cbr"):
    temp_dir = "comic_images"
    os.makedirs(temp_dir, exist_ok=True)

    print("Converting PDF to images...")
    images = convert_from_path(pdf_path)
    for i, img in enumerate(images):
        img.save(f"{temp_dir}/{i:03}.jpg", "JPEG")

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
pdf_to_cbr("Shuna's Journey (Hayao Miyazaki) (2022).pdf", "Shuna\'s Journey.cbr")
