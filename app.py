from flask import Flask, render_template, request, send_file, jsonify, make_response
import os
from werkzeug.utils import secure_filename
import numpy as np

from cipher.vigenere import encrypt, decrypt
from cipher.vigenere_auto import encrypt_autokey, decrypt_autokey
from cipher.vigenere_extended import encrypt_extended, decrypt_extended
from cipher.affine import encrypt_affine, decrypt_affine
from cipher.playfair import encrypt_playfair, decrypt_playfair
from cipher.hill import encrypt_hill, decrypt_hill

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'

# Ensure upload and download folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = ''
    tampilkan_file = False
    nama_file_hasil = None

    if request.method == 'POST':
        metode = request.form.get('metode')
        algoritma = request.form.get('algoritma')
        kunci = request.form.get('kunci', '')
        teks = request.form.get('teks', '')
        file_input = request.files.get('file_input')

        if not teks and not file_input:
            return render_template('index.html', error='Harap isi teks atau unggah file.', hasil=hasil, tampilkan_file=tampilkan_file)

        data = teks
        nama_file = None

        if file_input and file_input.filename:
            nama_file = secure_filename(file_input.filename)
            path_file = os.path.join(app.config['UPLOAD_FOLDER'], nama_file)
            file_input.save(path_file)

            if algoritma == 'vigenere_extended':
                with open(path_file, 'rb') as f:
                    data = f.read()
            else:
                with open(path_file, 'r', encoding='utf-8', errors='ignore') as f:
                    data = f.read()

        if algoritma == 'vigenere_extended' and isinstance(data, str):
            data = data.encode()

        if algoritma == 'vigenere':
            hasil = encrypt(data, kunci) if metode == 'enkripsi' else decrypt(data, kunci)

        elif algoritma == 'vigenere_auto':
            hasil = encrypt_autokey(data, kunci) if metode == 'enkripsi' else decrypt_autokey(data, kunci)

        elif algoritma == 'vigenere_extended':
            if metode == 'enkripsi':
                binary = teks.encode()
                hasil = encrypt_extended(binary, kunci)
            else:
                try:
                    binary = bytes.fromhex(teks)
                except:
                    binary = teks.encode()
                hasil = decrypt_extended(binary, kunci)
            
            try:
                hasil = hasil.decode('utf-8')
            except:
                hasil = hasil.hex()

        elif algoritma == 'affine':
            try:
                a, b = map(int, kunci.split(','))
                hasil = encrypt_affine(data, a, b) if metode == 'enkripsi' else decrypt_affine(data, a, b)
            except:
                hasil = 'Kunci affine harus dalam format angka a,b (contoh: 5,8)'

        elif algoritma == 'playfair':
            hasil = encrypt_playfair(data, kunci) if metode == 'enkripsi' else decrypt_playfair(data, kunci)

        elif algoritma == 'hill':
            try:
                kunci = kunci.replace(' ', '').lower()
                
                if ';' in kunci:
                    rows = [list(map(int, row.split(','))) for row in kunci.split(';')]
                else:
                    numbers = list(map(int, kunci.split(',')))
                    n = int(len(numbers) ** 0.5)
                    if n * n != len(numbers):
                        return jsonify({'error': 'Jumlah angka tidak bisa membentuk matriks persegi'}), 400
                    rows = [numbers[i:i+n] for i in range(0, len(numbers), n)]
                
                key_matrix = np.array(rows)
                
                if key_matrix.shape[0] != key_matrix.shape[1]:
                    return jsonify({'error': 'Matriks harus persegi (jumlah baris = jumlah kolom)'}), 400
                
                det = int(np.linalg.det(key_matrix))
                if det == 0:
                    return jsonify({'error': 'Determinan matriks tidak boleh 0'}), 400
                
                def gcd(a, b):
                    while b:
                        a, b = b, a % b
                    return a
                
                if gcd(abs(det), 26) != 1:
                    return jsonify({'error': 'Determinan matriks harus relatif prima dengan 26'}), 400
                
                hasil = encrypt_hill(data, key_matrix) if metode == 'enkripsi' else decrypt_hill(data, key_matrix)
                
            except ValueError:
                return jsonify({'error': 'Format kunci tidak valid. Gunakan format: 3,3;2,5 atau 3,3,2,5'}), 400
            except Exception as e:
                return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 400

        # Save hasil to a file for download
        nama_file_hasil = f"hasil_{metode}_{algoritma}.txt"
        path_hasil = os.path.join(app.config['DOWNLOAD_FOLDER'], nama_file_hasil)
        with open(path_hasil, 'w', encoding='utf-8') as f:
            f.write(hasil)

        tampilkan_file = True

    return render_template('index.html', hasil=hasil, tampilkan_file=tampilkan_file, nama_file_hasil=nama_file_hasil)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    return jsonify({'error': 'File tidak ditemukan'}), 404

