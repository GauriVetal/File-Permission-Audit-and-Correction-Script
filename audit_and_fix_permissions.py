
import os
import stat
import sys

# Output file for inconsistencies
REPORT_FILE = "expected_report.txt"

# Get symbolic (e.g., -rw-r--r--) permissions of a file or directory
def get_symbolic_permissions(path):
    return stat.filemode(os.stat(path, follow_symlinks=False).st_mode)

# Get raw permission bits (e.g., 0o755)
def get_permission_bits(path):
    return os.stat(path, follow_symlinks=False).st_mode

# Extract user/group/other permission bits separately
def extract_bits(mode):
    return {
        'user':  (mode & 0o700) >> 6,
        'group': (mode & 0o070) >> 3,
        'other': (mode & 0o007)
    }

# Compare file and directory permissions and describe missing ones
def describe_difference(file_bits, dir_bits):
    messages = set()
    for entity in ['user', 'group', 'other']:
        f = file_bits[entity]
        d = dir_bits[entity]
        if (d & 4) and not (f & 4):
            messages.add("read")
        if (d & 1) and not (f & 1):
            messages.add("execute")
    if not messages:
       return None
    return f"Missing {' and '.join(sorted(messages))} permission{'s' if len(messages) > 1 else ''} compared to parent directory"
    

# Fix file permissions to match missing read/execute from parent
def correct_permissions(file_path, file_bits, dir_bits):
    new_bits = {}
    changed = False
    for entity in ['user', 'group', 'other']:
        f = file_bits[entity]
        d = dir_bits[entity]
        updated = f
        if (d & 4) and not (f & 4):
            updated |= 4  # add read
            changed = True
        if (d & 1) and not (f & 1):
            updated |= 1  # add execute
            changed = True
        new_bits[entity] = updated

    if changed:
        # Combine updated bits into full mode
        new_mode = (new_bits['user'] << 6) | (new_bits['group'] << 3) | new_bits['other']
        os.chmod(file_path, new_mode)

# Main logic
def main(directory):
    with open(REPORT_FILE, 'w') as report:
        for root, dirs, files in os.walk(directory, followlinks=False):
            for fname in files:
                file_path = os.path.join(root, fname)

                if os.path.islink(file_path):
                    continue  # skip symbolic links

                try:
                    file_mode = get_permission_bits(file_path)
                    dir_mode = get_permission_bits(os.path.dirname(file_path))
                    file_bits = extract_bits(file_mode)
                    dir_bits = extract_bits(dir_mode)

                    diff = describe_difference(file_bits, dir_bits)

                    if diff:
                        # Log to report and correct
                        report.write(f"File Path: {file_path}\n")
                        report.write(f"File Permissions: {stat.filemode(file_mode)}\n")
                        report.write(f"Parent Directory Permissions: {stat.filemode(dir_mode)}\n")
                        report.write(f"Differences: {diff}\n\n")

                        correct_permissions(file_path, file_bits, dir_bits)

                except Exception as e:
                    report.write(f"Error processing {file_path}: {str(e)}\n\n")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python audit_and_fix_permissions.py <directory_path>")
        sys.exit(1)

    main(sys.argv[1])
