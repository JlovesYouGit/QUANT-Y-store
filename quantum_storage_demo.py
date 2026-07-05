"""
Quantum Storage Integration Demo
Demonstrates the interlinking of quantum states with SSD/HDD storage using cubical spacing
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import our quantum storage manager
from src.core.quantum_storage_manager import get_storage_manager
from src.core.code_structure_3d import get_optimal_3d_component

def create_sample_quantum_states(count: int) -> list:
    """Create sample quantum states for demonstration"""
    states = []
    for i in range(count):
        state = {
            "id": f"state_{i}",
            "amplitudes": [0.5, 0.5, 0.0, 0.0],  # Simplified quantum state
            "qubit_count": 2,
            "entanglement": [],
            "timestamp": f"2023-01-{i+1:02d}T10:00:00Z"
        }
        states.append(state)
    return states

def demonstrate_quantum_storage():
    """Demonstrate quantum storage management with SSD/HDD interlinking"""
    
    print("🔬 Quantum Storage Manager Demo")
    print("=" * 50)
    
    # Get the storage manager
    storage_manager = get_storage_manager()
    
    # Show initial storage statistics
    print("\n📊 Initial Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    print(f"SSD Capacity: {stats['ssd_capacity_tb']:.2f} TB")
    print(f"HDD Capacity: {stats['hdd_capacity_tb']:.2f} TB")
    print(f"SSD Efficiency: {stats['ssd_efficiency']:.2f}")
    print(f"HDD Efficiency: {stats['hdd_efficiency']:.2f}")
    
    # Create sample quantum states
    print("\n⚡ Creating 50 sample quantum states...")
    quantum_states = create_sample_quantum_states(50)
    print(f"Created {len(quantum_states)} quantum states")
    
    # Save quantum states with metadata
    print("\n💾 Saving quantum states to storage...")
    metadata = {
        "experiment_id": "QUANTUM_STORAGE_DEMO_001",
        "researcher": "Quantum DevOps Team",
        "purpose": "Storage interlinking demonstration"
    }
    
    result = storage_manager.save_quantum_states(quantum_states, metadata)
    print(f"Successfully saved {result['states_saved']} quantum states")
    print(f"Storage distribution: {result['storage_distribution']}")
    print(f"Spatial volume: {result['spatial_arrangement']['total_volume_m3']:.2e} m³")
    
    # Show updated storage statistics
    print("\n📈 Updated Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    print(f"Total Quantum States: {stats['total_quantum_states']}")
    print(f"SSD Stored States: {stats['ssd_stored_states']}")
    print(f"HDD Stored States: {stats['hdd_stored_states']}")
    
    # Apply storage enhancement
    print("\n🚀 Applying storage capacity enhancement...")
    enhancement_result = storage_manager.enhance_storage_capacity(enhancement_cycles=3)
    print(f"Applied {enhancement_result['enhancement_cycles']} enhancement cycles")
    print(f"New SSD Capacity: {enhancement_result['new_ssd_capacity_tb']:.2f} TB")
    print(f"New HDD Capacity: {enhancement_result['new_hdd_capacity_tb']:.2f} TB")
    print(f"Improved SSD Efficiency: {enhancement_result['improved_ssd_efficiency']:.3f}")
    print(f"Improved HDD Efficiency: {enhancement_result['improved_hdd_efficiency']:.3f}")
    
    # Show final storage statistics
    print("\n📊 Final Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    print(f"SSD Capacity: {stats['ssd_capacity_tb']:.2f} TB (+{stats['ssd_capacity_tb'] - 1.0:.2f} TB)")
    print(f"HDD Capacity: {stats['hdd_capacity_tb']:.2f} TB (+{stats['hdd_capacity_tb'] - 4.0:.2f} TB)")
    print(f"SSD Efficiency: {stats['ssd_efficiency']:.3f}")
    print(f"HDD Efficiency: {stats['hdd_efficiency']:.3f}")
    
    print("\n✨ Quantum Storage Manager demonstration completed successfully!")

def demonstrate_cubical_spacing():
    """Demonstrate the cubical spacing arrangement for quantum states"""
    
    print("\n" + "=" * 50)
    print("📐 Cubical Spacing Demonstration")
    print("=" * 50)
    
    # Get the storage manager
    storage_manager = get_storage_manager()
    
    # Create different numbers of quantum states to show scaling
    state_counts = [1, 8, 27, 64]  # Perfect cubes for clean visualization
    
    for count in state_counts:
        print(f"\n📦 Arranging {count} quantum states in cubical spacing:")
        states = create_sample_quantum_states(count)
        arrangement = storage_manager.apply_cubical_spacing(states)
        
        cube_dim = arrangement['cube_dimensions']
        volume = arrangement['total_volume_m3']
        
        print(f"   Cube dimensions: {cube_dim[0]} × {cube_dim[1]} × {cube_dim[2]}")
        print(f"   Total volume: {volume:.2e} m³")
        print(f"   Cell size: {arrangement['cell_size_m']:.2e} m")

if __name__ == "__main__":
    # Demonstrate quantum storage management
    demonstrate_quantum_storage()
    
    # Demonstrate cubical spacing
    demonstrate_cubical_spacing()
    
    print("\n🎯 Quantum Storage Integration with SSD/HDD interlinking is ready!")
    print("   Features demonstrated:")
    print("   • Exponential storage capacity growth")
    print("   • Cubical spacing for optimal quantum state arrangement")
    print("   • SSD/HDD distribution based on access patterns")
    print("   • Enhanced retention and retrieval capabilities")