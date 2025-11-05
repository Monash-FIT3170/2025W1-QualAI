# ============================================================================
# Focused LIWC Category Analysis
# ============================================================================
# This script provides focused analysis functions for specific LIWC categories
# based on the LIWC2015 framework priorities
# ============================================================================

library(dplyr)
library(ggplot2)
library(tidyr)

#' Define LIWC2015 priority categories
#'
#' @return List of LIWC variable categories
define_liwc_categories <- function() {
  list(
    summary = c("Analytic", "Clout", "Authentic", "Tone"),
    
    linguistic_dims = c("WC", "WPS", "Dic", "function", "pronoun", "ppron",
                       "i", "we", "you", "shehe", "they", "ipron",
                       "article", "prep", "auxverb", "adverb", "conj",
                       "negate", "verb", "adj", "compare", "interrog",
                       "number", "quant"),
    
    affect = c("affect", "posemo", "negemo", "anx", "anger", "sad"),
    
    social = c("social", "family", "friend", "female", "male"),
    
    cognitive = c("cogproc", "insight", "cause", "discrep", "tentat",
                 "certain", "differ"),
    
    perceptual = c("percept", "see", "hear", "feel"),
    
    biological = c("bio", "body", "health", "sexual", "ingest"),
    
    drives = c("drives", "affiliation", "achieve", "power", "reward", "risk"),
    
    time = c("focuspast", "focuspresent", "focusfuture"),
    
    relativity = c("relativ", "motion", "space", "time"),
    
    personal_concerns = c("work", "leisure", "home", "money", "relig", "death")
  )
}

#' Analyze specific LIWC category
#'
#' @param data Dataset
#' @param category_name Name of the category
#' @param category_vars Variables in the category
#' @param group_var Grouping variable
#' @param output_dir Output directory
analyze_liwc_category <- function(data, category_name, category_vars, 
                                  group_var, output_dir = "output") {
  cat(sprintf("\n=== Analyzing %s category ===\n", category_name))
  
  # Filter to existing variables in dataset
  existing_vars <- intersect(category_vars, colnames(data))
  
  if (length(existing_vars) == 0) {
    cat(sprintf("Warning: No variables found for %s category\n", category_name))
    return(NULL)
  }
  
  cat(sprintf("Found %d/%d variables in dataset\n", 
              length(existing_vars), length(category_vars)))
  
  # Clean data
  data_clean <- data[!is.na(data[[group_var]]), ]
  
  # Summary statistics
  summary_list <- list()
  for (var in existing_vars) {
    if (is.numeric(data_clean[[var]])) {
      var_summary <- data_clean %>%
        group_by(!!sym(group_var)) %>%
        summarise(
          Variable = var,
          Category = category_name,
          N = sum(!is.na(!!sym(var))),
          Mean = mean(!!sym(var), na.rm = TRUE),
          SD = sd(!!sym(var), na.rm = TRUE),
          Median = median(!!sym(var), na.rm = TRUE)
        )
      summary_list[[var]] <- var_summary
    }
  }
  
  category_summary <- bind_rows(summary_list)
  
  # Create visualization
  plot_dir <- file.path(output_dir, "plots", "categories")
  dir.create(plot_dir, showWarnings = FALSE, recursive = TRUE)
  
  # Prepare data for plotting
  plot_data <- data_clean %>%
    select(!!sym(group_var), all_of(existing_vars)) %>%
    pivot_longer(cols = all_of(existing_vars), 
                names_to = "Variable", 
                values_to = "Value")
  
  # Create grouped boxplot
  p <- ggplot(plot_data, aes(x = Variable, y = Value, fill = !!sym(group_var))) +
    geom_boxplot(alpha = 0.7) +
    theme_minimal() +
    labs(
      title = sprintf("%s Variables by %s", category_name, group_var),
      x = "LIWC Variable",
      y = "Value",
      fill = group_var
    ) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 8))
  
  filename <- file.path(plot_dir, 
                       sprintf("%s_by_%s.png", 
                              gsub(" ", "_", category_name), 
                              group_var))
  ggsave(filename, p, width = 12, height = 6, dpi = 300)
  
  cat(sprintf("Saved plot: %s\n", filename))
  
  return(category_summary)
}

