"""
Hardware-Adaptive Quantum Storage Demo
Demonstrates the interlinking of quantum states with RAM/SSD/HDD storage using cubical spacing
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import our quantum storage manager
from src.core.quantum_storage_manager import get_storage_manager

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

def demonstrate_hardware_adaptive_storage():
    """Demonstrate hardware-adaptive quantum storage management"""
    
    print("🖥️  Hardware-Adaptive Quantum Storage Manager Demo")
    print("=" * 55)
    
    # Get the storage manager
    storage_manager = get_storage_manager()
    
    # Show system hardware specifications
    print("\n🖥️  System Hardware Specifications:")
    hardware_specs = storage_manager.hardware_specs
    print(f"RAM Capacity: {hardware_specs['ram_gb']:.2f} GB")
    print(f"SSD Capacity: {hardware_specs['ssd_tb']:.2f} TB")
    print(f"HDD Capacity: {hardware_specs['hdd_tb']:.2f} TB")
    
    # Show initial storage characteristics
    print("\n⚙️  Storage Device Characteristics:")
    ram_chars = storage_manager.ram_characteristics
    ssd_chars = storage_manager.ssd_characteristics
    hdd_chars = storage_manager.hdd_characteristics
    
    print(f"RAM: {ram_chars['current_capacity_gb']:.2f} GB, Efficiency: {ram_chars['quantum_coupling_efficiency']:.2f}, Latency: {ram_chars['latency_us']:.1f}μs")
    print(f"SSD: {ssd_chars['current_capacity_tb']:.2f} TB, Efficiency: {ssd_chars['quantum_coupling_efficiency']:.2f}, Latency: {ssd_chars['latency_us']:.0f}μs")
    print(f"HDD: {hdd_chars['current_capacity_tb']:.2f} TB, Efficiency: {hdd_chars['quantum_coupling_efficiency']:.2f}, Latency: {hdd_chars['latency_us']:.0f}μs")
    
    # Create sample quantum states
    print("\n⚡ Creating 100 sample quantum states...")
    quantum_states = create_sample_quantum_states(100)
    print(f"Created {len(quantum_states)} quantum states")
    
    # Save quantum states with metadata
    print("\n💾 Saving quantum states to hardware-adaptive storage...")
    metadata = {
        "experiment_id": "HARDWARE_ADAPTIVE_DEMO_001",
        "researcher": "Quantum DevOps Team",
        "purpose": "Hardware-adaptive storage demonstration"
    }
    
    result = storage_manager.save_quantum_states(quantum_states, metadata)
    print(f"Successfully saved {result['states_saved']} quantum states")
    print(f"Storage distribution: {result['storage_distribution']}")
    print(f"Spatial volume: {result['spatial_arrangement']['total_volume_m3']:.2e} m³")
    
    # Show updated storage statistics
    print("\n📈 Hardware-Adaptive Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    print(f"Total Quantum States: {stats['total_quantum_states']}")
    print(f"RAM Stored States: {stats['ram_stored_states']}")
    print(f"SSD Stored States: {stats['ssd_stored_states']}")
    print(f"HDD Stored States: {stats['hdd_stored_states']}")
    
    # Apply storage enhancement
    print("\n🚀 Applying storage capacity enhancement...")
    enhancement_result = storage_manager.enhance_storage_capacity(enhancement_cycles=5)
    print(f"Applied {enhancement_result['enhancement_cycles']} enhancement cycles")
    print(f"New SSD Capacity: {enhancement_result['new_ssd_capacity_tb']:.2f} TB")
    print(f"New HDD Capacity: {enhancement_result['new_hdd_capacity_tb']:.2f} TB")
    print(f"Improved SSD Efficiency: {enhancement_result['improved_ssd_efficiency']:.3f}")
    print(f"Improved HDD Efficiency: {enhancement_result['improved_hdd_efficiency']:.3f}")
    
    # Show final storage statistics
    print("\n📊 Final Hardware-Adaptive Storage Statistics:")
    stats = storage_manager.get_storage_statistics()
    print(f"RAM Capacity: {stats['ram_capacity_gb']:.2f} GB")
    print(f"SSD Capacity: {stats['ssd_capacity_tb']:.2f} TB (+{stats['ssd_capacity_tb'] - hardware_specs['ssd_tb']:.2f} TB)")
    print(f"HDD Capacity: {stats['hdd_capacity_tb']:.2f} TB (+{stats['hdd_capacity_tb'] - hardware_specs['hdd_tb']:.2f} TB)")
    print(f"RAM Efficiency: {stats['ram_efficiency']:.3f}")
    print(f"SSD Efficiency: {stats['ssd_efficiency']:.3f}")
    print(f"HDD Efficiency: {stats['hdd_efficiency']:.3f}")
    
    print("\n✨ Hardware-Adaptive Quantum Storage Manager demonstration completed successfully!")

def demonstrate_storage_optimization():
    """Demonstrate storage optimization based on hardware capabilities"""
    
    print("\n" + "=" * 55)
    print("⚙️  Storage Optimization Based on Hardware Capabilities")
    print("=" * 55)
    
    # Get the storage manager
    storage_manager = get_storage_manager()
    
    # Show different storage distributions based on state count
    state_counts = [10, 50, 100, 500]
    
    for count in state_counts:
        print(f"\n📦 Optimizing storage for {count} quantum states:")
        states = create_sample_quantum_states(count)
        distribution = storage_manager.distribute_across_storage_media(states)
        
        total = sum(len(v) for v in distribution.values())
        ram_pct = (len(distribution['ram']) / total) * 100 if total > 0 else 0
        ssd_pct = (len(distribution['ssd']) / total) * 100 if total > 0 else 0
        hdd_pct = (len(distribution['hdd']) / total) * 100 if total > 0 else 0
        
        print(f"   RAM:  {len(distribution['ram']):3d} states ({ram_pct:5.1f}%) - Fastest access")
        print(f"   SSD:  {len(distribution['ssd']):3d} states ({ssd_pct:5.1f}%) - Fast access")
        print(f"   HDD:  {len(distribution['hdd']):3d} states ({hdd_pct:5.1f}%) - Archival storage")

if __name__ == "__main__":
    # Demonstrate hardware-adaptive quantum storage management
    demonstrate_hardware_adaptive_storage()
    
    # Demonstrate storage optimization
    demonstrate_storage_optimization()
    
    print("\n🎯 Hardware-Adaptive Quantum Storage Integration is ready!")
    print("   Features demonstrated:")
    print("   • Automatic hardware detection (RAM, SSD, HDD)")
    print("   • Hardware-adaptive storage distribution")
    print("   • Cubical spacing for optimal quantum state arrangement")
    print("   • RAM/SSD/HDD distribution based on access patterns")
    print("   • Enhanced retention and retrieval capabilities")
    print("   • Exponential storage capacity growth")