import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

def error_calc(uncalibrated, calibrated, plot_title):
    frequency = uncalibrated.f  # Frequency in Hz from the Network object

    uncalibrated = uncalibrated.interpolate(calibrated.f)   # Interpolate uncalibrated frequency range to match calibrated
                                                            # in case there is any discrepency
    # Calculating simple error terms
    Ed = uncalibrated.s11 - calibrated.s11  # Directivity
    Es = uncalibrated.s11 / calibrated.s11  # Source Mismatch
    El = uncalibrated.s22 / calibrated.s22  # Load Mismatch
    Ex = uncalibrated.s21 - calibrated.s21  # Crosstalk
    Er = uncalibrated.s11 * calibrated.s11  # Reflection Tracking
    Et = uncalibrated.s21 / calibrated.s21  # Transmission Tracking

    # Convert all error terms to decibels
    Ed_db = 20 * np.log10(np.abs(Ed.s))  # Directivity
    Es_db = 20 * np.log10(np.abs(Es.s))  # Source Mismatch
    El_db = 20 * np.log10(np.abs(El.s))  # Load Mismatch
    Ex_db = 20 * np.log10(np.abs(Ex.s))  # Crosstalk
    Er_db = 20 * np.log10(np.abs(Er.s))  # Reflection Tracking
    Et_db = 20 * np.log10(np.abs(Et.s))  # Transmission Tracking

    # Plot the error terms in dB over frequency
    plt.figure(figsize=(10, 6))

    plt.plot(frequency, Ed_db.flatten(), label='Directivity [dB]')
    plt.plot(frequency, Es_db.flatten(), label='Source Mismatch [dB]')
    plt.plot(frequency, El_db.flatten(), label='Load Mismatch [dB]')
    plt.plot(frequency, Ex_db.flatten(), label='Crosstalk [dB]')
    plt.plot(frequency, Er_db.flatten(), label='Reflection Tracking [dB]')
    plt.plot(frequency, Et_db.flatten(), label='Transmission Tracking [dB]')

    plt.title(plot_title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Error Magnitude (dB)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
