from setuptools import setup, find_packages

setup(
    name="quantum-devops-toolchain",
    version="1.0.0",
    author="Quantum DevOps Team",
    author_email="quantum-devops@example.com",
    description="A comprehensive toolchain for quantum computing DevOps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/quantum-devops/quantum-devops-toolchain",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "qiskit>=0.45.0",
        "cirq>=1.2.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
)