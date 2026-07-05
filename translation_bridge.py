"""
Quantum Translation Bridge
Main integration module connecting classical computation with quantum hardware
"""

import sys
sys.path.append('c:\\quantum-devops-project')

from translation_layer import get_translator
from quantum_hardware import get_hardware_interface

class QuantumTranslationBridge:
    """Main bridge between classical computation and quantum hardware"""
    
    def __init__(self):
        self.translator = get_translator()
        self.hardware = get_hardware_interface()
        self.initialized = False
        
    def initialize_bridge(self, qubit_count: int = 8):
        """Initialize the quantum translation bridge"""
        print("Initializing Quantum Translation Bridge...")
        
        # Initialize quantum hardware
        self.hardware.initialize_qubits(qubit_count)
        self.hardware.allocate_classical_register("result", 32)
        self.hardware.allocate_classical_register("temp", 16)
        
        # Connect translator to hardware
        self.translator.set_quantum_backend(self.hardware)
        
        self.initialized = True
        print("✅ Quantum Translation Bridge initialized successfully!")
        
    def translate_and_execute(self, classical_instruction: dict):
        """
        Translate classical instruction to quantum operations and execute
        
        Args:
            classical_instruction: Classical instruction to translate and execute
            
        Returns:
            Execution results
        """
        if not self.initialized:
            raise RuntimeError("Bridge not initialized. Call initialize_bridge() first.")
            
        print(f"Translating classical instruction: {classical_instruction}")
        
        # Translate classical instruction to quantum circuit
        quantum_circuit = self.translator.translate_instruction(classical_instruction)
        
        print(f"Translation result: {quantum_circuit['circuit_type']} circuit")
        
        # Execute on quantum hardware
        result = self.hardware.execute_quantum_circuit(quantum_circuit)
        
        return result
        
    def execute_classical_program(self, program: list):
        """
        Execute a sequence of classical instructions as quantum operations
        
        Args:
            program: List of classical instructions
            
        Returns:
            List of execution results
        """
        if not self.initialized:
            raise RuntimeError("Bridge not initialized. Call initialize_bridge() first.")
            
        print(f"Executing classical program with {len(program)} instructions...")
        
        results = []
        for i, instruction in enumerate(program):
            print(f"\n--- Instruction {i+1}/{len(program)} ---")
            try:
                result = self.translate_and_execute(instruction)
                results.append(result)
                print(f"✅ Instruction executed successfully")
            except Exception as e:
                print(f"❌ Error executing instruction: {e}")
                results.append({"error": str(e)})
                
        return results
        
    def get_bridge_status(self):
        """Get the current status of the quantum translation bridge"""
        return {
            "initialized": self.initialized,
            "hardware_info": self.hardware.get_backend_info() if self.initialized else {},
            "translation_map_size": len(self.translator.translation_map),
            "execution_history_count": len(self.hardware.get_execution_history()) if self.initialized else 0
        }
        
    def reset_bridge(self):
        """Reset the quantum translation bridge"""
        if self.initialized:
            self.hardware.reset_qubits()
            print("Quantum Translation Bridge reset completed")

# Global bridge instance
bridge = QuantumTranslationBridge()

def get_bridge():
    """Get the global quantum translation bridge"""
    return bridge

def demonstrate_translation_bridge():
    """Demonstrate the quantum translation bridge capabilities"""
    print("🌟 Quantum Translation Bridge Demonstration 🌟")
    print("=" * 50)
    
    # Initialize the bridge
    bridge.initialize_bridge(qubit_count=16)
    
    # Show bridge status
    status = bridge.get_bridge_status()
    print(f"\n📊 Bridge Status:")
    print(f"   Initialized: {status['initialized']}")
    print(f"   Qubit Count: {status['hardware_info'].get('qubit_count', 0)}")
    print(f"   Supported Instructions: {status['translation_map_size']}")
    
    # Example classical program
    classical_program = [
        {"opcode": "LOAD", "operands": ["q0", "q1"]},
        {"opcode": "AND", "operands": ["q0", "q1", "q2"]},
        {"opcode": "NOT", "operands": ["q0"]},
        {"opcode": "XOR", "operands": ["q1", "q3"]},
        {"opcode": "ADD", "operands": ["q4", "q5", "q6"]},
        {"opcode": "MOVE", "operands": ["q6", "q7"]}
    ]
    
    print(f"\n📋 Executing Classical Program:")
    for i, instruction in enumerate(classical_program):
        print(f"   {i+1}. {instruction['opcode']} {instruction['operands']}")
    
    # Execute the program
    results = bridge.execute_classical_program(classical_program)
    
    # Show results
    print(f"\n📈 Execution Results:")
    for i, result in enumerate(results):
        if "error" in result:
            print(f"   {i+1}. Error: {result['error']}")
        else:
            print(f"   {i+1}. Success - Final states: {len(result.get('final_states', {}))} qubits")
    
    # Show hardware info
    hardware_info = bridge.hardware.get_backend_info()
    print(f"\n⚙️  Hardware Information:")
    print(f"   Backend Type: {hardware_info['backend_type']}")
    print(f"   Supported Gates: {len(hardware_info['supported_gates'])}")
    print(f"   Total Executions: {hardware_info['total_executions']}")
    
    print(f"\n✨ Quantum Translation Bridge demonstration completed!")

if __name__ == "__main__":
    demonstrate_translation_bridge()