#' Run focused analysis on all priority categories
#'
#' @param data Dataset
#' @param group_var Grouping variable
#' @param output_dir Output directory
#' @return Combined summary for all categories
analyze_all_priority_categories <- function(data, group_var, 
                                           output_dir = "output") {
  cat("\n============================================================\n")
  cat("FOCUSED LIWC CATEGORY ANALYSIS\n")
  cat("============================================================\n")
  
  categories <- define_liwc_categories()
  all_summaries <- list()
  
  for (cat_name in names(categories)) {
    summary <- analyze_liwc_category(
      data = data,
      category_name = cat_name,
      category_vars = categories[[cat_name]],
      group_var = group_var,
      output_dir = output_dir
    )
    
    if (!is.null(summary)) {
      all_summaries[[cat_name]] <- summary
    }
  }
  
  # Combine all summaries
  combined_summary <- bind_rows(all_summaries)
  
  # Save combined summary
  table_dir <- file.path(output_dir, "tables", "categories")
  dir.create(table_dir, showWarnings = FALSE, recursive = TRUE)
  
  filename <- file.path(table_dir, 
                       sprintf("category_summary_by_%s.csv", group_var))
  write.csv(combined_summary, filename, row.names = FALSE)
  
  cat(sprintf("\nCombined summary saved: %s\n", filename))
  
  return(combined_summary)
}

