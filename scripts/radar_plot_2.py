import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Force matplotlib to use 'TkAgg' backend, which opens plots in a separate window
matplotlib.use('TkAgg')

# Data
categories = ['CC', 'PM', 'MRD', 'LU', 'EFW', 'POF', 'HTOX_nC', 'WU', 'FRD']
Cost_opti = [0.46,	0.83,	1.53,	7.13,	2.34,	0.06,	0.05,	0.04,	0.43]
LCA_opti = [0.03,	1.94,	6.45,	10.85,	6.37,	0.14,	0.22,	0.04,	0.41]
COST_opti_49 = [1.09,	0.98,	1.44,	7.35,	2.31,	0.06,	0.05,	0.03,	0.60]
LCA_opti_49 = [0.03,	1.75,	5.96,	9.10,	5.74,	0.12,	0.20,	0.04,	0.37]
MC1_opti_49 = [0.09,	0.85,	1.63,	9.27,	2.47,	0.05,	0.05,	0.06,	0.22]
MC2_opti_49 = [0.03,	0.63,	1.27,	4.11,	1.29,	0.03,	0.04,	0.01,	0.08]


values = MC2_opti_49
# Number of variables
num_vars = len(categories)

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Complete the loop for the values and angles
values += values[:1]
angles += angles[:1]

# Create polar plot
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Set up color for each segment
colors = ['green' if v <= 1 else 'yellow' if v <= 3 else 'orange' if v <= 7 else 'red' for v in values[:-1]]

# Plot each segment starting further out to make the inner circle larger
bars = ax.bar(angles[:-1], values[:-1], width=2*np.pi/num_vars, color=colors, align='edge', edgecolor='black', bottom=3)  # Increase 'bottom' for larger inner circle

# Set the radial limit so the circle is capped at 15 (to leave some space)
ax.set_ylim(0, 15)

# Make the center circle white by setting the facecolor
ax.set_facecolor('white')

# Remove category labels on the axes
ax.set_xticks(angles[:-1])
ax.set_xticklabels([])

# Set the radial ticks (grey circles) with a step size of 1
ax.set_yticks(np.arange(1, 15, 2))  # Tick marks from 1 to 15 with a step size of 2
ax.yaxis.grid(True, linestyle=':', alpha=0.8)

# Remove radial labels (already hidden)
ax.set_yticklabels([])

# Show the plot in a separate window
plt.show()
