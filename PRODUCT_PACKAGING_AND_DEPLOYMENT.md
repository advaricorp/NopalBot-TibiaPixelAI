# 🚀 Product Packaging & Deployment - IP Protection Guide

## 📋 Table of Contents
1. [Code Obfuscation Techniques](#code-obfuscation-techniques)
2. [Binary Protection](#binary-protection)
3. [Anti-Reverse Engineering](#anti-reverse-engineering)
4. [Deployment Strategies](#deployment-strategies)
5. [License Management](#license-management)

---

## 🔒 Code Obfuscation Techniques

### **Concept Overview**

Code obfuscation involves transforming source code to make it difficult to understand while maintaining functionality. This protects intellectual property and prevents reverse engineering.

### **C/C++ Obfuscation**

#### **1. Variable/Function Name Obfuscation**

```c
// Original code
int calculate_player_health(int base_health, int armor_bonus) {
    int total_health = base_health + armor_bonus;
    return total_health;
}

// Obfuscated code
int a1(int b1, int c1) {
    int d1 = b1 + c1;
    return d1;
}

// Advanced obfuscation with random names
int _0x7f3a2b1c(int _0x4d8e9f2a, int _0x1b5c7d3e) {
    int _0x9a2f4e8b = _0x4d8e9f2a + _0x1b5c7d3e;
    return _0x9a2f4e8b;
}
```

#### **2. Control Flow Obfuscation**

```c
// Original control flow
if (player_health > 0) {
    attack_enemy();
} else {
    retreat();
}

// Obfuscated control flow
int _0x3f2a1b8c = (player_health > 0) ? 1 : 0;
switch (_0x3f2a1b8c) {
    case 1:
        _0x7d4e2f1a();
        break;
    case 0:
        _0x9b3c5e8f();
        break;
    default:
        _0x2a1f4d7c();
        break;
}
```

#### **3. String Obfuscation**

```c
// Original strings
const char* error_msg = "Memory access denied";
const char* success_msg = "Operation completed";

// Obfuscated strings
const char _0x4a2b1c8d[] = {0x4d, 0x65, 0x6d, 0x6f, 0x72, 0x79, 0x20, 0x61, 0x63, 0x63, 0x65, 0x73, 0x73, 0x20, 0x64, 0x65, 0x6e, 0x69, 0x65, 0x64, 0x00};
const char _0x7f3e2d1a[] = {0x4f, 0x70, 0x65, 0x72, 0x61, 0x74, 0x69, 0x6f, 0x6e, 0x20, 0x63, 0x6f, 0x6d, 0x70, 0x6c, 0x65, 0x74, 0x65, 0x64, 0x00};

// XOR encryption
void decrypt_string(char* str, unsigned char key) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] ^= key;
    }
}
```

#### **4. Advanced Obfuscation Script**

```python
# obfuscator.py
import random
import string
import re

class CodeObfuscator:
    def __init__(self):
        self.name_mapping = {}
        self.string_mapping = {}
        
    def generate_random_name(self, length=8):
        """Generate random variable/function name"""
        return '_0x' + ''.join(random.choices('0123456789abcdef', k=length))
    
    def obfuscate_variables(self, code):
        """Obfuscate variable and function names"""
        # Find all variable and function names
        pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_name(match):
            name = match.group(1)
            if name in ['int', 'char', 'void', 'return', 'if', 'else', 'for', 'while']:
                return name  # Don't obfuscate keywords
            
            if name not in self.name_mapping:
                self.name_mapping[name] = self.generate_random_name()
            
            return self.name_mapping[name]
        
        return re.sub(pattern, replace_name, code)
    
    def obfuscate_strings(self, code):
        """Obfuscate string literals"""
        pattern = r'"([^"]*)"'
        
        def replace_string(match):
            string_val = match.group(1)
            if string_val not in self.string_mapping:
                # Convert to hex array
                hex_array = [hex(ord(c)) for c in string_val]
                hex_string = '{' + ', '.join(hex_array) + ', 0x00}'
                self.string_mapping[string_val] = hex_string
            
            return self.string_mapping[string_val]
        
        return re.sub(pattern, replace_string, code)
    
    def obfuscate_control_flow(self, code):
        """Obfuscate control flow with switch statements"""
        # Convert if-else to switch
        pattern = r'if\s*\(([^)]+)\)\s*{([^}]*)}\s*else\s*{([^}]*)}'
        
        def replace_if_else(match):
            condition = match.group(1)
            if_body = match.group(2)
            else_body = match.group(3)
            
            switch_var = self.generate_random_name()
            return f"""
            int {switch_var} = ({condition}) ? 1 : 0;
            switch ({switch_var}) {{
                case 1:
                    {if_body}
                    break;
                case 0:
                    {else_body}
                    break;
            }}
            """
        
        return re.sub(pattern, replace_if_else, code)
    
    def obfuscate_code(self, source_code):
        """Apply all obfuscation techniques"""
        obfuscated = source_code
        
        # Apply obfuscations
        obfuscated = self.obfuscate_strings(obfuscated)
        obfuscated = self.obfuscate_control_flow(obfuscated)
        obfuscated = self.obfuscate_variables(obfuscated)
        
        return obfuscated

# Usage
obfuscator = CodeObfuscator()
with open('source.c', 'r') as f:
    source = f.read()

obfuscated = obfuscator.obfuscate_code(source)
with open('obfuscated.c', 'w') as f:
    f.write(obfuscated)
```

---

## 🛡️ Binary Protection

### **Executable Protection**

#### **1. UPX Packing**

```bash
#!/bin/bash
# pack_binary.sh

echo "Packing binary with UPX..."

# Install UPX if not present
if ! command -v upx &> /dev/null; then
    echo "Installing UPX..."
    sudo apt-get install upx
fi

# Pack the binary
upx --best --ultra-brute ./tibia_bypass

echo "Binary packed successfully!"
```

#### **2. Custom Packer**

```c
// custom_packer.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

typedef struct {
    unsigned char *data;
    size_t size;
    unsigned char *compressed;
    size_t compressed_size;
} packed_binary_t;

// Compress binary data
packed_binary_t* compress_binary(const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (!file) return NULL;
    
    // Get file size
    fseek(file, 0, SEEK_END);
    size_t file_size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    // Read file data
    unsigned char *data = malloc(file_size);
    fread(data, 1, file_size, file);
    fclose(file);
    
    // Compress data
    size_t compressed_size = compressBound(file_size);
    unsigned char *compressed = malloc(compressed_size);
    
    if (compress(compressed, &compressed_size, data, file_size) != Z_OK) {
        free(data);
        free(compressed);
        return NULL;
    }
    
    // Create packed binary structure
    packed_binary_t *packed = malloc(sizeof(packed_binary_t));
    packed->data = data;
    packed->size = file_size;
    packed->compressed = compressed;
    packed->compressed_size = compressed_size;
    
    return packed;
}

// Create self-extracting executable
int create_self_extractor(const char *input_file, const char *output_file) {
    packed_binary_t *packed = compress_binary(input_file);
    if (!packed) return -1;
    
    // Create self-extracting stub
    const char *stub_template = 
        "#include <stdio.h>\n"
        "#include <stdlib.h>\n"
        "#include <zlib.h>\n"
        "#include <string.h>\n"
        "\n"
        "int main() {\n"
        "    // Embedded compressed data\n"
        "    unsigned char compressed_data[] = {\n"
        "        %s\n"
        "    };\n"
        "    \n"
        "    // Decompress and execute\n"
        "    size_t original_size = %zu;\n"
        "    unsigned char *decompressed = malloc(original_size);\n"
        "    \n"
        "    if (uncompress(decompressed, &original_size, \n"
        "                   compressed_data, sizeof(compressed_data)) == Z_OK) {\n"
        "        // Execute decompressed code\n"
        "        // Implementation depends on platform\n"
        "    }\n"
        "    \n"
        "    free(decompressed);\n"
        "    return 0;\n"
        "}\n";
    
    // Convert compressed data to C array
    char *hex_data = malloc(packed->compressed_size * 6); // "0xXX, " per byte
    char *ptr = hex_data;
    
    for (size_t i = 0; i < packed->compressed_size; i++) {
        ptr += sprintf(ptr, "0x%02x, ", packed->compressed[i]);
    }
    
    // Remove trailing comma
    if (ptr > hex_data) {
        *(ptr - 2) = '\0';
    }
    
    // Generate stub code
    char stub_code[8192];
    snprintf(stub_code, sizeof(stub_code), stub_template, hex_data, packed->size);
    
    // Write stub to file
    FILE *stub_file = fopen(output_file, "w");
    if (stub_file) {
        fwrite(stub_code, 1, strlen(stub_code), stub_file);
        fclose(stub_file);
    }
    
    free(hex_data);
    free(packed->data);
    free(packed->compressed);
    free(packed);
    
    return 0;
}
```

#### **3. Anti-Debug Protection**

```c
// anti_debug.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <signal.h>

// Check if process is being debugged
int is_being_debugged(void) {
    // Method 1: ptrace self-attach
    if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
        return 1; // Already being traced
    }
    ptrace(PTRACE_DETACH, 0, NULL, NULL);
    
    // Method 2: Check parent process
    pid_t ppid = getppid();
    char status_path[256];
    snprintf(status_path, sizeof(status_path), "/proc/%d/status", ppid);
    
    FILE *status_file = fopen(status_path, "r");
    if (status_file) {
        char line[256];
        while (fgets(line, sizeof(line), status_file)) {
            if (strstr(line, "TracerPid:")) {
                int tracer_pid;
                sscanf(line, "TracerPid: %d", &tracer_pid);
                fclose(status_file);
                return tracer_pid != 0;
            }
        }
        fclose(status_file);
    }
    
    return 0;
}

// Anti-debugging techniques
void install_anti_debug_protection(void) {
    // Set up signal handlers
    signal(SIGTRAP, SIG_IGN);
    signal(SIGSEGV, SIG_IGN);
    
    // Disable core dumps
    prctl(PR_SET_DUMPABLE, 0);
    
    // Check for debugger periodically
    if (is_being_debugged()) {
        printf("Debugger detected! Exiting...\n");
        exit(1);
    }
}

// Timing-based anti-debug
void timing_anti_debug(void) {
    clock_t start = clock();
    
    // Perform some operations
    for (int i = 0; i < 1000; i++) {
        // Normal operation
    }
    
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    
    // If execution is too slow, might be debugged
    if (time_spent > 0.1) { // 100ms threshold
        printf("Suspicious timing detected!\n");
        exit(1);
    }
}
```

---

## 🔍 Anti-Reverse Engineering

### **Code Virtualization**

#### **1. Simple VM Implementation**

```c
// code_vm.h
#ifndef CODE_VM_H
#define CODE_VM_H

typedef enum {
    OP_NOP,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_LOAD,
    OP_STORE,
    OP_JMP,
    OP_JZ,
    OP_CALL,
    OP_RET
} opcode_t;

typedef struct {
    opcode_t opcode;
    int operand1;
    int operand2;
    int operand3;
} instruction_t;

typedef struct {
    int registers[16];
    int stack[256];
    int stack_ptr;
    int pc; // Program counter
    instruction_t *code;
    int code_size;
} virtual_machine_t;

// VM functions
virtual_machine_t* vm_init(instruction_t *code, int size);
void vm_execute(virtual_machine_t *vm);
void vm_cleanup(virtual_machine_t *vm);

#endif
```

```c
// code_vm.c
#include "code_vm.h"
#include <stdio.h>
#include <stdlib.h>

virtual_machine_t* vm_init(instruction_t *code, int size) {
    virtual_machine_t *vm = malloc(sizeof(virtual_machine_t));
    vm->code = code;
    vm->code_size = size;
    vm->pc = 0;
    vm->stack_ptr = 0;
    
    // Initialize registers and stack
    for (int i = 0; i < 16; i++) {
        vm->registers[i] = 0;
    }
    
    return vm;
}

void vm_execute(virtual_machine_t *vm) {
    while (vm->pc < vm->code_size) {
        instruction_t *instr = &vm->code[vm->pc];
        
        switch (instr->opcode) {
            case OP_NOP:
                break;
                
            case OP_ADD:
                vm->registers[instr->operand1] = 
                    vm->registers[instr->operand2] + vm->registers[instr->operand3];
                break;
                
            case OP_SUB:
                vm->registers[instr->operand1] = 
                    vm->registers[instr->operand2] - vm->registers[instr->operand3];
                break;
                
            case OP_MUL:
                vm->registers[instr->operand1] = 
                    vm->registers[instr->operand2] * vm->registers[instr->operand3];
                break;
                
            case OP_DIV:
                if (vm->registers[instr->operand3] != 0) {
                    vm->registers[instr->operand1] = 
                        vm->registers[instr->operand2] / vm->registers[instr->operand3];
                }
                break;
                
            case OP_LOAD:
                vm->registers[instr->operand1] = instr->operand2;
                break;
                
            case OP_STORE:
                vm->stack[vm->stack_ptr++] = vm->registers[instr->operand1];
                break;
                
            case OP_JMP:
                vm->pc = instr->operand1;
                continue;
                
            case OP_JZ:
                if (vm->registers[instr->operand1] == 0) {
                    vm->pc = instr->operand2;
                    continue;
                }
                break;
                
            case OP_CALL:
                vm->stack[vm->stack_ptr++] = vm->pc + 1;
                vm->pc = instr->operand1;
                continue;
                
            case OP_RET:
                vm->pc = vm->stack[--vm->stack_ptr];
                continue;
        }
        
        vm->pc++;
    }
}

void vm_cleanup(virtual_machine_t *vm) {
    free(vm);
}
```

#### **2. Code to VM Converter**

```python
# code_to_vm.py
import ast
import random

class CodeToVMConverter:
    def __init__(self):
        self.vm_code = []
        self.variable_mapping = {}
        self.label_counter = 0
        
    def convert_expression(self, expr):
        """Convert Python expression to VM instructions"""
        if isinstance(expr, ast.Num):
            # Load constant
            reg = self.allocate_register()
            self.vm_code.append(('LOAD', reg, expr.n, 0))
            return reg
            
        elif isinstance(expr, ast.Name):
            # Load variable
            if expr.id in self.variable_mapping:
                reg = self.allocate_register()
                self.vm_code.append(('LOAD', reg, self.variable_mapping[expr.id], 0))
                return reg
            return None
            
        elif isinstance(expr, ast.BinOp):
            # Binary operation
            left_reg = self.convert_expression(expr.left)
            right_reg = self.convert_expression(expr.right)
            result_reg = self.allocate_register()
            
            if isinstance(expr.op, ast.Add):
                self.vm_code.append(('ADD', result_reg, left_reg, right_reg))
            elif isinstance(expr.op, ast.Sub):
                self.vm_code.append(('SUB', result_reg, left_reg, right_reg))
            elif isinstance(expr.op, ast.Mult):
                self.vm_code.append(('MUL', result_reg, left_reg, right_reg))
            elif isinstance(expr.op, ast.Div):
                self.vm_code.append(('DIV', result_reg, left_reg, right_reg))
                
            return result_reg
            
        return None
    
    def convert_statement(self, stmt):
        """Convert Python statement to VM instructions"""
        if isinstance(stmt, ast.Assign):
            # Variable assignment
            value_reg = self.convert_expression(stmt.value)
            if value_reg is not None:
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        self.variable_mapping[target.id] = value_reg
                        
        elif isinstance(stmt, ast.If):
            # If statement
            condition_reg = self.convert_expression(stmt.test)
            if condition_reg is not None:
                # Jump if condition is false
                false_label = self.generate_label()
                self.vm_code.append(('JZ', condition_reg, false_label, 0))
                
                # Convert if body
                for body_stmt in stmt.body:
                    self.convert_statement(body_stmt)
                    
                # End label
                self.vm_code.append(('NOP', 0, 0, 0))  # Placeholder for label
                
        elif isinstance(stmt, ast.While):
            # While loop
            start_label = self.generate_label()
            end_label = self.generate_label()
            
            # Start of loop
            self.vm_code.append(('NOP', 0, 0, 0))  # Placeholder for start label
            
            # Convert condition
            condition_reg = self.convert_expression(stmt.test)
            if condition_reg is not None:
                self.vm_code.append(('JZ', condition_reg, end_label, 0))
                
                # Convert loop body
                for body_stmt in stmt.body:
                    self.convert_statement(body_stmt)
                    
                # Jump back to start
                self.vm_code.append(('JMP', start_label, 0, 0))
                
                # End of loop
                self.vm_code.append(('NOP', 0, 0, 0))  # Placeholder for end label
    
    def allocate_register(self):
        """Allocate a virtual register"""
        return random.randint(0, 15)
    
    def generate_label(self):
        """Generate a unique label"""
        self.label_counter += 1
        return self.label_counter
    
    def convert_code(self, source_code):
        """Convert Python code to VM instructions"""
        tree = ast.parse(source_code)
        
        for stmt in tree.body:
            self.convert_statement(stmt)
            
        return self.vm_code

# Usage example
converter = CodeToVMConverter()
source_code = """
x = 10
y = 20
z = x + y
if z > 25:
    print("High value")
"""

vm_instructions = converter.convert_code(source_code)
print("VM Instructions:")
for instr in vm_instructions:
    print(f"  {instr}")
```

---

## 🚀 Deployment Strategies

### **Automated Build System**

#### **1. Build Script**

```bash
#!/bin/bash
# build_product.sh

set -e

echo "🚀 Building Tibia Bypass Product..."

# Configuration
PRODUCT_NAME="TibiaEliteBypass"
VERSION="1.0.0"
BUILD_DIR="build"
DIST_DIR="dist"

# Clean previous builds
rm -rf $BUILD_DIR $DIST_DIR
mkdir -p $BUILD_DIR $DIST_DIR

echo "📦 Step 1: Compiling source code..."

# Compile with optimization and stripping
gcc -O3 -s -fvisibility=hidden \
    -DNDEBUG \
    -DTIBIA_BYPASS_VERSION=\"$VERSION\" \
    -o $BUILD_DIR/$PRODUCT_NAME \
    src/*.c \
    -lz -lm

echo "🔒 Step 2: Applying obfuscation..."

# Apply obfuscation
python3 tools/obfuscator.py $BUILD_DIR/$PRODUCT_NAME

echo "📦 Step 3: Packing binary..."

# Pack with UPX
upx --best --ultra-brute $BUILD_DIR/$PRODUCT_NAME

echo "🛡️ Step 4: Adding anti-debug protection..."

# Inject anti-debug code
python3 tools/inject_protection.py $BUILD_DIR/$PRODUCT_NAME

echo "🔐 Step 5: Encrypting strings..."

# Encrypt sensitive strings
python3 tools/string_encryptor.py $BUILD_DIR/$PRODUCT_NAME

echo "📋 Step 6: Creating installer..."

# Create installer
python3 tools/create_installer.py \
    --input $BUILD_DIR/$PRODUCT_NAME \
    --output $DIST_DIR/${PRODUCT_NAME}_${VERSION}.run \
    --version $VERSION

echo "✅ Build completed successfully!"
echo "📁 Output: $DIST_DIR/${PRODUCT_NAME}_${VERSION}.run"
```

#### **2. Installer Generator**

```python
# create_installer.py
#!/usr/bin/env python3

import argparse
import os
import stat
import tarfile
import tempfile
import zlib
import base64

class InstallerGenerator:
    def __init__(self, input_file, output_file, version):
        self.input_file = input_file
        self.output_file = output_file
        self.version = version
        
    def create_installer(self):
        """Create self-extracting installer"""
        
        # Read binary data
        with open(self.input_file, 'rb') as f:
            binary_data = f.read()
        
        # Compress binary
        compressed_data = zlib.compress(binary_data, 9)
        encoded_data = base64.b64encode(compressed_data).decode('ascii')
        
        # Create installer script
        installer_script = f'''#!/bin/bash
# Tibia Elite Bypass Installer v{self.version}
# Auto-generated installer

set -e

echo "🚀 Installing Tibia Elite Bypass v{self.version}..."

# Check system requirements
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This installer is for Linux only"
    exit 1
fi

# Check for root privileges
if [[ $EUID -ne 0 ]]; then
    echo "❌ Error: This installer requires root privileges"
    exit 1
fi

# Create installation directory
INSTALL_DIR="/opt/tibia_elite_bypass"
mkdir -p $INSTALL_DIR

# Extract binary
echo "📦 Extracting files..."
BINARY_DATA="{encoded_data}"
echo $BINARY_DATA | base64 -d | gunzip > $INSTALL_DIR/tibia_bypass
chmod +x $INSTALL_DIR/tibia_bypass

# Create desktop shortcut
cat > /usr/share/applications/tibia-elite-bypass.desktop << EOF
[Desktop Entry]
Name=Tibia Elite Bypass
Comment=Advanced Tibia Anti-Cheat Bypass
Exec=$INSTALL_DIR/tibia_bypass
Icon=game
Terminal=true
Type=Application
Categories=Game;
EOF

# Create systemd service
cat > /etc/systemd/system/tibia-elite-bypass.service << EOF
[Unit]
Description=Tibia Elite Bypass Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=$INSTALL_DIR/tibia_bypass
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable service
systemctl daemon-reload
systemctl enable tibia-elite-bypass.service

echo "✅ Installation completed successfully!"
echo "🎮 You can now run: tibia_bypass"
echo "🔧 Service will start automatically on boot"
'''
        
        # Write installer
        with open(self.output_file, 'w') as f:
            f.write(installer_script)
        
        # Make installer executable
        os.chmod(self.output_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        
        print(f"✅ Installer created: {self.output_file}")

def main():
    parser = argparse.ArgumentParser(description='Create Tibia Bypass Installer')
    parser.add_argument('--input', required=True, help='Input binary file')
    parser.add_argument('--output', required=True, help='Output installer file')
    parser.add_argument('--version', required=True, help='Product version')
    
    args = parser.parse_args()
    
    generator = InstallerGenerator(args.input, args.output, args.version)
    generator.create_installer()

if __name__ == '__main__':
    main()
```

---

## 🔑 License Management

### **License System**

#### **1. License Generator**

```python
# license_generator.py
#!/usr/bin/env python3

import hashlib
import hmac
import json
import time
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class LicenseGenerator:
    def __init__(self, secret_key):
        self.secret_key = secret_key.encode()
        
    def generate_license(self, customer_id, features, expiry_days=365):
        """Generate a license for a customer"""
        
        # Create license data
        license_data = {
            'customer_id': customer_id,
            'features': features,
            'created_at': int(time.time()),
            'expires_at': int(time.time() + (expiry_days * 24 * 60 * 60)),
            'license_id': str(uuid.uuid4()),
            'version': '1.0.0'
        }
        
        # Create signature
        data_string = json.dumps(license_data, sort_keys=True)
        signature = hmac.new(
            self.secret_key,
            data_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Add signature to license
        license_data['signature'] = signature
        
        # Encrypt license
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'tibia_bypass_salt',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key))
        fernet = Fernet(key)
        
        encrypted_license = fernet.encrypt(json.dumps(license_data).encode())
        
        return base64.b64encode(encrypted_license).decode()
    
    def verify_license(self, encrypted_license):
        """Verify a license"""
        try:
            # Decrypt license
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'tibia_bypass_salt',
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.secret_key))
            fernet = Fernet(key)
            
            decrypted_data = fernet.decrypt(base64.b64decode(encrypted_license))
            license_data = json.loads(decrypted_data.decode())
            
            # Verify signature
            data_copy = license_data.copy()
            signature = data_copy.pop('signature')
            data_string = json.dumps(data_copy, sort_keys=True)
            
            expected_signature = hmac.new(
                self.secret_key,
                data_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_signature:
                return False, "Invalid signature"
            
            # Check expiration
            if time.time() > license_data['expires_at']:
                return False, "License expired"
            
            return True, license_data
            
        except Exception as e:
            return False, f"License verification failed: {str(e)}"

# Usage
if __name__ == '__main__':
    generator = LicenseGenerator("your-secret-key-here")
    
    # Generate license
    license_key = generator.generate_license(
        customer_id="CUST001",
        features=["bypass", "screenshot", "memory_reading"],
        expiry_days=365
    )
    
    print(f"Generated License: {license_key}")
    
    # Verify license
    is_valid, data = generator.verify_license(license_key)
    if is_valid:
        print(f"License valid for customer: {data['customer_id']}")
    else:
        print(f"License invalid: {data}")
```

#### **2. License Checker in Binary**

```c
// license_checker.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <openssl/hmac.h>
#include <openssl/sha.h>
#include <openssl/aes.h>

// License verification function
int verify_license(const char *license_key) {
    // This would be integrated into the main binary
    // Implementation depends on the license format
    
    // Check if license file exists
    FILE *license_file = fopen("/opt/tibia_elite_bypass/license.key", "r");
    if (!license_file) {
        return 0;
    }
    
    char stored_license[1024];
    fgets(stored_license, sizeof(stored_license), license_file);
    fclose(license_file);
    
    // Remove newline
    stored_license[strcspn(stored_license, "\n")] = 0;
    
    // Verify license (simplified)
    if (strcmp(stored_license, license_key) == 0) {
        return 1;
    }
    
    return 0;
}

// Check license on startup
void check_license_on_startup(void) {
    const char *license_key = getenv("TIBIA_BYPASS_LICENSE");
    if (!license_key) {
        printf("❌ License key not found. Please set TIBIA_BYPASS_LICENSE environment variable.\n");
        exit(1);
    }
    
    if (!verify_license(license_key)) {
        printf("❌ Invalid or expired license key.\n");
        exit(1);
    }
    
    printf("✅ License verified successfully!\n");
}
```

---

## 📦 Complete Deployment Package

### **Final Product Structure**

```
TibiaEliteBypass/
├── bin/
│   └── tibia_bypass (obfuscated, packed binary)
├── lib/
│   ├── libbypass.so (obfuscated library)
│   └── libprotection.so (anti-debug library)
├── config/
│   ├── bypass.conf (encrypted configuration)
│   └── license.key (encrypted license)
├── scripts/
│   ├── install.sh (installer script)
│   ├── uninstall.sh (cleanup script)
│   └── update.sh (update script)
├── docs/
│   ├── README.md (user documentation)
│   └── CHANGELOG.md (version history)
└── tools/
    ├── license_manager.py (license management)
    └── config_editor.py (configuration tool)
```

### **Deployment Checklist**

- [ ] **Code obfuscation** applied
- [ ] **Binary packing** completed
- [ ] **Anti-debug protection** installed
- [ ] **String encryption** applied
- [ ] **License system** integrated
- [ ] **Installer** created
- [ ] **Documentation** prepared
- [ ] **Testing** completed
- [ ] **Distribution** package ready

---

*This document provides comprehensive strategies for protecting intellectual property when deploying bypass solutions as commercial products.* 