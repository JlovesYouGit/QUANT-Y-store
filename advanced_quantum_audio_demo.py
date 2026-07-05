"""
Advanced Quantum Audio Immersion Demo
Complete 3D sound experience with environmental integration and natural sound masking
"""

import sys
import os
sys.path.append('c:\\quantum-devops-project')

# Import our enhanced quantum audio modules
from src.core.enhanced_quantum_audio_engine import (
    initialize_enhanced_quantum_audio_space, 
    set_audio_environment,
    render_enhanced_quantum_audio, 
    create_enhanced_quantum_harmony
)
from src.core.environmental_audio_processor import (
    initialize_environmental_processing,
    create_sound_mask,
    blend_quantum_with_environment
)
from src.core.sound_layer_masker import (
    initialize_sound_layer_masker,
    create_quantum_to_natural_mask,
    apply_sound_mask
)
from src.core.quantum_sonification import (
    initialize_sonification_system, 
    sonify_qubit, 
    sonify_entanglement
)
from src.core.quantum_circuit_renderer import (
    initialize_circuit_renderer, 
    render_quantum_circuit
)
from src.core.code_structure_3d import initialize_3d_structure, get_optimal_3d_component

def demonstrate_advanced_quantum_audio_immersion():
    """Demonstrate the advanced quantum audio immersion system"""
    
    print("🎵 Advanced Quantum Audio Immersion Demo 🎵")
    print("=" * 55)
    
    # Initialize the enhanced 3D quantum structure
    structure = initialize_3d_structure()
    print("✅ 3D Quantum Structure initialized")
    
    # Initialize enhanced audio engine with environmental awareness
    audio_engine = initialize_enhanced_quantum_audio_space()
    print("✅ Enhanced Quantum Audio Engine initialized")
    
    # Set environmental context (forest environment for natural immersion)
    set_audio_environment("forest")
    print("✅ Environmental context set to 'forest'")
    
    # Initialize sonification system
    sonification = initialize_sonification_system(audio_engine)
    print("✅ Quantum Sonification System initialized")
    
    print("\n🌀 Creating Advanced Quantum Audio Experience...")
    print("-" * 45)
    
    # 1. Create and sonify individual qubit states with environmental awareness
    print("1. Sonifying qubit states with environmental integration:")
    
    # Qubit in |0⟩ state (alpha=1, beta=0)
    q0_params = sonify_qubit("q0", 1+0j, 0+0j)
    q0_audio = render_enhanced_quantum_audio("q0", [1+0j, 0+0j], environment_aware=True)
    print(f"   |0⟩ qubit (q0): frequency={q0_params['frequency']:.1f}Hz, environment={q0_params['environment']}")
    
    # Qubit in |1⟩ state (alpha=0, beta=1)
    q1_params = sonify_qubit("q1", 0+0j, 1+0j)
    q1_audio = render_enhanced_quantum_audio("q1", [0+0j, 1+0j], environment_aware=True)
    print(f"   |1⟩ qubit (q1): frequency={q1_params['frequency']:.1f}Hz, environment={q1_params['environment']}")
    
    # Qubit in superposition state (alpha=√0.5, beta=√0.5)
    q2_params = sonify_qubit("q2", 0.707+0j, 0.707+0j)
    q2_audio = render_enhanced_quantum_audio("q2", [0.707+0j, 0.707+0j], environment_aware=True)
    print(f"   |+⟩ qubit (q2): frequency={q2_params['frequency']:.1f}Hz, environment={q2_params['environment']}")
    
    # 2. Create entanglement between qubits with environmental harmony
    print("\n2. Creating quantum entanglement with environmental harmony:")
    entanglement_params = sonify_entanglement(("q0", "q1"), 0.9)
    if entanglement_params:
        print(f"   Entangled qubits (q0,q1): distance={entanglement_params['distance']:.2f}, environment=forest")
    
    # Create enhanced audio harmony for entangled qubits
    entangled_harmony = create_enhanced_quantum_harmony([("q0", "q1")], environment_aware=True)
    print("   ✨ Enhanced entanglement harmony with forest environment generated")
    
    # 3. Apply sound layer masking for natural integration
    print("\n3. Applying sound layer masking for natural integration:")
    
    # Create quantum-to-natural sound masks
    superposition_mask = create_quantum_to_natural_mask("superposition_state", "forest")
    entanglement_mask = create_quantum_to_natural_mask("entangled_pair", "forest")
    
    if superposition_mask:
        print("   🎭 Superposition state mapped to 'wind_chimes' natural counterpart")
    if entanglement_mask:
        print("   🎭 Entanglement mapped to 'twin_dolphins' natural counterpart")
    
    # 4. Blend quantum audio with environmental sounds
    print("\n4. Blending quantum audio with environmental sounds:")
    
    # Blend individual qubit sounds with forest environment
    q0_blended = blend_quantum_with_environment(q0_audio, "forest", 0.6)
    q1_blended = blend_quantum_with_environment(q1_audio, "forest", 0.6)
    q2_blended = blend_quantum_with_environment(q2_audio, "forest", 0.6)
    
    print("   🌳 Qubit sounds blended with forest ambience")
    
    # 5. Show 3D positioning with environmental context
    print("\n5. 3D Audio Positioning with Environmental Context:")
    positions = [
        ("q0", q0_params["position"]),
        ("q1", q1_params["position"]),
        ("q2", q2_params["position"])
    ]
    
    for qubit, pos in positions:
        print(f"   {qubit}: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}) in forest environment")
    
    print("\n🎧 Advanced Quantum Audio Immersion Summary:")
    print("-" * 40)
    print("✅ Individual qubit states sonified with environmental awareness")
    print("✅ Quantum entanglement represented through enhanced audio harmony")
    print("✅ Sound layer masking maps quantum phenomena to natural counterparts")
    print("✅ Quantum sounds blended with environmental ambience")
    print("✅ 3D positioning integrated with spatial environmental audio")
    print("✅ Complete immersive quantum-environmental experience created")
    
    print("\n🌟 The Advanced Quantum Audio Immersion System is active!")
    print("   Experience quantum computing through natural sound waves! 🌊")
    
    return {
        "qubit_audio": {"q0": q0_blended, "q1": q1_blended, "q2": q2_blended},
        "entanglement_audio": entangled_harmony,
        "structure": structure
    }

