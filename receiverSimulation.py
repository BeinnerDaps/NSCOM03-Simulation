import pickle
import numpy as np
import matplotlib.pyplot as plt
import socket

def receive_message():
    array = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 12345
        s.bind((HOST, PORT))

        s.listen(5)
        print(f"Listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    array.append(pickle.loads(data))
                    print(f"Received array: {array}")
                    # ASK_demod(array[0],array[1],array[2],array[3])
                except EOFError as e:
                    break
                except Exception as e:
                    print(f"Exception:{e}")
                    break

# def ASK_demod(fc,Tb,rate,ask_signal):
#     N = len(ask_signal) // (rate * Tb)
#     t = np.arange(0, N*Tb, Tb/rate)
#     c = []
#     for i in fc:
#         c.append(np.sqrt(2/Tb)*np.sin(2*np.pi*fc[i]*t))

#     # Coherent Detection
#     msg_sig = ask_signal * c

#     lp_signal = np.zeros(N)
#     for i in range(N):
#         lp_signal[i] = np.mean(msg_sig[i*rate:(i+1)*rate])

receive_message()
