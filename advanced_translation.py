"""
Advanced Quantum Translation Bridge Examples
Demonstrates complex classical-to-quantum translations
"""

import sys
sys.path.append('c:\\quantum-devops-project\\src')

from translation_bridge import get_bridge

def advanced_translation_examples():
    """Demonstrate advanced classical-to-quantum translations"""
    
    print("🔬 Advanced Quantum Translation Bridge Examples 🔬")
    print("=" * 55)
    
    # Get the bridge instance
    bridge = get_bridge()
    
    # Initialize with more qubits for complex operations
    bridge.initialize_bridge(qubit_count=32)
    
    print("✅ Bridge initialized with 32 qubits")
    
    # Example 1: Complex logical operations
    print("\n1. 🔣 Complex Logical Operations")
    logical_program = [
        {"opcode": "LOAD", "operands": ["q0", 1]},
        {"opcode": "LOAD", "operands": ["q1", 0]},
        {"opcode": "AND", "operands": ["q0", "q1", "q2"]},
        {"opcode": "OR", "operands": ["q0", "q1", "q3"]},
        {"opcode": "XOR", "operands": ["q0", "q1", "q4"]},
        {"opcode": "NAND", "operands": ["q0", "q1", "q5"]},
        {"opcode": "NOR", "operands": ["q0", "q1", "q6"]}
    ]
    
    print("   Executing logical operations program...")
    results = bridge.execute_classical_program(logical_program)
    print(f"   ✅ Completed with {len([r for r in results if 'error' not in r])} successful operations")
    
    # Example 2: Arithmetic operations
    print("\n2. ➕ Arithmetic Operations")
    arithmetic_program = [
        {"opcode": "LOAD", "operands": ["q10", 5]},
        {"opcode": "LOAD", "operands": ["q11", 3]},
        {"opcode": "ADD", "operands": ["q10", "q11", "q12"]},
        {"opcode": "SUB", "operands": ["q10", "q11", "q13"]},
        {"opcode": "MUL", "operands": ["q10", "q11", "q14"]},
        {"opcode": "DIV", "operands": ["q10", "q11", "q15"]}
    ]
    
    print("   Executing arithmetic operations program...")
    results = bridge.execute_classical_program(arithmetic_program)
    print(f"   ✅ Completed with {len([r for r in results if 'error' not in r])} successful operations")
    
    # Example 3: Memory operations
    print("\n3. 💾 Memory Operations")
    memory_program = [
        {"opcode": "LOAD", "operands": ["q20", 42]},
        {"opcode": "STORE", "operands": ["q20", "temp[0]"]},
        {"opcode": "LOAD", "operands": ["q21", 24]},
        {"opcode": "STORE", "operands": ["q21", "temp[1]"]},
        {"opcode": "MOVE", "operands": ["q20", "q22"]},
        {"opcode": "MOVE", "operands": ["q21", "q23"]}
    ]
    
    print("   Executing memory operations program...")
    results = bridge.execute_classical_program(memory_program)
    print(f"   ✅ Completed with {len([r for r in results if 'error' not in r])} successful operations")
    
    # Example 4: Control flow operations
    print("\n4. 🔁 Control Flow Operations")
    control_program = [
        {"opcode": "LOAD", "operands": ["q25", 1]},
        {"opcode": "LOAD", "operands": ["q26", 0]},
        {"opcode": "JUMP", "operands": ["q25", "label1"]},
        {"opcode": "CALL", "operands": ["function1", "q27"]},
        {"opcode": "RETURN", "operands": ["q27"]}
    ]
    
    print("   Executing control flow program...")
    results = bridge.execute_classical_program(control_program)
    print(f"   ✅ Completed with {len([r for r in results if 'error' not in r])} successful operations")
    
    # Show final status
    status = bridge.get_bridge_status()
    print(f"\n📊 Final Bridge Status:")
    print(f"   Total Executions: {status['hardware_info']['total_executions']}")
    print(f"   Qubit Utilization: {status['hardware_info']['qubit_count']}/32")
    print(f"   Classical Registers: {status['hardware_info']['classical_registers']}")
    
    print("\n✨ Advanced translation examples completed successfully!")

def custom_instruction_translation():
    """Example of translating custom classical instructions"""
    
    print("\n" + "=" * 55)
    print("🔧 Custom Instruction Translation Example")
    print("=" * 55)
    
    # Get the bridge
    bridge = get_bridge()
    
    # Define a custom classical program for demonstration
    custom_program = [
        # Simple bit manipulation
        {"opcode": "LOAD", "operands": ["q0", 1]},
        {"opcode": "LOAD", "operands": ["q1", 1]},
        {"opcode": "AND", "operands": ["q0", "q1", "q2"]},
        
        # More complex operation
        {"opcode": "LOAD", "operands": ["q3", 0]},
        {"opcode": "NOT", "operands": ["q3"]},
        {"opcode": "XOR", "operands": ["q2", "q3", "q4"]},
        
        # Arithmetic
        {"opcode": "ADD", "operands": ["q4", "q0", "q5"]},
        
        # Store result
        {"opcode": "STORE", "operands": ["q5", "result[0]"]}
    ]
    
    print("Executing custom bit manipulation program:")
    for i, instruction in enumerate(custom_program, 1):
        print(f"  {i}. {instruction['opcode']} {instruction['operands']}")
    
    # Execute the program
    results = bridge.execute_classical_program(custom_program)
    
    # Show results
    print(f"\n📈 Execution Results:")
    successful_ops = len([r for r in results if 'error' not in r])
    print(f"   Successful Operations: {successful_ops}/{len(custom_program)}")
    
    # Show final quantum state
    final_state = bridge.hardware.get_quantum_state()
    print(f"\n⚛️  Final Quantum State Sample:")
    qubit_count = 0
    for qubit, state in list(final_state.items())[:5]:  # Show first 5 qubits
        print(f"   {qubit}: |{state['state']}⟩ {'(entangled)' if state['entangled'] else ''}")
        qubit_count += 1
    if len(final_state) > 5:
        print(f"   ... and {len(final_state) - 5} more qubits")
    
    print(f"\n🎯 Custom instruction translation completed!")

if __name__ == "__main__":
    # Run advanced examples
    advanced_translation_examples()
    
    # Run custom instruction example
    custom_instruction_translation()