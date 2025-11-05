# ============================================================================
# Test Script: Validate R Code Syntax and Structure
# ============================================================================
# This script validates that the analysis scripts have correct syntax
# and can be loaded without errors (doesn't require actual data)
# ============================================================================

cat("============================================================\n")
cat("LIWC ANALYSIS - SYNTAX VALIDATION TEST\n")
cat("============================================================\n\n")

# Track test results
test_results <- list()
all_passed <- TRUE

# ============================================================================
# Test 1: Check if required packages are available
# ============================================================================

cat("Test 1: Checking Required Packages\n")
cat("--------------------------------------------------------------\n")

required_packages <- c("dplyr", "ggplot2", "tidyr", "reshape2", 
                      "gridExtra", "effsize")

for (pkg in required_packages) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    cat(sprintf("  [PASS] %s is installed\n", pkg))
    test_results[[paste0("package_", pkg)]] <- TRUE
  } else {
    cat(sprintf("  [FAIL] %s is NOT installed\n", pkg))
    cat(sprintf("         Install with: install.packages('%s')\n", pkg))
    test_results[[paste0("package_", pkg)]] <- FALSE
    all_passed <- FALSE
  }
}

# ============================================================================
# Test 2: Load main analysis script
# ============================================================================

cat("\nTest 2: Loading Main Analysis Script (liwc_analysis.R)\n")
cat("--------------------------------------------------------------\n")

tryCatch({
  source("liwc_analysis.R")
  cat("  [PASS] liwc_analysis.R loaded successfully\n")
  test_results$main_script <- TRUE
  
  # Check if key functions are defined
  required_functions <- c(
    "load_and_merge_data",
    "identify_liwc_variables",
    "generate_summary_stats",
    "create_boxplots",
    "create_violin_plots",
    "create_correlation_heatmap",
    "conduct_anova_tests",
    "conduct_ttest_analysis",
    "run_liwc_analysis",
    "generate_summary_report"
  )
  
  cat("\n  Checking function definitions:\n")
  for (func in required_functions) {
    if (exists(func) && is.function(get(func))) {
      cat(sprintf("    [PASS] %s() is defined\n", func))
    } else {
      cat(sprintf("    [FAIL] %s() is NOT defined\n", func))
      all_passed <- FALSE
    }
  }
  
}, error = function(e) {
  cat("  [FAIL] Error loading liwc_analysis.R:\n")
  cat(sprintf("         %s\n", e$message))
  test_results$main_script <- FALSE
  all_passed <- FALSE
})

# ============================================================================
# Test 3: Load focused analysis script
# ============================================================================

cat("\nTest 3: Loading Focused Analysis Script (liwc_focused_analysis.R)\n")
cat("--------------------------------------------------------------\n")

tryCatch({
  source("liwc_focused_analysis.R")
  cat("  [PASS] liwc_focused_analysis.R loaded successfully\n")
  test_results$focused_script <- TRUE
  
  # Check if key functions are defined
  focused_functions <- c(
    "define_liwc_categories",
    "analyze_liwc_category",
    "analyze_all_priority_categories",
    "create_key_dimensions_plot",
    "identify_top_differences",
    "generate_interpretive_report"
  )
  
  cat("\n  Checking function definitions:\n")
  for (func in focused_functions) {
    if (exists(func) && is.function(get(func))) {
      cat(sprintf("    [PASS] %s() is defined\n", func))
    } else {
      cat(sprintf("    [FAIL] %s() is NOT defined\n", func))
      all_passed <- FALSE
    }
  }
  
}, error = function(e) {
  cat("  [FAIL] Error loading liwc_focused_analysis.R:\n")
  cat(sprintf("         %s\n", e$message))
  test_results$focused_script <- FALSE
  all_passed <- FALSE
})

# ============================================================================
# Test 4: Check LIWC categories definition
# ============================================================================

cat("\nTest 4: Checking LIWC Categories Definition\n")
cat("--------------------------------------------------------------\n")

