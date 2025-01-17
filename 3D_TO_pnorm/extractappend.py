import os
import pandas as pd # type: ignore

results_dir = "results"

# Get list of all subdirectories in the results folder
subdirs = [os.path.join(results_dir, d) for d in sorted(os.listdir(results_dir)) if os.path.isdir(os.path.join(results_dir, d))]

# Last 4 subdirectories
last_four_dirs = subdirs[-4:]

combined_results = pd.DataFrame()

# Loop through the last four folders and read iteration_results.txt
for folder in last_four_dirs:
    file_path = os.path.join(folder, "iteration_results.txt")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep="\t")
        combined_results = pd.concat([combined_results, df], ignore_index=True)
    else:
        print(f"File not found: {file_path}")

combined_results.to_csv("combined_iteration_results.txt", sep="\t", index=False)
print("Combined results saved as combined_iteration_results.txt")
