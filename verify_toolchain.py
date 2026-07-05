"""
Verification script for Quantum DevOps Toolchain
"""

def verify_toolchain():
    """Verify that all components of the toolchain can be imported"""
    
    try:
        # Test importing quantum compiler
        import sys
        sys.path.append('c:\\quantum-devops-project\\src')
        
        from quantum_compiler import QuantumCompilerOptimizer
        print("✓ Quantum compiler module imported successfully")
        
        # Test creating compiler optimizer
        optimizer = QuantumCompilerOptimizer()
        print("✓ QuantumCompilerOptimizer instantiated successfully")
        
        # Test importing circuit optimizer
        from circuit_optimizer import CircuitOptimizer
        print("✓ Circuit optimizer module imported successfully")
        
        # Test importing error correction
        from error_correction import QuantumErrorCorrection
        qec = QuantumErrorCorrection()
        print("✓ Error correction module imported successfully")
        
        # Test importing quantum simulation
        from quantum_simulation import QuantumSimulator
        simulator = QuantumSimulator()
        print("✓ Quantum simulation module imported successfully")
        
        # Test importing algorithm optimizer
        from algorithm_optimizer import QuantumAlgorithmOptimizer
        algo_optimizer = QuantumAlgorithmOptimizer()
        print("✓ Algorithm optimizer module imported successfully")
        
        # Test importing main toolchain
        from src.main import QuantumDevOpsToolchain
        toolchain = QuantumDevOpsToolchain()
        print("✓ Main toolchain module imported successfully")
        
        print("\n🎉 All components of the Quantum DevOps Toolchain verified successfully!")
        print("The toolchain is ready for use in your quantum DevOps workflows.")
        
    except Exception as e:
        print(f"❌ Error verifying toolchain: {e}")
        return False
        
    return True

if __name__ == "__main__":
    verify_toolchain()