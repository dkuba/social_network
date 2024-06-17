# import matplotlib.pyplot as plt
#
# num_requests = [1, 10, 100, 1000]
# latency_results = [2.1289, 2.1538, 4.8062, 41.6390]
# throughput_results = [0.4697, 3.5135, 10.3955, 11.4468]
#
# plt.figure(figsize=(10, 6))
# plt.plot(len(num_requests), latency_results, label='Latency')
# plt.plot(range(num_requests), throughput_results[-num_requests:], label='Throughput', linestyle='--')
# plt.xlabel('Request Number')
# plt.ylabel('Latency (s)')
# plt.title('API Loading Test Results')
# plt.legend()
# plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Generating some sample data
num_requests = [1, 10, 100, 1000]
latency_results = [2.1289, 2.1538, 4.8062, 41.6390]
throughput_results = [0.4697, 3.5135, 10.3955, 11.4468]

index_latency_results = [2.0799, 2.0180, 3.2657, 20.2774]
index_throughput_results = [0.4807, 5.0098, 15.8719, 25.6885]

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2)

# Plot data on the first subplot
ax1.plot(num_requests, latency_results, label='latency')
ax1.plot(num_requests, throughput_results, label='throughput')
ax1.set_title('Without index')

# Plot data on the second subplot
ax2.plot(num_requests, index_latency_results, label='latency')
ax2.plot(num_requests, index_throughput_results, label='throughput')
ax2.set_title('With index')

# Add legend to each subplot
ax1.legend()
ax2.legend()

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
