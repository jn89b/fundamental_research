import re
import pandas as pd

# Define the regex pattern to extract fields
pattern = re.compile(
    r'^\((?P<timestamp>\d+\.\d+)\)\s+'  # Timestamp in parentheses
    r'(?P<interface>\w+)\s+'            # CAN interface (e.g., can0)
    r'(?P<id>[0-9A-Fa-f]+)\s+'          # CAN ID (hex)
    r'\[\d+\]\s+'                       # DLC (ignored)
    r'(?P<data>.+)$'                    # Data bytes
)

# Read and parse the log file
rows = []
with open('can-relative.log', 'r') as f:
    for line in f:
        match = pattern.match(line.strip())
        if match:
            rows.append({
                'timestamp': float(match.group('timestamp')),
                'interface': match.group('interface'),
                'id': match.group('id'),
                'data': match.group('data').strip(),
            })

# Create a DataFrame
df = pd.DataFrame(rows)

# save to CSV
df.to_csv('parsed_log.csv', index=False)