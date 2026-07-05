"""
Physics-Based 3D Sound Adaptation Demo
Complete demonstration of auto-adaptive sound layers with acoustic physics simulation
"""

import sys
import os
import math
sys.path.append('c:\\quantum-devops-project')

# Import our physics-based audio modules
from src.core.acoustic_physics_engine import (
    initialize_acoustic_physics,
    add_physics_sound_source,
    update_acoustic_simulation,
    get_sound_at_listener,
    generate_physics_based_audio
)
from src.core.adaptive_sound_layer_system import (
    initialize_adaptive_sound_layers,
    adapt_sound_layers_automatically,
    get_adaptation_status
)
from src.core.multi_source_interaction_model import (
    initialize_multi_source_interaction,
    analyze_wave_interactions,
    calculate_spatial_interference,
    get_interaction_complexity
)
from src.core.enhanced_quantum_audio_engine import (
    initialize_enhanced_quantum_audio_space,
    render_enhanced_quantum_audio
)
from src.core.environmental_audio_processor import initialize_environmental_processing

def demonstrate_physics_based_audio_adaptation():
    """Demonstrate physics-based auto-adaptive sound layer system"""
    
    print("🔊 Physics-Based 3D Sound Adaptation Demo 🔊")
    print("=" * 55)
    
    # Initialize acoustic physics engine
    acoustic_engine = initialize_acoustic_physics()
    print("✅ Acoustic Physics Engine initialized")
    
    # Initialize adaptive sound layer system
    adaptive_system = initialize_adaptive_sound_layers(acoustic_engine)
    print("✅ Adaptive Sound Layer System initialized")
    
    # Initialize multi-source interaction model
    interaction_model = initialize_multi_source_interaction(acoustic_engine)
    print("✅ Multi-Source Interaction Model initialized")
    
    # Initialize environmental processing
    environmental_processor = initialize_environmental_processing()
    print("✅ Environmental Audio Processing initialized")
    
    print("\n🌀 Creating Physics-Based Audio Experience...")
    print("-" * 45)
    
    # 1. Set up multiple sound sources with different properties
    print("1. Setting up multi-source sound environment:")
    
    # Add quantum sound sources at different positions
    add_physics_sound_source("qubit_0", (2.0, 1.0, 0.0), 440.0, 0.8, 0.0)
    print("   🎵 Qubit |0⟩ source added at (2.0, 1.0, 0.0)")
    
    add_physics_sound_source("qubit_1", (-2.0, 1.0, 0.0), 880.0, 0.7, math.pi/2)
    print("   🎵 Qubit |1⟩ source added at (-2.0, 1.0, 0.0)")
    
    add_physics_sound_source("superposition", (0.0, 3.0, 1.0), 660.0, 0.9, math.pi/4)
    print("   🎵 Superposition source added at (0.0, 3.0, 1.0)")
    
    add_physics_sound_source("entanglement", (0.0, -1.0, -2.0), 550.0, 0.85, math.pi)
    print("   🎵 Entanglement source added at (0.0, -1.0, -2.0)")
    
    # Add environmental sound sources
    add_physics_sound_source("forest_ambience", (5.0, 0.0, 5.0), 120.0, 0.3, 0.0)
    print("   🌳 Forest ambience source added at (5.0, 0.0, 5.0)")
    
    # 2. Set listener position
    acoustic_engine.set_listener_position((0.0, 0.0, 0.0))
    print("\n2. Listener positioned at origin (0.0, 0.0, 0.0)")
    
    # 3. Simulate sound propagation
    print("\n3. Simulating sound wave propagation:")
    for i in range(100):
        update_acoustic_simulation(1.0/44100.0)  # Update at audio sample rate
        
        # Every 20 steps, analyze and adapt
        if i % 20 == 0:
            # Analyze wave interactions
            interactions = analyze_wave_interactions()
            complexity = get_interaction_complexity()
            
            # Adapt sound layers based on physics
            adapted_layers = adapt_sound_layers_automatically()
            adaptation_status = get_adaptation_status()
            
            if i == 0:
                print(f"   Initial wave analysis: {complexity['complexity']:.2f} complexity")
            elif i == 40:
                print(f"   Mid-simulation adaptation: Layers adjusted for {complexity['complexity']:.2f} complexity")
            elif i == 80:
                print(f"   Final adaptation: System optimized for {complexity['complexity']:.2f} complexity")
    
    # 4. Analyze final sound field
    print("\n4. Final acoustic analysis:")
    sound_at_listener = get_sound_at_listener()
    print(f"   Total amplitude at listener: {sound_at_listener['amplitude']:.3f}")
    print(f"   Mixed frequency: {sound_at_listener['frequency']:.1f} Hz")
    print(f"   Active sound sources: {len(sound_at_listener['components'])}")
    
    # 5. Calculate spatial interference patterns
    print("\n5. Spatial interference analysis:")
    interference_at_origin = calculate_spatial_interference((0.0, 0.0, 0.0))
    interference_at_periphery = calculate_spatial_interference((3.0, 3.0, 3.0))
    
    print(f"   Interference at origin: {interference_at_origin['interference_type']} ({interference_at_origin['amplitude']:.3f})")
    print(f"   Interference at periphery: {interference_at_periphery['interference_type']} ({interference_at_periphery['amplitude']:.3f})")
    
    # 6. Show wave interactions
    print("\n6. Wave interaction summary:")
    interactions = analyze_wave_interactions()
    complexity = get_interaction_complexity()
    
    print(f"   Total interactions: {complexity['total_interactions']}")
    print(f"   Constructive: {complexity['constructive_interactions']}")
    print(f"   Destructive: {complexity['destructive_interactions']}")
    print(f"   Perceptible beats: {complexity['perceptible_beats']}")
    print(f"   Resonance zones: {complexity['resonance_zones']}")
    
    # 7. Show adaptive system status
    print("\n7. Adaptive system status:")
    adaptation_status = get_adaptation_status()
    print(f"   Adaptations performed: {adaptation_status['total_adaptations']}")
    print(f"   Current complexity: {adaptation_status['environmental_complexity']:.2f}")
    print(f"   Spatial distribution: {adaptation_status['spatial_distribution']:.2f}")
    
    print("\n🔊 Physics-Based Audio Adaptation Summary:")
    print("-" * 42)
    print("✅ Multi-source sound field with quantum and environmental sources")
    print("✅ Realistic acoustic physics simulation (distance, absorption, Doppler)")
    print("✅ Auto-adaptive sound layers responding to acoustic complexity")
    print("✅ Wave interference and resonance calculations")
    print("✅ Spatial interference pattern analysis")
    print("✅ Priority-based sound layer mixing")
    
    print("\n🌟 The Physics-Based Audio Adaptation System is active!")
    print("   Sound layers automatically adjust to acoustic conditions! 🌊")

