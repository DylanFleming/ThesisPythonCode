# =========================================================================
#           12 Term Error Model - Comparison of Term Plots
#           By Dylan Fleming, 45313345
# =========================================================================

# Imports
import skrf as rf
import numpy as np
import matplotlib.pyplot as plt


def plot_error_terms(frequency, uncalibrated, calibrated_1, calibrated_2, label_base):
    """
    plot_error_terms plots the comparison error terms as separate plots on same subplot frame
    :param frequency: The frequency range to plot over
    :param uncalibrated: The uncalibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param calibrated_1: The first calibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param calibrated_2: The second calibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param label_base: A string defining type of device that is being tested
    :return: NULL
    """
    # Directivity errors
    Ed1_case1 = uncalibrated[0] - calibrated_1[0]
    Ed2_case1 = uncalibrated[3] - calibrated_1[3]
    Ed1_case2 = uncalibrated[0] - calibrated_2[0]
    Ed2_case2 = uncalibrated[3] - calibrated_2[3]

    # Source match errors
    Es1_case1 = (uncalibrated[0] / calibrated_1[0]) - 1
    Es2_case1 = (uncalibrated[3] / calibrated_1[3]) - 1
    Es1_case2 = (uncalibrated[0] / calibrated_2[0]) - 1
    Es2_case2 = (uncalibrated[3] / calibrated_2[3]) - 1

    # Load match errors
    El1_case1 = (calibrated_1[0] / uncalibrated[0]) - 1
    El2_case1 = (calibrated_1[3] / uncalibrated[3]) - 1
    El1_case2 = (calibrated_2[0] / uncalibrated[0]) - 1
    El2_case2 = (calibrated_2[3] / uncalibrated[3]) - 1

    # Crosstalk errors
    Ex12_case1 = uncalibrated[1] - calibrated_1[1]
    Ex21_case1 = uncalibrated[2] - calibrated_1[2]
    Ex12_case2 = uncalibrated[1] - calibrated_2[1]
    Ex21_case2 = uncalibrated[2] - calibrated_2[2]

    # Reflection tracking errors
    Er1_case1 = uncalibrated[0] * calibrated_1[0]
    Er2_case1 = uncalibrated[3] * calibrated_1[3]
    Er1_case2 = uncalibrated[0] * calibrated_2[0]
    Er2_case2 = uncalibrated[3] * calibrated_2[3]

    # Transmission tracking errors
    Et1_case1 = uncalibrated[1] / calibrated_1[1]
    Et2_case1 = uncalibrated[2] / calibrated_1[2]
    Et1_case2 = uncalibrated[1] / calibrated_2[1]
    Et2_case2 = uncalibrated[2] / calibrated_2[2]

    # List of error terms for plotting
    # Forward errors on row 1, backward errors on row 2
    error_terms_row1_case1 = [Ed1_case1, Es1_case1, El1_case1, Ex12_case1, Er1_case1, Et1_case1]
    error_terms_row2_case1 = [Ed2_case1, Es2_case1, El2_case1, Ex21_case1, Er2_case1, Et2_case1]
    error_terms_row1_case2 = [Ed1_case2, Es1_case2, El1_case2, Ex12_case2, Er1_case2, Et1_case2]
    error_terms_row2_case2 = [Ed2_case2, Es2_case2, El2_case2, Ex21_case2, Er2_case2, Et2_case2]

    labels_row1 = ['Directivity (Ed1)', 'Source Match (Es1)', 'Load Match (El1)', 'Crosstalk (Ex12)',
                   'Reflection Tracking (Er1)', 'Transmission Tracking (Et1)']
    labels_row2 = ['Directivity (Ed2)', 'Source Match (Es2)', 'Load Match (El2)', 'Crosstalk (Ex21)',
                   'Reflection Tracking (Er2)', 'Transmission Tracking (Et2)']

    # Create subplots for each error term in a 2-row, 6-column grid
    plt.figure(figsize=(36, 16))
    # Plot forward errors (Row 1)
    for i in range(6):
        plt.subplot(2, 6, i + 1)  # First row (6 columns)
        plt.plot(frequency, 20 * np.log10(np.abs(error_terms_row1_case1[i].s.flatten())),
                 label=f'{label_base} Mechanical Standard')
        plt.plot(frequency, 20 * np.log10(np.abs(error_terms_row1_case2[i].s.flatten())),
                 label=f'{label_base} Electronic Standard')
        plt.title(labels_row1[i])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Error Magnitude (dB)')
        plt.legend()
        plt.grid(True)

    # Plot backward errors (Row 2)
    for i in range(6):
        plt.subplot(2, 6, i + 7)  # Second row (6 columns)
        plt.plot(frequency, 20 * np.log10(np.abs(error_terms_row2_case1[i].s.flatten())),
                 label=f'{label_base} Mechanical Standard')
        plt.plot(frequency, 20 * np.log10(np.abs(error_terms_row2_case2[i].s.flatten())),
                 label=f'{label_base} Electronic Standard')
        plt.title(labels_row2[i])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Error Magnitude (dB)')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()

def error_12_term_comparison(uncalibrated, calibrated_1, calibrated_2):
    """
    error_12_term_comparison is a handler to initiate the comparison calculation of 12 term error model
    :param uncalibrated: The uncalibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param calibrated_1: The first calibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :param calibrated_2: The second calibrated measurement network in the form of rf.Network('path-to-file.s2p')
    :return: NULL
    """
    # Interpolate both calibrated networks to match the frequency of the uncalibrated data
    calibrated_1 = calibrated_1.interpolate(uncalibrated.f)
    calibrated_2 = calibrated_2.interpolate(uncalibrated.f)

    # Extract the S-parameters for the uncalibrated and both calibrated cases
    S11_meas, S21_meas, S12_meas, S22_meas = uncalibrated.s11, uncalibrated.s21, uncalibrated.s12, uncalibrated.s22
    S11_true_case1, S21_true_case1, S12_true_case1, S22_true_case1 = calibrated_1.s11, calibrated_1.s21, calibrated_1.s12, calibrated_1.s22
    S11_true_case2, S21_true_case2, S12_true_case2, S22_true_case2 = calibrated_2.s11, calibrated_2.s21, calibrated_2.s12, calibrated_2.s22

    # Frequency for plotting
    frequency = uncalibrated.f

    # Combine the measured and true S-parameters into lists for easier processing
    S_meas = [S11_meas, S21_meas, S12_meas, S22_meas]
    S_true_case1 = [S11_true_case1, S21_true_case1, S12_true_case1, S22_true_case1]
    S_true_case2 = [S11_true_case2, S21_true_case2, S12_true_case2, S22_true_case2]

    # Plot the error terms for the two cases
    plot_error_terms(frequency, S_meas, S_true_case1, S_true_case2, '12-Term Error')
