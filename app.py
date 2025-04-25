from flask import Flask, render_template, request, send_file, jsonify

from werkzeug.utils import secure_filename
import numpy as np

from cipher.vigenere import encrypt, decrypt
from cipher.vigenere_auto import encrypt_autokey, decrypt_autokey
from cipher.vigenere_extended import encrypt_extended, decrypt_extended
from cipher.affine import encrypt_affine, decrypt_affine
from cipher.playfair import encrypt_playfair, decrypt_playfair
from cipher.hill import encrypt_hill, decrypt_hill

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = ''
    tampilkan_file = False

    if request.method == 'POST':
        metode = request.form.get('metode')
        algoritma = request.form.get('algoritma')
        kunci = request.form.get('kunci', '')
        teks = request.form.get('teks', '')

        data = teks


        if algoritma == 'vigenere_extended' and isinstance(data, str):
            data = data.encode()

        if algoritma == 'vigenere':
            hasil = encrypt(data, kunci) if metode == 'enkripsi' else decrypt(data, kunci)

        elif algoritma == 'vigenere_auto':
            hasil = encrypt_autokey(data, kunci) if metode == 'enkripsi' else decrypt_autokey(data, kunci)

        elif algoritma == 'vigenere_extended':
            if metode == 'enkripsi':
                hasil = encrypt_extended(data, kunci)
            else:
                hasil = decrypt_extended(data, kunci)

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
                rows = [list(map(int, row.split(','))) for row in kunci.split(';')]
                key_matrix = np.array(rows)
                hasil = encrypt_hill(data, key_matrix) if metode == 'enkripsi' else decrypt_hill(data, key_matrix)
            except:
                hasil = 'Kunci hill harus dalam format matriks, contoh: 6,24,1;13,16,10;20,17,15'

        tampilkan_file = True

    return render_template('index.html', hasil=hasil, tampilkan_file=tampilkan_file)

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
            binary = teks.encode()
            hasil = encrypt_extended(binary, kunci) if metode == 'enkripsi' else decrypt_extended(binary, kunci)
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
                rows = [list(map(int, row.split(','))) for row in kunci.split(';')]
                key_matrix = np.array(rows)
                hasil = encrypt_hill(teks, key_matrix) if metode == 'enkripsi' else decrypt_hill(teks, key_matrix)
            except:
                return jsonify({'error': 'Kunci hill harus dalam format matriks, contoh: 6,24,1;13,16,10;20,17,15'}), 400
        else:
            return jsonify({'error': 'Algoritma tidak dikenali'}), 400

        return jsonify({'hasil': hasil})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
