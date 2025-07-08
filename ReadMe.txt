Assignment: File Permission Audit and Correction Script.

Developed by: Gauri Vetal

--- A brief explanation of your approach and any assumptions ---

 Approach:
- The script uses Python that scans all files inside a selected directory, including its subfolders. 
- For each file, the script checks its permission and compares then with the permissions of the folder it is in.
- If the folder has read or execute permission, but the file does not, then the script identifies this as inconsistent.
- These mismatches are recorded in a report file called "expected_report.txt".
- Symbolic links are skipped to avoid problems like infinite loops.
- The script also fixes the file's permission by adding only the missing read or execute permissions.
- The script is written in an efficient way so that it can handle large directories without slowing down.

 Assumptions:
- The script is executed in a Linux-based system (like WSL on Windows or Ubuntu)
- Files are regular.
- The user running the script has permission to read and modify the files.
- It is assumed that the parent directory's permissions are correct.


---- Recommendations for preventing similar issues in the future or suggestions for automated periodic checks ----

- Use proper default file permission settings using 'umask'.
- Apply the 'setgid' bit on shared folders so all files created inside inherit the folder's group permissions.
- Schedule this script to run regularly using a cron job to automatically detect and fix issues.