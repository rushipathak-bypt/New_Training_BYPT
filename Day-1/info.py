import sys
import pkg_resources

print("Python Version:", sys.version)

print("\nInstalled Packages:")
for pkg in pkg_resources.working_set:
    print(pkg.project_name, "==", pkg.version)
