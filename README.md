# 🔐 Etyczny Keylogger (Ethical Keylogger)

Ten projekt to moje osobiste wyzwanie: stworzyć działającego keyloggera w Pythonie całkowicie od podstaw.  
Celem jest zasymulowanie, jak działają prawdziwe narzędzia — **wyłącznie w celach edukacyjnych, red teamingu oraz treningu obrony**.

## 📚 Wykorzystywane biblioteki

- **pynput** – do nasłuchiwania naciśnięć klawiszy
- **cryptography** – Do szyfrowania asymetrycznego RSA. Komunikacja między payloadem a serwerem C2 jest w pełni szyfrowana
- **Flask** – Do budowy serwera C2, który odbiera logi.
- **requests** - Używane przez payload do wysyłania danych do serwera C2.
- 

##  Jak to działa?

   1. Payload (keylogger) używa klucza publicznego do zaszyfrowania przechwyconych danych.
   2. Dane są wysyłane do serwera C2.
   3. Serwer C2 używa pasującego klucza prywatnego do odszyfrowania danych. Dzięki temu nikt, kto przechwyci ruch sieciowy, nie
      będzie w stanie odczytać logów.


##  Uruchomienie Projektu
   1. Sklonuj repozytorium i zainstaluj zależności:


        - git clone <adres-twojego-repo>
        - cd ethical-keylogger
        - pip install pynput cryptography flask requests



   2. Wygeneruj klucze szyfrujące:

        - python3 generate_key.py

      W folderze pojawią się pliki `public_key.pem` i `private_key.pem`.

   3. Uruchom serwer C2 (w osobnym terminalu):

        - python3 c2_server.py

      Serwer będzie oczekiwał na połączenia przychodzące.

   4. Uruchom keyloggera (w drugim terminalu):

        - python3 main.py

      To uruchomi loader, który załaduje payload do pamięci. Od tego momentu klawisze są rejestrowane.



## C2 SERVER
<img width="640" height="337" alt="image" src="https://github.com/user-attachments/assets/57090903-7161-430f-88da-168416089bee" />


## Main
<img width="640" height="151" alt="image" src="https://github.com/user-attachments/assets/d4017924-6cd7-48aa-89b4-4e6148b41993" />





## ⚠️ Zastrzeżenie

To oprogramowanie służy **wyłącznie do celów badawczych i edukacyjnych**.  
Nie wolno go wdrażać ani rozpowszechniać bez uzyskania odpowiednich zgód prawnych i etycznych.
