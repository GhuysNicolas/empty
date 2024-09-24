import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Force matplotlib to use 'TkAgg' backend, which opens plots in a separate window
matplotlib.use('TkAgg')

# Data
categories = ['CC', 'PM', 'MRD', 'LU', 'EFW', 'POF', 'HTOX_nC', 'WU', 'FRD']
Cost_opti = [3.75, 4.44, 6.86, 31.35, 10.91, 0.35, 0.25, 0.18, 2.74]
LCA_opti = [1.44,	2.43,	7.47,	10.94,	6.53,	0.14,	0.24,	0.06,	0.70]
values = LCA_opti
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
