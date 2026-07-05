"""
Quantum Audio Integration Demo
Immersive 3D audio experience blending quantum computing with spatial sound
"""

import sys
import os
sys.path.append('c:\\quantum-devops-project')

# Import our quantum audio modules
from src.core.quantum_audio_engine import initialize_quantum_audio_space, render_quantum_audio, create_quantum_harmony
from src.core.quantum_sonification import initialize_sonification_system, sonify_qubit, sonify_entanglement
from src.core.quantum_circuit_renderer import initialize_circuit_renderer, render_quantum_circuit
from src.core.code_structure_3d import initialize_3d_structure, get_optimal_3d_component

def demonstrate_quantum_audio_integration():
    """Demonstrate the full quantum audio integration system"""
    
    print("🎵 Quantum Audio Integration Demo 🎵")
    print("=" * 50)
    
    # Initialize the 3D quantum structure
    structure = initialize_3d_structure()
    print("✅ 3D Quantum Structure initialized")
    
    # Initialize audio engine
    audio_engine = initialize_quantum_audio_space()
    print("✅ Quantum Audio Engine initialized")
    
    # Initialize sonification system
    sonification = initialize_sonification_system(audio_engine)
    print("✅ Quantum Sonification System initialized")
    
    # Initialize circuit renderer
    circuit_renderer = initialize_circuit_renderer(audio_engine, sonification)
    print("✅ Quantum Circuit Renderer initialized")
    
    print("\n🌀 Creating Quantum Audio Experience...")
    print("-" * 40)
    
    # 1. Create and sonify individual qubit states
    print("1. Sonifying individual qubit states:")
    
    # Qubit in |0⟩ state (alpha=1, beta=0)
    q0_params = sonify_qubit("q0", 1+0j, 0+0j)
    q0_audio = render_quantum_audio("q0", [1+0j, 0+0j])
    print(f"   |0⟩ qubit (q0): frequency={q0_params['frequency']:.1f}Hz, prob_0={q0_params['probability_0']:.2f}")
    
    # Qubit in |1⟩ state (alpha=0, beta=1)
    q1_params = sonify_qubit("q1", 0+0j, 1+0j)
    q1_audio = render_quantum_audio("q1", [0+0j, 1+0j])
    print(f"   |1⟩ qubit (q1): frequency={q1_params['frequency']:.1f}Hz, prob_1={q1_params['probability_1']:.2f}")
    
    # Qubit in superposition state (alpha=√0.5, beta=√0.5)
    q2_params = sonify_qubit("q2", 0.707+0j, 0.707+0j)
    q2_audio = render_quantum_audio("q2", [0.707+0j, 0.707+0j])
    print(f"   |+⟩ qubit (q2): frequency={q2_params['frequency']:.1f}Hz, prob_0={q2_params['probability_0']:.2f}, prob_1={q2_params['probability_1']:.2f}")
    
    # 2. Create entanglement between qubits
    print("\n2. Creating quantum entanglement:")
    entanglement_params = sonify_entanglement(("q0", "q1"), 0.9)
    if entanglement_params:
        print(f"   Entangled qubits (q0,q1): distance={entanglement_params['distance']:.2f}, harmony={entanglement_params['harmonic_tension']:.2f}")
    
    # Create audio harmony for entangled qubits
    entangled_harmony = create_quantum_harmony([("q0", "q1")])
    print("   ✨ Entanglement harmony generated")
    
    # 3. Render a quantum circuit as audio
    print("\n3. Rendering quantum circuit as audio:")
    circuit_operations = [
        {"gate": "H", "targets": ["q0"]},
        {"gate": "CNOT", "targets": ["q0", "q1"]},
        {"gate": "X", "targets": ["q2"]},
        {"gate": "R", "targets": ["q1"], "parameters": [1.57]}
    ]
    
    circuit_audio = render_quantum_circuit(3, circuit_operations)
    print("   Quantum circuit audio rendered")
    
    # 4. Show 3D positioning
    print("\n4. 3D Audio Positioning:")
    positions = [
        ("q0", q0_params["position"]),
        ("q1", q1_params["position"]),
        ("q2", q2_params["position"])
    ]
    
    for qubit, pos in positions:
        print(f"   {qubit}: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f})")
    
    print("\n🎧 Quantum Audio Experience Summary:")
    print("-" * 35)
    print("✅ Individual qubit states sonified")
    print("✅ Quantum entanglement represented through audio harmony")
    print("✅ Quantum circuit operations rendered as spatial audio")
    print("✅ 3D positioning mapped to stereo audio space")
    print("✅ Immersive quantum computing experience created")
    
    print("\n🌟 The Quantum Audio Integration System is ready!")
    print("   Experience the quantum realm through sound waves! 🌊")
    
    return {
        "qubit_audio": {"q0": q0_audio, "q1": q1_audio, "q2": q2_audio},
        "entanglement_audio": entangled_harmony,
        "circuit_audio": circuit_audio,
        "structure": structure
    }

def example_quantum_music_composition():
    """Example of creating music from quantum circuits"""
    
    print("\n" + "=" * 50)
    print("🎼 Quantum Music Composition Example")
    print("=" * 50)
    
    # Define a quantum musical piece
    musical_sections = [
        {
            "name": "Quantum Superposition",
            "operations": [
                {"gate": "H", "targets": ["q0"]},
                {"gate": "H", "targets": ["q1"]},
                {"gate": "H", "targets": ["q2"]}
            ],
            "repeats": 2
        },
        {
            "name": "Entanglement Harmony",
            "operations": [
                {"gate": "CNOT", "targets": ["q0", "q1"]},
                {"gate": "CNOT", "targets": ["q1", "q2"]},
                {"gate": "R", "targets": ["q0"], "parameters": [3.14]}
            ],
            "repeats": 1
        },
        {
            "name": "Quantum Measurement",
            "operations": [
                {"gate": "X", "targets": ["q0"]},
                {"gate": "Y", "targets": ["q1"]},
                {"gate": "Z", "targets": ["q2"]}
            ],
            "repeats": 3
        }
    ]
    
    print("Creating quantum musical composition:")
    for i, section in enumerate(musical_sections, 1):
        print(f"  {i}. {section['name']} ({section['repeats']} repeat{'s' if section['repeats'] > 1 else ''})")
        for op in section["operations"]:
            targets = ", ".join(op["targets"])
            params = f" with params {op['parameters']}" if "parameters" in op else ""
            print(f"     - {op['gate']} gate on {targets}{params}")
    
    print("\n🎵 Quantum composition ready to play!")
    print("   Each quantum operation creates unique audio signatures")
    print("   Entanglement produces harmonic resonance")
    print("   Superposition generates rich timbral textures")

if __name__ == "__main__":
    # Demonstrate the quantum audio integration
    result = demonstrate_quantum_audio_integration()
    
    # Show example quantum music composition
    example_quantum_music_composition()
    
    print("\n" + "=" * 50)
    print("🎉 Quantum Audio Demo Complete!")
    print("   The bridge between quantum computing and immersive audio is now active!")
    print("   Experience quantum states through sound waves in 3D space! 🌌")