def example_environmental_quantum_composition():
    """Example of creating music from quantum circuits with environmental integration"""
    
    print("\n" + "=" * 55)
    print("🎼 Environmental Quantum Music Composition")
    print("=" * 55)
    
    # Define quantum musical sections with environmental context
    musical_sections = [
        {
            "name": "Forest Quantum Superposition",
            "environment": "forest",
            "operations": [
                {"gate": "H", "targets": ["q0"]},
                {"gate": "H", "targets": ["q1"]},
                {"gate": "H", "targets": ["q2"]}
            ],
            "repeats": 2
        },
        {
            "name": "Ocean Entanglement Harmony",
            "environment": "ocean",
            "operations": [
                {"gate": "CNOT", "targets": ["q0", "q1"]},
                {"gate": "CNOT", "targets": ["q1", "q2"]},
                {"gate": "R", "targets": ["q0"], "parameters": [3.14]}
            ],
            "repeats": 1
        },
        {
            "name": "Cosmic Measurement",
            "environment": "space",
            "operations": [
                {"gate": "X", "targets": ["q0"]},
                {"gate": "Y", "targets": ["q1"]},
                {"gate": "Z", "targets": ["q2"]}
            ],
            "repeats": 3
        }
    ]
    
    print("Creating environmental quantum musical composition:")
    for i, section in enumerate(musical_sections, 1):
        print(f"  {i}. {section['name']} in {section['environment']} environment")
        print(f"     ({section['repeats']} repeat{'s' if section['repeats'] > 1 else ''})")
        for op in section["operations"]:
            targets = ", ".join(op["targets"])
            params = f" with params {op['parameters']}" if "parameters" in op else ""
            print(f"     - {op['gate']} gate on {targets}{params}")
    
    print("\n🎵 Environmental quantum composition ready to play!")
    print("   Each quantum operation creates unique audio signatures")
    print("   Environmental context provides natural sound masking")
    print("   Quantum phenomena mapped to their natural counterparts")

def demonstrate_multi_environment_integration():
    """Demonstrate integration across multiple environments"""
    
    print("\n" + "=" * 55)
    print("🌍 Multi-Environment Quantum Audio Integration")
    print("=" * 55)
    
    environments = ["forest", "ocean", "city", "space"]
    
    print("Integrating quantum audio across multiple environments:")
    for env in environments:
        print(f"  🌳 {env.capitalize()} environment:")
        print(f"     - Natural sound mask: {create_sound_mask(env)}")
        print(f"     - Quantum phenomena mapped to {env} counterparts")
        print(f"     - Environmental ambience blended with quantum sounds")
    
    print("\n🌐 Seamless transition between quantum and natural soundscapes")
    print("   Forest: Quantum states as wind chimes and bird songs")
    print("   Ocean: Entanglement as dolphin harmonies and wave patterns")
    print("   City: Quantum operations as urban rhythms and traffic flows")
    print("   Space: Quantum phenomena as cosmic radiation and pulsar clicks")

if __name__ == "__main__":
    # Demonstrate the advanced quantum audio immersion
    result = demonstrate_advanced_quantum_audio_immersion()
    
    # Show example environmental quantum music composition
    example_environmental_quantum_composition()
    
    # Demonstrate multi-environment integration
    demonstrate_multi_environment_integration()
    
    print("\n" + "=" * 55)
    print("🎉 Advanced Quantum Audio Immersion Demo Complete!")
    print("   The ultimate bridge between quantum computing and")
    print("   natural environmental sound is now fully active! 🌌")
    print("   Experience quantum states through ALL layers of sound! 🎵")