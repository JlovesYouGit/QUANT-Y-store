"""
Core module package initialization
"""
# This file makes the core directory a Python package

# Import core modules for easy access
try:
    from .code_structure_3d import initialize_3d_structure, get_optimal_3d_component
except ImportError:
    pass  # Handle case where dependencies aren't available

try:
    from .quantum_audio_engine import initialize_quantum_audio_space, render_quantum_audio, create_quantum_harmony
except ImportError:
    pass  # Handle case where dependencies aren't available

try:
    from .quantum_sonification import initialize_sonification_system, sonify_qubit, sonify_entanglement
except ImportError:
    pass  # Handle case where dependencies aren't available

try:
    from .quantum_circuit_renderer import initialize_circuit_renderer, render_quantum_circuit, create_quantum_composition
except ImportError:
    pass  # Handle case where dependencies aren't available