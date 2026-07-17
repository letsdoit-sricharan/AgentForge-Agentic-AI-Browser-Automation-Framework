import os
import re
import ast

RUNTIME_DIR = r"E:\projrcts\AI_project\backend\app\runtime"

# Map Class Name -> module path (e.g., 'app.runtime.execution.execution_context')
class_to_module = {}

# 1. Discover all classes
for root, dirs, files in os.walk(RUNTIME_DIR):
    for f in files:
        if f.endswith('.py') and f != '__init__.py':
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as f_in:
                    content = f_in.read()
                tree = ast.parse(content)
                rel_path = os.path.relpath(filepath, start=RUNTIME_DIR).replace(os.sep, '.')[:-3]
                module_path = f"app.runtime.{rel_path}"
                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        class_to_module[node.name] = module_path
                    elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        pass # if functions are imported
            except Exception as e:
                pass

# Let's add some enums or other symbols explicitly if ast didn't pick up (like assignments)
# We will use regex as a fallback.

# 2. Rewrite imports in all files
modified_files = []
for root, dirs, files in os.walk(RUNTIME_DIR):
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as f_in:
                lines = f_in.readlines()
            
            new_lines = []
            changed = False
            
            # Very basic parser for multi-line imports
            # This is a naive state machine
            i = 0
            while i < len(lines):
                line = lines[i]
                
                # Check for: from app.runtime.x import ( ... )
                match_from = re.match(r'^from\s+(app\.runtime\.[a-zA-Z0-9_]+)\s+import\s+(.*)', line.strip())
                if match_from:
                    pkg = match_from.group(1)
                    rest = match_from.group(2)
                    
                    imported_names = []
                    
                    if rest.startswith('('):
                        # Multi-line import
                        buffer = line
                        while ')' not in buffer:
                            i += 1
                            buffer += lines[i]
                        # extract names
                        names_str = buffer[buffer.find('(')+1 : buffer.find(')')]
                        imported_names = [n.strip() for n in names_str.split(',') if n.strip()]
                    else:
                        imported_names = [n.strip() for n in rest.split(',') if n.strip()]
                    
                    # check if the package is exactly a module or a dir?
                    # if it's already a module (e.g. app.runtime.execution.execution_engine), we shouldn't change it,
                    # UNLESS it's a self-import, which we need to remove entirely. But the rule says:
                    # "Replace every package import with direct module imports."
                    # We will rewrite ALL app.runtime.* imports to their exact module path based on class_to_module, 
                    # except if it's not in our map (e.g., we couldn't find the class).
                    
                    new_import_lines = []
                    for name in imported_names:
                        # strip alias if any
                        real_name = name.split(' as ')[0].strip()
                        if real_name in class_to_module:
                            exact_mod = class_to_module[real_name]
                            new_import_lines.append(f"from {exact_mod} import {name}\n")
                        else:
                            # fallback: just keep it as is
                            new_import_lines.append(f"from {pkg} import {name}\n")
                    
                    # Deduplicate or just add
                    for nl in sorted(list(set(new_import_lines))):
                        new_lines.append(nl)
                    changed = True
                    i += 1
                    continue
                
                new_lines.append(line)
                i += 1
            
            # Rule 3: Remove every self-import. 
            # e.g. in execution_engine.py, remove `from app.runtime.execution.execution_engine import ExecutionEngine`
            rel_path = os.path.relpath(filepath, start=RUNTIME_DIR).replace(os.sep, '.')[:-3]
            current_mod = f"app.runtime.{rel_path}"
            
            final_lines = []
            for line in new_lines:
                # regex to check if we are importing from our own module
                if line.startswith(f"from {current_mod} import "):
                    changed = True
                    continue # skip this line (remove self-import)
                final_lines.append(line)

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f_out:
                    f_out.writelines(final_lines)
                modified_files.append(filepath)

print("Modified files:")
for mf in modified_files:
    print(mf)