if (exists("define_liwc_categories") && is.function(define_liwc_categories)) {
  tryCatch({
    categories <- define_liwc_categories()
    
    expected_categories <- c("summary", "linguistic_dims", "affect", "social",
                           "cognitive", "perceptual", "biological", "drives",
                           "time", "relativity", "personal_concerns")
    
    cat(sprintf("  Total category groups defined: %d\n", length(categories)))
    
    for (cat_name in expected_categories) {
      if (cat_name %in% names(categories)) {
        n_vars <- length(categories[[cat_name]])
        cat(sprintf("    [PASS] %s: %d variables\n", cat_name, n_vars))
      } else {
        cat(sprintf("    [WARN] %s: not defined\n", cat_name))
      }
    }
    
    test_results$categories <- TRUE
  }, error = function(e) {
    cat("  [FAIL] Error checking categories:\n")
    cat(sprintf("         %s\n", e$message))
    test_results$categories <- FALSE
    all_passed <- FALSE
  })
} else {
  cat("  [SKIP] define_liwc_categories() not available\n")
}

# ============================================================================
# Test 5: Check directory structure
# ============================================================================

cat("\nTest 5: Checking Directory Structure\n")
cat("--------------------------------------------------------------\n")

expected_dirs <- c("data", "output")
expected_files <- c("README.md", "LIWC2015_Reference.md", "QUICK_START.md",
                   "liwc_analysis.R", "liwc_focused_analysis.R", 
                   "run_analysis.R")

cat("  Directories:\n")
for (dir in expected_dirs) {
  if (dir.exists(dir)) {
    cat(sprintf("    [PASS] %s/ exists\n", dir))
  } else {
    cat(sprintf("    [INFO] %s/ does not exist (will be created on run)\n", dir))
  }
}

cat("\n  Files:\n")
for (file in expected_files) {
  if (file.exists(file)) {
    cat(sprintf("    [PASS] %s exists\n", file))
  } else {
    cat(sprintf("    [WARN] %s does not exist\n", file))
  }
}

# ============================================================================
# Test 6: Validate documentation
# ============================================================================

cat("\nTest 6: Validating Documentation\n")
cat("--------------------------------------------------------------\n")

doc_files <- c(
  "README.md" = "Main documentation",
  "QUICK_START.md" = "Quick start guide",
  "LIWC2015_Reference.md" = "LIWC framework reference",
  "data/README.md" = "Data directory instructions"
)

for (file in names(doc_files)) {
  if (file.exists(file)) {
    file_size <- file.info(file)$size
    cat(sprintf("    [PASS] %s exists (%d bytes)\n", 
                doc_files[file], file_size))
  } else {
    cat(sprintf("    [WARN] %s not found\n", doc_files[file]))
  }
}

# ============================================================================
# Summary
# ============================================================================

cat("\n============================================================\n")
cat("TEST SUMMARY\n")
cat("============================================================\n\n")

passed_tests <- sum(unlist(test_results))
total_tests <- length(test_results)

cat(sprintf("Tests Passed: %d/%d\n", passed_tests, total_tests))

if (all_passed && passed_tests == total_tests) {
  cat("\n[SUCCESS] All validation tests passed!\n")
  cat("The analysis scripts are ready to use.\n\n")
  cat("Next steps:\n")
  cat("  1. Place data files in data/ directory\n")
  cat("  2. Run: source('run_analysis.R')\n")
  cat("  3. Review results in output/ directory\n")
} else {
  cat("\n[WARNING] Some tests did not pass.\n")
  cat("Please address the issues above before running the analysis.\n\n")
  
  if (sum(!unlist(lapply(required_packages, function(p) 
                        requireNamespace(p, quietly = TRUE)))) > 0) {
    cat("Missing packages can be installed with:\n")
    cat('  install.packages(c("dplyr", "ggplot2", "tidyr", "reshape2", "gridExtra", "effsize"))\n')
  }
}

cat("\n============================================================\n")

# Return TRUE if all tests passed, FALSE otherwise
invisible(all_passed && passed_tests == total_tests)
