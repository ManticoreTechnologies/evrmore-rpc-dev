#!/usr/bin/env python3
"""
Code Quality Check Script

This script runs various code quality tools on the evrmore-rpc codebase.
"""

import subprocess
import sys
import os
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def run_command(command, description):
    """Run a shell command and print its output"""
    print_header(description)
    print(f"{Colors.OKBLUE}Running command: {' '.join(command)}{Colors.ENDC}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"{Colors.OKGREEN}✓ {description} completed successfully{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}Command failed with exit code {e.returncode}{Colors.ENDC}")
        if e.stdout:
            print(f"Standard output:\n{e.stdout}")
        if e.stderr:
            print(f"Standard error:\n{e.stderr}")
        return False

def check_tools_installed():
    """Check if required tools are installed"""
    required_tools = ["flake8", "black", "isort", "mypy"]
    missing_tools = []
    
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"{Colors.WARNING}Warning: The following tools are not installed:{Colors.ENDC}")
        for tool in missing_tools:
            print(f"  - {tool}")
        print("\nYou can install them with:")
        print(f"  pip install {' '.join(missing_tools)}")
        return False
    
    return True

def main():
    """Main function to run code quality checks"""
    # Get the project root directory
    script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    project_root = script_dir.parent
    
    # Change to the project root directory
    os.chdir(project_root)
    
    print_header("Code Quality Check for evrmore-rpc")
    print(f"Project root: {project_root}\n")
    
    # Check if tools are installed
    if not check_tools_installed():
        print(f"\n{Colors.WARNING}Some tools are not installed. Continuing with available tools...{Colors.ENDC}\n")
    
    # Keep track of whether all checks pass
    all_passed = True
    
    # Run flake8
    all_passed &= run_command(
        ["flake8", "evrmore_rpc", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"],
        "Running Flake8 (Critical Errors)"
    )
    
    # Run black in check mode
    all_passed &= run_command(
        ["black", "--check", "evrmore_rpc"],
        "Checking Code Formatting with Black"
    )
    
    # Run isort in check mode
    all_passed &= run_command(
        ["isort", "--check-only", "--profile", "black", "evrmore_rpc"],
        "Checking Import Sorting with isort"
    )
    
    # Run mypy type checking
    all_passed &= run_command(
        ["mypy", "evrmore_rpc", "--ignore-missing-imports"],
        "Checking Type Hints with mypy"
    )
    
    # Print summary
    print_header("Summary")
    if all_passed:
        print(f"{Colors.OKGREEN}All code quality checks passed!{Colors.ENDC}")
        return 0
    else:
        print(f"{Colors.FAIL}Some code quality checks failed. Please fix the issues and run again.{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 