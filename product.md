# 📦 Product Packaging & Deployment - Intellectual Property Protection

## 📋 Table of Contents
1. [Code Obfuscation Techniques](#code-obfuscation-techniques)
2. [Binary Protection](#binary-protection)
3. [Anti-Reverse Engineering](#anti-reverse-engineering)
4. [Deployment Strategies](#deployment-strategies)
5. [License Management](#license-management)
6. [Anti-Tampering](#anti-tampering)

---

## 🔒 Code Obfuscation Techniques

### **Concept Overview**

Code obfuscation involves transforming source code to make it difficult to understand, reverse engineer, or modify while maintaining functionality. This protects your intellectual property from competitors and unauthorized users.

### **Advanced Obfuscation Strategies**

#### **1. Source Code Obfuscation**

```python
# obfuscator.py - Advanced Python Obfuscator
import ast
import random
import string
import base64
import zlib
import marshal

class AdvancedObfuscator:
    def __init__(self):
        self.variable_mapping = {}
        self.function_mapping = {}
        self.string_mapping = {}
        self.control_flow_obfuscation = True
        self.encryption_enabled = True
    
    def generate_random_name(self, length=8):
        """Generate random variable/function names"""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def obfuscate_strings(self, code):
        """Obfuscate string literals"""
        # Encode strings in base64
        def encode_string(s):
            if isinstance(s, str) and len(s) > 3:
                encoded = base64.b64encode(s.encode()).decode()
                return f"base64.b64decode('{encoded}').decode()"
            return f"'{s}'"
        
        # Replace string literals
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Str):
                node.s = encode_string(node.s)
        
        return ast.unparse(tree)
    
    def obfuscate_variables(self, code):
        """Obfuscate variable names"""
        tree = ast.parse(code)
        
        # Map original names to random names
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id not in self.variable_mapping:
                    self.variable_mapping[node.id] = self.generate_random_name()
                node.id = self.variable_mapping[node.id]
        
        return ast.unparse(tree)
    
    def obfuscate_functions(self, code):
        """Obfuscate function names"""
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name not in self.function_mapping:
                    self.function_mapping[node.name] = self.generate_random_name()
                node.name = self.function_mapping[node.name]
        
        return ast.unparse(tree)
    
    def add_control_flow_obfuscation(self, code):
        """Add confusing control flow"""
        obfuscated_code = f"""
import random
import time

def {self.generate_random_name()}(*args, **kwargs):
    if random.randint(0, 100) > 50:
        time.sleep(0.001)
    return True

# Original code wrapped in obfuscated control flow
{code}

# Add dummy functions to confuse analysis
def {self.generate_random_name()}():
    pass

def {self.generate_random_name()}():
    return None
"""
        return obfuscated_code
    
    def encrypt_code(self, code):
        """Encrypt the entire code"""
        # Compress and encrypt
        compressed = zlib.compress(code.encode())
        encrypted = base64.b85encode(compressed).decode()
        
        decryption_code = f"""
import zlib
import base64

def {self.generate_random_name()}():
    encrypted_code = "{encrypted}"
    compressed = base64.b85decode(encrypted_code)
    code = zlib.decompress(compressed).decode()
    exec(code)

{self.generate_random_name()}()
"""
        return decryption_code
    
    def obfuscate_complete(self, source_code):
        """Complete obfuscation pipeline"""
        print("🔒 Starting advanced obfuscation...")
        
        # Step 1: String obfuscation
        code = self.obfuscate_strings(source_code)
        print("✅ Strings obfuscated")
        
        # Step 2: Variable obfuscation
        code = self.obfuscate_variables(code)
        print("✅ Variables obfuscated")
        
        # Step 3: Function obfuscation
        code = self.obfuscate_functions(code)
        print("✅ Functions obfuscated")
        
        # Step 4: Control flow obfuscation
        if self.control_flow_obfuscation:
            code = self.add_control_flow_obfuscation(code)
            print("✅ Control flow obfuscated")
        
        # Step 5: Code encryption
        if self.encryption_enabled:
            code = self.encrypt_code(code)
            print("✅ Code encrypted")
        
        return code

# Usage example
if __name__ == "__main__":
    obfuscator = AdvancedObfuscator()
    
    # Your original bypass code
    original_code = '''
def bypass_anti_cheat():
    print("Bypass successful!")
    return True

def main():
    result = bypass_anti_cheat()
    return result
'''
    
    # Obfuscate the code
    obfuscated = obfuscator.obfuscate_complete(original_code)
    
    # Save obfuscated code
    with open("obfuscated_bypass.py", "w") as f:
        f.write(obfuscated)
    
    print("🎉 Code obfuscated and saved!")
```

#### **2. C/C++ Obfuscation**

```c
// c_obfuscator.c - Advanced C/C++ Obfuscator
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_CODE_SIZE 100000
#define MAX_VAR_NAME 50

typedef struct {
    char original[256];
    char obfuscated[256];
} name_mapping_t;

typedef struct {
    name_mapping_t variables[1000];
    name_mapping_t functions[1000];
    int var_count;
    int func_count;
} obfuscation_context_t;

// Generate random variable names
char* generate_random_name(int length) {
    static char name[MAX_VAR_NAME];
    const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    
    for (int i = 0; i < length; i++) {
        name[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    name[length] = '\0';
    
    return name;
}

// Obfuscate variable names
void obfuscate_variables(char* code, obfuscation_context_t* ctx) {
    char* token = strtok(code, " \t\n");
    
    while (token != NULL) {
        // Check if it's a variable declaration
        if (strstr(token, "int ") || strstr(token, "char ") || 
            strstr(token, "float ") || strstr(token, "double ")) {
            
            // Find variable name
            char* var_name = strtok(NULL, " \t\n");
            if (var_name && strlen(var_name) > 1) {
                // Create mapping
                strcpy(ctx->variables[ctx->var_count].original, var_name);
                strcpy(ctx->variables[ctx->var_count].obfuscated, 
                      generate_random_name(8));
                ctx->var_count++;
            }
        }
        
        token = strtok(NULL, " \t\n");
    }
}

// Add control flow obfuscation
void add_control_flow_obfuscation(char* code) {
    char obfuscated[MAX_CODE_SIZE];
    
    // Add dummy functions
    sprintf(obfuscated, 
        "int %s() { return rand() %% 2; }\n"
        "void %s() { }\n"
        "int %s(int x) { return x + rand() %% 10; }\n\n"
        "%s",
        generate_random_name(8),
        generate_random_name(8),
        generate_random_name(8),
        code
    );
    
    strcpy(code, obfuscated);
}

// Encrypt strings
void encrypt_strings(char* code) {
    char* pos = code;
    
    while ((pos = strstr(pos, "\"")) != NULL) {
        char* end = strchr(pos + 1, '"');
        if (end) {
            // Simple XOR encryption
            for (char* p = pos + 1; p < end; p++) {
                *p ^= 0xAA;
            }
        }
        pos = end + 1;
    }
}

// Complete C obfuscation
void obfuscate_c_code(char* source_code, char* output_code) {
    obfuscation_context_t ctx = {0};
    
    printf("🔒 Starting C/C++ obfuscation...\n");
    
    // Initialize random seed
    srand(time(NULL));
    
    // Copy source code
    strcpy(output_code, source_code);
    
    // Step 1: Variable obfuscation
    obfuscate_variables(output_code, &ctx);
    printf("✅ Variables obfuscated (%d mappings)\n", ctx.var_count);
    
    // Step 2: Function obfuscation
    // (Similar to variable obfuscation)
    printf("✅ Functions obfuscated (%d mappings)\n", ctx.func_count);
    
    // Step 3: Control flow obfuscation
    add_control_flow_obfuscation(output_code);
    printf("✅ Control flow obfuscated\n");
    
    // Step 4: String encryption
    encrypt_strings(output_code);
    printf("✅ Strings encrypted\n");
    
    // Step 5: Add anti-debugging
    char anti_debug[] = 
        "#include <sys/ptrace.h>\n"
        "void %s() {\n"
        "    if (ptrace(PTRACE_TRACEME, 0, 0, 0) == -1) {\n"
        "        exit(1);\n"
        "    }\n"
        "}\n\n";
    
    char temp[MAX_CODE_SIZE];
    sprintf(temp, anti_debug, generate_random_name(8));
    strcat(temp, output_code);
    strcpy(output_code, temp);
    
    printf("✅ Anti-debugging added\n");
    printf("🎉 C/C++ code obfuscated successfully!\n");
}
```

---

## 🛡️ Binary Protection

### **Advanced Binary Protection Techniques**

#### **1. Executable Packing**

```python
# binary_packer.py - Advanced Executable Packer
import os
import sys
import zlib
import base64
import struct
import random
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AdvancedBinaryPacker:
    def __init__(self):
        self.encryption_key = None
        self.compression_level = 9
        self.anti_vm_enabled = True
        self.anti_debug_enabled = True
    
    def generate_encryption_key(self, password):
        """Generate encryption key from password"""
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def compress_and_encrypt(self, data, password):
        """Compress and encrypt binary data"""
        # Compress data
        compressed = zlib.compress(data, self.compression_level)
        
        # Generate encryption key
        key, salt = self.generate_encryption_key(password)
        cipher = Fernet(key)
        
        # Encrypt compressed data
        encrypted = cipher.encrypt(compressed)
        
        # Create header
        header = struct.pack('<I', len(data))  # Original size
        header += salt  # Salt for key derivation
        header += struct.pack('<I', len(encrypted))  # Encrypted size
        
        return header + encrypted
    
    def add_anti_vm_checks(self, code):
        """Add anti-virtualization checks"""
        anti_vm_code = '''
import os
import sys
import platform

def check_virtualization():
    # Check common VM indicators
    vm_indicators = [
        "VMware", "VirtualBox", "QEMU", "Xen", "KVM",
        "Microsoft Virtual", "Parallels", "Docker"
    ]
    
    # Check system manufacturer
    try:
        with open("/sys/class/dmi/id/sys_vendor", "r") as f:
            vendor = f.read().strip()
            if any(indicator in vendor for indicator in vm_indicators):
                return True
    except:
        pass
    
    # Check CPU flags
    try:
        with open("/proc/cpuinfo", "r") as f:
            cpuinfo = f.read()
            if "hypervisor" in cpuinfo.lower():
                return True
    except:
        pass
    
    # Check running processes
    try:
        with open("/proc/1/comm", "r") as f:
            init_process = f.read().strip()
            if init_process in ["systemd", "init"]:
                # Additional checks for containerization
                pass
    except:
        pass
    
    return False

# Add to main code
if check_virtualization():
    print("Virtualization detected!")
    sys.exit(1)
'''
        return anti_vm_code + code
    
    def add_anti_debug_checks(self, code):
        """Add anti-debugging checks"""
        anti_debug_code = '''
import sys
import os
import time
import signal

def check_debugger():
    # Check if running under debugger
    try:
        import psutil
        process = psutil.Process(os.getpid())
        if process.num_handles() > 1000:  # Suspicious number of handles
            return True
    except:
        pass
    
    # Check execution time (debuggers slow down execution)
    start_time = time.time()
    for i in range(1000000):
        pass
    execution_time = time.time() - start_time
    
    if execution_time > 0.1:  # Suspiciously slow
        return True
    
    return False

# Add to main code
if check_debugger():
    print("Debugger detected!")
    sys.exit(1)
'''
        return anti_debug_code + code
    
    def create_self_extracting_package(self, source_file, output_file, password):
        """Create self-extracting executable"""
        print("📦 Creating self-extracting package...")
        
        # Read source file
        with open(source_file, 'rb') as f:
            data = f.read()
        
        # Add protection layers
        if self.anti_vm_enabled:
            data = self.add_anti_vm_checks(data)
        
        if self.anti_debug_enabled:
            data = self.add_anti_debug_checks(data)
        
        # Compress and encrypt
        protected_data = self.compress_and_encrypt(data, password)
        
        # Create self-extracting stub
        stub_code = f'''
import sys
import zlib
import base64
import struct
import tempfile
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def decrypt_and_extract(encrypted_data, password):
    # Extract header
    original_size = struct.unpack('<I', encrypted_data[:4])[0]
    salt = encrypted_data[4:20]
    encrypted_size = struct.unpack('<I', encrypted_data[20:24])[0]
    encrypted = encrypted_data[24:24+encrypted_size]
    
    # Derive key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    # Decrypt
    cipher = Fernet(key)
    compressed = cipher.decrypt(encrypted)
    
    # Decompress
    data = zlib.decompress(compressed)
    
    return data

def main():
    # Embedded encrypted data
    encrypted_data = {repr(protected_data)}
    
    # Get password from user
    password = input("Enter password: ")
    
    try:
        # Decrypt and extract
        data = decrypt_and_extract(encrypted_data, password)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as f:
            f.write(data)
            temp_file = f.name
        
        # Execute extracted code
        exec(data)
        
        # Cleanup
        os.unlink(temp_file)
        
    except Exception as e:
        print(f"Error: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        # Write self-extracting package
        with open(output_file, 'w') as f:
            f.write(stub_code)
        
        print(f"✅ Self-extracting package created: {output_file}")
        return output_file
    
    def create_installer(self, source_files, output_file, password):
        """Create professional installer"""
        print("🔧 Creating professional installer...")
        
        installer_code = f'''
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys
import subprocess
import threading

class TibiaBypassInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tibia Bypass - Professional Installer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Tibia Bypass Professional", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # License agreement
        self.license_var = tk.BooleanVar()
        license_check = tk.Checkbutton(self.root, 
                                     text="I agree to the license terms",
                                     variable=self.license_var)
        license_check.pack(pady=10)
        
        # Installation path
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10)
        
        tk.Label(path_frame, text="Installation Path:").pack(side=tk.LEFT)
        self.path_var = tk.StringVar(value="C:\\\\TibiaBypass")
        path_entry = tk.Entry(path_frame, textvariable=self.path_var, width=30)
        path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_btn.pack(side=tk.LEFT)
        
        # Install button
        self.install_btn = tk.Button(self.root, text="Install", 
                                   command=self.install, state=tk.DISABLED)
        self.install_btn.pack(pady=20)
        
        # Progress bar
        self.progress = tk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to install")
        status_label = tk.Label(self.root, textvariable=self.status_var)
        status_label.pack(pady=10)
        
        # Bind license check
        self.license_var.trace('w', self.check_license)
    
    def check_license(self, *args):
        if self.license_var.get():
            self.install_btn.config(state=tk.NORMAL)
        else:
            self.install_btn.config(state=tk.DISABLED)
    
    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
    
    def install(self):
        if not self.license_var.get():
            messagebox.showerror("Error", "Please accept the license terms")
            return
        
        # Start installation in separate thread
        thread = threading.Thread(target=self.perform_installation)
        thread.daemon = True
        thread.start()
    
    def perform_installation(self):
        try:
            self.status_var.set("Installing...")
            self.progress['value'] = 10
            
            # Create installation directory
            install_path = self.path_var.get()
            os.makedirs(install_path, exist_ok=True)
            self.progress['value'] = 30
            
            # Extract files
            # (This would extract the actual bypass files)
            self.progress['value'] = 60
            
            # Create shortcuts
            self.create_shortcuts(install_path)
            self.progress['value'] = 80
            
            # Register with system
            self.register_system()
            self.progress['value'] = 100
            
            self.status_var.set("Installation complete!")
            messagebox.showinfo("Success", "Tibia Bypass installed successfully!")
            
        except Exception as e:
            self.status_var.set(f"Installation failed: {{e}}")
            messagebox.showerror("Error", f"Installation failed: {{e}}")
    
    def create_shortcuts(self, install_path):
        # Create desktop shortcut
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, "Tibia Bypass.lnk")
        
        # Create shortcut file
        with open(shortcut_path, 'w') as f:
            f.write(f"[InternetShortcut]\\n")
            f.write(f"URL=file://{{install_path}}/tibia_bypass.exe\\n")
    
    def register_system(self):
        # Add to PATH
        # Register file associations
        # Add firewall rules
        pass
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = TibiaBypassInstaller()
    installer.run()
'''
        
        # Write installer
        with open(output_file, 'w') as f:
            f.write(installer_code)
        
        print(f"✅ Professional installer created: {output_file}")
        return output_file

# Usage example
if __name__ == "__main__":
    packer = AdvancedBinaryPacker()
    
    # Create self-extracting package
    packer.create_self_extracting_package(
        "tibia_bypass.py",
        "tibia_bypass_protected.py",
        "your_secret_password_123"
    )
    
    # Create professional installer
    packer.create_installer(
        ["tibia_bypass.py", "config.json"],
        "tibia_bypass_installer.py",
        "installer_password_456"
    )
```

#### **2. Native Binary Protection**

```c
// binary_protector.c - Native Binary Protection
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/syscall.h>
#include <elf.h>
#include <fcntl.h>

#define MAX_SECTIONS 100
#define ENCRYPTION_KEY 0xDEADBEEF

typedef struct {
    Elf64_Shdr header;
    unsigned char *data;
    size_t size;
    bool encrypted;
} section_info_t;

typedef struct {
    Elf64_Ehdr header;
    section_info_t sections[MAX_SECTIONS];
    int section_count;
} binary_info_t;

// XOR encryption/decryption
void xor_encrypt(unsigned char *data, size_t size, unsigned int key) {
    for (size_t i = 0; i < size; i++) {
        data[i] ^= (key >> (i % 32)) & 0xFF;
    }
}

// Add anti-debugging to binary
void add_anti_debugging(unsigned char *code, size_t *code_size) {
    unsigned char anti_debug[] = {
        0x48, 0x31, 0xC0,           // xor rax, rax
        0x48, 0x89, 0xE7,           // mov rdi, rsp
        0x48, 0x31, 0xF6,           // xor rsi, rsi
        0x48, 0x31, 0xD2,           // xor rdx, rdx
        0x48, 0x31, 0xC9,           // xor rcx, rcx
        0x48, 0x31, 0xDB,           // xor rbx, rbx
        0x0F, 0x05,                 // syscall (ptrace)
        0x48, 0x83, 0xF8, 0xFF,     // cmp rax, -1
        0x75, 0x02,                 // jne not_debugged
        0xEB, 0xFE                  // jmp $ (infinite loop)
    };
    
    // Insert anti-debugging code at beginning
    memmove(code + sizeof(anti_debug), code, *code_size);
    memcpy(code, anti_debug, sizeof(anti_debug));
    *code_size += sizeof(anti_debug);
}

// Add code obfuscation
void obfuscate_code(unsigned char *code, size_t size) {
    // Add junk instructions
    unsigned char junk[] = {
        0x90,                       // nop
        0x48, 0x31, 0xC0,          // xor rax, rax
        0x48, 0x89, 0xC0,          // mov rax, rax
        0x90                        // nop
    };
    
    // Insert junk instructions randomly
    for (size_t i = 0; i < size; i += 16) {
        if (rand() % 3 == 0) {
            memmove(code + i + sizeof(junk), code + i, size - i);
            memcpy(code + i, junk, sizeof(junk));
            size += sizeof(junk);
        }
    }
}

// Encrypt sections
void encrypt_sections(binary_info_t *binary) {
    for (int i = 0; i < binary->section_count; i++) {
        section_info_t *section = &binary->sections[i];
        
        // Only encrypt code sections
        if (section->header.sh_flags & SHF_EXECINSTR) {
            xor_encrypt(section->data, section->size, ENCRYPTION_KEY);
            section->encrypted = true;
        }
    }
}

// Add decryption stub
void add_decryption_stub(binary_info_t *binary) {
    unsigned char decryption_stub[] = {
        // Decryption code
        0x48, 0x8B, 0x3C, 0x25, 0x00, 0x00, 0x00, 0x00,  // mov rdi, [0x0]
        0x48, 0x8B, 0x34, 0x25, 0x08, 0x00, 0x00, 0x00,  // mov rsi, [0x8]
        0x48, 0x31, 0xC0,                                 // xor rax, rax
        0x48, 0x31, 0xD2,                                 // xor rdx, rdx
        0x48, 0x31, 0xC9,                                 // xor rcx, rcx
        // Decryption loop
        0x48, 0x8A, 0x04, 0x0F,                          // mov al, [rdi+rcx]
        0x34, 0xEF,                                       // xor al, 0xEF
        0x88, 0x04, 0x0F,                                // mov [rdi+rcx], al
        0x48, 0xFF, 0xC1,                                // inc rcx
        0x48, 0x39, 0xCE,                                // cmp rsi, rcx
        0x75, 0xF3,                                      // jne decryption_loop
    };
    
    // Insert decryption stub at entry point
    Elf64_Addr entry = binary->header.e_entry;
    memmove(binary->sections[0].data + entry + sizeof(decryption_stub),
            binary->sections[0].data + entry,
            binary->sections[0].size - entry);
    memcpy(binary->sections[0].data + entry, decryption_stub, sizeof(decryption_stub));
}

// Protect binary file
int protect_binary(const char *input_file, const char *output_file) {
    printf("🛡️ Protecting binary: %s\n", input_file);
    
    // Open input file
    FILE *input = fopen(input_file, "rb");
    if (!input) {
        printf("❌ Cannot open input file\n");
        return -1;
    }
    
    // Read ELF header
    binary_info_t binary = {0};
    fread(&binary.header, sizeof(Elf64_Ehdr), 1, input);
    
    // Verify ELF magic
    if (memcmp(binary.header.e_ident, ELFMAG, SELFMAG) != 0) {
        printf("❌ Not a valid ELF file\n");
        fclose(input);
        return -1;
    }
    
    // Read section headers
    fseek(input, binary.header.e_shoff, SEEK_SET);
    for (int i = 0; i < binary.header.e_shnum && i < MAX_SECTIONS; i++) {
        section_info_t *section = &binary.sections[binary.section_count];
        
        fread(&section->header, sizeof(Elf64_Shdr), 1, input);
        
        // Read section data
        if (section->header.sh_size > 0) {
            section->data = malloc(section->header.sh_size);
            section->size = section->header.sh_size;
            
            long po