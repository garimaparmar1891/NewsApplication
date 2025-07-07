#!/usr/bin/env python3
"""
Test runner script for the News Application server
"""

import subprocess
import sys
import os
import argparse

def run_tests(args):
    """Run pytest with the given arguments"""
    cmd = ["python", "-m", "pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend(["--cov=services", "--cov=utils", "--cov=repositories", "--cov-report=html:htmlcov"])
    
    if args.markers:
        cmd.extend(["-m", args.markers])
    
    if args.file:
        cmd.append(f"tests/test_{args.file}.py")
    
    if args.function:
        cmd.append(f"tests/test_{args.file}.py::{args.function}")
    
    if args.parallel:
        cmd.extend(["-n", "auto"])
    
    if args.html:
        cmd.append("--html=test_report.html")
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode

def main():
    parser = argparse.ArgumentParser(description="Run tests for News Application server")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-c", "--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("-m", "--markers", help="Run tests with specific markers (e.g., unit, admin)")
    parser.add_argument("-f", "--file", help="Run tests from specific file (without test_ prefix)")
    parser.add_argument("-t", "--function", help="Run specific test function")
    parser.add_argument("-p", "--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--html", action="store_true", help="Generate HTML test report")
    
    args = parser.parse_args()
    
    # Change to the server directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    return run_tests(args)

if __name__ == "__main__":
    sys.exit(main()) 