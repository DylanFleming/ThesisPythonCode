import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

def plot_mag_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(15, 12))
    fig.suptitle(title)

    # Filter frequencies up to 1 GHz (1e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Magnitude of S11, S12, and S22
    axs.set_title('Log Magnitude (S11, S12, S22)')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15), label='S11')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1]) + 1e-15), label='S12')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1]) + 1e-15), label='S22')

    # Labeling and grid
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Magnitude (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_phase_nano_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Phase response for S11, S22 and S12
    axs.set_title('Phase Response (S11, S12, S22)')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Phase (degrees)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_mag_nano_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 1 GHz (1e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Magnitude of S11, S12, and S22
    axs.set_title('Log Magnitude (S11, S12, S22)')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])), label='S11')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])), label='S12')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])), label='S22')

    # Labeling and grid
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Magnitude (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_return_nano_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 1 GHz (1e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Return Loss
    axs.set_title('Return Loss (S11)')
    return_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15)
    axs.plot(ntwk.f[freq_mask], return_loss, label='Return Loss (S11)')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Return Loss (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_insertion_nano_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 1 GHz (1e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Insertion Loss
    axs.set_title('Insertion Loss (S21)')
    insertion_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 0]) + 1e-15)
    axs.plot(ntwk.f[freq_mask], insertion_loss, label='Insertion Loss (S21)')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Insertion Loss (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_group_nano_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 1 GHz (1e9 Hz)
    max_freq = 1e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Group delay of S11 and S22
    axs.set_title('Group Delay (S11, S22)')
    group_delay_s11 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 0, 0]))) / np.diff(ntwk.f[freq_mask])
    group_delay_s22 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 1, 1]))) / np.diff(ntwk.f[freq_mask])
    axs.plot(ntwk.f[freq_mask][:-1], group_delay_s11, label='S11 Group Delay')
    axs.plot(ntwk.f[freq_mask][:-1], group_delay_s22, label='S22 Group Delay')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Group Delay (s)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()


def plot_phase_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Phase response of S11, S22, S21
    axs.set_title('Phase Response (S11, S12, S22)')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs.plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Phase (degrees)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_mag_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Magnitude of S11, S12, and S22
    axs.set_title('Log Magnitude (S11, S12, S22)')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])), label='S11')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])), label='S12')
    axs.plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])), label='S22')

    # Labeling and grid
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Magnitude (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_return_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Return Loss
    axs.set_title('Return Loss (S11)')
    return_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15)
    axs.plot(ntwk.f[freq_mask], return_loss, label='Return Loss (S11)')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Return Loss (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_insertion_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Insertion Loss
    axs.set_title('Insertion Loss (S21)')
    insertion_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 0]) + 1e-15)
    axs.plot(ntwk.f[freq_mask], insertion_loss, label='Insertion Loss (S21)')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Insertion Loss (dB)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)
    #plt.show()

def plot_group_s2p(ntwk, title, plot_title):
    # Create the figure and axis
    fig, axs = plt.subplots(figsize=(36, 16))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot: Group delay of S11 and S22
    axs.set_title('Group Delay (S11, S22)')
    group_delay_s11 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 0, 0]))) / np.diff(ntwk.f[freq_mask])
    group_delay_s22 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 1, 1]))) / np.diff(ntwk.f[freq_mask])
    axs.plot(ntwk.f[freq_mask][:-1], group_delay_s11, label='S11 Group Delay')
    axs.plot(ntwk.f[freq_mask][:-1], group_delay_s22, label='S22 Group Delay')
    axs.set_xlabel('Frequency (Hz)')
    axs.set_ylabel('Group Delay (s)')
    axs.grid(True)
    axs.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig(plot_title)  # Save the plot as a .png file
    #plt.show()

