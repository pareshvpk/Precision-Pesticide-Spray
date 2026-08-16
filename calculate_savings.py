import os

# 1. Find the latest report in your logs folder
log_dir = 'logs'
files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.csv')]

if not files:
    print("No log files found. Run main_sim.py first!")
else:
    latest_file = max(files, key=os.path.getctime)
    print(f"Analyzing: {latest_file}")

    # 2. Read the file manually
    with open(latest_file, 'r') as f:
        lines = f.readlines()[1:] # Skip the header row
        
    total_images = len(lines)
    total_dose = 0.0

    for line in lines:
        # Extract the percentage (e.g., '25.0%') and convert to float
        columns = line.split(',')
        dose_str = columns[3].replace('%', '') 
        total_dose += float(dose_str) / 100.0

    # 3. Calculate Efficiency
    # Blanket spraying would use 1.0 units per image
    blanket_total = total_images * 1.0
    efficiency = ((blanket_total - total_dose) / blanket_total) * 100

    print("-" * 30)
    print(f"Total Images: {total_images}")
    print(f"Chemical Used: {total_dose:.2f} units")
    print(f"Blanket Use: {blanket_total:.2f} units")
    print(f"CHEMICAL SAVING EFFICIENCY: {efficiency:.2f}%")
    print("-" * 30)