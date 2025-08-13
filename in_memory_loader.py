import base64

payload_code = """
print("------------------------------------")
print("payload")
print("kod z pamięci.")
print("------------------------------------")
"""



# Kodujemy payload do base64
encoded_payload = base64.b64encode(payload_code.encode('utf-8'))

print("zakodowany payload (base64):")
print(encoded_payload)
print("\n")



############################ Dekodowanie
decoded_payload_bytes = base64.b64decode(encoded_payload)
decoded_payload_code = decoded_payload_bytes.decode('utf-8')

print("Odkodowany payload (gotowy do wykonania):")
print(decoded_payload_code)
print("\n")

# Wykonujemy odkodowany kod
# exec() bierze string i wykonuje go jako kod Pythona
print("--- Uruchamiam payload z pamięci ---")
exec(decoded_payload_code)
print("--- Payload zakończył działanie ---")

