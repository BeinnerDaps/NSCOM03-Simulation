import pickle
import numpy as np
import matplotlib.pyplot as plt
import socket

def receive_message():
    arr = []
    s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    PORT = 12345
    s.bind((HOST, PORT))
    s.listen(1)
    s.settimeout(100.0)
    print(f"Listening on {HOST}:{PORT}")
    try:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                try:
                    data = conn.recv(4)
                    if not data:
                        break
                    d_len = int.from_bytes(data,'big')
                    received = b''
                    while len(received) < d_len:
                        chunk = d_len-len(received)
                        received += conn.recv(chunk)
                    arr.extend(pickle.loads(received))
                except EOFError as e:
                        break
                except Exception as e:
                        print(f"Exception:{e}")
                        break
    except socket.timeout:
        print("Connection timeout")
    finally:
        s.close()
    if arr:
        if arr[0] == "ASK":
            ASK_demod(arr[1],arr[2],arr[3],arr[4])
        elif arr[0] == "FSK":
            FSK_demod(arr[1],arr[2],arr[3],arr[4])

def ASK_demod(fc,Tb,rate,ask_signal):
    m,c = [],[]
    N = len(ask_signal)
    t = np.arange(0, Tb, Tb/rate)
    c = np.sqrt(2/Tb)*np.sin(2*np.pi*fc[0]*t)

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        sig = ask_signal[i,:]*c
        m += [1] if sum(sig) > max(sig) else [0]

        #Plot ASK signal
        plt.figure("ASK", figsize=(10, 7))
        plt.subplot(2,1,2)
        plt.plot(t, ask_signal[i,:])
        plt.title('ASK signal')
        plt.xlabel('t--->')
        plt.ylabel('s(t)')
        plt.fill_between(t, ask_signal[i,:], where=ask_signal[i,:] > 0, color='green', step='pre')
        plt.fill_between(t, 0, where=ask_signal[i,:] <= 0, color='red', step='pre')
        plt.grid(True)

    m = np.array(m)
    print(f'ASK: {m}')

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
        sum1 = np.sum(co1)
        sum0 = np.sum(co0)
        m += [1] if  sum1 > sum0 else [0]

        # Plot FSK signal
        plt.figure("ASK", figsize=(10, 7))
        plt.subplot(3,1,3)
        plt.plot(t,fsk_signal[i,:])
        plt.title('FSK signal')
        plt.xlabel('t---->')
        plt.ylabel('s(t)')
        plt.grid(True)

    m = np.array(m)
    print(f'FSK: {m}')

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
