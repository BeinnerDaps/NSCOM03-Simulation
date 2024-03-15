# ASK
import numpy as np
import matplotlib.pyplot as plt

def ASK(m):
    Tb = 1
    fc = 50
    sampling_rate = fc * 2 * 10
    t = np.arange(0, Tb, Tb/sampling_rate)
    c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc * t)

    # generate message signal
    N = len(m)
    plt.figure("ASK", figsize=(15, 8))

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/sampling_rate)
        m_s = np.ones(len(t)) if m[i] == 1 else np.zeros(len(t))

        message = np.tile(m_s, (N, 1))
        ask_sig = c*m_s

        # Plot the message and ASK signal
        plt.subplot(4,1,2)
        plt.axis([0, N, -2, 2])
        plt.plot(t,message[i,:],'r')
        plt.title('message signal')
        plt.xlabel('t--->')
        plt.ylabel('m(t)')
        plt.grid(True)

        plt.subplot(4,1,4)
        plt.plot(t, ask_sig)
        plt.title('ASK signal')
        plt.xlabel('t--->')
        plt.ylabel('s(t)')
        plt.grid(True)

    # Plot the carrier signal and input binary data
    plt.subplot(4,1,3)
    plt.plot(t, c)
    plt.title('carrier signal')
    plt.xlabel('t--->')
    plt.ylabel('c(t)')
    plt.grid(True)

    plt.subplot(4,1,1)
    plt.stem(m)
    plt.title('binary data bits')
    plt.xlabel('n--->')
    plt.ylabel('b(n)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def FSK (m):
    # generate carrier signal
    Tb = 1
    fc1, fc2 = 25, 50
    sampling_rate = max(fc1, fc2) * 2 * 10
    t = np.arange(0, Tb, Tb/sampling_rate)
    c1 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc1 * t)
    c2 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc2 * t)

    # generate message signal
    N = len(m)
    message = np.zeros((N, len(t)))
    fsk = np.zeros((N, len(t)))

    plt.figure("FSK", figsize=(15, 8))

    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/sampling_rate)
        if m[i] == 1:
            m_s = np.ones(len(t))
            invm_s = np.zeros(len(t))
        else:
            m_s = np.zeros(len(t))
            invm_s = np.ones(len(t))

        message[i, :] = m_s

        fsk_sig1 = c1 * m_s
        fsk_sig2 = c2 * invm_s
        fsk[i, :] = fsk_sig1 + fsk_sig2

        # plotting the message signal and the modulated signal
        plt.subplot(5,1,2)
        plt.axis([0, N, -2, 2])
        plt.plot(t,message[i,:], 'r')
        plt.title('message signal')
        plt.xlabel('t---->')
        plt.ylabel('m(t)')
        plt.grid(True)

        plt.subplot(5,1,5)
        plt.plot(t,fsk[i,:])
        plt.title('FSK signal')
        plt.xlabel('t---->')
        plt.ylabel('s(t)')
        plt.grid(True)

    # plotting binary data bits and carrier signal
    plt.subplot(5,1,1)
    plt.stem(m)
    plt.title('binary data')
    plt.xlabel('n---->')
    plt.ylabel('b(n)')
    plt.grid(True)

    plt.subplot(5,1,3)
    plt.plot(t, c1)
    plt.title('carrier signal-1')
    plt.xlabel('t---->')
    plt.ylabel('c1(t)')
    plt.grid(True)

    plt.subplot(5,1,4)
    plt.plot(t, c2)
    plt.title('carrier signal-2')
    plt.xlabel('t---->')
    plt.ylabel('c2(t)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

m = input("Enter input signal:  ")
while set(m).issubset({'0', '1'}) is False:
    print("Error: Linecode should be binary")
    m = input("Enter linecode: ")

choose = input("Choose input signal {ASK/FSK}: ")
while choose not in ('ASK', 'FSK'):
    print("Error: Signals should be ASK or FSK")
    choose = input("Choose input signal: (ASK/FSK)")

m = np.array(list(map(int, m)))
if choose == "ASK":
    ASK(m)
elif choose == "FSK":
    FSK(m)