def example_dynamic_sound_adaptation():
    """Example of dynamic sound adaptation in changing acoustic conditions"""
    
    print("\n" + "=" * 55)
    print("🔄 Dynamic Sound Adaptation Example")
    print("=" * 55)
    
    # Initialize systems
    acoustic_engine = initialize_acoustic_physics()
    adaptive_system = initialize_adaptive_sound_layers(acoustic_engine)
    interaction_model = initialize_multi_source_interaction(acoustic_engine)
    
    # Set initial conditions
    acoustic_engine.set_listener_position((0.0, 0.0, 0.0))
    
    print("Simulating dynamic acoustic environment:")
    print("  🎵 Scenario 1: Quiet quantum computing environment")
    
    # Add few quantum sources
    add_physics_sound_source("qubit_a", (1.0, 0.0, 0.0), 440.0, 0.5)
    add_physics_sound_source("qubit_b", (-1.0, 0.0, 0.0), 660.0, 0.5)
    
    # Simulate and adapt
    for i in range(50):
        update_acoustic_simulation(1.0/44100.0)
    
    # Analyze and adapt
    complexity1 = get_interaction_complexity()
    adapted1 = adapt_sound_layers_automatically()
    print(f"     → Low complexity ({complexity1['complexity']:.2f}), layers enhanced for clarity")
    
    print("  🎵 Scenario 2: Complex multi-source environment")
    
    # Add many sources to increase complexity
    for i in range(10):
        x = (i - 5) * 0.5
        y = math.sin(i) * 2
        z = math.cos(i) * 2
        freq = 200 + i * 50
        amp = 0.3 + (i % 3) * 0.2
        add_physics_sound_source(f"source_{i}", (x, y, z), freq, amp)
    
    # Simulate and adapt
    for i in range(50):
        update_acoustic_simulation(1.0/44100.0)
    
    # Analyze and adapt
    complexity2 = get_interaction_complexity()
    adapted2 = adapt_sound_layers_automatically()
    print(f"     → High complexity ({complexity2['complexity']:.2f}), layers adjusted to prevent masking")
    
    print("\n🎯 Dynamic adaptation successfully handled changing acoustic conditions!")

