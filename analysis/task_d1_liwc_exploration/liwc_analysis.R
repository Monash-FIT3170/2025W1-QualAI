# ============================================================================
# Task D.1: LIWC Dataset Exploration for Faculty & Sex Differences
# ============================================================================
# Author: QualAI Team
# Date: 2025-11-05
# Description: This script explores LIWC datasets to investigate differences
#              among faculties and between sexes on LIWC variables.
# ============================================================================

# Load required libraries
# If any library is not installed, use: install.packages("package_name")
library(dplyr)      # Data manipulation
library(ggplot2)    # Visualization
library(tidyr)      # Data reshaping
library(reshape2)   # Data reshaping (for heatmaps)
library(gridExtra)  # Multiple plots
library(effsize)    # Effect size calculations

# ============================================================================
# 1. DATA LOADING & PREPARATION
# ============================================================================

#' Load and merge LIWC datasets
#'
#' @param ind_file Path to forum_ind_train.csv
#' @param dep_file Path to forum_dep_train.csv
#' @return Merged dataset
load_and_merge_data <- function(ind_file, dep_file) {
  cat("Loading datasets...\n")
  
  # Load datasets
  ind_data <- read.csv(ind_file, stringsAsFactors = FALSE)
  dep_data <- read.csv(dep_file, stringsAsFactors = FALSE)
  
  cat(sprintf("Independent variables: %d rows, %d columns\n", 
              nrow(ind_data), ncol(ind_data)))
  cat(sprintf("Dependent variables: %d rows, %d columns\n", 
              nrow(dep_data), ncol(dep_data)))
  
  # Merge datasets on Unique_ID
  merged_data <- merge(ind_data, dep_data, by = "Unique_ID", all = TRUE)
  
  cat(sprintf("Merged dataset: %d rows, %d columns\n", 
              nrow(merged_data), ncol(merged_data)))
  
  return(merged_data)
}

#' Identify and extract LIWC variables
#'
#' @param data Merged dataset
#' @return List containing full data, LIWC variable names, and metadata columns
identify_liwc_variables <- function(data) {
  cat("\nIdentifying LIWC variables...\n")
  
  # Print first few column names to understand structure
  cat("First 10 column names:\n")
  print(head(colnames(data), 10))
  
  # Common metadata columns (adjust based on actual data)
  metadata_cols <- c("Unique_ID", "Faculty", "Sex", "Student_ID", "Post_ID")
  
  # LIWC2015 variables typically include:
  # - Summary variables: Analytic, Clout, Authentic, Tone
  # - Linguistic dimensions: WC, WPS, Dic, function, pronoun, ppron, i, we, you, etc.
  # - Psychological constructs: affect, posemo, negemo, anx, anger, sad, etc.
  # - Personal concerns: work, leisure, home, money, relig, death, etc.
  
  # Filter out metadata columns to get LIWC variables
  all_cols <- colnames(data)
  liwc_cols <- setdiff(all_cols, metadata_cols)
  
  # Further filter to numeric columns (LIWC variables are numeric)
  numeric_cols <- names(data)[sapply(data, is.numeric)]
  liwc_numeric <- intersect(liwc_cols, numeric_cols)
  
  cat(sprintf("Found %d LIWC variables (numeric columns)\n", length(liwc_numeric)))
  cat("First 10 LIWC variables:\n")
  print(head(liwc_numeric, 10))
  
  return(list(
    data = data,
    liwc_vars = liwc_numeric,
    metadata_cols = intersect(metadata_cols, all_cols)
  ))
}

# ============================================================================
# 2. EXPLORATORY DATA ANALYSIS
# ============================================================================

#' Generate summary statistics by groups
#'
#' @param data Dataset
#' @param liwc_vars LIWC variable names
#' @param group_var Grouping variable (Faculty or Sex)
#' @return Summary statistics data frame
generate_summary_stats <- function(data, liwc_vars, group_var) {
  cat(sprintf("\nGenerating summary statistics by %s...\n", group_var))
  
  # Remove rows with missing group variable
  data_clean <- data[!is.na(data[[group_var]]), ]
  
  summary_list <- list()
  
  for (var in liwc_vars) {
    if (var %in% colnames(data_clean) && is.numeric(data_clean[[var]])) {
      group_summary <- data_clean %>%
        group_by(!!sym(group_var)) %>%
        summarise(
          Variable = var,
          N = sum(!is.na(!!sym(var))),
          Mean = mean(!!sym(var), na.rm = TRUE),
          SD = sd(!!sym(var), na.rm = TRUE),
          Median = median(!!sym(var), na.rm = TRUE),
          Min = min(!!sym(var), na.rm = TRUE),
          Max = max(!!sym(var), na.rm = TRUE)
        )
      
      summary_list[[var]] <- group_summary
    }
  }
  
  summary_df <- bind_rows(summary_list)
  return(summary_df)
}

