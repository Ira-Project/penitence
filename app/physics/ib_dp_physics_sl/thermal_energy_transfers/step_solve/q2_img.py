import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(8, 8))

# Create the first block (left) - light gray
# Front face
plt.fill([1, 3, 3, 1, 1], [1, 1, 1.5, 1.5, 1], '#D3D3D3', edgecolor='black')
# Add '3k' label on the front face of light gray block
plt.text(2, 1.25, r'$\it{3k}$', fontsize=12, ha='center', va='center')

# Top face
plt.fill([1, 3, 3.3, 1.3, 1], [1.5, 1.5, 1.8, 1.8, 1.5], '#C0C0C0', edgecolor='black')
# Side face
plt.fill([3, 3.3, 3.3, 3], [1, 1.3, 1.8, 1.5], '#BEBEBE', edgecolor='black')

# Create the second block (right) - dark gray
# Front face
plt.fill([3, 4, 4, 3, 3], [1, 1, 1.5, 1.5, 1], '#808080', edgecolor='black')
# Add 'k' label on the front face of dark gray block
plt.text(3.5, 1.25, r'$\it{k}$', fontsize=12, ha='center', va='center')

# Top face
plt.fill([4, 4.3, 3.3, 3, 4], [1.5, 1.8, 1.8, 1.5, 1.5], '#707070', edgecolor='black')
# Side face
plt.fill([4, 4.3, 4.3, 4], [1, 1.3, 1.8, 1.5], '#696969', edgecolor='black')
# Add 'A' label on the side face
plt.text(4.15, 1.4, r'$A$', fontsize=12, ha='center', va='center')

# Add double-headed arrows and labels for lengths
# Arrow for light gray block (2l)
plt.annotate('', xy=(1, 0.9), xytext=(3, 0.9),
            arrowprops=dict(arrowstyle='<->', color='black'))
plt.text(2, 0.8, r'$\it{2l}$', fontsize=12, ha='center', va='center')
# Add 200 K temperature label
plt.text(0.8, 1.25, r'$200\,\mathrm{K}$', fontsize=14, ha='right', va='bottom')

# Arrow for dark gray block (l)
plt.annotate('', xy=(3, 0.9), xytext=(4, 0.9),
            arrowprops=dict(arrowstyle='<->', color='black'))
plt.text(3.5, 0.8, r'$\it{l}$', fontsize=12, ha='center', va='center')
# Add 750 K temperature label
plt.text(4.4, 1.25, r'$750\,\mathrm{K}$', fontsize=14, ha='left', va='bottom')

# Set axis limits
plt.xlim(0.5, 5)
plt.ylim(0.5, 2.5)

# Remove axes and grid
ax.set_xticks([])
ax.set_yticks([])
plt.box(False)

plt.show()