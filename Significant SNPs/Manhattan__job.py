import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

# Read SLURM array task ID
task_id = int(sys.argv[1])

base_input_dir = "/sise/nadav-group/nadavrap-group/ECGs/Final Project/GWAS/GWAS_Final_without_norm"
base_output_dir = "/sise/nadav-group/nadavrap-group/ECGs/Final Project/P-VALUE/Manhattan_plots_without_norm"
os.makedirs(base_output_dir, exist_ok=True)

# List phenotype folders
phenotype_folders = sorted([
    d for d in os.listdir(base_input_dir)
    if os.path.isdir(os.path.join(base_input_dir, d))
])

# Validate task ID
if task_id < 1 or task_id > len(phenotype_folders):
    raise ValueError(f"Task ID {task_id} is out of bounds (1-{len(phenotype_folders)})")

phenotype = phenotype_folders[task_id - 1]
phenotype_path = os.path.join(base_input_dir, phenotype)

# Regex to extract chrom + feature
file_pattern = re.compile(r"gwas_chrom(\d+)_ecg_phenotype_.*\.feature_(\d+)\.glm\.linear")

# Significance threshold
sig_threshold = -np.log10(5e-8)

for filename in os.listdir(phenotype_path):
    match = file_pattern.match(filename)
    if match:
        chrom = match.group(1)
        feature = match.group(2)
        file_path = os.path.join(phenotype_path, filename)

        try:
            df = pd.read_csv(file_path, sep='\s+')
            if '#CHROM' in df.columns:
                df.rename(columns={'#CHROM': 'CHROM'}, inplace=True)

            # Drop rows where P is NA
            df = df[df['P'].notna()]
            if df.empty:
                print(f"⚠️ Skipping {filename} - all P-values are NA.")
                continue

            df['-log10(P)'] = -np.log10(df['P'])
            df_significant = df[df['-log10(P)'] > sig_threshold]

            if not df_significant.empty:
                output_dir = os.path.join(base_output_dir, phenotype, f"feature_{feature}")
                os.makedirs(output_dir, exist_ok=True)

                # Plot Manhattan
                plt.figure(figsize=(12, 6))
                plt.scatter(df['POS'], df['-log10(P)'], c='darkblue', s=10)
                plt.axhline(sig_threshold, color='red', linestyle='--', label='Genome-wide significance')
                plt.title(f'Manhattan Plot - {phenotype}, Chr {chrom}, Feature {feature}')
                plt.xlabel('Position')
                plt.ylabel('-log10(p-value)')
                plt.legend(loc='upper right')
                plt.tight_layout()

                plot_path = os.path.join(output_dir, f"manhattan_chrom{chrom}_feature{feature}.png")
                plt.savefig(plot_path)
                plt.close()
                print(f"✅ Plot saved: {plot_path}")

                # Save significant SNPs to CSV
                csv_path = os.path.join(output_dir, f"significant_snps_chrom{chrom}_feature{feature}.csv")
                df_significant.to_csv(csv_path, index=False)
                print(f"📄 CSV saved: {csv_path}")
            else:
                print(f"ℹ️ No significant SNPs in {filename}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