#' Create boxplots for LIWC variables across groups
#'
#' @param data Dataset
#' @param liwc_vars LIWC variables to plot (subset recommended)
#' @param group_var Grouping variable
#' @param output_dir Directory to save plots
create_boxplots <- function(data, liwc_vars, group_var, output_dir = "plots") {
  cat(sprintf("\nCreating boxplots for %s differences...\n", group_var))
  
  # Create output directory if it doesn't exist
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  
  # Remove rows with missing group variable
  data_clean <- data[!is.na(data[[group_var]]), ]
  
  # Create boxplots for top variables (limit to avoid overwhelming output)
  n_plots <- min(length(liwc_vars), 12)
  selected_vars <- liwc_vars[1:n_plots]
  
  for (var in selected_vars) {
    if (var %in% colnames(data_clean) && is.numeric(data_clean[[var]])) {
      p <- ggplot(data_clean, aes(x = !!sym(group_var), y = !!sym(var), 
                                   fill = !!sym(group_var))) +
        geom_boxplot(alpha = 0.7) +
        theme_minimal() +
        labs(
          title = sprintf("%s by %s", var, group_var),
          x = group_var,
          y = var
        ) +
        theme(axis.text.x = element_text(angle = 45, hjust = 1))
      
      # Save plot
      filename <- file.path(output_dir, 
                           sprintf("boxplot_%s_by_%s.png", var, group_var))
      ggsave(filename, p, width = 8, height = 6, dpi = 300)
    }
  }
  
  cat(sprintf("Saved %d boxplots to %s/\n", n_plots, output_dir))
}

#' Create violin plots for sex differences
#'
#' @param data Dataset
#' @param liwc_vars LIWC variables to plot
#' @param output_dir Directory to save plots
create_violin_plots <- function(data, liwc_vars, output_dir = "plots") {
  cat("\nCreating violin plots for sex differences...\n")
  
  # Create output directory if it doesn't exist
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  
  # Remove rows with missing Sex
  data_clean <- data[!is.na(data$Sex), ]
  
  # Create violin plots for top variables
  n_plots <- min(length(liwc_vars), 12)
  selected_vars <- liwc_vars[1:n_plots]
  
  for (var in selected_vars) {
    if (var %in% colnames(data_clean) && is.numeric(data_clean[[var]])) {
      p <- ggplot(data_clean, aes(x = Sex, y = !!sym(var), fill = Sex)) +
        geom_violin(alpha = 0.7, trim = FALSE) +
        geom_boxplot(width = 0.1, alpha = 0.5) +
        theme_minimal() +
        labs(
          title = sprintf("%s by Sex", var),
          x = "Sex",
          y = var
        )
      
      # Save plot
      filename <- file.path(output_dir, sprintf("violin_%s_by_sex.png", var))
      ggsave(filename, p, width = 8, height = 6, dpi = 300)
    }
  }
  
  cat(sprintf("Saved %d violin plots to %s/\n", n_plots, output_dir))
}

