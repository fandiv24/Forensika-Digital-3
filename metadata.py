import PyPDF2
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


def create_page_with_logo_and_blank(logo_path, page_size=letter):
    """Membuat PDF dengan logo yang disembunyikan oleh halaman kosong."""
    # Buat halaman dengan logo
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=page_size)
    
    # Tambahkan logo yang memenuhi seluruh halaman
    can.drawImage(logo_path, 0, 0, width=page_size[0], height=page_size[1])
    
    # Tambahkan lapisan putih untuk menutupi logo
    can.setFillColorRGB(1, 1, 1)  # Warna putih
    can.rect(0, 0, page_size[0], page_size[1], fill=1, stroke=0)  # Menutupi logo dengan lapisan putih
    
    can.showPage()
    can.save()

    packet.seek(0)  # Kembali ke awal data
    new_pdf = PyPDF2.PdfReader(packet)
    
    return new_pdf.pages[0]


def caesar_cipher(text, shift):
    """Mengubah teks berdasarkan pergeseran tertentu (Caesar cipher)."""
    result = []
    for char in text:
        if char.isalpha():  # Hanya ubah karakter alfabet
            # Tentukan apakah karakter besar atau kecil
            start = ord('A') if char.isupper() else ord('a')
            # Pergeseran dengan wrap-around (mod 26)
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result.append(new_char)
        else:
            result.append(char)  # Karakter non-alfabet tetap sama
    return ''.join(result)


def encode_metadata_base64(metadata):
    """Encode metadata dengan Base64."""
    encoded_metadata = {}
    for key, value in metadata.items():
        encoded_str = base64.b64encode(caesar_cipher(value, 4).encode()).decode()
        encoded_metadata[key] = encoded_str
    return encoded_metadata


def edit_pdf_with_modifications(input_pdf, output_pdf, new_metadata, logo_path):
    """Mengedit PDF dengan halaman tersembunyi di awal dan halaman kosong di akhir."""
    # Baca PDF asli
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # Tambahkan halaman dengan logo yang disembunyikan
        hidden_logo_page = create_page_with_logo_and_blank(logo_path)
        pdf_writer.add_page(hidden_logo_page)

        # Tambahkan semua halaman dari input PDF
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Tambahkan halaman kosong di akhir
        pdf_writer.add_page(create_page_with_logo_and_blank(logo_path))

        # Encode metadata baru dengan Caesar cipher dan Base64
        encrypted_metadata = encode_metadata_base64(new_metadata)

        # Tambahkan metadata yang sudah dienkode
        pdf_writer.add_metadata(encrypted_metadata)

        # Tulis ke file output
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)


# Contoh penggunaan
input_pdf = 'PDF 1.pdf'
output_pdf = 'output.pdf'
logo_path = 'logotelu.png'  # Ganti dengan path ke file logo Anda
new_metadata = {'/Title': 'Desain dan Implementasi Sistem Informasi Usaha Mikro Kecil Menengah dan Pariwisata Desa Tambak Kalisogo', '/Author': 'Tifanni', '/Subject': 'Forensika Metadata'}

edit_pdf_with_modifications(input_pdf, output_pdf, new_metadata, logo_path)
