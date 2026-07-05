"""
Enhanced Quantum Audio Engine with Environmental Awareness
Immersive audio system that translates quantum states into spatial soundscapes with environmental integration
"""

import math
from typing import Tuple, List, Dict, Any
from array import array
from .environmental_audio_processor import EnvironmentalAudioProcessor
from .sound_layer_masker import SoundLayerMasker

class EnhancedQuantumAudioEngine:
    """Enhanced 3D audio engine for quantum computing sonification with environmental awareness"""
    
    def __init__(self):
        """Initialize the enhanced quantum audio engine with environmental capabilities"""
        self.sample_rate = 44100
        self.spatial_positions = {}
        self.quantum_states = {}
        self.audio_buffers = {}
        self.environmental_processor = EnvironmentalAudioProcessor()
        self.sound_layer_masker = None
        self.environmental_layers = {}
        self.sound_masks = {}
        
    def initialize_3d_space(self, dimensions: Tuple[float, float, float] = (10.0, 10.0, 10.0)):
        """
        Initialize the 3D audio space for quantum state rendering with environmental layers
        
        Args:
            dimensions: 3D space dimensions (width, height, depth)
        """
        self.space_width, self.space_height, self.space_depth = dimensions
        print(f"🌌 Enhanced Quantum Audio Space initialized: {dimensions[0]}x{dimensions[1]}x{dimensions[2]} units")
        
        # Initialize environmental processing
        self.environmental_processor.initialize_environmental_layers()
        
    def initialize_environmental_awareness(self):
        """Initialize environmental awareness features"""
        # Set up environmental sound layers for quantum audio integration
        self.environmental_layers = {
            "quantum_background": {
                "type": "quantum_ambient",
                "frequency_range": (10, 100),  # Ultra-low frequency quantum ambient
                "intensity": 0.2,
                "spatial_spread": 1.0
            },
            "quantum_midground": {
                "type": "quantum_texture",
                "frequency_range": (100, 1000),  # Mid frequency quantum textures
                "intensity": 0.4,
                "spatial_spread": 0.8
            },
            "quantum_foreground": {
                "type": "quantum_detail",
                "frequency_range": (1000, 10000),  # High frequency quantum details
                "intensity": 0.8,
                "spatial_spread": 0.4
            }
        }
        
        print("🌍 Environmental awareness initialized for quantum audio immersion")
        
    def set_environment_type(self, environment_type: str):
        """
        Set the environmental type for sound masking
        
        Args:
            environment_type: Type of environment (forest, ocean, city, space, etc.)
        """
        self.current_environment = environment_type
        self.sound_masks = self.environmental_processor.create_natural_sound_mask(environment_type)
        
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
                                 duration: float = 1.0,
                                 quantum_phenomenon = None):
        """
        Generate a spatialized audio waveform based on 3D position with environmental awareness
        
        Args:
            position: 3D position (x, y, z)
            frequency: Base frequency in Hz
            duration: Duration in seconds
            quantum_phenomenon: Type of quantum phenomenon for environmental masking
            
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
        left_channel = [s * left_balance for s in waveform]
        right_channel = [s * right_balance for s in waveform]
        stereo_waveform = [left_channel, right_channel]
        
        # Apply environmental masking if specified
        if quantum_phenomenon and hasattr(self, 'current_environment'):
            # Create a sound mask for this quantum phenomenon
            mask_id = f"{quantum_phenomenon}_{self.current_environment}"
            if self.sound_layer_masker:
                stereo_waveform = self.sound_layer_masker.apply_layer_mask(
                    stereo_waveform, mask_id, position
                )
            else:
                # Apply basic environmental blending
                stereo_waveform = self.environmental_processor.apply_spatial_filtering(
                    stereo_waveform, position, "quantum_foreground"
                )
        
        return stereo_waveform
    
    def render_quantum_state_audio(self, qubit_id: str, state_vector: List[complex], 
                                  environment_aware: bool = True):
        """
        Render audio for a quantum state in 3D space with environmental awareness
        
        Args:
            qubit_id: Qubit identifier
            state_vector: Quantum state vector
            environment_aware: Whether to apply environmental processing
            
        Returns:
            Stereo audio waveform
        """
        # Map quantum state to 3D position
        position = self.map_quantum_state_to_position(qubit_id, state_vector)
        
        # Determine frequency based on quantum state
        alpha, beta = state_vector[0], state_vector[1]
        base_frequency = 220 + 220 * abs(beta)  # Range from 220Hz to 440Hz
        
        # Generate spatialized waveform with environmental awareness
        if environment_aware and hasattr(self, 'current_environment'):
            waveform = self.generate_spatial_waveform(
                position, base_frequency, 0.5, "qubit_state"
            )
        else:
            waveform = self.generate_spatial_waveform(position, base_frequency, 0.5)
        
        # Store for later use
        self.audio_buffers[qubit_id] = waveform
        
        return waveform
    
    def create_entanglement_harmony(self, qubit_pairs: List[Tuple[str, str]], 
                                   environment_aware: bool = True):
        """
        Create harmonic audio representation of quantum entanglement with environmental awareness
        
        Args:
            qubit_pairs: List of entangled qubit pairs
            environment_aware: Whether to apply environmental processing
            
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
                
                min_length = min(len(self.audio_buffers[q1][0]), len(self.audio_buffers[q2][0]))
                for i in range(min_length):
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
            
            stereo_waveform = [mixed_left, mixed_right]
            
            # Apply environmental blending if requested
            if environment_aware and hasattr(self, 'current_environment'):
                stereo_waveform = self.environmental_processor.blend_with_environment(
                    stereo_waveform, self.current_environment, 0.6
                )
            
            return stereo_waveform
        
        return [[], []]
    
    def get_spatial_audio_parameters(self, qubit_id: str) -> Dict[str, Any]:
        """
        Get spatial audio parameters for a qubit with environmental context
        
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
        
        # Add environmental context
        params = {
            "position": (x, y, z),
            "frequency": 220 + 220 * (y / self.space_height),
            "pan": (z + self.space_depth/2) / self.space_depth,  # 0=left, 1=right
            "intensity": spatial_distance / max_distance if max_distance > 0 else 0,
            "environment": getattr(self, 'current_environment', 'space')
        }
        
        return params
    
    def render_environmental_quantum_experience(self, quantum_audio: List[List[float]], 
                                              blend_ratio: float = 0.7) -> List[List[float]]:
        """
        Render a complete environmental quantum audio experience
        
        Args:
            quantum_audio: Quantum audio data as [left_channel, right_channel]
            blend_ratio: Ratio of environmental sound to quantum sound (0.0 to 1.0)
            
        Returns:
            Fully immersive environmental quantum audio
        """
        if hasattr(self, 'current_environment'):
            return self.environmental_processor.blend_with_environment(
                quantum_audio, self.current_environment, blend_ratio
            )
        return quantum_audio

# Global instance
enhanced_quantum_audio_engine = EnhancedQuantumAudioEngine()

def initialize_enhanced_quantum_audio_space():
    """Initialize the global enhanced quantum audio engine"""
    global enhanced_quantum_audio_engine
    enhanced_quantum_audio_engine.initialize_3d_space()
    enhanced_quantum_audio_engine.initialize_environmental_awareness()
    return enhanced_quantum_audio_engine

def set_audio_environment(environment_type: str):
    """Set the environmental type for quantum audio"""
    enhanced_quantum_audio_engine.set_environment_type(environment_type)

def render_enhanced_quantum_audio(qubit_id: str, state_vector: List[complex], 
                                 environment_aware: bool = True):
    """Render enhanced audio for a quantum state with environmental awareness"""
    return enhanced_quantum_audio_engine.render_quantum_state_audio(
        qubit_id, state_vector, environment_aware
    )

def create_enhanced_quantum_harmony(entangled_pairs: List[Tuple[str, str]], 
                                   environment_aware: bool = True):
    """Create enhanced audio harmony for entangled qubits with environmental awareness"""
    return enhanced_quantum_audio_engine.create_entanglement_harmony(
        entangled_pairs, environment_aware
    )