def plot_uncal_s2p(ntwk, title):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot 1: Smith chart with S11, S22, and S12
    axs[0, 0].set_title('Smith Chart (S11, S22, S12)')
    ntwk[freq_mask].plot_s_smith(m=0, n=0, ax=axs[0, 0], label='S11')
    ntwk[freq_mask].plot_s_smith(m=1, n=1, ax=axs[0, 0], label='S22')
    ntwk[freq_mask].plot_s_smith(m=0, n=1, ax=axs[0, 0], label='S12')

    # Plot 2: Magnitude of S11, S12, and S22
    axs[0, 1].set_title('Log Magnitude (S11, S12, S22)')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])+ 1e-15), label='S11')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])+ 1e-15), label='S12')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])+ 1e-15), label='S22')
    axs[0, 1].set_xlabel('Frequency (Hz)')
    axs[0, 1].set_ylabel('Magnitude (dB)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Plot 3: Phase response of S11, S12, and S22
    axs[1, 0].set_title('Phase Response (S11, S12, S22)')
    axs[1, 0].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs[1, 0].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs[1, 0].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs[1, 0].set_xlabel('Frequency (Hz)')
    axs[1, 0].set_ylabel('Phase (degrees)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Plot 4: Group delay of S11 and S22
    axs[1, 1].set_title('Group Delay (S11, S22)')
    group_delay_s11 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 0, 0]))) / np.diff(ntwk.f[freq_mask])
    group_delay_s22 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 1, 1]))) / np.diff(ntwk.f[freq_mask])
    axs[1, 1].plot(ntwk.f[freq_mask][:-1], group_delay_s11, label='S11 Group Delay')
    axs[1, 1].plot(ntwk.f[freq_mask][:-1], group_delay_s22, label='S22 Group Delay')
    axs[1, 1].set_xlabel('Frequency (Hz)')
    axs[1, 1].set_ylabel('Group Delay (s)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

def plot_s2p_pres(ntwk, title):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot 2: Magnitude of S11, S12, and S22
    axs[0, 0].set_title('Log Magnitude (S11, S12, S22)')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])), label='S11')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])), label='S12')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])), label='S22')
    axs[0, 0].set_xlabel('Frequency (Hz)')
    axs[0, 0].set_ylabel('Magnitude (dB)')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Plot 3: Phase response of S11, S12, and S22
    axs[0, 1].set_title('Phase Response (S11, S12, S22)')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs[0, 1].set_xlabel('Frequency (Hz)')
    axs[0, 1].set_ylabel('Phase (degrees)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Plot 5: Return loss (S11)
    axs[1, 0].set_title('Return Loss (S11)')
    return_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15)
    axs[1, 0].plot(ntwk.f[freq_mask], return_loss, label='Return Loss (S11)')
    axs[1, 0].set_xlabel('Frequency (Hz)')
    axs[1, 0].set_ylabel('Return Loss (dB)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Plot 6: Insertion loss (S21)
    axs[1, 1].set_title('Insertion Loss (S21)')
    insertion_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 0]) + 1e-15)
    axs[1, 1].plot(ntwk.f[freq_mask], insertion_loss, label='Insertion Loss (S21)')
    axs[1, 1].set_xlabel('Frequency (Hz)')
    axs[1, 1].set_ylabel('Insertion Loss (dB)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

def plot_s2p(ntwk, title):
    fig, axs = plt.subplots(2, 3, figsize=(15, 12))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot 1: Smith chart with S11, S22, and S12
    axs[0, 0].set_title('Smith Chart (S11, S22, S12)')
    ntwk[freq_mask].plot_s_smith(m=0, n=0, ax=axs[0, 0], label='S11')
    ntwk[freq_mask].plot_s_smith(m=1, n=1, ax=axs[0, 0], label='S22')
    ntwk[freq_mask].plot_s_smith(m=0, n=1, ax=axs[0, 0], label='S12')

    # Plot 2: Magnitude of S11, S12, and S22
    axs[0, 1].set_title('Log Magnitude (S11, S12, S22)')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])+ 1e-15), label='S11')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])+ 1e-15), label='S12')
    axs[0, 1].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])+ 1e-15), label='S22')
    axs[0, 1].set_xlabel('Frequency (Hz)')
    axs[0, 1].set_ylabel('Magnitude (dB)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Plot 3: Phase response of S11, S12, and S22
    axs[0, 2].set_title('Phase Response (S11, S12, S22)')
    axs[0, 2].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs[0, 2].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs[0, 2].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs[0, 2].set_xlabel('Frequency (Hz)')
    axs[0, 2].set_ylabel('Phase (degrees)')
    axs[0, 2].grid(True)
    axs[0, 2].legend()

    # Plot 4: Group delay of S11 and S22
    axs[1, 0].set_title('Group Delay (S11, S22)')
    group_delay_s11 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 0, 0]))) / np.diff(ntwk.f[freq_mask])
    group_delay_s22 = -np.diff(np.unwrap(np.angle(ntwk.s[freq_mask, 1, 1]))) / np.diff(ntwk.f[freq_mask])
    axs[1, 0].plot(ntwk.f[freq_mask][:-1], group_delay_s11, label='S11 Group Delay')
    axs[1, 0].plot(ntwk.f[freq_mask][:-1], group_delay_s22, label='S22 Group Delay')
    axs[1, 0].set_xlabel('Frequency (Hz)')
    axs[1, 0].set_ylabel('Group Delay (s)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Plot 5: Return loss (S11)
    axs[1, 1].set_title('Return Loss (S11)')
    return_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15)
    axs[1, 1].plot(ntwk.f[freq_mask], return_loss, label='Return Loss (S11)')
    axs[1, 1].set_xlabel('Frequency (Hz)')
    axs[1, 1].set_ylabel('Return Loss (dB)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    # Plot 6: Insertion loss (S21)
    axs[1, 2].set_title('Insertion Loss (S21)')
    insertion_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 0]) + 1e-15)
    axs[1, 2].plot(ntwk.f[freq_mask], insertion_loss, label='Insertion Loss (S21)')
    axs[1, 2].set_xlabel('Frequency (Hz)')
    axs[1, 2].set_ylabel('Insertion Loss (dB)')
    axs[1, 2].grid(True)
    axs[1, 2].legend()

    plt.tight_layout()
    plt.show()

