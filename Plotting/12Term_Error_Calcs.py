# =========================================================================
#           12 Term Error Model - Combined Plot
#           By Dylan Fleming, 45313345
# =========================================================================

# Imports
import skrf as rf
import numpy as np
import matplotlib.pyplot as plt


def full_12_term_error_calc(uncalibrated, calibrated, plot_title):
    """
    full_12_term_error_calc is a handler to calculate and plot the full 12 term error model
    :param uncalibrated: The uncalibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param calibrated: The calibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param plot_title: A string representing the title to be displayed on the plot
    :return: NULL
    """
    uncalibrated = uncalibrated.interpolate(calibrated.f) # Interpolate uncalibrated frequency range to match calibrated
                                                          # in case there is any discrepency

    # Extract the measured S-parameters (from uncalibrated) and "true" S-parameters (from calibrated)
    S11_meas, S21_meas, S12_meas, S22_meas = uncalibrated.s11, uncalibrated.s21, uncalibrated.s12, uncalibrated.s22
    S11_true, S21_true, S12_true, S22_true = calibrated.s11, calibrated.s21, calibrated.s12, calibrated.s22

    # Calculate the error terms for the 12-term error model
    # Directivity errors
    Ed1 = S11_meas - S11_true  # Error in S11 reflection at port 1
    Ed2 = S22_meas - S22_true  # Error in S22 reflection at port 2

    # Source match errors
    Es1 = (S11_meas / S11_true) - 1  # Source match at port 1
    Es2 = (S22_meas / S22_true) - 1  # Source match at port 2

    # Load match errors
    El1 = (S11_true / S11_meas) - 1  # Load match at port 1
    El2 = (S22_true / S22_meas) - 1  # Load match at port 2

    # Crosstalk errors
    Ex12 = S21_meas - S21_true  # Crosstalk from port 1 to 2
    Ex21 = S12_meas - S12_true  # Crosstalk from port 2 to 1

    # Reflection tracking errors
    Er1 = S11_meas * S11_true   # Reflection tracking for S11
    Er2 = S22_meas * S22_true   # Reflection tracking for S22

    # Transmission tracking errors
    Et1 = S21_meas / S21_true   # Transmission tracking for S21
    Et2 = S12_meas / S12_true   # Transmission tracking for S12

    # Plotting the error terms over frequency
    frequency = uncalibrated.f  # Frequency in Hz from the Network object

    plt.figure(figsize=(15, 6))
    plt.plot(frequency, 20 * np.log10(np.abs(Ed1.s.flatten())), label='Directivity Error (Ed1) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Ed2.s.flatten())), label='Directivity Error (Ed2) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Es1.s.flatten())), label='Source Match Error (Es1) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Es2.s.flatten())), label='Source Match Error (Es2) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(El1.s.flatten())), label='Load Match Error (El1) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(El2.s.flatten())), label='Load Match Error (El2) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Ex12.s.flatten())), label='Crosstalk Error (Ex12) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Ex21.s.flatten())), label='Crosstalk Error (Ex21) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Er1.s.flatten())), label='Reflection Tracking Error (Er1) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Er2.s.flatten())), label='Reflection Tracking Error (Er2) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Et1.s.flatten())), label='Transmission Tracking Error (Et1) [dB]')
    plt.plot(frequency, 20 * np.log10(np.abs(Et2.s.flatten())), label='Transmission Tracking Error (Et2) [dB]')

    plt.title(plot_title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Error Magnitude (dB)')

    # Moving legend to the right side of the plot
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)

    plt.grid(True)
    plt.tight_layout()
    plt.show()
