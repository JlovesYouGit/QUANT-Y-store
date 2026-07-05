"""
Quantum Circuit 3D Audio Renderer
Renders quantum circuits as immersive 3D audio experiences
"""

import math
from typing import List, Tuple, Dict, Any, Optional
from .quantum_audio_engine import QuantumAudioEngine
from .quantum_sonification import QuantumSonificationSystem

class QuantumCircuitRenderer:
    """Renders quantum circuits as 3D spatial audio experiences"""
    
    def __init__(self, audio_engine: QuantumAudioEngine, sonification_system: QuantumSonificationSystem):
        """Initialize the circuit renderer with audio and sonification systems"""
        self.audio_engine = audio_engine
        self.sonification_system = sonification_system
        self.circuit_operations = []
        self.qubit_tracks = {}
        
    def initialize_circuit_space(self, num_qubits: int):
        """
        Initialize the 3D space for rendering a quantum circuit
        
        Args:
            num_qubits: Number of qubits in the circuit
        """
        # Set up 3D space with qubits arranged along the Y-axis
        space_depth = max(5.0, num_qubits * 1.5)
        self.audio_engine.initialize_3d_space((10.0, num_qubits * 2.0, space_depth))
        
        # Initialize qubit tracks
        for i in range(num_qubits):
            qubit_id = f"q{i}"
            # Position qubits evenly along Y-axis
            position = (0, i * 2.0, 0)
            self.qubit_tracks[qubit_id] = {
                "position": position,
                "operations": [],
                "audio_buffer": None
            }
            
        print(f"🌀 Quantum Circuit Space initialized for {num_qubits} qubits")
        
    def add_quantum_gate(self, gate_name: str, target_qubits: List[str], parameters = None):
        """
        Add a quantum gate operation to the circuit
        
        Args:
            gate_name: Name of the quantum gate
            target_qubits: List of qubit identifiers the gate acts on
            parameters: Gate parameters (for parametric gates)
        """
        operation = {
            "gate": gate_name,
            "targets": target_qubits,
            "parameters": parameters or [],
            "time_step": len(self.circuit_operations)
        }
        
        self.circuit_operations.append(operation)
        
        # Add to individual qubit tracks
        for qubit in target_qubits:
            if qubit in self.qubit_tracks:
                self.qubit_tracks[qubit]["operations"].append(operation)
                
    def render_circuit_step(self, step_index: int):
        """
        Render audio for a specific step in the quantum circuit
        
        Args:
            step_index: Index of the circuit step to render
            
        Returns:
            Audio waveform for this step
        """
        if step_index >= len(self.circuit_operations):
            return []
            
        operation = self.circuit_operations[step_index]
        gate_name = operation["gate"]
        target_qubits = operation["targets"]
        
        # Sonify the gate operation for each target qubit
        step_audio = []
        for qubit in target_qubits:
            gate_audio_params = self.sonification_system.sonify_quantum_gate(
                gate_name, qubit, operation["parameters"]
            )
            
            if gate_audio_params:
                # Generate audio for this gate operation
                frequency = gate_audio_params["modified_frequency"]
                duration = gate_audio_params["duration"]
                
                # Get qubit position
                position = self.qubit_tracks[qubit]["position"]
                
                # Generate spatial waveform
                waveform = self.audio_engine.generate_spatial_waveform(
                    position, frequency, duration
                )
                step_audio.append(waveform)
                
        return step_audio
    
    def render_complete_circuit(self) -> List:
        """
        Render audio for the complete quantum circuit
        
        Returns:
            Combined audio waveform for the entire circuit
        """
        all_waveforms = []
        
        # Render each step of the circuit
        for i in range(len(self.circuit_operations)):
            step_audio = self.render_circuit_step(i)
            all_waveforms.extend(step_audio)
            
        # Combine all waveforms
        if not all_waveforms:
            return [[], []]  # Return empty stereo waveform
            
        # Mix all waveforms
        # For simplicity, we'll just take the first waveform as representative
        # In a full implementation, we would properly mix all audio
        return all_waveforms[0] if all_waveforms else [[], []]
    
    def create_qubit_interaction_audio(self, entangled_qubits: List[Tuple[str, str]]):
        """
        Create special audio effects for qubit interactions and entanglement
        
        Args:
            entangled_qubits: List of qubit pairs that are entangled
        """
        # Create harmonic representations of entanglement
        harmony = self.audio_engine.create_entanglement_harmony(entangled_qubits)
        return harmony
    
    def visualize_circuit_in_3d_audio_space(self):
        """
        Create a 3D audio map of the quantum circuit
        
        Returns:
            Dictionary mapping qubit positions to audio characteristics
        """
        audio_map = {}
        
        for qubit_id, track_info in self.qubit_tracks.items():
            position = track_info["position"]
            
            # Get audio parameters for this qubit's position
            audio_params = {
                "x": position[0],
                "y": position[1],
                "z": position[2],
                "frequency": 220 + position[1] * 50,  # Frequency based on Y position
                "pan": (position[2] + 5) / 10 if len(position) > 2 else 0.5  # Pan based on Z position
            }
            
            audio_map[qubit_id] = audio_params
            
        return audio_map

class QuantumCircuitSequencer:
    """Sequencer for playing quantum circuits as musical compositions"""
    
    def __init__(self, renderer: QuantumCircuitRenderer):
        """Initialize the sequencer with a circuit renderer"""
        self.renderer = renderer
        self.sequence = []
        self.tempo = 120  # BPM
        
    def add_circuit_section(self, operations: List[Dict], repeat_count: int = 1):
        """
        Add a section of circuit operations to the sequence
        
        Args:
            operations: List of circuit operations
            repeat_count: Number of times to repeat this section
        """
        section = {
            "operations": operations,
            "repeats": repeat_count
        }
        self.sequence.append(section)
        
    def set_tempo(self, bpm: int):
        """Set the tempo for the quantum music sequence"""
        self.tempo = bpm
        
    def generate_audio_sequence(self):
        """
        Generate the complete audio sequence for the quantum composition
        
        Returns:
            Combined audio waveform for the entire sequence
        """
        # This would combine all sections with timing based on tempo
        # For now, we'll just return a representative waveform
        return self.renderer.render_complete_circuit()

# Global instances
quantum_circuit_renderer = None
quantum_sequencer = None

def initialize_circuit_renderer(audio_engine: QuantumAudioEngine, sonification_system: QuantumSonificationSystem):
    """Initialize the global quantum circuit renderer"""
    global quantum_circuit_renderer, quantum_sequencer
    quantum_circuit_renderer = QuantumCircuitRenderer(audio_engine, sonification_system)
    quantum_sequencer = QuantumCircuitSequencer(quantum_circuit_renderer)
    return quantum_circuit_renderer

def render_quantum_circuit(num_qubits: int, operations: List[Dict]):
    """Render a quantum circuit as 3D audio"""
    if quantum_circuit_renderer:
        quantum_circuit_renderer.initialize_circuit_space(num_qubits)
        for op in operations:
            quantum_circuit_renderer.add_quantum_gate(
                op["gate"], op["targets"], op.get("parameters"))
        return quantum_circuit_renderer.render_complete_circuit()
    return [[], []]

def create_quantum_composition(sections: List[Dict], bpm: int = 120):
    """Create a musical composition from quantum circuit sections"""
    if quantum_sequencer:
        quantum_sequencer.set_tempo(bpm)
        for section in sections:
            quantum_sequencer.add_circuit_section(
                section["operations"], section.get("repeats", 1)
            )
        return quantum_sequencer.generate_audio_sequence()
    return [[], []]