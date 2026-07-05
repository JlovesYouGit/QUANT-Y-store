"""
Tests for 3D Quantum Code Structure
"""

import sys
import os
sys.path.append('c:\\quantum-devops-project\\src')

import unittest
from src.core.code_structure_3d import QuantumCodeStructure3D

class TestQuantumCodeStructure3D(unittest.TestCase):
    """Test the 3D quantum code structure"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.structure = QuantumCodeStructure3D()
        
    def test_initialization(self):
        """Test structure initialization"""
        self.assertIsInstance(self.structure, QuantumCodeStructure3D)
        self.assertIsInstance(self.structure.code_space, dict)
        
    def test_register_component(self):
        """Test component registration"""
        # Register a test component
        self.structure.register_component("TestModule", "Python", 1, "test_component")
        
        # Verify it was registered
        component = self.structure.get_component("TestModule", "Python", 1)
        self.assertEqual(component, "test_component")
        
    def test_get_component(self):
        """Test component retrieval"""
        # Try to get a non-existent component
        component = self.structure.get_component("NonExistent", "Python", 1)
        self.assertIsNone(component)
        
    def test_get_optimal_component(self):
        """Test optimal component selection"""
        # Register test components
        self.structure.register_component("Optimization", "Rust", 0, "rust_optimizer")
        self.structure.register_component("Precision", "C#", 2, "csharp_engine")
        self.structure.register_component("StateRecovery", "Node", 1, "node_recovery")
        self.structure.register_component("Compiler", "Python", 1, "python_compiler")
        
        # Test performance-optimized selection
        perf_component = self.structure.get_optimal_component("Optimization", True, False)
        self.assertEqual(perf_component, "rust_optimizer")
        
        # Test precision-optimized selection
        prec_component = self.structure.get_optimal_component("Precision", False, True)
        self.assertEqual(prec_component, "csharp_engine")
        
        # Test state recovery selection
        recovery_component = self.structure.get_optimal_component("StateRecovery")
        self.assertEqual(recovery_component, "node_recovery")
        
        # Test general selection
        general_component = self.structure.get_optimal_component("Compiler")
        self.assertEqual(general_component, "python_compiler")

if __name__ == '__main__':
    unittest.main()