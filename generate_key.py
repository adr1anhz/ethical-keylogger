from cryptography.fernet import Fernet

klucz = Fernet.generate_key()

# Zapis binarny
with open("klucz.key", "wb") as file:
    file.write(klucz)


print(f"Klucz: {klucz}")