def plot_s2p_pres(ntwk, title):
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(title)

    # Filter frequencies up to 6 GHz (6e9 Hz)
    max_freq = 6e9
    freq_mask = ntwk.f <= max_freq

    # Plot 1: Magnitude of S11, S12, and S22
    axs[0, 0].set_title('Log Magnitude (S11, S12, S22)')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0])), label='S11')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 1])), label='S12')
    axs[0, 0].plot(ntwk.f[freq_mask], 20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 1])), label='S22')
    axs[0, 0].set_xlabel('Frequency (Hz)')
    axs[0, 0].set_ylabel('Magnitude (dB)')
    axs[0, 0].grid(True)
    axs[0, 0].legend()

    # Plot 2: Phase response of S11, S12, and S22
    axs[0, 1].set_title('Phase Response (S11, S12, S22)')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 0], deg=True), label='S11')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 0, 1], deg=True), label='S12')
    axs[0, 1].plot(ntwk.f[freq_mask], np.angle(ntwk.s[freq_mask, 1, 1], deg=True), label='S22')
    axs[0, 1].set_xlabel('Frequency (Hz)')
    axs[0, 1].set_ylabel('Phase (degrees)')
    axs[0, 1].grid(True)
    axs[0, 1].legend()

    # Plot 3: Return loss (S11)
    axs[1, 0].set_title('Return Loss (S11)')
    return_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 0, 0]) + 1e-15)
    axs[1, 0].plot(ntwk.f[freq_mask], return_loss, label='Return Loss (S11)')
    axs[1, 0].set_xlabel('Frequency (Hz)')
    axs[1, 0].set_ylabel('Return Loss (dB)')
    axs[1, 0].grid(True)
    axs[1, 0].legend()

    # Plot 4: Insertion loss (S21)
    axs[1, 1].set_title('Insertion Loss (S21)')
    insertion_loss = -20 * np.log10(np.abs(ntwk.s[freq_mask, 1, 0]) + 1e-15)
    axs[1, 1].plot(ntwk.f[freq_mask], insertion_loss, label='Insertion Loss (S21)')
    axs[1, 1].set_xlabel('Frequency (Hz)')
    axs[1, 1].set_ylabel('Insertion Loss (dB)')
    axs[1, 1].grid(True)
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

