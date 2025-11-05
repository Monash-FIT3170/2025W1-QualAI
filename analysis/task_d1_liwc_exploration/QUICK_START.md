# Quick Start Guide - Task D.1 LIWC Analysis

## Setup (One-time)

### 1. Install R and Required Packages

First, ensure R is installed on your system. Then install the required packages:

```r
# Run this in R console or RStudio
install.packages(c("dplyr", "ggplot2", "tidyr", "reshape2", "gridExtra", "effsize"))
```

### 2. Prepare Your Data

Place your data files in the `data/` directory:
- `forum_ind_train.csv` - Independent variables (Faculty, Sex, etc.)
- `forum_dep_train.csv` - LIWC variables

See `data/README.md` for expected data format.

## Running the Analysis

### Option 1: Complete Analysis (Recommended)

Open R in the `task_d1_liwc_exploration/` directory and run:

```r
source("run_analysis.R")
```

This will:
1. Load and merge datasets
2. Generate summary statistics
3. Create all visualizations
4. Conduct statistical tests (ANOVA and t-tests)
5. Perform focused category analysis
6. Generate interpretive reports

All outputs will be saved to the `output/` directory.

### Option 2: Step-by-Step Analysis

If you prefer more control:

```r
# Load the main analysis functions
source("liwc_analysis.R")
source("liwc_focused_analysis.R")

# Step 1: Run main analysis
results <- run_liwc_analysis(
  ind_file = "data/forum_ind_train.csv",
  dep_file = "data/forum_dep_train.csv",
  output_dir = "output"
)

# Step 2: View results
View(results$faculty_summary)
View(results$anova_results)
View(results$ttest_results)

# Step 3: Run additional focused analyses
faculty_categories <- analyze_all_priority_categories(
  data = results$data,
  group_var = "Faculty",
  output_dir = "output"
)

# Step 4: Create key visualizations
create_key_dimensions_plot(results$data, "output")

# Step 5: Generate interpretive report
generate_interpretive_report(
  results$anova_results,
  results$ttest_results,
  "output"
)
```

### Option 3: Custom Analysis

You can also run specific analyses:

```r
source("liwc_analysis.R")

# Load data
merged_data <- load_and_merge_data(
  "data/forum_ind_train.csv",
  "data/forum_dep_train.csv"
)

data_info <- identify_liwc_variables(merged_data)

# Run only ANOVA for faculty differences
anova_results <- conduct_anova_tests(
  data_info$data,
  data_info$liwc_vars
)

# Create specific plots
create_boxplots(
  data_info$data,
  data_info$liwc_vars[1:5],  # First 5 variables only
  "Faculty",
  "output/plots"
)
```

## Understanding the Output

### Output Directory Structure

```
output/
├── plots/                          # Visualizations
│   ├── boxplot_*.png              # Boxplots by faculty
│   ├── violin_*.png               # Violin plots by sex
│   ├── heatmap_*.png              # Correlation heatmaps
│   ├── key_dimensions_*.png       # Summary visualizations
│   └── categories/                # Category-specific plots
├── tables/                         # Statistical results
│   ├── summary_by_faculty.csv     # Descriptive stats by faculty
│   ├── summary_by_sex.csv         # Descriptive stats by sex
│   ├── anova_results.csv          # ANOVA test results
│   ├── ttest_results.csv          # T-test results
│   └── categories/                # Category summaries
├── analysis_summary.txt            # Main findings summary
└── interpretive_findings.txt       # Detailed interpretation
```

### Key Files to Review

1. **Start Here**: `analysis_summary.txt`
   - Quick overview of significant findings
   - Number of significant variables
   - Top differentiating variables

2. **Deep Dive**: `interpretive_findings.txt`
   - Categorized findings
   - Theoretical interpretations
   - Recommendations for further analysis

3. **Statistical Results**:
   - `anova_results.csv`: Faculty differences with F-statistics, p-values, effect sizes
   - `ttest_results.csv`: Sex differences with t-statistics, p-values, Cohen's d

4. **Visual Summary**: 
   - `key_dimensions_faculty_heatmap.png`
   - `key_dimensions_sex_barplot.png`

