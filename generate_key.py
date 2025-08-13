from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generowanie klucza prywatnego RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Pobranie klucza publicznego z klucza prywatnego
public_key = private_key.public_key()

# Serializacja klucza prywatnego do formatu PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption() # Klucz prywatny nie jest szyfrowany hasłem
)

# Zapis klucza prywatnego do pliku
with open('private_key.pem', 'wb') as f:
    f.write(private_pem)

# Serializacja klucza publicznego do formatu PEM
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Zapis klucza publicznego do pliku
with open('public_key.pem', 'wb') as f:
    f.write(public_pem)

print("Wygenerowano i zapisano klucze: private_key.pem i public_key.pem")