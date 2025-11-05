# ============================================================================
# Example Usage: Complete LIWC Analysis Workflow
# ============================================================================
# This script demonstrates how to run the complete LIWC analysis pipeline
# ============================================================================

# Clear workspace
rm(list = ls())

# Load the main analysis script
source("liwc_analysis.R")

# Load the focused analysis script
source("liwc_focused_analysis.R")

# ============================================================================
# STEP 1: RUN MAIN ANALYSIS
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("STEP 1: Running Main LIWC Analysis\n")
cat("============================================================\n")

# Define file paths
ind_file <- "data/forum_ind_train.csv"
dep_file <- "data/forum_dep_train.csv"
output_dir <- "output"

# Check if files exist
if (!file.exists(ind_file) || !file.exists(dep_file)) {
  cat("\nERROR: Data files not found!\n")
  cat("Please place the following files in the data/ directory:\n")
  cat("  - forum_ind_train.csv\n")
  cat("  - forum_dep_train.csv\n")
  cat("\nSee data/README.md for more information.\n")
  stop("Data files missing")
}

# Run the main analysis
results <- run_liwc_analysis(
  ind_file = ind_file,
  dep_file = dep_file,
  output_dir = output_dir
)

# ============================================================================
# STEP 2: RUN FOCUSED CATEGORY ANALYSIS
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("STEP 2: Running Focused Category Analysis\n")
cat("============================================================\n")

# Analyze by faculty
cat("\nAnalyzing by Faculty...\n")
faculty_categories <- analyze_all_priority_categories(
  data = results$data,
  group_var = "Faculty",
  output_dir = output_dir
)

# Analyze by sex
cat("\nAnalyzing by Sex...\n")
sex_categories <- analyze_all_priority_categories(
  data = results$data,
  group_var = "Sex",
  output_dir = output_dir
)

# ============================================================================
# STEP 3: CREATE KEY DIMENSIONS VISUALIZATIONS
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("STEP 3: Creating Key Dimensions Visualizations\n")
cat("============================================================\n")

create_key_dimensions_plot(results$data, output_dir)

# ============================================================================
# STEP 4: IDENTIFY TOP DIFFERENCES
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("STEP 4: Identifying Top Differentiating Variables\n")
cat("============================================================\n")

top_diffs <- identify_top_differences(
  anova_results = results$anova_results,
  ttest_results = results$ttest_results,
  n_top = 10
)

# ============================================================================
# STEP 5: GENERATE INTERPRETIVE REPORT
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("STEP 5: Generating Interpretive Report\n")
cat("============================================================\n")

generate_interpretive_report(
  anova_results = results$anova_results,
  ttest_results = results$ttest_results,
  output_dir = output_dir
)

# ============================================================================
# STEP 6: DISPLAY SUMMARY INFORMATION
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("ANALYSIS COMPLETE - SUMMARY\n")
cat("============================================================\n\n")

cat("Data Overview:\n")
cat(sprintf("  - Total records: %d\n", nrow(results$data)))
cat(sprintf("  - LIWC variables analyzed: %d\n", length(results$liwc_vars)))

if ("Faculty" %in% colnames(results$data)) {
  faculties <- unique(results$data$Faculty[!is.na(results$data$Faculty)])
  cat(sprintf("  - Number of faculties: %d\n", length(faculties)))
  cat("  - Faculties:", paste(faculties, collapse = ", "), "\n")
}

if ("Sex" %in% colnames(results$data)) {
  sexes <- unique(results$data$Sex[!is.na(results$data$Sex)])
  cat(sprintf("  - Sex categories: %d\n", length(sexes)))
  cat("  - Categories:", paste(sexes, collapse = ", "), "\n")
}

cat("\nStatistical Results:\n")
if (nrow(results$anova_results) > 0) {
  sig_anova <- sum(results$anova_results$significant_adjusted == "Yes", na.rm = TRUE)
  cat(sprintf("  - Faculty differences (significant): %d/%d\n", 
              sig_anova, nrow(results$anova_results)))
}

if (nrow(results$ttest_results) > 0) {
  sig_ttest <- sum(results$ttest_results$significant_adjusted == "Yes", na.rm = TRUE)
  cat(sprintf("  - Sex differences (significant): %d/%d\n", 
              sig_ttest, nrow(results$ttest_results)))
}

cat("\nOutput Files:\n")
cat(sprintf("  - Main directory: %s/\n", output_dir))
cat("  - Tables: output/tables/\n")
cat("  - Plots: output/plots/\n")
cat("  - Summary report: output/analysis_summary.txt\n")
cat("  - Interpretive report: output/interpretive_findings.txt\n")

cat("\nNext Steps:\n")
cat("  1. Review plots in output/plots/ directory\n")
cat("  2. Examine statistical results in output/tables/ directory\n")
cat("  3. Read summary reports for key findings\n")
cat("  4. Consider post-hoc analyses for significant results\n")
cat("  5. Interpret findings in context of LIWC theory\n")

cat("\n============================================================\n")

# ============================================================================
# OPTIONAL: QUICK PREVIEW OF TOP FINDINGS
# ============================================================================

cat("\n")
cat("============================================================\n")
cat("QUICK PREVIEW: Top Findings\n")
cat("============================================================\n\n")

# Top faculty differences
if (!is.null(top_diffs$faculty) && nrow(top_diffs$faculty) > 0) {
  cat("Top 5 Faculty Differences (by effect size):\n")
  print(head(top_diffs$faculty[, c("Variable", "F_statistic", "eta_squared", "p_adjusted")], 5))
  cat("\n")
}

# Top sex differences
if (!is.null(top_diffs$sex) && nrow(top_diffs$sex) > 0) {
  cat("Top 5 Sex Differences (by effect size):\n")
  print(head(top_diffs$sex[, c("Variable", "t_statistic", "cohens_d", "p_adjusted")], 5))
  cat("\n")
}

cat("============================================================\n")
cat("For detailed interpretation, see: output/interpretive_findings.txt\n")
cat("============================================================\n\n")

# ============================================================================
# SAVE WORKSPACE (OPTIONAL)
# ============================================================================

# Uncomment to save the workspace for later use
# save.image(file = file.path(output_dir, "liwc_analysis_workspace.RData"))
# cat("Workspace saved to: output/liwc_analysis_workspace.RData\n")
# cat("Load it later with: load('output/liwc_analysis_workspace.RData')\n")
