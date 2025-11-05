# Analysis Directory

This directory contains data analysis tasks and research implementations for the QualAI project.

## Current Analyses

### Task D.1: LIWC Dataset Exploration for Faculty & Sex Differences

**Location**: `task_d1_liwc_exploration/`

**Description**: Comprehensive analysis of Linguistic Inquiry and Word Count (LIWC) datasets from Monash University Moodle forums to investigate differences in linguistic patterns between faculties and sexes.

**Features**:
- Complete R-based analysis pipeline
- Statistical testing (ANOVA, t-tests) with effect sizes
- Multiple visualization types (boxplots, violin plots, heatmaps)
- Comprehensive documentation and guides
- LIWC2015 framework reference

**Status**: ✅ Implementation complete, ready for use with data files

**Quick Start**:
```r
setwd("task_d1_liwc_exploration")
source("run_analysis.R")
```

See `task_d1_liwc_exploration/README.md` for detailed documentation.

## Directory Structure

```
analysis/
├── README.md                      # This file
└── task_d1_liwc_exploration/     # Task D.1 implementation
    ├── README.md                 # Detailed documentation
    ├── QUICK_START.md           # Getting started guide
    ├── IMPLEMENTATION_SUMMARY.md # Complete implementation details
    ├── LIWC2015_Reference.md    # LIWC framework reference
    ├── liwc_analysis.R          # Main analysis script
    ├── liwc_focused_analysis.R  # Category-specific analysis
    ├── run_analysis.R           # Example usage script
    ├── test_syntax.R            # Validation script
    ├── data/                    # Data directory (user provides files)
    └── output/                  # Generated results (created by scripts)
```

## Adding New Analyses

When adding new analysis tasks to this directory:

1. Create a new subdirectory with a descriptive name (e.g., `task_x_description`)
2. Include at minimum:
   - `README.md` - Documentation and usage instructions
   - Analysis scripts (R, Python, or other languages)
   - `.gitignore` - To exclude data and output files
3. Update this README to list the new analysis
4. Follow the structure established in `task_d1_liwc_exploration` as a template

## Best Practices

- **Reproducibility**: Ensure all analyses are fully reproducible with clear documentation
- **Data Privacy**: Never commit sensitive data files; use `.gitignore`
- **Documentation**: Provide comprehensive documentation for all analyses
- **Code Quality**: Comment code thoroughly and follow consistent style
- **Dependencies**: Clearly document all required packages and dependencies
- **Testing**: Include validation scripts where applicable

## Resources

- **R Documentation**: https://www.r-project.org/
- **Python Documentation**: https://www.python.org/doc/
- **Statistical Analysis**: Consult appropriate statistical references for your methodology
- **Data Visualization**: Follow best practices for academic/scientific visualization

## Contact

For questions about specific analyses, refer to the README in each task directory.

For general questions about the analysis structure, contact the QualAI development team.
