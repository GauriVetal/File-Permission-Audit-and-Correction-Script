# File-Permission-Audit-and-Correction-Script

# File Permission Audit Script

# About

This Python script audits a given directory [and subdirectories] for files whose permissions lack read (`r`) or execute (`x`) bits compared to their parent directory.

If any mismatch is found, it:
- Logs the details in `expected_report.txt`
- Fixes the file permissions (without changing write permission)

# How to Run in Command Prompt:
python audit_and_fix_permissions.py sample_directory_structure/

# Structure of Folder
sample_directory_structure/
├── dir1/
│   ├── file1.txt
│   ├── file2.sh
│   └── subdir1/
│       └── file3.log
└── dir2/
    ├── file4.txt
    └── file5.bin

# Output:
expected_report.txt: shows mismatches and corrections.

