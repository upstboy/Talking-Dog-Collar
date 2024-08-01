import numpy as np
import matplotlib.pyplot as plt

# Define the quadratic function
def quadratic(x, a=10, b=-13, c=12):
    return a * x**2 + b * x + c

# Generate x values
x_values = np.linspace(-10, 10, 1000)  # 400 points between -10 and 10

# Compute y values
y_values = quadratic(x_values)

# Plot the equation
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, label='y = x^2 - 3x + 2')
plt.title('Plot of the Quadratic Equation')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axhline(0, color='black',linewidth=0.5)
plt.axvline(0, color='black',linewidth=0.5)
plt.legend()
plt.show()
