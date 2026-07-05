"""
Main Quantum DevOps Toolchain Integration
Integrates all components of the quantum computing DevOps toolchain
"""

from .quantum_compiler import QuantumCompilerOptimizer
from .circuit_optimizer import CircuitOptimizer, light_optimization_pipeline, medium_optimization_pipeline, heavy_optimization_pipeline
from .error_correction import QuantumErrorCorrection, DevOpsIntegration as ErrorCorrectionDevOps
from .quantum_simulation import QuantumSimulator, SimulationDevOps
from .algorithm_optimizer import QuantumAlgorithmOptimizer, AlgorithmPerformanceAnalyzer
from .core.quantum_storage_manager import get_storage_manager

class QuantumDevOpsToolchain:
    """Main class for the quantum DevOps toolchain"""
    
    def __init__(self):
        # Initialize all components
        self.compiler_optimizer = QuantumCompilerOptimizer()
        self.circuit_optimizer = CircuitOptimizer()
        self.error_correction = ErrorCorrectionDevOps()
        self.simulation_devops = SimulationDevOps()
        self.algorithm_optimizer = QuantumAlgorithmOptimizer()
        self.performance_analyzer = AlgorithmPerformanceAnalyzer()
        self.storage_manager = get_storage_manager()  # Quantum storage manager
        
    def ci_pipeline(self, circuit, target_error_rate=0.01):
        """
        Complete CI pipeline for quantum circuits
        
        Args:
            circuit: Quantum circuit to validate
            target_error_rate (float): Target error rate threshold
            
        Returns:
            dict: CI pipeline results
        """
        results = {}
        
        # 1. Circuit optimization
        optimized_circuit = self.circuit_optimizer.optimize(circuit)
        results["optimization"] = {"completed": True}
        
        # 2. Error correction validation
        error_correction_results = self.error_correction.ci_pipeline_integration(
            optimized_circuit, target_error_rate)
        results["error_correction"] = error_correction_results
        
        # 3. Simulation testing
        simulation_results = self.simulation_devops.ci_testing_pipeline(optimized_circuit)
        results["simulation"] = simulation_results
        
        # 4. Performance analysis
        performance = self.performance_analyzer.analyze_complexity(optimized_circuit)
        results["performance"] = performance
        
        return results
        
    def cd_pipeline(self, circuit):
        """
        Complete CD pipeline for quantum circuits
        
        Args:
            circuit: Quantum circuit to deploy
            
        Returns:
            dict: CD pipeline configuration
        """
        # Apply heavy optimization for deployment
        self.compiler_optimizer.optimization_level = 3
        optimized_circuit = self.compiler_optimizer.optimize_circuit(circuit)
        
        # Get deployment configuration
        deployment_config = self.error_correction.cd_pipeline_integration(optimized_circuit)
        
        # Add simulation staging configuration
        staging_config = self.simulation_devops.staging_deployment(optimized_circuit)
        
        return {
            "deployment": deployment_config,
            "staging": staging_config,
            "optimized_circuit": optimized_circuit
        }
        
    def optimize_for_hardware(self, circuit, hardware_specs):
        """
        Optimize circuit for specific hardware specifications
        
        Args:
            circuit: Quantum circuit to optimize
            hardware_specs (dict): Hardware specifications
            
        Returns:
            Optimized circuit for the target hardware
        """
        # Select appropriate optimization level based on hardware
        if hardware_specs.get("quality") == "high":
            self.compiler_optimizer.optimization_level = 3
        elif hardware_specs.get("quality") == "medium":
            self.compiler_optimizer.optimization_level = 2
        else:
            self.compiler_optimizer.optimization_level = 1
            
        # Apply optimization
        optimized_circuit = self.compiler_optimizer.optimize_circuit(circuit)
        
        # Apply error correction if needed
        if hardware_specs.get("error_correction_required", False):
            optimized_circuit = self.error_correction.qec.apply_error_correction(optimized_circuit)
            
        return optimized_circuit

# Global instance for easy access
toolchain = QuantumDevOpsToolchain()

def get_toolchain():
    """Get the global toolchain instance"""
    return toolchain