#' Create summary visualization for key LIWC dimensions
#'
#' @param data Dataset
#' @param output_dir Output directory
create_key_dimensions_plot <- function(data, output_dir = "output") {
  cat("\nCreating key dimensions comparison plot...\n")
  
  # Define key variables to compare
  key_vars <- c("Analytic", "Clout", "Authentic", "Tone", 
               "posemo", "negemo", "cogproc", "social")
  
  # Filter to existing variables
  existing_vars <- intersect(key_vars, colnames(data))
  
  if (length(existing_vars) == 0) {
    cat("Warning: No key variables found in dataset\n")
    return(NULL)
  }
  
  # Prepare data for Faculty comparison
  if ("Faculty" %in% colnames(data)) {
    data_clean <- data[!is.na(data$Faculty), ]
    
    plot_data <- data_clean %>%
      select(Faculty, all_of(existing_vars)) %>%
      pivot_longer(cols = all_of(existing_vars), 
                  names_to = "Variable", 
                  values_to = "Value") %>%
      group_by(Faculty, Variable) %>%
      summarise(Mean = mean(Value, na.rm = TRUE), .groups = "drop")
    
    # Create heatmap
    p1 <- ggplot(plot_data, aes(x = Variable, y = Faculty, fill = Mean)) +
      geom_tile() +
      scale_fill_gradient2(low = "blue", mid = "white", high = "red",
                          midpoint = 50) +
      theme_minimal() +
      labs(
        title = "Key LIWC Dimensions by Faculty",
        x = "LIWC Variable",
        y = "Faculty",
        fill = "Mean Score"
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    plot_dir <- file.path(output_dir, "plots")
    filename1 <- file.path(plot_dir, "key_dimensions_faculty_heatmap.png")
    ggsave(filename1, p1, width = 10, height = 6, dpi = 300)
    cat(sprintf("Saved: %s\n", filename1))
  }
  
  # Prepare data for Sex comparison
  if ("Sex" %in% colnames(data)) {
    data_clean <- data[!is.na(data$Sex), ]
    
    plot_data <- data_clean %>%
      select(Sex, all_of(existing_vars)) %>%
      pivot_longer(cols = all_of(existing_vars), 
                  names_to = "Variable", 
                  values_to = "Value") %>%
      group_by(Sex, Variable) %>%
      summarise(Mean = mean(Value, na.rm = TRUE),
               SD = sd(Value, na.rm = TRUE), .groups = "drop")
    
    # Create bar plot with error bars
    p2 <- ggplot(plot_data, aes(x = Variable, y = Mean, fill = Sex)) +
      geom_bar(stat = "identity", position = "dodge", alpha = 0.7) +
      geom_errorbar(aes(ymin = Mean - SD, ymax = Mean + SD),
                   position = position_dodge(0.9), width = 0.2) +
      theme_minimal() +
      labs(
        title = "Key LIWC Dimensions by Sex",
        x = "LIWC Variable",
        y = "Mean Score",
        fill = "Sex"
      ) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    plot_dir <- file.path(output_dir, "plots")
    filename2 <- file.path(plot_dir, "key_dimensions_sex_barplot.png")
    ggsave(filename2, p2, width = 10, height = 6, dpi = 300)
    cat(sprintf("Saved: %s\n", filename2))
  }
}

#' Identify top differentiating variables
#'
#' @param anova_results ANOVA results dataframe
#' @param ttest_results T-test results dataframe
#' @param n_top Number of top variables to return
#' @return List with top variables for each test
identify_top_differences <- function(anova_results, ttest_results, n_top = 10) {
  cat("\n=== Identifying Top Differentiating Variables ===\n")
  
  top_list <- list()
  
  # Top faculty differences (by effect size)
  if (nrow(anova_results) > 0) {
    top_faculty <- anova_results %>%
      filter(significant_adjusted == "Yes") %>%
      arrange(desc(eta_squared)) %>%
      head(n_top)
    
    cat(sprintf("\nTop %d variables by faculty (eta-squared):\n", 
                min(n_top, nrow(top_faculty))))
    if (nrow(top_faculty) > 0) {
      print(top_faculty[, c("Variable", "eta_squared", "p_adjusted")])
    } else {
      cat("No significant variables after correction\n")
    }
    
    top_list$faculty <- top_faculty
  }
  
  # Top sex differences (by effect size)
  if (nrow(ttest_results) > 0) {
    top_sex <- ttest_results %>%
      filter(significant_adjusted == "Yes") %>%
      arrange(desc(abs(cohens_d))) %>%
      head(n_top)
    
    cat(sprintf("\nTop %d variables by sex (|Cohen's d|):\n", 
                min(n_top, nrow(top_sex))))
    if (nrow(top_sex) > 0) {
      print(top_sex[, c("Variable", "cohens_d", "p_adjusted")])
    } else {
      cat("No significant variables after correction\n")
    }
    
    top_list$sex <- top_sex
  }
  
  return(top_list)
}

#' Generate interpretive report for significant findings
#'
#' @param anova_results ANOVA results
#' @param ttest_results T-test results
#' @param output_dir Output directory
generate_interpretive_report <- function(anova_results, ttest_results, 
                                        output_dir = "output") {
  cat("\nGenerating interpretive report...\n")
  
  report_file <- file.path(output_dir, "interpretive_findings.txt")
  
  sink(report_file)
  
  cat("============================================================\n")
  cat("INTERPRETIVE FINDINGS: LIWC ANALYSIS\n")
  cat("============================================================\n\n")
  
  cat("This report provides interpretation of significant findings from\n")
  cat("the LIWC analysis in the context of psychological and linguistic theory.\n\n")
  
  # Get LIWC categories
  categories <- define_liwc_categories()
  
  # Analyze ANOVA results
  cat("1. FACULTY DIFFERENCES\n")
  cat("--------------------------------------------------------------\n\n")
  
  if (nrow(anova_results) > 0) {
    sig_vars <- anova_results %>%
      filter(significant_adjusted == "Yes") %>%
      arrange(desc(eta_squared))
    
    if (nrow(sig_vars) > 0) {
      cat(sprintf("Found %d significant variables (Bonferroni-corrected)\n\n", 
                  nrow(sig_vars)))
      
      # Categorize significant variables
      for (cat_name in names(categories)) {
        cat_vars <- intersect(sig_vars$Variable, categories[[cat_name]])
        
        if (length(cat_vars) > 0) {
          cat(sprintf("\n%s Category:\n", toupper(cat_name)))
          cat(sprintf("- %d significant variables\n", length(cat_vars)))
          cat("Variables:", paste(cat_vars, collapse = ", "), "\n")
          
          # Provide category-specific interpretation
          if (cat_name == "summary") {
            cat("\nInterpretation: Differences in summary variables suggest\n")
            cat("faculties vary in fundamental writing style characteristics.\n")
            cat("- Analytic: logical vs. narrative thinking\n")
            cat("- Clout: confidence and social status\n")
            cat("- Authentic: personal vs. distanced writing\n")
            cat("- Tone: emotional positivity\n")
          } else if (cat_name == "affect") {
            cat("\nInterpretation: Emotional expression varies across faculties.\n")
            cat("May reflect discipline norms for emotional expression in\n")
            cat("academic discourse.\n")
          } else if (cat_name == "cognitive") {
            cat("\nInterpretation: Cognitive processing differences may reflect\n")
            cat("disciplinary thinking styles and problem-solving approaches.\n")
          }
        }
      }
    } else {
      cat("No significant differences found after Bonferroni correction.\n")
      cat("Consider using uncorrected p-values for exploratory analysis.\n")
    }
  }
  
  cat("\n\n2. SEX DIFFERENCES\n")
  cat("--------------------------------------------------------------\n\n")
  
  if (nrow(ttest_results) > 0) {
    sig_vars <- ttest_results %>%
      filter(significant_adjusted == "Yes") %>%
      arrange(desc(abs(cohens_d)))
    
    if (nrow(sig_vars) > 0) {
      cat(sprintf("Found %d significant variables (Bonferroni-corrected)\n\n", 
                  nrow(sig_vars)))
      
      # Categorize significant variables
      for (cat_name in names(categories)) {
        cat_vars <- intersect(sig_vars$Variable, categories[[cat_name]])
        
        if (length(cat_vars) > 0) {
          cat(sprintf("\n%s Category:\n", toupper(cat_name)))
          cat(sprintf("- %d significant variables\n", length(cat_vars)))
          cat("Variables:", paste(cat_vars, collapse = ", "), "\n")
          
          # Show direction of effects
          cat("\nEffect directions:\n")
          for (var in cat_vars) {
            d <- sig_vars$cohens_d[sig_vars$Variable == var]
            direction <- ifelse(d > 0, "Group 1 > Group 2", "Group 2 > Group 1")
            cat(sprintf("  %s: d = %.3f (%s)\n", var, d, direction))
          }
          
          # Provide category-specific interpretation
          if (cat_name == "social") {
            cat("\nInterpretation: Gender differences in social language use\n")
            cat("are well-documented in communication literature.\n")
          } else if (cat_name == "linguistic_dims") {
            cat("\nInterpretation: Linguistic style differences may reflect\n")
            cat("different communication strategies and norms.\n")
          }
        }
      }
    } else {
      cat("No significant differences found after Bonferroni correction.\n")
      cat("Consider using uncorrected p-values for exploratory analysis.\n")
    }
  }
  
  cat("\n\n3. RECOMMENDATIONS FOR FURTHER ANALYSIS\n")
  cat("--------------------------------------------------------------\n\n")
  
  cat("1. Post-hoc Tests:\n")
  cat("   - For significant ANOVA results, conduct pairwise comparisons\n")
  cat("   - Use Tukey HSD or similar methods to identify specific differences\n\n")
  
  cat("2. Interaction Effects:\n")
  cat("   - Examine Faculty × Sex interactions using two-way ANOVA\n")
  cat("   - Some effects may be moderated by the other factor\n\n")
  
  cat("3. Context Analysis:\n")
  cat("   - Review actual forum posts exhibiting extreme values\n")
  cat("   - Qualitative analysis can provide deeper understanding\n\n")
  
  cat("4. Validation:\n")
  cat("   - Test findings on hold-out data (forum_ind_test.csv)\n")
  cat("   - Ensure results generalize beyond training data\n\n")
  
  cat("5. Theoretical Integration:\n")
  cat("   - Consult LIWC2015 validation studies\n")
  cat("   - Review literature on academic discourse and gender communication\n")
  cat("   - Consider disciplinary differences in communication norms\n\n")
  
  cat("============================================================\n")
  
  sink()
  
  cat(sprintf("Interpretive report saved: %s\n", report_file))
}

# ============================================================================
# EXAMPLE USAGE WITH MAIN ANALYSIS
# ============================================================================

# After running main analysis with run_liwc_analysis():
#
# # Run focused category analysis
# faculty_categories <- analyze_all_priority_categories(
#   data = results$data,
#   group_var = "Faculty",
#   output_dir = "output"
# )
#
# sex_categories <- analyze_all_priority_categories(
#   data = results$data,
#   group_var = "Sex",
#   output_dir = "output"
# )
#
# # Create key dimensions visualizations
# create_key_dimensions_plot(results$data, "output")
#
# # Identify top differentiating variables
# top_diffs <- identify_top_differences(
#   results$anova_results,
#   results$ttest_results,
#   n_top = 10
# )
#
# # Generate interpretive report
# generate_interpretive_report(
#   results$anova_results,
#   results$ttest_results,
#   "output"
# )
