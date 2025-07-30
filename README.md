# 🔐 Etyczny Keylogger (Ethical Keylogger)

Ten projekt to moje osobiste wyzwanie: stworzyć działającego keyloggera w Pythonie całkowicie od podstaw.  
Celem jest zasymulowanie, jak działają prawdziwe narzędzia — **wyłącznie w celach edukacyjnych, red teamingu oraz treningu obrony**.

## 📚 Wykorzystywane biblioteki

- **pynput** – do nasłuchiwania naciśnięć klawiszy
- **cryptography** – do szyfrowania danych  
  (na początku używamy szyfrowania **symetrycznego**, ponieważ program działa lokalnie; po dodaniu C2 przejdziemy na **asymetryczne**)
- **Fernet** – używany do szyfrowania symetrycznego

## ⚠️ Zastrzeżenie

To oprogramowanie służy **wyłącznie do celów badawczych i edukacyjnych**.  
Nie wolno go wdrażać ani rozpowszechniać bez uzyskania odpowiednich zgód prawnych i etycznych.
