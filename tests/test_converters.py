import os
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path
from PIL import Image

from core.image_converter import convert_image, png_to_svg
from core.pdf_doc import pdf_to_images, images_to_pdf, office_to_pdf
from core.gif_converter import images_to_gif, video_to_gif, gif_to_mp4
from core.video_audio import video_to_mp4, video_to_mp3, audio_to_format

class TestFileConverters(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_file_to_file_")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_image_conversions(self):
        # 1. Create a dummy PNG image
        png_path = os.path.join(self.test_dir, "sample.png")
        img = Image.new("RGBA", (100, 100), color=(255, 0, 0, 200))
        img.save(png_path)

        # Convert to JPG
        jpg_out = convert_image(png_path, "jpg")
        self.assertTrue(os.path.exists(jpg_out))
        self.assertGreater(os.path.getsize(jpg_out), 0)

        # Convert to WebP
        webp_out = convert_image(png_path, "webp")
        self.assertTrue(os.path.exists(webp_out))
        self.assertGreater(os.path.getsize(webp_out), 0)

        # Convert to ICO
        ico_out = convert_image(png_path, "ico")
        self.assertTrue(os.path.exists(ico_out))
        self.assertGreater(os.path.getsize(ico_out), 0)

        # Convert to SVG
        svg_out = png_to_svg(png_path)
        self.assertTrue(os.path.exists(svg_out))
        self.assertGreater(os.path.getsize(svg_out), 0)

    def test_pdf_and_document_conversions(self):
        # 1. Images to PDF
        img1_path = os.path.join(self.test_dir, "page1.png")
        img2_path = os.path.join(self.test_dir, "page2.png")
        Image.new("RGB", (80, 80), color=(0, 255, 0)).save(img1_path)
        Image.new("RGB", (80, 80), color=(0, 0, 255)).save(img2_path)

        pdf_out = images_to_pdf([img1_path, img2_path])
        self.assertTrue(os.path.exists(pdf_out))
        self.assertGreater(os.path.getsize(pdf_out), 0)

        # 2. PDF to Images
        pages = pdf_to_images(pdf_out, fmt="png")
        self.assertEqual(len(pages), 2)
        for p in pages:
            self.assertTrue(os.path.exists(p))
            self.assertGreater(os.path.getsize(p), 0)

        # 3. Text to PDF via LibreOffice
        txt_path = os.path.join(self.test_dir, "notes.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("Hello from FILE-to-file test document!")
        doc_pdf = office_to_pdf(txt_path)
        self.assertTrue(os.path.exists(doc_pdf))
        self.assertGreater(os.path.getsize(doc_pdf), 0)

        # 4. PDF to DOCX
        from core.pdf_doc import pdf_to_docx
        docx_out = pdf_to_docx(doc_pdf)
        self.assertTrue(os.path.exists(docx_out))
        self.assertGreater(os.path.getsize(docx_out), 0)

    def test_media_and_gif_conversions(self):
        # Generate a 1-second synthetic video using ffmpeg
        video_src = os.path.join(self.test_dir, "synth.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "testsrc=duration=1:size=160x120:rate=10",
            "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
            "-c:v", "libx264", "-c:a", "aac",
            video_src
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        self.assertTrue(os.path.exists(video_src))

        # 1. Video to MP3
        mp3_out = video_to_mp3(video_src)
        self.assertTrue(os.path.exists(mp3_out))
        self.assertGreater(os.path.getsize(mp3_out), 0)

        # 2. Audio to WAV
        wav_out = audio_to_format(mp3_out, "wav")
        self.assertTrue(os.path.exists(wav_out))
        self.assertGreater(os.path.getsize(wav_out), 0)

        # 3. Video to GIF
        gif_out = video_to_gif(video_src)
        self.assertTrue(os.path.exists(gif_out))
        self.assertGreater(os.path.getsize(gif_out), 0)

        # 4. GIF to MP4
        mp4_out = gif_to_mp4(gif_out)
        self.assertTrue(os.path.exists(mp4_out))
        self.assertGreater(os.path.getsize(mp4_out), 0)

if __name__ == "__main__":
    unittest.main()
