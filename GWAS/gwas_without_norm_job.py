import os
import glob
import subprocess
import sys

# Get SLURM_ARRAY_TASK_ID (1-based indexing)
task_id = int(sys.argv[1])  

# List phenotype files
pheno_files = sorted(glob.glob("/sise/nadav-group/nadavrap-group/ECGs/Final Project/GWAS/ECG_PHENOTYPE_without_norm/ecg_phenotype_*.txt"))

if task_id < 1 or task_id > len(pheno_files):
    raise ValueError(f"Task ID {task_id} is out of bounds for number of phenotype files ({len(pheno_files)}).")

pheno_file = pheno_files[task_id - 1]
base_name = os.path.splitext(os.path.basename(pheno_file))[0]

# Common paths
covar_file = "/sise/nadav-group/nadavrap-group/ECGs/Final Project/GWAS/Covariates/covariates_for_plink7.txt"
output_dir = f"/sise/nadav-group/nadavrap-group/ECGs/Final Project/GWAS/GWAS_Final_without_norm/{base_name}"
os.makedirs(output_dir, exist_ok=True)

# Covariate names
covar_names = ",".join([
    "age_when_attended_assessment_centre_f21003_0_0",
    "genetic_sex_f22001_0_0",
    "genetic_principal_components_f22009_0_1",
    "genetic_principal_components_f22009_0_2",
    "genetic_principal_components_f22009_0_3",
    "genetic_principal_components_f22009_0_4",
    "genetic_principal_components_f22009_0_5",
    "genetic_principal_components_f22009_0_6",
    "genetic_principal_components_f22009_0_7",
    "genetic_principal_components_f22009_0_8",
    "genetic_principal_components_f22009_0_9",
    "genetic_principal_components_f22009_0_10",
    "uk_biobank_center_11001", "uk_biobank_center_11002", "uk_biobank_center_11004",
    "uk_biobank_center_11005", "uk_biobank_center_11006", "uk_biobank_center_11007",
    "uk_biobank_center_11008", "uk_biobank_center_11009", "uk_biobank_center_11010",
    "uk_biobank_center_11011", "uk_biobank_center_11012", "uk_biobank_center_11013",
    "uk_biobank_center_11014", "uk_biobank_center_11016", "uk_biobank_center_11017",
    "uk_biobank_center_11018", "uk_biobank_center_11020", "uk_biobank_center_11021"
])

# Phenotype names (feature_1 to feature_32)
pheno_names = ",".join([f"feature_{i}" for i in range(1, 33)])

# Loop through chromosomes 1–22
for chrom in range(1, 23):
    bfile_path = f"/sise/nadav-group/nadavrap-group/UKBB/GEN/ukb{chrom}"
    output_file = os.path.join(output_dir, f"gwas_chrom{chrom}_{base_name}")

    cmd = [
        "plink2",
        "--bfile", bfile_path,
        "--pheno", pheno_file,
        "--pheno-name", pheno_names,
        "--covar", covar_file,
        "--covar-name", covar_names,
        "--glm",
        "--no-fid",
        "--no-input-missing-phenotype",
        "--out", output_file
    ]

    print(f"🔬 Running PLINK for chromosome {chrom}, phenotypes: {pheno_names}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Error in chromosome {chrom} for {pheno_file}")
        print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)
    else:
        print(f"✅ Finished chromosome {chrom} → {output_file}")