@app.route('/api/proses', methods=['POST'])
def proses_api():
    try:
        data = request.get_json()
        algoritma = data.get('algoritma')
        metode = data.get('metode')
        teks = data.get('teks', '')
        kunci = data.get('kunci', '')

        if algoritma == 'vigenere':
            hasil = encrypt(teks, kunci) if metode == 'enkripsi' else decrypt(teks, kunci)

        elif algoritma == 'vigenere_auto':
            hasil = encrypt_autokey(teks, kunci) if metode == 'enkripsi' else decrypt_autokey(teks, kunci)

        elif algoritma == 'vigenere_extended':
            if metode == 'enkripsi':
                binary = teks.encode()
                hasil = encrypt_extended(binary, kunci)
            else:
                try:
                    binary = bytes.fromhex(teks)
                except:
                    binary = teks.encode()
                hasil = decrypt_extended(binary, kunci)
            
            try:
                hasil = hasil.decode('utf-8')
            except:
                hasil = hasil.hex()

        elif algoritma == 'affine':
            try:
                a, b = map(int, kunci.split(','))
                hasil = encrypt_affine(teks, a, b) if metode == 'enkripsi' else decrypt_affine(teks, a, b)
            except:
                return jsonify({'error': 'Kunci affine harus dalam format angka a,b (contoh: 5,8)'}), 400

        elif algoritma == 'playfair':
            hasil = encrypt_playfair(teks, kunci) if metode == 'enkripsi' else decrypt_playfair(teks, kunci)

        elif algoritma == 'hill':
            try:
                kunci = kunci.replace(' ', '').lower()
                
                if ';' in kunci:
                    rows = [list(map(int, row.split(','))) for row in kunci.split(';')]
                else:
                    numbers = list(map(int, kunci.split(',')))
                    n = int(len(numbers) ** 0.5)
                    if n * n != len(numbers):
                        return jsonify({'error': 'Jumlah angka tidak bisa membentuk matriks persegi'}), 400
                    rows = [numbers[i:i+n] for i in range(0, len(numbers), n)]
                
                key_matrix = np.array(rows)
                
                if key_matrix.shape[0] != key_matrix.shape[1]:
                    return jsonify({'error': 'Matriks harus persegi (jumlah baris = jumlah kolom)'}), 400
                
                det = int(np.linalg.det(key_matrix))
                if det == 0:
                    return jsonify({'error': 'Determinan matriks tidak boleh 0'}), 400
                
                def gcd(a, b):
                    while b:
                        a, b = b, a % b
                    return a
                
                if gcd(abs(det), 26) != 1:
                    return jsonify({'error': 'Determinan matriks harus relatif prima dengan 26'}), 400
                
                hasil = encrypt_hill(teks, key_matrix) if metode == 'enkripsi' else decrypt_hill(teks, key_matrix)
                
            except ValueError:
                return jsonify({'error': 'Format kunci tidak valid. Gunakan format: 3,3;2,5 atau 3,3,2,5'}), 400
            except Exception as e:
                return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 400
        else:
            return jsonify({'error': 'Algoritma tidak dikenali'}), 400

        return jsonify({'hasil': hasil})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)