# =========================================================================
#           Result Table Plot
#           By Dylan Fleming, 45313345
# =========================================================================

# Imports
import skrf as rf
import pandas as pd
import numpy as np


def result_tables(network1, network2, frequency_start, frequency_end, frequency_step, file_name):
    """
    result_tables is a handler to determine and save values to a csv file
    :param network1: The first measurement network in the form of rf.Network('path-to-file.s2p')
    :param network2: The second measurement network in the form of rf.Network('path-to-file.s2p')
    :param frequency_start: The starting frequency value
    :param frequency_end: The ending frequency value
    :param frequency_step: The frequency step value between each value saved to table
    :param file_name: The name of the csv file to save data to
    :return: NULL
    """
    # Ensure both networks have the same frequency points
    frequencies1 = network1.f
    frequencies2 = network2.f

    # Define the specific frequency points at given intervals
    target_frequencies = np.arange(frequency_start, frequency_end + frequency_step, frequency_step)

    # Find indices of closest matching frequencies in the network data
    indices = [np.argmin(np.abs(frequencies1 - f)) for f in target_frequencies]

    # Extract log magnitude, phase, return loss, and insertion loss for both networks at these indices
    s1_mag_db = network1.s_db[indices]  # Magnitude in dB for network 1 at target frequencies
    s1_phase_deg = network1.s_deg[indices]  # Phase in degrees for network 1 at target frequencies

    s2_mag_db = network2.s_db[indices]  # Magnitude in dB for network 2 at target frequencies
    s2_phase_deg = network2.s_deg[indices]  # Phase in degrees for network 2 at target frequencies

    # Calculate return loss and insertion loss for both networks at these indices
    return_loss_s11_1 = -s1_mag_db[:, 0, 0]  # Return loss S11 (network 1)
    return_loss_s11_2 = -s2_mag_db[:, 0, 0]  # Return loss S11 (network 2)

    insertion_loss_s21_1 = -s1_mag_db[:, 1, 0]  # Insertion loss S21 (network 1)
    insertion_loss_s21_2 = -s2_mag_db[:, 1, 0]  # Insertion loss S21 (network 2)

    # Create a DataFrame to compare the two networks at the specified frequencies
    comparison_df = pd.DataFrame({
        'Frequency (Hz)': target_frequencies,
        'S11 Magnitude (dB) - Uncalibrated': s1_mag_db[:, 0, 0],
        'S11 Magnitude (dB) - Calibrated': s2_mag_db[:, 0, 0],
        'S11 Phase (deg) - Uncalibrated': s1_phase_deg[:, 0, 0],
        'S11 Phase (deg) - Calibrated': s2_phase_deg[:, 0, 0],
        'S21 Magnitude (dB) - Uncalibrated': s1_mag_db[:, 1, 0],
        'S21 Magnitude (dB) - Calibrated': s2_mag_db[:, 1, 0],
        'S21 Phase (deg) - Uncalibrated': s1_phase_deg[:, 1, 0],
        'S21 Phase (deg) - Calibrated': s2_phase_deg[:, 1, 0],
        'Return Loss S11 (dB) - Uncalibrated': return_loss_s11_1,
        'Return Loss S11 (dB) - Calibrated': return_loss_s11_2,
        'Insertion Loss S21 (dB) - Uncalibrated': insertion_loss_s21_1,
        'Insertion Loss S21 (dB) - Calibrated': insertion_loss_s21_2,
    })

    # Export the comparison to a CSV file
    comparison_df.to_csv(file_name, index=False)

    print("Comparison data saved to " + file_name)
