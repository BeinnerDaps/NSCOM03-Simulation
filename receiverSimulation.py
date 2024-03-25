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
        s.listen(1)
        print(f"Listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(4)
                    if not data:
                        break
                    data_len = int.from_bytes(data, 'big')
                    received = b''
                    while len(received) < data_len:
                        chunk = conn.recv(data_len-len(received))
                        if not chunk:
                            raise ValueError("Could not complete transfer")
                        received += chunk
                    array.extend(pickle.loads(received))
                except EOFError as e:
                    break
                except Exception as e:
                    print(f"Exception:{e}")
                    break

        if array[0] == "ASK":
            ASK_demod(array[1],array[2],array[3],array[4])
        elif array[0] == "FSK":
            FSK_demod(array[1],array[2],array[3],array[4])

def ASK_demod(fc,Tb,rate,ask_signal):
    m,c = [],[]
    N = len(ask_signal)
    t = np.arange(0, Tb, Tb/rate)
    c = np.sqrt(2/Tb)*np.sin(2*np.pi*fc[0]*t)

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        sig = ask_signal[i,:]*c
        m.append(1) if sum(sig) > max(sig) else m.append(0)

        #Plot ASK signal
        plt.figure("ASK", figsize=(10, 7))
        plt.subplot(2,1,2)
        plt.plot(t, ask_signal[i,:])
        plt.title('ASK signal')
        plt.xlabel('t--->')
        plt.ylabel('s(t)')
        plt.grid(True)

    m = np.array(m)
    print(m)

    # Plotting carrier signal
    plt.subplot(2,1,1)
    plt.plot(t, c)
    plt.title('carrier signal')
    plt.xlabel('t--->')
    plt.ylabel('c(t)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def FSK_demod(fc,Tb,rate,fsk_signal):
    m = []
    N = len(fsk_signal)
    t = np.arange(0, Tb, Tb/rate)
    c1 = np.sqrt(2/Tb)*np.sin(2*np.pi*fc[0]*t) # 25
    c2 = np.sqrt(2/Tb)*np.sin(2*np.pi*fc[1]*t) # 50

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        segment = fsk_signal[i,:]
        co1 = segment * c1[:len(segment)]
        co0 = segment * c2[:len(segment)]
        m.append(1) if np.sum(co1) > np.sum(co0) else m.append(0)

        # Plot FSK signal
        plt.figure("ASK", figsize=(10, 7))
        plt.subplot(3,1,3)
        plt.plot(t,fsk_signal[i,:])
        plt.title('FSK signal')
        plt.xlabel('t---->')
        plt.ylabel('s(t)')
        plt.grid(True)

    m = np.array(m)
    print(m)

    # Plotting carrier signals
    plt.subplot(3,1,1)
    plt.plot(t, c1)
    plt.title('carrier signal-1')
    plt.xlabel('t---->')
    plt.ylabel('c1(t)')
    plt.grid(True)

    plt.subplot(3,1,2)
    plt.plot(t, c2)
    plt.title('carrier signal-2')
    plt.xlabel('t---->')
    plt.ylabel('c2(t)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

receive_message()