#' Create correlation heatmap
#'
#' @param data Dataset
#' @param liwc_vars LIWC variables
#' @param group_var Grouping variable
#' @param output_dir Directory to save plots
create_correlation_heatmap <- function(data, liwc_vars, group_var, 
                                       output_dir = "plots") {
  cat(sprintf("\nCreating correlation heatmap by %s...\n", group_var))
  
  # Create output directory if it doesn't exist
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  
  # Remove rows with missing group variable
  data_clean <- data[!is.na(data[[group_var]]), ]
  
  # Get unique groups
  groups <- unique(data_clean[[group_var]])
  
  for (grp in groups) {
    subset_data <- data_clean[data_clean[[group_var]] == grp, ]
    
    # Select subset of LIWC variables for readability
    n_vars <- min(length(liwc_vars), 20)
    selected_vars <- liwc_vars[1:n_vars]
    
    # Calculate correlation matrix
    cor_data <- subset_data[, selected_vars]
    cor_data <- cor_data[, sapply(cor_data, is.numeric)]
    cor_matrix <- cor(cor_data, use = "pairwise.complete.obs")
    
    # Melt for ggplot
    cor_melted <- melt(cor_matrix)
    
    # Create heatmap
    p <- ggplot(cor_melted, aes(Var1, Var2, fill = value)) +
      geom_tile() +
      scale_fill_gradient2(low = "blue", mid = "white", high = "red", 
                          midpoint = 0, limits = c(-1, 1)) +
      theme_minimal() +
      labs(
        title = sprintf("LIWC Variable Correlations - %s: %s", group_var, grp),
        x = "",
        y = "",
        fill = "Correlation"
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 8),
            axis.text.y = element_text(size = 8))
    
    # Save plot
    filename <- file.path(output_dir, 
                         sprintf("heatmap_%s_%s.png", group_var, 
                                gsub(" ", "_", grp)))
    ggsave(filename, p, width = 12, height = 10, dpi = 300)
  }
  
  cat(sprintf("Saved correlation heatmaps to %s/\n", output_dir))
}

# ============================================================================
# 3. STATISTICAL TESTING
# ============================================================================

#' Conduct ANOVA for faculty differences
#'
#' @param data Dataset
#' @param liwc_vars LIWC variables
#' @return Data frame with ANOVA results
conduct_anova_tests <- function(data, liwc_vars) {
  cat("\nConducting ANOVA tests for faculty differences...\n")
  
  # Remove rows with missing Faculty
  data_clean <- data[!is.na(data$Faculty), ]
  
  anova_results <- list()
  
  for (var in liwc_vars) {
    if (var %in% colnames(data_clean) && is.numeric(data_clean[[var]])) {
      # Remove missing values
      analysis_data <- data_clean[!is.na(data_clean[[var]]), ]
      
      if (nrow(analysis_data) > 0 && length(unique(analysis_data$Faculty)) > 1) {
        # Perform ANOVA
        formula_str <- paste(var, "~ Faculty")
        anova_model <- aov(as.formula(formula_str), data = analysis_data)
        anova_summary <- summary(anova_model)
        
        # Extract F-statistic and p-value
        f_stat <- anova_summary[[1]]$`F value`[1]
        p_value <- anova_summary[[1]]$`Pr(>F)`[1]
        
        # Calculate eta-squared (effect size)
        ss_between <- anova_summary[[1]]$`Sum Sq`[1]
        ss_total <- sum(anova_summary[[1]]$`Sum Sq`)
        eta_squared <- ss_between / ss_total
        
        anova_results[[var]] <- data.frame(
          Variable = var,
          F_statistic = f_stat,
          p_value = p_value,
          eta_squared = eta_squared,
          significant = ifelse(p_value < 0.05, "Yes", "No")
        )
      }
    }
  }
  
  results_df <- bind_rows(anova_results)
  
  # Apply Bonferroni correction
  if (nrow(results_df) > 0) {
    results_df$p_adjusted <- p.adjust(results_df$p_value, method = "bonferroni")
    results_df$significant_adjusted <- ifelse(results_df$p_adjusted < 0.05, 
                                             "Yes", "No")
  }
  
  cat(sprintf("Completed ANOVA tests for %d variables\n", nrow(results_df)))
  
  return(results_df)
}

