#!/usr/bin/env python3

import os
import sys
import argparse

def create_problem(name, category="arrays"):
    # Convert problem name to file name format
    file_name = name.lower().replace(' ', '_')
    class_name = ''.join(word.capitalize() for word in name.split())
    
    # Create the problem directory
    problem_dir = f"problems/{category}/{file_name}"
    os.makedirs(problem_dir, exist_ok=True)
    
    # Create the files
    with open(f"{problem_dir}/README.md", 'w') as f:
        f.write(f"# {name}\n\n## Problem Description\n\n## Examples\n\n## Approach\n")
    
    # Create empty language files
    open(f"{problem_dir}/{file_name}.py", 'w').close()
    open(f"{problem_dir}/{file_name}.go", 'w').close()
    open(f"{problem_dir}/{file_name}.cpp", 'w').close()
    open(f"{problem_dir}/{class_name}.java", 'w').close()
    
    print(f"Created problem '{name}' in {problem_dir}")
    print(f"Files created: {file_name}.py, {file_name}.go, {file_name}.cpp, {class_name}.java, README.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new DSA problem")
    parser.add_argument("name", help="Name of the problem")
    parser.add_argument("--category", "-c", default="arrays", 
                        help="Category of the problem (arrays, strings, etc.)")
    
    args = parser.parse_args()
    create_problem(args.name, args.category)