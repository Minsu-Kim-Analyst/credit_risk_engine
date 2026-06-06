import importlib.metadata
import sys

# 1. Define your strict top-level dependencies
TARGET_PACKAGES = [
    "pandas",
    "numpy",
    "scikit-learn",
    "streamlit",
    "plotly",
    "python-dotenv",
    "psycopg2-binary"
]

def generate_requirements(packages, filename="requirements.txt"):
    print(f"Auditing local environment and generating {filename}...\n")
    
    with open(filename, "w") as file:
        file.write("# --- Automated Enterprise Requirements ---\n")
        
        for pkg in packages:
            try:
                # Fetch the exact version installed in the active environment
                version = importlib.metadata.version(pkg)
                line = f"{pkg}=={version}\n"
                
                file.write(line)
                print(f"✅ Locked: {line.strip()}")
                
            except importlib.metadata.PackageNotFoundError:
                print(f"❌ WARNING: '{pkg}' is not installed in this environment.")
                
    print(f"\nSuccess! {filename} has been updated with strict version pinning.")

if __name__ == "__main__":
    generate_requirements(TARGET_PACKAGES)
