# ASK
import pickle
import numpy as np
import matplotlib.pyplot as plt
import socket

def ASK_mod(m):
    N = len(m)
    Tb = 1
    fc = []
    fc.append(50)
    rate = fc[0] * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[0] * t)

    plt.figure("ASK", figsize=(10, 7))
    ask_signal = np.zeros((N, len(t)))
    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        if m[i] == 1:
            m_s = np.ones(len(t))
        else:
            m_s = np.zeros(len(t))

        ask_signal[i,:] = c*m_s
        # print(ask_signal[i*(len(t)//len(m)):(i+1)*(len(t)//len(m))])

        # Plot ASK signal
        plt.subplot(2,1,2)
        plt.plot(t, ask_signal[i,:])
        plt.title('ASK signal')
        plt.xlabel('t--->')
        plt.ylabel('s(t)')
        plt.grid(True)

    # Plot the carrier signal
    plt.subplot(2,1,1)
    plt.plot(t, c)
    plt.title('carrier signal')
    plt.xlabel('t--->')
    plt.ylabel('c(t)')
    plt.grid(True)

    transmit_message(fc, Tb, rate, ask_signal)

    plt.tight_layout()
    # plt.show()

def FSK_mod(m):
    N = len(m)
    Tb = 1
    fc = []
    fc.append(25)
    fc.append(50)
    rate = max(fc[0], fc[1]) * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c1 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[0] * t)
    c2 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc[1] * t)
    fsk_signal = np.zeros((N, len(t)))

    plt.figure("FSK", figsize=(15, 7))
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

        # plotting the message signal
        plt.subplot(3,1,3)
        plt.plot(t,fsk_signal[i,:])
        plt.title('FSK signal')
        plt.xlabel('t---->')
        plt.ylabel('s(t)')
        plt.grid(True)

    # plotting carrier signals
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

    transmit_message(fc, Tb, rate, fsk_signal)

def transmit_message(fc, Tb, rate, mod_sig):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        HOST = socket.gethostbyname(socket.gethostname())
        PORT = 12345
        s.connect((HOST, PORT))
        send = [fc,Tb,rate]
        send_pickle = pickle.dumps(send)
        s.sendall(send_pickle)
        for i in mod_sig:
            send_pickle = pickle.dumps(i)
            s.sendall(len(send_pickle).to_bytes(4,'big') + send_pickle)
        s.close()

# m = input("Enter input signal:  ")
# while set(m).issubset({'0', '1'}) is False:
#     print("Error: Linecode should be binary")
#     m = input("Enter linecode: ")

# choose = input("Choose input signal {ASK/FSK}: ")
# while choose not in ('ASK', 'FSK'):
#     print("Error: Signals should be ASK or FSK")
#     choose = input("Choose input signal: (ASK/FSK)")
m = "010101011"
choose = "ASK"
m = np.array(list(map(int, m)))
if choose == "ASK":
    ASK_mod(m)
elif choose == "FSK":
    FSK_mod(m)

