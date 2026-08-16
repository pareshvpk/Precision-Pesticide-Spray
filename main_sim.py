import cv2
import numpy as np
import os
import csv
from datetime import datetime

# --- Parameters from Methodology Section 3.2 & 3.4 ---
MAX_PESTS = 50          # N_max: normalization for pest count
S_THRESH = 0.10         # 10% severity threshold to start spraying
W1, W2 = 0.6, 0.4       # Weighting: 60% on count, 40% on area

# --- 3.4 PWM Duty Cycle Mapping ---
D_MIN = 0.20            # Minimum spray intensity (20%)
D_MAX = 1.00            # Maximum spray intensity (100%)

def run_simulation():
    # Setup directories for organized research data
    for d in ['processed_output', 'logs', 'dataset']:
        os.makedirs(d, exist_ok=True)

    log_path = f"logs/proportional_report_{datetime.now().strftime('%H%M')}.csv"
    
    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['File', 'Pests', 'Severity_Index', 'Spray_Intensity_PWM', 'Action'])

        # Filter for standard image formats
        files = [f for f in os.listdir('dataset') if f.endswith(('.jpg', '.png', '.jpeg'))]
        
        if not files:
            print("No images found in /dataset folder. Please add images to proceed.")
            return

        for filename in files:
            # 3.1 Image Acquisition
            img = cv2.imread(f'dataset/{filename}')
            if img is None: continue

            # --- ENHANCED PRE-PROCESSING FOR ACCURACY ---
            # Apply Gaussian Blur to reduce noise from leaf edges/gaps
            blurred = cv2.GaussianBlur(img, (5, 5), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            
            # Gap-Aware Logic: Targeting specific pest colors
            lower_pest = np.array([8, 50, 40])  
            upper_pest = np.array([35, 255, 230]) 
            mask = cv2.inRange(hsv, lower_pest, upper_pest)
            
            # Dilation merges nearby spots into one accurate bounding box
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)
            # Opening removes small noise artifacts
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # 3.2 Severity Calculation Logic
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter by area: Ignore anything smaller than 50 pixels to ensure accuracy
            valid_contours = [c for c in contours if cv2.contourArea(c) > 50]
            
            n = len(valid_contours)
            p_area = sum(cv2.contourArea(c) for c in valid_contours)
            t_area = img.shape[0] * img.shape[1]
            
            # Combined Severity Index (S)
            S = (W1 * min(n/MAX_PESTS, 1.0)) + (W2 * (p_area/t_area))

            # 3.4 Efficient Spraying/PWM Logic
            if S < S_THRESH:
                D = 0.0
                action = "OFF"
            else:
                # Proportional calculation: maps S to Duty Cycle D
                D = D_MIN + (D_MAX - D_MIN) * ((S - S_THRESH) / (1.0 - S_THRESH))
                action = f"ON ({D:.1%})"

            # --- 4.3 Visual Proof (Bounding Boxes) ---
            for cnt in valid_contours:
                x, y, w, h = cv2.boundingRect(cnt)
                # Blue boxes for localization
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Overlay metadata for paper results
            color = (0, 255, 0) if D == 0 else (0, 165, 255)
            cv2.putText(img, f"Pests: {n} | Spray: {D:.1%}", (20, 50), 2, 0.8, color, 2)
            
            # Save results and log data
            cv2.imwrite(f'processed_output/vbox_{filename}', img)
            writer.writerow([filename, n, f"{S:.2f}", f"{D:.1%}", action])
            
            print(f"Processed {filename}: Found {n} pests. Severity: {S:.2f} | Action: {action}")

    print(f"\nSimulation Complete! Data saved to {log_path}")

if __name__ == "__main__":
    run_simulation()