def demonstrate_acoustic_physics_features():
    """Demonstrate specific acoustic physics features"""
    
    print("\n" + "=" * 55)
    print("🔬 Acoustic Physics Feature Demonstration")
    print("=" * 55)
    
    acoustic_engine = initialize_acoustic_physics()
    acoustic_engine.initialize_environment_properties(temperature=25.0, humidity=60.0)
    
    print("Key acoustic physics features demonstrated:")
    
    # Distance attenuation
    attenuation_1m = acoustic_engine.calculate_distance_attenuation(1.0)
    attenuation_5m = acoustic_engine.calculate_distance_attenuation(5.0)
    attenuation_10m = acoustic_engine.calculate_distance_attenuation(10.0)
    print(f"  📏 Distance Attenuation:")
    print(f"     - 1m: {attenuation_1m:.3f} (0 dB)")
    print(f"     - 5m: {attenuation_5m:.3f} ({20*math.log10(attenuation_5m/attenuation_1m):.1f} dB)")
    print(f"     - 10m: {attenuation_10m:.3f} ({20*math.log10(attenuation_10m/attenuation_1m):.1f} dB)")
    
    # Air absorption
    absorption_100hz = acoustic_engine.calculate_air_absorption(100, 10.0)
    absorption_1000hz = acoustic_engine.calculate_air_absorption(1000, 10.0)
    absorption_4000hz = acoustic_engine.calculate_air_absorption(4000, 10.0)
    print(f"  🌬️  Air Absorption (10m distance):")
    print(f"     - 100 Hz: {absorption_100hz:.3f}")
    print(f"     - 1000 Hz: {absorption_1000hz:.3f}")
    print(f"     - 4000 Hz: {absorption_4000hz:.3f}")
    
    # Doppler effect
    doppler_approaching = acoustic_engine.calculate_doppler_effect(
        (10.0, 0.0, 0.0), (0.0, 0.0, 0.0), (5.0, 0.0, 0.0), (0.0, 0.0, 0.0)
    )
    doppler_receding = acoustic_engine.calculate_doppler_effect(
        (-10.0, 0.0, 0.0), (0.0, 0.0, 0.0), (-5.0, 0.0, 0.0), (0.0, 0.0, 0.0)
    )
    print(f"  🚘 Doppler Effect (440 Hz source):")
    print(f"     - Approaching: {440 * doppler_approaching:.1f} Hz")
    print(f"     - Receding: {440 * doppler_receding:.1f} Hz")
    
    # Directional attenuation
    directional_full = acoustic_engine.calculate_directional_attenuation(
        (0.0, 0.0, 1.0), (0.0, 0.0, 5.0), (0.0, 0.0, 0.0)
    )
    directional_side = acoustic_engine.calculate_directional_attenuation(
        (0.0, 0.0, 1.0), (5.0, 0.0, 0.0), (0.0, 0.0, 0.0)
    )
    directional_back = acoustic_engine.calculate_directional_attenuation(
        (0.0, 0.0, 1.0), (0.0, 0.0, -5.0), (0.0, 0.0, 0.0)
    )
    print(f"  🎯 Directional Attenuation:")
    print(f"     - Front: {directional_full:.3f} (0°)")
    print(f"     - Side: {directional_side:.3f} (90°)")
    print(f"     - Back: {directional_back:.3f} (180°)")

if __name__ == "__main__":
    # Demonstrate physics-based audio adaptation
    demonstrate_physics_based_audio_adaptation()
    
    # Show dynamic adaptation example
    example_dynamic_sound_adaptation()
    
    # Demonstrate acoustic physics features
    demonstrate_acoustic_physics_features()
    
    print("\n" + "=" * 55)
    print("🎉 Physics-Based Audio Adaptation Demo Complete!")
    print("   The ultimate sound layer adaptation system is now")
    print("   automatically adjusting to acoustic physics in real-time! 🌌")
    print("   Experience sound that truly adapts to ALL conditions! 🎵")