# Re-importing necessary libraries as the execution state has been reset
import numpy as np

# Re-defining the amino acid sequence and their monoisotopic masses
amino_acid_masses = {
    'G': 57.02, 'A': 71.04, 'S': 87.03, 'P': 97.05, 'V': 99.07, 'T': 101.05,
    'L': 113.08, 'I': 113.08, 'N': 114.04, 'D': 115.03, 'Q': 128.06,
    'K': 128.09, 'E': 129.04, 'M': 131.04, 'H': 137.06, 'F': 147.07,
    'R': 156.10, 'C': 160.06, 'Y': 163.06, 'W': 186.08
}

sequence = 'HELTEISNVDVETQSGK'

# Calculate the b-type ions by sequentially adding the mass of each amino acid from the N-terminus.
b_ions = [sum(amino_acid_masses[aa] for aa in sequence[:i+1]) for i in range(len(sequence))]

# Calculate the y-type ions by sequentially adding the mass of each amino acid from the C-terminus.
y_ions = [sum(amino_acid_masses[aa] for aa in sequence[-i-1:]) for i in range(len(sequence))]

# a-ions are the b-ions minus the mass of CO (28.03 Da)
a_ions = [b_ion - 28.03 for b_ion in b_ions]

# Calculate the +2H ions for both b and y ions
b_ions_2H = [mz / 2 for mz in b_ions]
y_ions_2H = [mz / 2 for mz in y_ions]

# Define the observed peaks (m/z, intensity)
observed_peaks = [
    (147.11, 5816.1), (204.13, 9940.3), (239.11, 31797.1), (267.11, 128489.5),
    (362.18, 46755.3), (380.19, 39560.5), (419.23, 7716.1), (481.24, 10153.8),
    (520.28, 45374.6), (610.28, 53161.8), (649.31, 42469.9), (723.37, 48555.8),
    (748.39, 29821.2), (810.41, 10799.5), (863.41, 38602.8), (926.45, 21049.9),
    (934.46, 39395.7), (1076.52, 25272.7), (1138.55, 27930.7), (1163.55, 74982.1),
    (1237.60, 10679.8), (1276.64, 37540.7), (1405.68, 21377.9), (1467.70, 9944.6),
    (1506.72, 36270.1), (1619.80, 40099.0)
]

# Define a function to match the observed peaks with theoretical ions
def match_ions(theoretical_ions, observed_peaks, ion_type):
    matched_ions = {}
    for mz, intensity in observed_peaks:
        # Find the closest theoretical ion within a certain tolerance (0.5 Da)
        closest_ion = min(theoretical_ions, key=lambda x: abs
