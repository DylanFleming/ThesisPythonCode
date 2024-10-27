import skrf as rf
import numpy as np
import matplotlib.pyplot as plt

def plot_seperated_error_terms(frequency, S_meas, S_true_case, label_base):
    # Directivity errors
    Ed1_case = S_meas[0] - S_true_case[0]
    Ed2_case = S_meas[3] - S_true_case[3]

    # Source match errors
    Es1_case = (S_meas[0] / S_true_case[0]) - 1
    Es2_case = (S_meas[3] / S_true_case[3]) - 1

    # Load match errors
    El1_case = (S_true_case[0] / S_meas[0]) - 1
    El2_case = (S_true_case[3] / S_meas[3]) - 1

    # Crosstalk errors
    Ex12_case = S_meas[1] - S_true_case[1]
    Ex21_case = S_meas[2] - S_true_case[2]

    # Reflection tracking errors
    Er1_case = S_meas[0] * S_true_case[0]
    Er2_case = S_meas[3] * S_true_case[3]

    # Transmission tracking errors
    Et1_case = S_meas[1] / S_true_case[1]
    Et2_case = S_meas[2] / S_true_case[2]

    # List of error terms for plotting
    # Forward errors on row 1, backward errors on row 2
    error_terms_row1_case1 = [Ed1_case, Es1_case, El1_case, Ex12_case, Er1_case, Et1_case]
    error_terms_row2_case1 = [Ed2_case, Es2_case, El2_case, Ex21_case, Er2_case, Et2_case]

    labels_row1 = ['Directivity (Ed1)', 'Source Match (Es1)', 'Load Match (El1)', 'Crosstalk (Ex12)',
                   'Reflection Tracking (Er1)', 'Transmission Tracking (Et1)']
    labels_row2 = ['Directivity (Ed2)', 'Source Match (Es2)', 'Load Match (El2)', 'Crosstalk (Ex21)',
                   'Reflection Tracking (Er2)', 'Transmission Tracking (Et2)']

    # Create subplots for each error term in a 2-row, 6-column grid
    plt.figure(figsize=(36, 16))  # Adjusted figure size to accommodate 6 columns
    # Plot forward errors (Row 1)
    for i in range(6):
        plt.subplot(2, 6, i + 1)  # First row (6 columns)
        plt.plot(frequency, 20 * np.log10(np.abs(error_terms_row1_case1[i].s.flatten())),
                 label=f'{label_base} Mechanical Standard')
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
        plt.title(labels_row2[i])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Error Magnitude (dB)')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()  # Increased padding for more space between subplots
    plt.show()

def seperated_error_calcs(calibrated_case, uncalibrated):
    # Interpolate both calibrated networks to match the frequency of the uncalibrated data
    calibrated_case = calibrated_case.interpolate(uncalibrated.f)

    # Extract the S-parameters for the uncalibrated and both calibrated cases
    S11_meas, S21_meas, S12_meas, S22_meas = uncalibrated.s11, uncalibrated.s21, uncalibrated.s12, uncalibrated.s22
    S11_true_case, S21_true_case, S12_true_case, S22_true_case = calibrated_case.s11, calibrated_case.s21, calibrated_case.s12, calibrated_case.s22


    # Frequency for plotting
    frequency = uncalibrated.f

    # Combine the measured and true S-parameters into lists for easier processing
    S_meas = [S11_meas, S21_meas, S12_meas, S22_meas]
    S_true_case1 = [S11_true_case, S21_true_case, S12_true_case, S22_true_case]

    # Plot the error terms for the two cases
    plot_seperated_error_terms(frequency, S_meas, S_true_case1, '12-Term Error')