def plot_s2p_comparison_four(ntwk1, ntwk2, ntwk3, ntwk4, title):
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))  # Adjust figure size for poster
    fig.suptitle(title, fontsize=28)  # Large title for the poster

    max_freq = 1.2e9
    freq_mask = ntwk1.f <= max_freq

    # Define labels
    labels = ['NanoVNA-H4', 'FieldFox N9916A', 'R&S ZVL', 'Ideal']

    # Set tick parameters for all subplots
    for ax in axs.flat:
        ax.tick_params(axis='both', which='major', labelsize=16)  # Increase tick label size
        ax.tick_params(axis='both', which='minor', labelsize=12)

    # Smith Chart for S11, S22, S12
    axs[0, 0].set_title('Smith Chart S11', fontsize=22)
    ntwk1.plot_s_smith(m=0, n=0, ax=axs[0, 0], show_legend=False)
    ntwk2.plot_s_smith(m=0, n=0, ax=axs[0, 0], show_legend=False)
    ntwk3.plot_s_smith(m=0, n=0, ax=axs[0, 0], show_legend=False)
    ntwk4.plot_s_smith(m=0, n=0, ax=axs[0, 0], show_legend=False)

    axs[0, 1].set_title('Smith Chart S22', fontsize=22)
    ntwk1.plot_s_smith(m=1, n=1, ax=axs[0, 1], show_legend=False)
    ntwk2.plot_s_smith(m=1, n=1, ax=axs[0, 1], show_legend=False)
    ntwk3.plot_s_smith(m=1, n=1, ax=axs[0, 1], show_legend=False)
    ntwk4.plot_s_smith(m=1, n=1, ax=axs[0, 1], show_legend=False)

    axs[0, 2].set_title('Smith Chart S12', fontsize=22)
    ntwk1.plot_s_smith(m=0, n=1, ax=axs[0, 2], show_legend=False)
    ntwk2.plot_s_smith(m=0, n=1, ax=axs[0, 2], show_legend=False)
    ntwk3.plot_s_smith(m=0, n=1, ax=axs[0, 2], show_legend=False)
    ntwk4.plot_s_smith(m=0, n=1, ax=axs[0, 2], show_legend=False)

    # Log magnitude plots
    axs[1, 0].set_title('Log Magnitude S11', fontsize=22)
    axs[1, 0].plot(ntwk1.f, 20 * np.log10(np.abs(ntwk1.s[freq_mask, 0, 0])), color='C0', label=labels[0])
    axs[1, 0].plot(ntwk2.f, 20 * np.log10(np.abs(ntwk2.s[:, 0, 0])), color='C1', label=labels[1])
    axs[1, 0].plot(ntwk3.f, 20 * np.log10(np.abs(ntwk3.s[:, 0, 0])), color='C2', label=labels[2])
    axs[1, 0].plot(ntwk4.f, 20 * np.log10(np.abs(ntwk4.s[:, 0, 0])), color='C3', label=labels[3])
    axs[1, 0].set_xlabel('Frequency (Hz)', fontsize=20)
    axs[1, 0].set_ylabel('Magnitude (dB)', fontsize=20)
    axs[1, 0].grid(True)

    axs[1, 1].set_title('Log Magnitude S22', fontsize=22)
    axs[1, 1].plot(ntwk1.f, 20 * np.log10(np.abs(ntwk1.s[freq_mask, 1, 1])), color='C0')
    axs[1, 1].plot(ntwk2.f, 20 * np.log10(np.abs(ntwk2.s[:, 1, 1])), color='C1')
    axs[1, 1].plot(ntwk3.f, 20 * np.log10(np.abs(ntwk3.s[:, 1, 1])), color='C2')
    axs[1, 1].plot(ntwk4.f, 20 * np.log10(np.abs(ntwk4.s[:, 1, 1])), color='C3')
    axs[1, 1].set_xlabel('Frequency (Hz)', fontsize=20)
    axs[1, 1].set_ylabel('Magnitude (dB)', fontsize=20)
    axs[1, 1].grid(True)

    axs[1, 2].set_title('Log Magnitude S12', fontsize=22)
    axs[1, 2].plot(ntwk1.f, 20 * np.log10(np.abs(ntwk1.s[freq_mask, 0, 1])), color='C0')
    axs[1, 2].plot(ntwk2.f, 20 * np.log10(np.abs(ntwk2.s[:, 0, 1])), color='C1')
    axs[1, 2].plot(ntwk3.f, 20 * np.log10(np.abs(ntwk3.s[:, 0, 1])), color='C2')
    axs[1, 2].plot(ntwk4.f, 20 * np.log10(np.abs(ntwk4.s[:, 0, 1])), color='C3')
    axs[1, 2].set_xlabel('Frequency (Hz)', fontsize=20)
    axs[1, 2].set_ylabel('Magnitude (dB)', fontsize=20)
    axs[1, 2].grid(True)

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to leave space for title
    plt.show()

