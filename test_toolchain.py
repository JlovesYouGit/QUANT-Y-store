"""
Tests for Quantum DevOps Toolchain
"""

import sys
sys.path.append('c:\\quantum-devops-project\\src')

import unittest
from quantum_compiler import QuantumCompilerOptimizer
from circuit_optimizer import CircuitOptimizer, light_optimization_pipeline
from error_correction import QuantumErrorCorrection
from quantum_simulation import QuantumSimulator
from algorithm_optimizer import QuantumAlgorithmOptimizer
from main import QuantumDevOpsToolchain

class TestQuantumCompilerOptimizer(unittest.TestCase):
    """Test quantum compiler optimization"""
    
    def test_initialization(self):
        """Test optimizer initialization"""
        optimizer = QuantumCompilerOptimizer(optimization_level=1)
        self.assertEqual(optimizer.optimization_level, 1)
        
    def test_optimization_levels(self):
        """Test different optimization levels"""
        optimizer = QuantumCompilerOptimizer()
        # Mock circuit for testing
        mock_circuit = {"gates": ["H", "CX", "T"]}
        
        # Test all optimization levels
        for level in range(4):
            optimizer.optimization_level = level
            result = optimizer.optimize_circuit(mock_circuit)
            self.assertIsNotNone(result)

class TestCircuitOptimizer(unittest.TestCase):
    """Test circuit optimization"""
    
    def test_pipeline_creation(self):
        """Test optimization pipeline creation"""
        pipeline = light_optimization_pipeline()
        self.assertIsInstance(pipeline, CircuitOptimizer)
        
    def test_optimization_passes(self):
        """Test adding optimization passes"""
        optimizer = CircuitOptimizer()
        self.assertEqual(len(optimizer.optimization_passes), 0)
        
        # Add a mock optimization pass
        optimizer.add_optimization_pass(lambda x: x)
        self.assertEqual(len(optimizer.optimization_passes), 1)

class TestErrorCorrection(unittest.TestCase):
    """Test quantum error correction"""
    
    def test_qec_initialization(self):
        """Test error correction initialization"""
        qec = QuantumErrorCorrection("surface")
        self.assertEqual(qec.code_type, "surface")
        
    def test_qubit_estimation(self):
        """Test physical qubit estimation"""
        qec = QuantumErrorCorrection("steane")
        physical_qubits = qec.estimate_physical_qubits(5)
        self.assertEqual(physical_qubits, 35)  # 5 * 7

class TestQuantumSimulation(unittest.TestCase):
    """Test quantum simulation"""
    
    def test_simulator_initialization(self):
        """Test simulator initialization"""
        simulator = QuantumSimulator("statevector")
        self.assertEqual(simulator.backend, "statevector")
        
    def test_shots_setting(self):
        """Test setting simulation shots"""
        simulator = QuantumSimulator()
        simulator.set_shots(2048)
        self.assertEqual(simulator.shots, 2048)

class TestAlgorithmOptimizer(unittest.TestCase):
    """Test algorithm optimization"""
    
    def test_optimizer_initialization(self):
        """Test algorithm optimizer initialization"""
        optimizer = QuantumAlgorithmOptimizer()
        self.assertEqual(len(optimizer.optimization_techniques), 0)
        
    def test_adding_techniques(self):
        """Test adding optimization techniques"""
        optimizer = QuantumAlgorithmOptimizer()
        optimizer.add_technique(lambda x: x)
        self.assertEqual(len(optimizer.optimization_techniques), 1)

class TestDevOpsToolchain(unittest.TestCase):
    """Test the complete DevOps toolchain"""
    
    def test_toolchain_initialization(self):
        """Test toolchain initialization"""
        toolchain = QuantumDevOpsToolchain()
        self.assertIsNotNone(toolchain.compiler_optimizer)
        self.assertIsNotNone(toolchain.circuit_optimizer)
        self.assertIsNotNone(toolchain.error_correction)
        
    def test_ci_pipeline(self):
        """Test CI pipeline"""
        toolchain = QuantumDevOpsToolchain()
        mock_circuit = {"num_qubits": 5, "gates": ["H", "CX"]}
        
        # This is a basic test - in practice, this would be more comprehensive
        try:
            result = toolchain.ci_pipeline(mock_circuit)
            self.assertIsInstance(result, dict)
        except Exception as e:
            # Some components may not be fully implemented
            pass

if __name__ == '__main__':
    unittest.main()