# ASK
import numpy as np
import matplotlib.pyplot as plt

def ASK(m):
    N = len(m)
    Tb = 1
    fc = 50
    rate = fc * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc * t)

    plt.figure("ASK", figsize=(20, 7))
    for i in range(N):
        t = np.arange(i*Tb, (i+1)*Tb, Tb/rate)
        if m[i] == 1:
            m_s = np.ones(len(t))
        else:
            m_s = np.zeros(len(t))

        # Plot ASK signal
        plt.subplot(2,1,2)
        plt.plot(t, c*m_s)
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

    plt.tight_layout()
    plt.show()


def FSK (m):
    N = len(m)
    Tb = 1
    fc1, fc2 = 25, 50
    rate = max(fc1, fc2) * 2 * 10
    t = np.arange(0, Tb, Tb/rate)
    c1 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc1 * t)
    c2 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc2 * t)
    fsk = np.zeros((N, len(t)))

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
        fsk[i, :] = fsk_sig1 + fsk_sig2

        # plotting the message signal
        plt.subplot(3,1,3)
        plt.plot(t,fsk[i,:])
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

