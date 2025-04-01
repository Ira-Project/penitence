import matplotlib.pyplot as plt
import numpy as np

# Define the x and y coordinates for the line segments with new slopes
x = [0, 1.5, 3, 5]
y = [0, 9, 9, 15]

# Create the plot
plt.figure(figsize=(8, 8))
plt.plot(x, y, 'k-', linewidth=1.5)

# Set labels and title
plt.xlabel('t (sec)', labelpad=0)
plt.ylabel('T (K)', labelpad=0)

# Add slope labels
# plt.text(0.6, 5, '5.0', fontsize=12)
# plt.text(3.5, 13.5, '8.0', fontsize=12)
# plt.text(6.5, 22, '4.0', fontsize=12)

# Add segment labels (A through F)
# plt.text(0, 1, 'A', fontsize=10, fontweight='bold')
# plt.text(2, 10.5, 'B', fontsize=10, fontweight='bold')
# plt.text(3.5, 9.5, 'C', fontsize=10, fontweight='bold')
# plt.text(4.4, 18.5, 'D', fontsize=10, fontweight='bold')
# plt.text(5.9, 18.5, 'E', fontsize=10, fontweight='bold')
# plt.text(7.8, 26, 'F', fontsize=10, fontweight='bold')

# Set ticks and limits
plt.xticks(np.arange(0, 6, 1))  # x-axis ticks from 0 to 5
plt.yticks(np.arange(0, 16, 3))  # y-axis ticks from 0 to 15 in steps of 3
plt.xlim(0, 5)  # Set x-axis limits
plt.ylim(0, 15)  # Set y-axis limits

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.7)

# Show only left and bottom spines
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)

# Adjust layout
plt.tight_layout()

plt.show()