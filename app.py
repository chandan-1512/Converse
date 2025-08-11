# import os
# from PIL import Image
# from pdf2image import convert_from_path

# def is_image(file_path):
#     try:
#         Image.open(file_path)
#         return True
#     except:
#         return False

# def convert_images_to_format(input_folder, output_format, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     for filename in os.listdir(input_folder):
#         input_path = os.path.join(input_folder, filename)
#         if is_image(input_path):
#             try:
#                 img = Image.open(input_path).convert("RGB")
#                 base = os.path.splitext(filename)[0]
#                 output_file = os.path.join(output_folder, f"{base}.{output_format.lower()}")
#                 save_format = "JPEG" if output_format.lower() in ["jpg", "jpeg"] else output_format.upper()
#                 img.save(output_file, save_format)
#                 print(f"✅ Converted {filename} → {output_format.upper()}")
#             except Exception as e:
#                 print(f"❌ Error converting {filename}: {e}")

# def images_to_pdf(input_folder, output_pdf_path):
#     os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
#     image_files = []
#     for file in os.listdir(input_folder):
#         path = os.path.join(input_folder, file)
#         if is_image(path):
#             try:
#                 img = Image.open(path).convert("RGB")
#                 image_files.append(img)
#             except:
#                 print(f"⚠️ Skipping corrupted image: {file}")
    
#     if image_files:
#         image_files[0].save(output_pdf_path, save_all=True, append_images=image_files[1:])
#         print(f"\n📄 PDF created successfully: {output_pdf_path}")
#     else:
#         print("❌ No valid images found to convert to PDF.")

# def pdf_to_images(pdf_path, output_folder):
#     os.makedirs(output_folder, exist_ok=True)
#     try:
#         images = convert_from_path(pdf_path)
#         for i, img in enumerate(images):
#             output_path = os.path.join(output_folder, f"page_{i+1}.jpg")
#             img.save(output_path, "JPEG")
#             print(f"🖼️ Saved page {i+1} as image")
#     except Exception as e:
#         print(f"❌ Error during PDF to image conversion: {e}")

# if __name__ == "__main__":
#     print("\n📦 CHOOSE AN OPERATION:")
#     print("1. Convert images to another image format")
#     print("2. Convert images to a single multi-page PDF")
#     print("3. Convert PDF to images")

#     choice = input("\nEnter your choice (1/2/3): ")

#     if choice == "1":
#         input_folder = input("Enter input folder path containing images: ").strip().strip('"')
#         format_ = input("Enter target format (e.g. png, jpg, webp, bmp): ")
#         output_folder = input("Enter output folder to save converted images: ").strip().strip('"')
#         convert_images_to_format(input_folder, format_, output_folder)

#     elif choice == "2":
#         input_folder = input("Enter folder path containing images: ").strip().strip('"')
#         output_pdf_path = input("Enter full output PDF path (e.g. C:\\output\\merged.pdf): ").strip().strip('"')
#         images_to_pdf(input_folder, output_pdf_path)

#     elif choice == "3":
#         pdf_file = input("Enter full path to PDF file: ").strip().strip('"')
#         out_folder = input("Enter output folder to save extracted images: ").strip().strip('"')
#         pdf_to_images(pdf_file, out_folder)

#     else:
#         print("❌ Invalid choice. Exiting.")

# import os
# import uuid
# from flask import Flask, request, send_file, render_template
# from PIL import Image

# app = Flask(__name__)
# UPLOAD_FOLDER = 'static/uploads'
# RESULT_FOLDER = 'static/results'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULT_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/convert-image', methods=['POST'])
# def convert_image():
#     file = request.files.get('image')
#     target_format = request.form.get('target_format').lower()

#     if not file or not target_format:
#         return "❌ Invalid input."

#     # Save uploaded image
#     filename = str(uuid.uuid4())
#     input_path = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(input_path)

#     # Convert image
#     try:
#         img = Image.open(input_path).convert("RGB")
#         output_ext = 'jpg' if target_format in ['jpg', 'jpeg'] else target_format
#         output_path = os.path.join(RESULT_FOLDER, f"{filename}.{output_ext}")
#         img.save(output_path, "JPEG" if output_ext in ["jpg", "jpeg"] else output_ext.upper())
#         return send_file(output_path, as_attachment=True)
#     except Exception as e:
#         return f"❌ Error during conversion: {e}"

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import uuid
from flask import Flask, request, send_file, render_template
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')
    target_format = request.form.get('target_format', '').lower()

    if not files or not target_format:
        return "❌ Invalid input."

    filename_base = str(uuid.uuid4())

    if target_format == 'pdf':
        images = []
        for file in files:
            temp_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
            file.save(temp_path)
            try:
                img = Image.open(temp_path).convert("RGB")
                images.append(img)
            except:
                continue

        if not images:
            return "❌ No valid images found."

        output_path = os.path.join(RESULT_FOLDER, f"{filename_base}.pdf")
        images[0].save(output_path, save_all=True, append_images=images[1:])
        return send_file(output_path, as_attachment=True)

    else:
        # Handle normal image format conversion
        file = files[0]  # Only one image expected
        input_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}")
        file.save(input_path)

        try:
            img = Image.open(input_path).convert("RGB")
            ext = 'jpg' if target_format in ['jpg', 'jpeg'] else target_format
            output_path = os.path.join(RESULT_FOLDER, f"{filename_base}.{ext}")
            img.save(output_path, "JPEG" if ext in ["jpg", "jpeg"] else ext.upper())
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return f"❌ Error during conversion: {e}"

if __name__ == '__main__':
    app.run(debug=True)
