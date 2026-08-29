"""
Build script to package the SDK for PyPI distribution
"""

import os
import shutil
import subprocess
from pathlib import Path

def build_pypi_package():
    sdk_dir = Path(__file__).parent
    os.chdir(sdk_dir)

    print("=" * 60)
    print(" 📦 BUILDING GOOGLE SERP EXTRACTOR PYPI PACKAGE")
    print("=" * 60)

    # Clean old build artifacts
    for folder in ["build", "dist", "google_serp_extractor.egg-info"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Removed old directory: {folder}")

    # Build sdist and wheel
    print("\n[Step 1] Building source distribution and wheel binary...")
    subprocess.run(["python3", "setup.py", "sdist", "bdist_wheel"], check=True)

    dist_files = list(Path("dist").glob("*"))
    print("\n✓ Build Successful! Generated distribution files:")
    for f in dist_files:
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

    print("\n" + "=" * 60)
    print(" 🚀 READY TO UPLOAD TO PYPI!")
    print(" Run command: twine upload dist/*")
    print("=" * 60)

if __name__ == "__main__":
    build_pypi_package()
