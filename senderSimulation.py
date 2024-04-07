import pickle
import numpy as np
import matplotlib.pyplot as plt
import socket

def ASK_mod(m):
    N = len(m)
    Tb = 1
    fc = [50]
    rate = fc[0] * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[0] * t)
    ask_signal = np.zeros((N, len(t)))

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        if m[i] == 1:
            m_s = np.ones(len(t))
        else:
            m_s = np.zeros(len(t))
        ask_signal[i,:] = c*m_s

    transmit_message("ASK", fc, Tb, rate, ask_signal)

def FSK_mod(m):
    N = len(m)
    Tb = 1
    fc = [25, 50]
    rate = max(fc[0], fc[1]) * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c1 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[0] * t)
    c2 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[1] * t)
    fsk_signal = np.zeros((N, len(t)))

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        if m[i] == 1:
            m_s = np.ones(len(t))
            invm_s = np.zeros(len(t))
        else:
            m_s = np.zeros(len(t))
            invm_s = np.ones(len(t))
        fsk_sig1 = c1 * m_s
        fsk_sig2 = c2 * invm_s
        fsk_signal[i,:] = fsk_sig1 + fsk_sig2

    transmit_message("FSK", fc, Tb, rate, fsk_signal)

def transmit_message(sig,fc, Tb, rate, mod_sig):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    PORT = 12345
    s.connect((HOST, PORT))

    try:
        send = [sig,fc,Tb,rate,mod_sig]
        send_pickle = pickle.dumps(send)
        buffer = len(send_pickle).to_bytes(4,'big')
        s.sendall(buffer + send_pickle)
        print(f"{sig} message sent")
    except socket.error as e:
        print(f"An error occurred: {e}")
    finally:
        s.close()

m = input("Enter input signal:  ")
while set(m).issubset({'0', '1'}) is False:
    print("Error: Linecode should be binary")
    m = input("Enter linecode: ")

choose = input("Choose input signal {ASK/FSK}: ")
while choose not in ('ASK', 'FSK'):
    print("Error: Signals should be ASK or FSK")
    choose = input("Choose input signal {ASK/FSK}: ")

m = np.array(list(map(int, m)))
if choose == "ASK": ASK_mod(m)
elif choose == "FSK": FSK_mod(m)

