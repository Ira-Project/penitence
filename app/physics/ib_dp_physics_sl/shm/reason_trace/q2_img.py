import matplotlib.pyplot as plt
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(figsize=(5, 5))

# Plot vertical line
plt.plot([0, 0], [0, 1.2], 'k-', linewidth=1)

# Plot horizontal line at top
plt.plot([-0.5, 0.5], [1.2, 1.2], 'k-', linewidth=1)

# Calculate arc endpoint (15 degrees = pi/12 radians)
angle = np.pi/12
end_x = -1.2 * np.sin(angle)  # x = r * sin(theta)
end_y = 1.2 - 1.2 * np.cos(angle)  # y = 1.2 - r * cos(theta)

# Plot the pendulum string (dashed line)
plt.plot([0, end_x], [1.2, end_y], 'k--', linewidth=1)

# Add angle arc between strings (larger radius)
theta_arc = np.linspace(0, -angle, 100)
r_arc = 0.4  # Larger radius for the arc
x_arc = r_arc * np.sin(theta_arc)
y_arc = -r_arc * np.cos(theta_arc)
plt.plot(x_arc, y_arc + 1.2, 'k-', linewidth=1)

# Add text for angle in the middle of the arc
plt.text(-0.08, 0.7, '9°')

# Calculate and plot the circular arc for pendulum motion
theta = np.linspace(0, -angle, 100)
x_arc = 1.2 * np.sin(theta)
y_arc = 1.2 - 1.2 * np.cos(theta)
plt.plot(x_arc, y_arc, 'k--', linewidth=1)

# Add circles
circle1 = plt.Circle((end_x, end_y), 0.05, color='gray')  # Updated position
circle2 = plt.Circle((0, 0), 0.05, color='gray')
ax.add_patch(circle1)
ax.add_patch(circle2)

# Set equal aspect ratio and remove axes
ax.set_aspect('equal')
plt.axis('off')

# Set limits
plt.xlim(-0.5, 0.5)
plt.ylim(-0.2, 1.6)

plt.show()