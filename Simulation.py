# ASK

import numpy as np
import matplotlib.pyplot as plt

Tb = 1
fc = 10
t = np.arange(0, 1 + Tb/100, Tb/100)
c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc * t)

# generate message signal
N = 8
m = np.random.rand(N)
t1, t2 = 0, Tb

plt.figure("ASK")

for i in range(N):
    t = np.arange(t1, t2 + 0.01, 0.01)
    if m[i] > 0.5:
        m[i] = 1
        m_s = np.ones(len(t))
    else:
        m[i] = 0
        m_s = np.zeros(len(t))

    message = np.tile(m_s, (N, 1))

    ask_sig = c * m_s

    t1 = t1+(Tb+ 0.01)
    t2 = t2+(Tb+ 0.01)


    # Plot the message and ASK signal
    plt.subplot(5,1,2)
    plt.axis([0, N, -2, 2])
    plt.plot(t,message[i,:],'r')
    plt.title('message signal')
    plt.xlabel('t--->')
    plt.ylabel('m(t)')
    plt.grid(True)
    plt.subplot(5,1,4)
    plt.plot(t, ask_sig)
    plt.title('ASK signal')
    plt.xlabel('t--->')
    plt.ylabel('s(t)')
    plt.grid(True)

# Plot the carrier signal and input binary data
plt.subplot(5,1,3)
plt.plot(t, c)
plt.title('carrier signal')
plt.xlabel('t--->')
plt.ylabel('c(t)')
plt.grid(True)
plt.subplot(5,1,1)
plt.stem(m)
plt.title('binary data bits')
plt.xlabel('n--->')
plt.ylabel('b(n)')
plt.grid(True)

plt.tight_layout()
plt.show()


# FSK
import numpy as np
import matplotlib.pyplot as plt

# generate carrier signal
Tb = 1
fc1 = 2
fc2 = 5

t = np.arange(0, Tb + Tb/100, Tb/100)
c1 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc1 * t)
c2 = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc2 * t)

# generate message signal
N = 8
# m = np.random.rand(N)
t1 = 0
t2 = Tb

message = np.zeros((N, len(t)))
fsk = np.zeros((N, len(t)))

plt.figure("FSK")

for i in range(N):
    t = np.arange(t1, t2 + Tb/100, Tb/100)
    if m[i] > 0.5:
        m[i] = 1
        m_s = np.ones(len(t))
        invm_s = np.zeros(len(t))
    else:
        m[i] = 0
        m_s = np.zeros(len(t))
        invm_s = np.ones(len(t))

    message[i, :] = m_s

    fsk_sig1 = c1 * m_s
    fsk_sig2 = c2 * invm_s
    fsk[i, :] = fsk_sig1 + fsk_sig2

    # plotting the message signal and the modulated signal
    plt.subplot(3,2,2)
    plt.axis([0, N, -2, 2])
    plt.plot(t,message[i,:], 'r')
    plt.title('message signal')
    plt.xlabel('t---->')
    plt.ylabel('m(t)')
    plt.grid(True)
    plt.subplot(3,2,5)
    plt.plot(t,fsk[i,:])
    plt.title('FSK signal')
    plt.xlabel('t---->')
    plt.ylabel('s(t)')
    plt.grid(True)

    t1 = t1+(Tb+ 0.01)
    t2 = t2+(Tb+ 0.01)

# plotting binary data bits and carrier signal
plt.subplot(3,2,1)
plt.stem(m)
plt.title('binary data')
plt.xlabel('n---->')
plt.ylabel('b(n)')
plt.grid(True)

plt.subplot(3,2,3)
plt.plot(t, c1)
plt.title('carrier signal-1')
plt.xlabel('t---->')
plt.ylabel('c1(t)')
plt.grid(True)

plt.subplot(3,2,4)
plt.plot(t, c2)
plt.title('carrier signal-2')
plt.xlabel('t---->')
plt.ylabel('c2(t)')
plt.grid(True)

plt.tight_layout()
plt.show()