#' Conduct t-tests for sex differences
#'
#' @param data Dataset
#' @param liwc_vars LIWC variables
#' @return Data frame with t-test results
conduct_ttest_analysis <- function(data, liwc_vars) {
  cat("\nConducting t-tests for sex differences...\n")
  
  # Remove rows with missing Sex
  data_clean <- data[!is.na(data$Sex), ]
  
  ttest_results <- list()
  
  for (var in liwc_vars) {
    if (var %in% colnames(data_clean) && is.numeric(data_clean[[var]])) {
      # Remove missing values
      analysis_data <- data_clean[!is.na(data_clean[[var]]), ]
      
      # Get unique sex categories
      sex_categories <- unique(analysis_data$Sex)
      
      if (length(sex_categories) == 2 && nrow(analysis_data) > 0) {
        # Perform t-test
        formula_str <- paste(var, "~ Sex")
        ttest_result <- t.test(as.formula(formula_str), data = analysis_data)
        
        # Calculate Cohen's d
        group1 <- analysis_data[[var]][analysis_data$Sex == sex_categories[1]]
        group2 <- analysis_data[[var]][analysis_data$Sex == sex_categories[2]]
        
        cohens_d <- tryCatch({
          effsize::cohen.d(group1, group2)$estimate
        }, error = function(e) {
          NA
        })
        
        ttest_results[[var]] <- data.frame(
          Variable = var,
          t_statistic = ttest_result$statistic,
          df = ttest_result$parameter,
          p_value = ttest_result$p.value,
          cohens_d = cohens_d,
          mean_diff = ttest_result$estimate[1] - ttest_result$estimate[2],
          significant = ifelse(ttest_result$p.value < 0.05, "Yes", "No")
        )
      }
    }
  }
  
  results_df <- bind_rows(ttest_results)
  
  # Apply Bonferroni correction
  if (nrow(results_df) > 0) {
    results_df$p_adjusted <- p.adjust(results_df$p_value, method = "bonferroni")
    results_df$significant_adjusted <- ifelse(results_df$p_adjusted < 0.05, 
                                             "Yes", "No")
  }
  
  cat(sprintf("Completed t-tests for %d variables\n", nrow(results_df)))
  
  return(results_df)
}

# ============================================================================
# 4. MAIN ANALYSIS PIPELINE
# ============================================================================

#' Main function to run complete LIWC analysis
#'
#' @param ind_file Path to forum_ind_train.csv
#' @param dep_file Path to forum_dep_train.csv
#' @param output_dir Base directory for outputs
#' @return List containing all analysis results
run_liwc_analysis <- function(ind_file, dep_file, output_dir = "output") {
  cat("============================================================\n")
  cat("LIWC DATASET EXPLORATION FOR FACULTY & SEX DIFFERENCES\n")
  cat("============================================================\n\n")
  
  # Create output directories
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)
  dir.create(file.path(output_dir, "plots"), showWarnings = FALSE, 
             recursive = TRUE)
  dir.create(file.path(output_dir, "tables"), showWarnings = FALSE, 
             recursive = TRUE)
  
  # 1. Load and prepare data
  merged_data <- load_and_merge_data(ind_file, dep_file)
  data_info <- identify_liwc_variables(merged_data)
  
  # 2. Generate summary statistics
  faculty_summary <- generate_summary_stats(
    data_info$data, data_info$liwc_vars, "Faculty"
  )
  sex_summary <- generate_summary_stats(
    data_info$data, data_info$liwc_vars, "Sex"
  )
  
  # Save summary statistics
  write.csv(faculty_summary, 
            file.path(output_dir, "tables", "summary_by_faculty.csv"),
            row.names = FALSE)
  write.csv(sex_summary, 
            file.path(output_dir, "tables", "summary_by_sex.csv"),
            row.names = FALSE)
  
  cat("\nSummary statistics saved.\n")
  
  # 3. Create visualizations
  create_boxplots(data_info$data, data_info$liwc_vars, "Faculty", 
                 file.path(output_dir, "plots"))
  create_violin_plots(data_info$data, data_info$liwc_vars, 
                     file.path(output_dir, "plots"))
  create_correlation_heatmap(data_info$data, data_info$liwc_vars, "Faculty",
                            file.path(output_dir, "plots"))
  
  # 4. Statistical testing
  anova_results <- conduct_anova_tests(data_info$data, data_info$liwc_vars)
  ttest_results <- conduct_ttest_analysis(data_info$data, data_info$liwc_vars)
  
  # Save statistical results
  write.csv(anova_results, 
            file.path(output_dir, "tables", "anova_results.csv"),
            row.names = FALSE)
  write.csv(ttest_results, 
            file.path(output_dir, "tables", "ttest_results.csv"),
            row.names = FALSE)
  
  cat("\nStatistical test results saved.\n")
  
  # 5. Generate summary report
  generate_summary_report(anova_results, ttest_results, output_dir)
  
  cat("\n============================================================\n")
  cat("ANALYSIS COMPLETE\n")
  cat(sprintf("Results saved to: %s/\n", output_dir))
  cat("============================================================\n")
  
  return(list(
    data = data_info$data,
    liwc_vars = data_info$liwc_vars,
    faculty_summary = faculty_summary,
    sex_summary = sex_summary,
    anova_results = anova_results,
    ttest_results = ttest_results
  ))
}

