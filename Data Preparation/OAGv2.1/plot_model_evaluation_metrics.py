import numpy as np
import matplotlib.pyplot as plt

# Data for the epochs
epochs = np.arange(101)  # 0 to 100 epochs
loss_values = [
    2.772, 4.991, 2.334, 3.629, 3.211, 2.224, 1.968, 2.198, 2.119, 1.758, 1.520, 1.528, 1.571, 1.483, 1.315,
    1.189, 1.111, 1.053, 1.009, 0.973, 0.902, 0.816, 0.759, 0.713, 0.657, 0.624, 0.614, 0.575, 0.507, 0.464,
    0.452, 0.430, 0.394, 0.375, 0.365, 0.335, 0.302, 0.288, 0.274, 0.251, 0.236, 0.231, 0.217, 0.200, 0.190,
    0.180, 0.167, 0.157, 0.151, 0.142, 0.134, 0.128, 0.122, 0.115, 0.109, 0.105, 0.099, 0.094, 0.090, 0.086,
    0.082, 0.078, 0.075, 0.072, 0.069, 0.066, 0.064, 0.061, 0.059, 0.056, 0.055, 0.053, 0.051, 0.049, 0.048,
    0.046, 0.045, 0.043, 0.042, 0.040, 0.039, 0.038, 0.037, 0.036, 0.035, 0.034, 0.033, 0.032, 0.032, 0.031,
    0.030, 0.030, 0.029, 0.029, 0.028, 0.028, 0.027, 0.026, 0.026, 0.025, 0.025,
]  # Sample loss values for each epoch

# Metrics recorded every 10 epochs
metric_epochs = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
nmi_values = [1.0] * len(metric_epochs)
ari_values = [1.0] * len(metric_epochs)
purity_values = [1.0] * len(metric_epochs)
modularity_values = [0.5458] * len(metric_epochs)

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Loss over epochs
ax1.plot(epochs, loss_values, label='Loss', color='blue')
ax1.set_title('Loss over Epochs')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('Loss')
ax1.grid(True)

# NMI, ARI, Purity, Modularity at specific epochs
ax2.plot(metric_epochs, nmi_values, 'o-', label='NMI', color='orange')
ax2.plot(metric_epochs, ari_values, 'o-', label='ARI', color='green')
ax2.plot(metric_epochs, purity_values, 'o-', label='Purity', color='purple')
ax2.plot(metric_epochs, modularity_values, 'o-', label='Modularity', color='red')
ax2.set_title('NMI, ARI, Purity, Modularity at Specific Epochs')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('Metric Value')
ax2.legend(loc='lower right')
ax2.grid(True)

plt.tight_layout()
plt.show()