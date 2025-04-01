import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 6))

# Draw first block (left subplot) - centered at water level
rect1 = plt.Rectangle((0.4, -0.25), 0.2, 0.5, facecolor='gray')
ax1.add_patch(rect1)

# Draw water line and label (left subplot)
ax1.axhline(y=0, color='black', linewidth=1)
ax1.axhline(y=0, xmin=0.4, xmax=0.6, color='black', linewidth=2)
ax1.text(0.1, 0, 'water', verticalalignment='bottom')

# Draw second block (right subplot) - centered at water level
rect2_bottom = plt.Rectangle((0.4, -0.4), 0.2, 0.25, facecolor='gray')
rect2_top = plt.Rectangle((0.4, -0.15), 0.2, 0.25, facecolor='gray')
ax2.add_patch(rect2_bottom)
ax2.add_patch(rect2_top)
ax2.axhline(y=-0.15, xmin=0.4, xmax=0.6, color='black', linewidth=2)

# Draw water line and label (right subplot)
ax2.axhline(y=0, color='black', linewidth=1)
ax2.text(0.1, 0, 'water', verticalalignment='bottom')

# Add 28 cm measurement
ax2.annotate('', xy=(0.65, -0.15), xytext=(0.65, 0), 
             arrowprops=dict(arrowstyle='<->'))
ax2.text(0.68, -0.09, '28 cm')

# Set equal aspect ratio and remove axes
for ax in [ax1, ax2]:
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_ylim(-0.5, 0.5)  # Set consistent y limits

plt.tight_layout()
plt.show()