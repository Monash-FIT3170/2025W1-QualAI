# Data Directory

## Required Files

Place the following CSV files in this directory:

1. **forum_ind_train.csv** - Independent variables dataset
   - Contains: Unique_ID, Faculty, Sex, and other metadata
   
2. **forum_dep_train.csv** - Dependent variables dataset (LIWC output)
   - Contains: Unique_ID and LIWC2015 variables (columns B-CP)

## Notes

- These files should be obtained from the LIWC2015 analysis of Monash University Moodle forum posts
- The files are not tracked in git for privacy and size considerations
- Ensure both files have a common `Unique_ID` column for merging
- CSV files should use standard formatting (comma-separated, with headers)

## Sample Data Structure

### forum_ind_train.csv
```
Unique_ID,Faculty,Sex,Student_ID,Post_ID
1,Engineering,Male,S123,P001
2,Arts,Female,S456,P002
...
```

### forum_dep_train.csv
```
Unique_ID,WC,Analytic,Clout,Authentic,Tone,WPS,Sixltr,Dic,function,...
1,120,85.5,60.2,45.8,70.3,15.2,25.6,95.4,55.3,...
2,95,78.9,55.1,50.2,65.8,12.8,20.3,93.2,58.7,...
...
```

Note: The actual LIWC variables include approximately 90 columns covering linguistic dimensions, psychological constructs, and summary measures as defined in the LIWC2015 framework.
