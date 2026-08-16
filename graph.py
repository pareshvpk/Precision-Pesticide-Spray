import matplotlib.pyplot as plt
import numpy as np

# --- Parameters from Methodology Section 3.4 ---
S_THRESH = 0.10         # Activation Threshold
D_MIN = 0.20            # Minimum Duty Cycle
D_MAX = 1.00            # Maximum Duty Cycle

# 1. Generate Severity Index (S) values from 0 to 1
s_values = np.linspace(0, 1, 500)

# 2. Apply the Proportional Actuation Formula
d_values = [0.0 if s < S_THRESH else D_MIN + (D_MAX - D_MIN) * ((s - S_THRESH) / (1.0 - S_THRESH)) for s in s_values]

# 3. Create High-Quality Plot for Research Paper
plt.figure(figsize=(10, 6))
plt.plot(s_values, d_values, color='#2ca02c', linewidth=3, label='Precision Spraying Logic')

# Add the Threshold line
plt.axvline(x=S_THRESH, color='red', linestyle='--', alpha=0.7, label=f'Spray Threshold (S={S_THRESH})')

# --- NEW: Shaded Zones for better visual explanation ---
plt.fill_between(s_values, d_values, where=(s_values < S_THRESH), color='grey', alpha=0.1, label='Saving Zone (Valve OFF)')
plt.fill_between(s_values, d_values, where=(s_values >= S_THRESH), color='green', alpha=0.1, label='Active Zone (PWM Control)')

# Formatting for academic standards
plt.title('Relationship between Infestation Severity and Sprayable Dose (PWM)', fontsize=14, pad=15)
plt.xlabel('Infestation Severity Index (S)', fontsize=12)
plt.ylabel('Spray Intensity / PWM Duty Cycle (D)', fontsize=12)
plt.ylim(-0.05, 1.05)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left')

# Annotations for the paper
plt.annotate('Minimum Effective Dose (20%)', xy=(S_THRESH, D_MIN), xytext=(0.25, 0.3),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))

# 4. Save the file in the project folder
plt.tight_layout()
plt.savefig('severity_vs_dose_graph_v2.png', dpi=300)
print("Enhanced graph saved as severity_vs_dose_graph_v2.png")