## Interpreting Results

### Statistical Significance

- **p_value < 0.05**: Traditionally significant
- **p_adjusted < 0.05**: Significant after Bonferroni correction (use this for conclusions)

### Effect Sizes

**Cohen's d** (sex differences):
- 0.2 = small
- 0.5 = medium  
- 0.8 = large

**Eta-squared** (faculty differences):
- 0.01 = small
- 0.06 = medium
- 0.14 = large

### Focus on:
1. Variables with **p_adjusted < 0.05** (statistically significant)
2. Variables with **large effect sizes** (practically meaningful)
3. Patterns across related LIWC categories

## Common Questions

**Q: How long does the analysis take?**
A: Typically 2-5 minutes depending on dataset size.

**Q: Which results file should I read first?**
A: Start with `analysis_summary.txt` for an overview, then review specific visualizations.

**Q: What if I get an error about missing packages?**
A: Run: `install.packages(c("dplyr", "ggplot2", "tidyr", "reshape2", "gridExtra", "effsize"))`

**Q: Can I analyze specific LIWC variables only?**
A: Yes, modify the script to filter `data_info$liwc_vars` to your variables of interest.

**Q: What if I have more than 2 groups for sex?**
A: The t-test function will skip the analysis. Modify to use ANOVA instead.

**Q: How do I export results to a report?**
A: Use R Markdown to integrate the analysis and automatically generate reports.

## Next Steps After Analysis

1. **Review significant findings** in context of LIWC theory (see `LIWC2015_Reference.md`)

2. **Conduct post-hoc tests** for significant ANOVA results:
   ```r
   # Example: Tukey HSD post-hoc test
   model <- aov(Analytic ~ Faculty, data = results$data)
   TukeyHSD(model)
   ```

3. **Examine specific posts** with extreme LIWC values to understand patterns

4. **Test interactions** between faculty and sex:
   ```r
   # Two-way ANOVA
   model <- aov(Analytic ~ Faculty * Sex, data = results$data)
   summary(model)
   ```

5. **Validate on test data** using `forum_ind_test.csv` and `forum_dep_test.csv`

## Getting Help

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Package not found | Install with `install.packages("package_name")` |
| File not found | Check paths, ensure data files are in `data/` directory |
| No significant results | Check sample size, variance, and consider exploratory analysis with uncorrected p-values |
| Out of memory | Process variables in batches, reduce plot outputs |

### Resources

- **LIWC Theory**: See `LIWC2015_Reference.md`
- **Detailed Documentation**: See `README.md`
- **Function Help**: Use `?function_name` in R console
- **Code Comments**: Review scripts for inline documentation

## Example: Minimal Working Example

```r
# Install packages (one-time)
install.packages(c("dplyr", "ggplot2", "tidyr", "reshape2", "gridExtra", "effsize"))

# Navigate to analysis directory
setwd("path/to/analysis/task_d1_liwc_exploration")

# Run complete analysis
source("run_analysis.R")

# Results are now in output/ directory
# Review: output/analysis_summary.txt
```

That's it! The analysis will run automatically and generate all outputs.

## Tips for Best Results

1. **Ensure data quality**: Check for missing values, outliers
2. **Understand your data**: Review variables before analysis
3. **Multiple testing**: Always use adjusted p-values for formal conclusions
4. **Effect sizes matter**: Statistical significance ≠ practical significance
5. **Context is key**: Interpret LIWC scores in context of your research domain
6. **Triangulate findings**: Combine quantitative LIWC analysis with qualitative review

## Citation

If you use this analysis in your work, please cite:

- The LIWC2015 framework:
  ```
  Pennebaker, J. W., Boyd, R. L., Jordan, K., & Blackburn, K. (2015). 
  The development and psychometric properties of LIWC2015. 
  Austin, TX: University of Texas at Austin.
  ```

- This analysis code:
  ```
  QualAI Project (2025). Task D.1: LIWC Dataset Exploration for Faculty & Sex Differences.
  GitHub: https://github.com/Monash-FIT3170/2025W1-QualAI
  ```
