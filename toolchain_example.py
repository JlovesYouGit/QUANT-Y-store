"""
Example usage of the Quantum DevOps Toolchain
"""

import sys
sys.path.append('c:\\quantum-devops-project\\src')

# Import our quantum DevOps components
from src.quantum_compiler import QuantumCompilerOptimizer, default_optimizer
from src.circuit_optimizer import light_optimization_pipeline, medium_optimization_pipeline, heavy_optimization_pipeline
from src.error_correction import surface_code_qec, steane_code_qec
from src.quantum_simulation import fast_simulator, accurate_simulator
from src.main import get_toolchain

def example_quantum_devops_workflow():
    """Example workflow demonstrating the quantum DevOps toolchain"""
    
    print("=== Quantum DevOps Toolchain Example ===")
    
    # 1. Create a mock quantum circuit (in practice, this would be a real circuit)
    mock_circuit = {
        "name": "example_quantum_circuit",
        "num_qubits": 5,
        "gates": ["H", "CX", "T", "H", "CX", "Tdg"],
        "measurements": [0, 1, 2]
    }
    
    print(f"Original circuit: {mock_circuit['name']} with {mock_circuit['num_qubits']} qubits")
    
    # 2. Use quantum compiler optimizer
    print("\n--- Compiler Optimization ---")
    compiler = QuantumCompilerOptimizer(optimization_level=2)
    optimized_circuit = compiler.optimize_circuit(mock_circuit)
    print(f"Applied optimization level {compiler.optimization_level}")
    
    # 3. Use circuit optimization pipelines
    print("\n--- Circuit Optimization ---")
    optimizer = medium_optimization_pipeline()
    further_optimized = optimizer.optimize(optimized_circuit)
    print("Applied medium optimization pipeline")
    
    # 4. Apply error correction
    print("\n--- Error Correction ---")
    physical_qubits = surface_code_qec.estimate_physical_qubits(further_optimized["num_qubits"])
    print(f"Logical qubits: {further_optimized['num_qubits']}")
    print(f"Physical qubits needed (surface code): {physical_qubits}")
    
    # 5. Simulation
    print("\n--- Quantum Simulation ---")
    simulator = accurate_simulator
    simulator.set_shots(2048)
    print(f"Using {simulator.backend} simulator with {simulator.shots} shots")
    
    # 6. DevOps integration
    print("\n--- DevOps Integration ---")
    toolchain = get_toolchain()
    print("Quantum DevOps toolchain initialized")
    
    # In a real CI/CD pipeline, we would run:
    # ci_results = toolchain.ci_pipeline(further_optimized)
    # cd_config = toolchain.cd_pipeline(further_optimized)
    
    print("\n=== Workflow Complete ===")
    print("The quantum DevOps toolchain is ready for integration into your CI/CD pipeline!")

if __name__ == "__main__":
    example_quantum_devops_workflow()