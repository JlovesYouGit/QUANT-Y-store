"""
Quantum Audio Engine with 3D Spatial Sound Rendering
Immersive audio system that translates quantum states into spatial soundscapes
"""

import math
from typing import Tuple, List, Dict, Any
from array import array

class QuantumAudioEngine:
    """3D audio engine for quantum computing sonification"""
    
    def __init__(self):
        """Initialize the quantum audio engine with spatial audio capabilities"""
        self.sample_rate = 44100
        self.spatial_positions = {}
        self.quantum_states = {}
        self.audio_buffers = {}
        
    def initialize_3d_space(self, dimensions: Tuple[float, float, float] = (10.0, 10.0, 10.0)):
        """
        Initialize the 3D audio space for quantum state rendering
        
        Args:
            dimensions: 3D space dimensions (width, height, depth)
        """
        self.space_width, self.space_height, self.space_depth = dimensions
        print(f"🌌 Quantum Audio Space initialized: {dimensions[0]}x{dimensions[1]}x{dimensions[2]} units")
        
    def map_quantum_state_to_position(self, qubit_id: str, state_vector: List[complex]) -> Tuple[float, float, float]:
        """
        Map a quantum state vector to a 3D spatial position
        
        Args:
            qubit_id: Unique identifier for the qubit
            state_vector: Quantum state vector [α, β] where |α|² + |β|² = 1
            
        Returns:
            3D position (x, y, z) in the audio space
        """
        # Extract probability amplitudes
        alpha, beta = state_vector[0], state_vector[1]
        
        # Calculate probabilities
        prob_0 = abs(alpha) ** 2
        prob_1 = abs(beta) ** 2
        
        # Map to 3D space based on quantum probabilities
        x = prob_0 * self.space_width
        y = prob_1 * self.space_height
        z = (prob_0 - prob_1) * self.space_depth / 2
        
        # Store position
        self.spatial_positions[qubit_id] = (x, y, z)
        
        return (x, y, z)
    
    def generate_spatial_waveform(self, position: Tuple[float, float, float], 
                                 frequency: float = 440.0, 
                                 duration: float = 1.0):
        """
        Generate a spatialized audio waveform based on 3D position
        
        Args:
            position: 3D position (x, y, z)
            frequency: Base frequency in Hz
            duration: Duration in seconds
            
        Returns:
            Audio waveform as array
        """
        x, y, z = position
        num_samples = int(self.sample_rate * duration)
        
        # Create waveform using sine wave approximation
        waveform = array('d')  # Double precision array
        
        for i in range(num_samples):
            t = i / self.sample_rate
            # Generate base waveform
            sample = math.sin(2 * math.pi * frequency * t)
            waveform.append(sample)
        
        # Apply spatial effects
        # Z-position affects stereo balance
        left_balance = max(0, min(1, (z + self.space_depth/2) / self.space_depth))
        right_balance = 1 - left_balance
        
        # Create stereo waveform approximation
        stereo_waveform = [
            [s * left_balance for s in waveform],
            [s * right_balance for s in waveform]
        ]
        
        return stereo_waveform
    
    def render_quantum_state_audio(self, qubit_id: str, state_vector: List[complex]):
        """
        Render audio for a quantum state in 3D space
        
        Args:
            qubit_id: Qubit identifier
            state_vector: Quantum state vector
            
        Returns:
            Stereo audio waveform
        """
        # Map quantum state to 3D position
        position = self.map_quantum_state_to_position(qubit_id, state_vector)
        
        # Determine frequency based on quantum state
        alpha, beta = state_vector[0], state_vector[1]
        base_frequency = 220 + 220 * abs(beta)  # Range from 220Hz to 440Hz
        
        # Generate spatialized waveform
        waveform = self.generate_spatial_waveform(position, base_frequency, 0.5)
        
        # Store for later use
        self.audio_buffers[qubit_id] = waveform
        
        return waveform
    
    def create_entanglement_harmony(self, qubit_pairs: List[Tuple[str, str]]):
        """
        Create harmonic audio representation of quantum entanglement
        
        Args:
            qubit_pairs: List of entangled qubit pairs
            
        Returns:
            Combined stereo waveform representing entanglement
        """
        if not qubit_pairs:
            return [[], []]  # Empty stereo array
            
        # Get waveforms for all qubits in pairs
        waveforms = []
        for q1, q2 in qubit_pairs:
            if q1 in self.audio_buffers and q2 in self.audio_buffers:
                # Combine waveforms with phase correlation to represent entanglement
                left_combined = []
                right_combined = []
                
                for i in range(min(len(self.audio_buffers[q1][0]), len(self.audio_buffers[q2][0]))):
                    left_combined.append((self.audio_buffers[q1][0][i] + self.audio_buffers[q2][0][i]) / 2)
                    right_combined.append((self.audio_buffers[q1][1][i] + self.audio_buffers[q2][1][i]) / 2)
                
                waveforms.append([left_combined, right_combined])
                
        if not waveforms:
            return [[], []]
            
        # Mix all waveforms
        if len(waveforms) > 0:
            mixed_left = [sum(w[0][i] for w in waveforms) for i in range(len(waveforms[0][0]))]
            mixed_right = [sum(w[1][i] for w in waveforms) for i in range(len(waveforms[0][1]))]
            
            # Normalize to prevent clipping
            max_amp = max(max(abs(s) for s in mixed_left), max(abs(s) for s in mixed_right)) if mixed_left and mixed_right else 1
            if max_amp > 0:
                mixed_left = [s / max_amp * 0.8 for s in mixed_left]  # 80% volume to leave headroom
                mixed_right = [s / max_amp * 0.8 for s in mixed_right]
            
            return [mixed_left, mixed_right]
        
        return [[], []]
    
    def get_spatial_audio_parameters(self, qubit_id: str) -> Dict[str, Any]:
        """
        Get spatial audio parameters for a qubit
        
        Args:
            qubit_id: Qubit identifier
            
        Returns:
            Dictionary of audio parameters
        """
        if qubit_id not in self.spatial_positions:
            return {}
            
        x, y, z = self.spatial_positions[qubit_id]
        
        # Calculate spatial parameters
        spatial_distance = math.sqrt(x**2 + y**2 + z**2)
        max_distance = math.sqrt(self.space_width**2 + self.space_height**2 + self.space_depth**2)
        
        return {
            "position": (x, y, z),
            "frequency": 220 + 220 * (y / self.space_height),
            "pan": (z + self.space_depth/2) / self.space_depth,  # 0=left, 1=right
            "intensity": spatial_distance / max_distance if max_distance > 0 else 0
        }

# Global instance
quantum_audio_engine = QuantumAudioEngine()

def initialize_quantum_audio_space():
    """Initialize the global quantum audio engine"""
    global quantum_audio_engine
    quantum_audio_engine.initialize_3d_space()
    return quantum_audio_engine

def render_quantum_audio(qubit_id: str, state_vector: List[complex]):
    """Render audio for a quantum state"""
    return quantum_audio_engine.render_quantum_state_audio(qubit_id, state_vector)

def create_quantum_harmony(entangled_pairs: List[Tuple[str, str]]):
    """Create audio harmony for entangled qubits"""
    return quantum_audio_engine.create_entanglement_harmony(entangled_pairs)