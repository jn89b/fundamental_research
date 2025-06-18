import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('parsed_log.csv')
# assume df has 'timestamp' and 'id' columns
start = df['timestamp'].iloc[1]
df['t_rel'] = df['timestamp'] - start

# 1-s bins
# remove the last row
df['bin'] = (df['t_rel'] // 1).astype(int)
counts = df.groupby(['bin','id']).size().unstack(fill_value=0)
print(counts)
plt.plot(counts.index, counts)
plt.xlabel('Time (s)')
plt.ylabel('Frames / s')
plt.title('CAN Message Rate by ID')
plt.legend(title='CAN ID')

# Save the plot to a file
plt.savefig('can_message_rate.png')
plt.show()