#' Generate summary report of findings
#'
#' @param anova_results ANOVA results
#' @param ttest_results T-test results
#' @param output_dir Output directory
generate_summary_report <- function(anova_results, ttest_results, output_dir) {
  cat("\nGenerating summary report...\n")
  
  report_file <- file.path(output_dir, "analysis_summary.txt")
  
  sink(report_file)
  
  cat("============================================================\n")
  cat("LIWC ANALYSIS SUMMARY REPORT\n")
  cat("============================================================\n\n")
  
  cat("1. FACULTY DIFFERENCES (ANOVA)\n")
  cat("--------------------------------------------------------------\n")
  if (nrow(anova_results) > 0) {
    sig_vars <- anova_results[anova_results$significant == "Yes", ]
    sig_adj_vars <- anova_results[anova_results$significant_adjusted == "Yes", ]
    
    cat(sprintf("Total variables tested: %d\n", nrow(anova_results)))
    cat(sprintf("Significant at p < 0.05: %d (%.1f%%)\n", 
                nrow(sig_vars), 
                100 * nrow(sig_vars) / nrow(anova_results)))
    cat(sprintf("Significant after Bonferroni correction: %d (%.1f%%)\n\n", 
                nrow(sig_adj_vars),
                100 * nrow(sig_adj_vars) / nrow(anova_results)))
    
    if (nrow(sig_adj_vars) > 0) {
      cat("Top significant variables (adjusted p-value):\n")
      top_vars <- head(sig_adj_vars[order(sig_adj_vars$p_adjusted), ], 10)
      print(top_vars[, c("Variable", "F_statistic", "p_adjusted", "eta_squared")])
    }
  } else {
    cat("No ANOVA results available.\n")
  }
  
  cat("\n\n2. SEX DIFFERENCES (T-TESTS)\n")
  cat("--------------------------------------------------------------\n")
  if (nrow(ttest_results) > 0) {
    sig_vars <- ttest_results[ttest_results$significant == "Yes", ]
    sig_adj_vars <- ttest_results[ttest_results$significant_adjusted == "Yes", ]
    
    cat(sprintf("Total variables tested: %d\n", nrow(ttest_results)))
    cat(sprintf("Significant at p < 0.05: %d (%.1f%%)\n", 
                nrow(sig_vars),
                100 * nrow(sig_vars) / nrow(ttest_results)))
    cat(sprintf("Significant after Bonferroni correction: %d (%.1f%%)\n\n", 
                nrow(sig_adj_vars),
                100 * nrow(sig_adj_vars) / nrow(ttest_results)))
    
    if (nrow(sig_adj_vars) > 0) {
      cat("Top significant variables (adjusted p-value):\n")
      top_vars <- head(sig_adj_vars[order(sig_adj_vars$p_adjusted), ], 10)
      print(top_vars[, c("Variable", "t_statistic", "p_adjusted", "cohens_d")])
    }
  } else {
    cat("No t-test results available.\n")
  }
  
  cat("\n\n3. INTERPRETATION NOTES\n")
  cat("--------------------------------------------------------------\n")
  cat("Effect Size Guidelines:\n")
  cat("- Cohen's d: Small = 0.2, Medium = 0.5, Large = 0.8\n")
  cat("- Eta-squared: Small = 0.01, Medium = 0.06, Large = 0.14\n\n")
  
  cat("Multiple Comparison Correction:\n")
  cat("- Bonferroni correction applied to control family-wise error rate\n")
  cat("- Use adjusted p-values for formal conclusions\n\n")
  
  cat("Next Steps:\n")
  cat("1. Review significant variables in the context of LIWC2015 framework\n")
  cat("2. Examine visualizations to understand the nature of differences\n")
  cat("3. Consider post-hoc tests for significant ANOVA results\n")
  cat("4. Interpret findings in relation to psychological/linguistic theory\n")
  
  cat("\n============================================================\n")
  
  sink()
  
  cat(sprintf("Summary report saved to: %s\n", report_file))
}

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

# Uncomment and modify the following lines to run the analysis:
#
# results <- run_liwc_analysis(
#   ind_file = "path/to/forum_ind_train.csv",
#   dep_file = "path/to/forum_dep_train.csv",
#   output_dir = "output"
# )
#
# # Access specific results:
# # results$faculty_summary
# # results$sex_summary
# # results$anova_results
# # results$ttest_results
