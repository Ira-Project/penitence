import numpy as np
import matplotlib.pyplot as plt

# Create data points
t = np.linspace(0, 40, 1000)

# Using a quadratic function that passes through (0,0) and (10,1)
def curve(t):
    return 0.01 * t * t  # Adjust to pass through (0,0) and (10,1)
n = curve(t)

plt.figure(figsize=(8, 8))
plt.grid(True)
plt.plot(t, n, 'k-', linewidth=1)

# Adjust font properties
plt.xlabel('t (min)', fontsize=14)
plt.ylabel('n', fontsize=14)

plt.xlim(0, 40)
plt.ylim(0, 16)

plt.xticks(np.arange(0, 41, 8))
plt.yticks(np.arange(0, 17, 4))

# Add minor gridlines
plt.grid(True, which='minor', alpha=0.4)
plt.minorticks_on()

plt.show()