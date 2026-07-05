"""
Quantum State Sonification System
Translates quantum mechanical properties into audio parameters for immersive experiences
"""

import math
from typing import List, Tuple, Dict
from .quantum_audio_engine import QuantumAudioEngine

class QuantumSonificationSystem:
    """System for converting quantum states and operations into audio representations"""
    
    def __init__(self, audio_engine: QuantumAudioEngine):
        """Initialize the sonification system with an audio engine"""
        self.audio_engine = audio_engine
        self.quantum_states = {}
        self.circuit_operations = {}
        
    def sonify_qubit_state(self, qubit_id: str, alpha: complex, beta: complex) -> Dict:
        """
        Convert a single qubit state into audio parameters
        
        Args:
            qubit_id: Identifier for the qubit
            alpha: Probability amplitude for |0⟩ state
            beta: Probability amplitude for |1⟩ state
            
        Returns:
            Dictionary of audio parameters
        """
        # Store the quantum state
        self.quantum_states[qubit_id] = [alpha, beta]
        
        # Calculate probabilities
        prob_0 = abs(alpha) ** 2
        prob_1 = abs(beta) ** 2
        
        # Map quantum properties to audio parameters
        # Frequency represents the balance between |0⟩ and |1⟩ states
        base_frequency = 220 + 220 * prob_1  # Range from 220Hz to 440Hz
        
        # Amplitude represents the coherence of the state
        coherence = abs(alpha * beta.conjugate())  # Off-diagonal element of density matrix
        amplitude = 0.5 + 0.5 * coherence.real
        
        # Spatial position based on quantum probabilities
        position = self.audio_engine.map_quantum_state_to_position(qubit_id, [alpha, beta])
        
        # Phase difference affects timbre
        phase_diff = math.atan2(beta.imag, beta.real) - math.atan2(alpha.imag, alpha.real)
        timbre_parameter = (phase_diff + math.pi) / (2 * math.pi)  # Normalize to 0-1
        
        return {
            "frequency": base_frequency,
            "amplitude": amplitude,
            "position": position,
            "timbre": timbre_parameter,
            "probability_0": prob_0,
            "probability_1": prob_1
        }
    
    def sonify_superposition_state(self, qubit_id: str, states: List[Tuple[complex, complex, float]]) -> Dict:
        """
        Sonify a superposition state composed of multiple basis states
        
        Args:
            qubit_id: Identifier for the qubit
            states: List of (alpha, beta, weight) tuples representing component states
            
        Returns:
            Dictionary of composite audio parameters
        """
        # Calculate weighted average of audio parameters
        total_weight = sum(weight for _, _, weight in states)
        
        avg_frequency = 0
        avg_amplitude = 0
        avg_timbre = 0
        total_prob_0 = 0
        total_prob_1 = 0
        
        positions = []
        
        for alpha, beta, weight in states:
            prob_0 = abs(alpha) ** 2
            prob_1 = abs(beta) ** 2
            
            # Weighted contributions
            normalized_weight = weight / total_weight if total_weight > 0 else 0
            avg_frequency += (220 + 220 * prob_1) * normalized_weight
            avg_amplitude += (0.5 + 0.5 * abs(alpha * beta.conjugate())) * normalized_weight
            avg_timbre += (((math.atan2(beta.imag, beta.real) - math.atan2(alpha.imag, alpha.real)) + math.pi) / (2 * math.pi)) * normalized_weight
            total_prob_0 += prob_0 * normalized_weight
            total_prob_1 += prob_1 * normalized_weight
            
            # Map each component to position
            position = self.audio_engine.map_quantum_state_to_position(f"{qubit_id}_comp", [alpha, beta])
            positions.append(position)
        
        # Average position
        if positions:
            avg_x = sum(pos[0] for pos in positions) / len(positions)
            avg_y = sum(pos[1] for pos in positions) / len(positions)
            avg_z = sum(pos[2] for pos in positions) / len(positions)
            avg_position = (avg_x, avg_y, avg_z)
        else:
            avg_position = (0, 0, 0)
        
        return {
            "frequency": avg_frequency,
            "amplitude": avg_amplitude,
            "position": avg_position,
            "timbre": avg_timbre,
            "probability_0": total_prob_0,
            "probability_1": total_prob_1,
            "component_count": len(states)
        }
    
    def sonify_entanglement(self, qubit_pair: Tuple[str, str], correlation_strength: float = 1.0) -> Dict:
        """
        Sonify quantum entanglement between two qubits
        
        Args:
            qubit_pair: Tuple of two qubit identifiers
            correlation_strength: Strength of entanglement (0.0 to 1.0)
            
        Returns:
            Dictionary of entanglement audio parameters
        """
        q1, q2 = qubit_pair
        
        # Get individual qubit parameters
        params1 = self.audio_engine.get_spatial_audio_parameters(q1)
        params2 = self.audio_engine.get_spatial_audio_parameters(q2)
        
        if not params1 or not params2:
            return {}
        
        # Create correlated audio effects
        # Distance between qubits affects harmony
        pos1, pos2 = params1["position"], params2["position"]
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
        
        # Correlation affects stereo positioning
        correlation_pan = (params1["pan"] + params2["pan"]) / 2
        
        # Entanglement strength affects modulation depth
        modulation_depth = correlation_strength * 0.5
        
        return {
            "distance": distance,
            "correlation_pan": correlation_pan,
            "modulation_depth": modulation_depth,
            "harmonic_tension": distance / 10.0,  # Normalize by space size
            "qubit_pair": qubit_pair
        }
    
    def sonify_quantum_gate(self, gate_name: str, target_qubit: str, parameters = None) -> Dict[str, float]:
        """
        Sonify quantum gate operations
        
        Args:
            gate_name: Name of the quantum gate
            target_qubit: Qubit the gate acts on
            parameters: Gate parameters (for parametric gates)
            
        Returns:
            Dictionary of gate audio parameters
        """
        # Map gate types to audio characteristics
        gate_sounds = {
            "H": {"frequency_multiplier": 1.5, "timbre_shift": 0.2, "duration": 0.1},      # Hadamard
            "X": {"frequency_multiplier": 2.0, "timbre_shift": 0.1, "duration": 0.05},     # Pauli-X
            "Y": {"frequency_multiplier": 1.8, "timbre_shift": 0.3, "duration": 0.05},     # Pauli-Y
            "Z": {"frequency_multiplier": 1.2, "timbre_shift": 0.4, "duration": 0.05},     # Pauli-Z
            "R": {"frequency_multiplier": 1.3, "timbre_shift": 0.25, "duration": 0.15},    # Rotation
            "CNOT": {"frequency_multiplier": 2.5, "timbre_shift": 0.15, "duration": 0.2}   # CNOT
        }
        
        # Get base parameters for target qubit
        base_params = self.audio_engine.get_spatial_audio_parameters(target_qubit)
        if not base_params:
            return {}
        
        # Apply gate-specific modifications
        gate_sound = gate_sounds.get(gate_name, {"frequency_multiplier": 1.0, "timbre_shift": 0.0, "duration": 0.1})
        
        return {
            "base_frequency": float(base_params["frequency"]),
            "modified_frequency": float(base_params["frequency"] * gate_sound["frequency_multiplier"]),
            "timbre_shift": float(gate_sound["timbre_shift"]),
            "duration": float(gate_sound["duration"])
        }
    
    def create_quantum_audio_waveform(self, qubit_id: str, alpha: complex, beta: complex):
        """
        Create an audio waveform representing a quantum state
        
        Args:
            qubit_id: Identifier for the qubit
            alpha: Probability amplitude for |0⟩ state
            beta: Probability amplitude for |1⟩ state
            
        Returns:
            Audio waveform
        """
        # Render audio using the engine
        waveform = self.audio_engine.render_quantum_state_audio(qubit_id, [alpha, beta])
        return waveform

# Global instance
quantum_sonification_system = None

def initialize_sonification_system(audio_engine: QuantumAudioEngine):
    """Initialize the global quantum sonification system"""
    global quantum_sonification_system
    quantum_sonification_system = QuantumSonificationSystem(audio_engine)
    return quantum_sonification_system

def sonify_qubit(qubit_id: str, alpha: complex, beta: complex):
    """Sonify a single qubit state"""
    if quantum_sonification_system:
        return quantum_sonification_system.sonify_qubit_state(qubit_id, alpha, beta)
    return {}

def sonify_entanglement(qubit_pair: Tuple[str, str], correlation_strength: float = 1.0):
    """Sonify quantum entanglement between qubits"""
    if quantum_sonification_system:
        return quantum_sonification_system.sonify_entanglement(qubit_pair, correlation_strength)
    return {}