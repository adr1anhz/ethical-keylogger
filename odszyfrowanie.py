from cryptography.fernet import Fernet


def zaladowanie_klucza():
    with open("klucz.key", "rb") as file:
        return file.read()
    

fernet = Fernet(zaladowanie_klucza())

def odszyfrowanie(token: bytes) -> str:
    return fernet.decrypt(token).decode()

with open("logs.txt", "rb") as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    tekst = odszyfrowanie(line)
    print(tekst)


