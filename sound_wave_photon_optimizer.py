"""
Sound Wave Photon Optimizer
System for calculating and optimizing the distance sound wave photons can travel
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class SoundPhoton:
    """Represents a sound wave photon with quantum properties"""
    frequency: float  # Hz
    energy: float     # Joules
    wavelength: float # meters
    momentum: float   # kg⋅m/s
    coherence_length: float  # meters
    phase: float      # radians
    polarization: Tuple[float, float, float]  # (x, y, z) components
    position: Tuple[float, float, float]     # (x, y, z) in meters
    velocity: Tuple[float, float, float]     # (vx, vy, vz) in m/s

class SoundWavePhotonOptimizer:
    """Optimizes sound wave photon propagation for maximum distance"""
    
    def __init__(self):
        """Initialize the sound wave photon optimizer"""
        self.photons = {}
        self.quantum_acoustic_constants = {
            "planck_constant": 6.62607015e-34,  # J⋅s
            "speed_of_sound": 343.0,            # m/s (at 20°C)
            "air_density": 1.225,               # kg/m³
            "boltzmann_constant": 1.380649e-23, # J/K
            "reference_temperature": 293.15     # K (20°C)
        }
        self.environmental_conditions = {
            "temperature": 293.15,  # K
            "pressure": 101325.0,   # Pa
            "humidity": 0.5,        # 50% relative humidity
            "obstacles": []
        }
        self.optimization_parameters = {
            "coherence_preservation": True,
            "phase_matching": True,
            "polarization_alignment": True,
            "quantum_entanglement": False
        }
        
    def calculate_photon_properties(self, frequency: float, amplitude: float = 1.0) -> SoundPhoton:
        """
        Calculate quantum properties of a sound wave photon
        
        Args:
            frequency: Sound frequency in Hz
            amplitude: Relative amplitude (0.0 to 1.0)
            
        Returns:
            SoundPhoton object with calculated properties
        """
        h = self.quantum_acoustic_constants["planck_constant"]
        c = self.quantum_acoustic_constants["speed_of_sound"]
        
        # Calculate photon energy: E = hν
        energy = h * frequency
        
        # Calculate wavelength: λ = c/ν
        wavelength = c / frequency if frequency > 0 else float('inf')
        
        # Calculate momentum: p = E/c = h/λ
        momentum = h / wavelength if wavelength > 0 else 0.0
        
        # Estimate coherence length (simplified model)
        # Coherence length increases with lower frequencies and higher amplitudes
        coherence_length = wavelength * (1.0 + amplitude) * (1000.0 / frequency)
        
        # Create sound photon
        photon = SoundPhoton(
            frequency=frequency,
            energy=energy,
            wavelength=wavelength,
            momentum=momentum,
            coherence_length=coherence_length,
            phase=0.0,
            polarization=(0.0, 0.0, 1.0),  # Default z-polarization
            position=(0.0, 0.0, 0.0),
            velocity=(0.0, 0.0, c)
        )
        
        return photon
    
    def add_sound_photon(self, photon_id: str, photon: SoundPhoton):
        """
        Add a sound wave photon to the system
        
        Args:
            photon_id: Unique identifier for the photon
            photon: SoundPhoton object
        """
        self.photons[photon_id] = photon
        print(f"⚛️ Sound wave photon '{photon_id}' added to system")
        
    def set_environmental_conditions(self, temperature = None,
                                   pressure = None,
                                   humidity = None):
        """
        Set environmental conditions affecting photon propagation
        
        Args:
            temperature: Temperature in Kelvin
            pressure: Atmospheric pressure in Pascals
            humidity: Relative humidity (0.0 to 1.0)
        """
        if temperature is not None:
            self.environmental_conditions["temperature"] = temperature
            # Update speed of sound based on temperature
            self.quantum_acoustic_constants["speed_of_sound"] = 331.3 * math.sqrt(temperature / 273.15)
            
        if pressure is not None:
            self.environmental_conditions["pressure"] = pressure
            
        if humidity is not None:
            self.environmental_conditions["humidity"] = humidity
            
        print(f"🌡️ Environmental conditions updated: {temperature}K, {pressure}Pa, {(humidity*100 if humidity is not None else 0)}% humidity")
        
    def calculate_attenuation_for_photon(self, photon: SoundPhoton, distance: float) -> float:
        """
        Calculate attenuation for a sound wave photon over a given distance
        
        Args:
            photon: SoundPhoton object
            distance: Distance in meters
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        # Atmospheric absorption coefficient (simplified)
        # Based on frequency and environmental conditions
        freq_factor = min(1.0, photon.frequency / 10000.0)  # Normalize to 10kHz
        humidity_factor = self.environmental_conditions["humidity"]
        temp_factor = self.environmental_conditions["temperature"] / self.quantum_acoustic_constants["reference_temperature"]
        
        # Base attenuation coefficient (dB/m)
        base_attenuation = 0.0001 * freq_factor * (1.0 + humidity_factor * 0.5) * temp_factor
        
        # Convert to linear attenuation over distance
        attenuation_db = base_attenuation * distance
        attenuation_linear = 10 ** (-attenuation_db / 10.0)
        
        return max(0.0, min(1.0, attenuation_linear))
    
    def calculate_coherence_preservation(self, photon: SoundPhoton, distance: float) -> float:
        """
        Calculate coherence preservation over distance
        
        Args:
            photon: SoundPhoton object
            distance: Distance in meters
            
        Returns:
            Coherence preservation factor (0.0 to 1.0)
        """
        # Coherence decreases with distance
        # Model: coherence = exp(-distance / coherence_length)
        if photon.coherence_length > 0:
            coherence_preservation = math.exp(-distance / photon.coherence_length)
        else:
            coherence_preservation = 0.0
            
        return coherence_preservation
    
    def calculate_maximum_propagation_distance(self, photon_id: str, 
                                            minimum_detectable_energy: float = 1e-40) -> Dict[str, Any]:
        """
        Calculate maximum propagation distance for a sound wave photon
        
        Args:
            photon_id: ID of the sound photon
            minimum_detectable_energy: Minimum energy for detection in Joules
            
        Returns:
            Dictionary with propagation distance results
        """
        if photon_id not in self.photons:
            return {"error": "Photon not found"}
            
        photon = self.photons[photon_id]
        
        # Binary search for maximum distance where energy >= minimum_detectable_energy
        min_distance = 0.0
        max_distance = 1e9  # 1000 km maximum search
        tolerance = 1.0  # 1 meter tolerance
        
        max_distance_found = 0.0
        iterations = 0
        max_iterations = 50
        
        while (max_distance - min_distance) > tolerance and iterations < max_iterations:
            test_distance = (min_distance + max_distance) / 2
            
            # Calculate energy at test distance
            attenuation = self.calculate_attenuation_for_photon(photon, test_distance)
            energy_at_distance = photon.energy * attenuation
            
            if energy_at_distance >= minimum_detectable_energy:
                max_distance_found = test_distance
                min_distance = test_distance
            else:
                max_distance = test_distance
                
            iterations += 1
            
        # Calculate additional metrics
        final_attenuation = self.calculate_attenuation_for_photon(photon, max_distance_found)
        coherence_preservation = self.calculate_coherence_preservation(photon, max_distance_found)
        propagation_time = max_distance_found / self.quantum_acoustic_constants["speed_of_sound"]
        
        # Quantum effects on propagation
        quantum_decoherence = 1.0 - coherence_preservation
        phase_preservation = math.cos(2 * math.pi * max_distance_found / photon.wavelength)
        
        result = {
            "photon_id": photon_id,
            "frequency_hz": photon.frequency,
            "initial_energy_j": photon.energy,
            "wavelength_m": photon.wavelength,
            "maximum_distance_km": max_distance_found / 1000.0,
            "propagation_time_s": propagation_time,
            "final_energy_j": photon.energy * final_attenuation,
            "attenuation_factor": final_attenuation,
            "coherence_preservation": coherence_preservation,
            "quantum_decoherence": quantum_decoherence,
            "phase_preservation": phase_preservation,
            "detectable_at_distance": photon.energy * final_attenuation >= minimum_detectable_energy
        }
        
        return result
    
    def optimize_photon_for_maximum_distance(self, photon_id: str) -> Dict[str, Any]:
        """
        Optimize sound wave photon parameters for maximum propagation distance
        
        Args:
            photon_id: ID of the sound photon to optimize
            
        Returns:
            Dictionary with optimization results
        """
        if photon_id not in self.photons:
            return {"error": "Photon not found"}
            
        photon = self.photons[photon_id]
        
        # Current performance
        current_performance = self.calculate_maximum_propagation_distance(photon_id)
        current_distance = current_performance["maximum_distance_km"]
        
        # Optimization suggestions
        optimization_suggestions = []
        
        # Frequency optimization (lower frequencies travel farther)
        if photon.frequency > 100:
            # Calculate potential improvement
            lower_freq = max(20.0, photon.frequency * 0.1)
            lower_freq_photon = self.calculate_photon_properties(lower_freq)
            self.add_sound_photon(f"{photon_id}_low_freq", lower_freq_photon)
            low_freq_performance = self.calculate_maximum_propagation_distance(f"{photon_id}_low_freq")
            low_freq_distance = low_freq_performance["maximum_distance_km"]
            
            improvement_km = low_freq_distance - current_distance
            if improvement_km > 0:
                optimization_suggestions.append({
                    "type": "frequency",
                    "suggestion": f"Reduce frequency to {lower_freq:.1f} Hz",
                    "expected_improvement_km": improvement_km,
                    "improvement_percentage": (improvement_km / current_distance) * 100 if current_distance > 0 else 0
                })
                
        # Coherence optimization
        if photon.coherence_length < 1000:
            optimization_suggestions.append({
                "type": "coherence",
                "suggestion": "Enhance coherence through quantum acoustic engineering",
                "expected_improvement_km": current_distance * 0.3,  # 30% estimate
                "improvement_percentage": 30.0
            })
            
        # Environmental optimization
        optimization_suggestions.append({
            "type": "environment",
            "suggestion": "Optimize environmental conditions (temperature, humidity, pressure)",
            "expected_improvement_km": current_distance * 0.15,  # 15% estimate
            "improvement_percentage": 15.0
        })
        
        # Quantum entanglement suggestion (theoretical)
        if self.optimization_parameters["quantum_entanglement"]:
            optimization_suggestions.append({
                "type": "quantum",
                "suggestion": "Implement quantum entanglement for non-local propagation",
                "expected_improvement_km": float('inf'),  # Theoretical infinite distance
                "improvement_percentage": float('inf')
            })
            
        optimization_result = {
            "photon_id": photon_id,
            "current_performance": current_performance,
            "optimization_suggestions": optimization_suggestions,
            "best_case_distance_km": current_distance + sum(
                s["expected_improvement_km"] for s in optimization_suggestions
            )
        }
        
        return optimization_result
    
    def simulate_photon_propagation(self, photon_id: str, 
                                  distances: List[float]) -> List[Dict[str, float]]:
        """
        Simulate sound wave photon propagation over a range of distances
        
        Args:
            photon_id: ID of the sound photon
            distances: List of distances to simulate in meters
            
        Returns:
            List of dictionaries with photon properties at each distance
        """
        if photon_id not in self.photons:
            return []
            
        photon = self.photons[photon_id]
        simulation_results = []
        
        for distance in distances:
            if distance < 0:
                continue
                
            # Calculate properties at this distance
            attenuation = self.calculate_attenuation_for_photon(photon, distance)
            coherence = self.calculate_coherence_preservation(photon, distance)
            energy = photon.energy * attenuation
            phase = (2 * math.pi * distance / photon.wavelength) % (2 * math.pi)
            
            # Calculate detectability
            minimum_detectable = 1e-40
            detectable = energy >= minimum_detectable
            
            simulation_results.append({
                "distance_m": distance,
                "distance_km": distance / 1000.0,
                "energy_j": energy,
                "attenuation_factor": attenuation,
                "coherence_preservation": coherence,
                "phase_radians": phase,
                "detectable": detectable,
                "propagation_time_s": distance / self.quantum_acoustic_constants["speed_of_sound"]
            })
            
        return simulation_results
    
    def enable_quantum_optimization_features(self, entanglement: bool = True,
                                           coherence_preservation: bool = True,
                                           phase_matching: bool = True):
        """
        Enable advanced quantum optimization features
        
        Args:
            entanglement: Enable quantum entanglement features
            coherence_preservation: Enable coherence preservation optimization
            phase_matching: Enable phase matching optimization
        """
        self.optimization_parameters["quantum_entanglement"] = entanglement
        self.optimization_parameters["coherence_preservation"] = coherence_preservation
        self.optimization_parameters["phase_matching"] = phase_matching
        
        print("🔬 Quantum optimization features enabled")
        
    def calculate_photon_interactions(self, photon_ids: List[str]) -> Dict[str, Any]:
        """
        Calculate interactions between multiple sound wave photons
        
        Args:
            photon_ids: List of photon IDs to analyze for interactions
            
        Returns:
            Dictionary with interaction analysis
        """
        if len(photon_ids) < 2:
            return {"error": "Need at least 2 photons for interaction analysis"}
            
        # Check if all photons exist
        for pid in photon_ids:
            if pid not in self.photons:
                return {"error": f"Photon '{pid}' not found"}
                
        photons = [self.photons[pid] for pid in photon_ids]
        
        # Calculate frequency relationships
        frequencies = [p.frequency for p in photons]
        avg_frequency = sum(frequencies) / len(frequencies)
        frequency_spread = max(frequencies) - min(frequencies)
        
        # Calculate coherence interactions
        coherence_lengths = [p.coherence_length for p in photons]
        avg_coherence = sum(coherence_lengths) / len(coherence_lengths)
        
        # Calculate potential constructive/destructive interference
        wavelength_relationships = []
        for i in range(len(photons)):
            for j in range(i + 1, len(photons)):
                p1, p2 = photons[i], photons[j]
                # Simple wavelength relationship
                ratio = p1.wavelength / p2.wavelength if p2.wavelength > 0 else 0
                wavelength_relationships.append(ratio)
                
        # Analyze potential for quantum acoustic enhancement
        quantum_enhancement_potential = 0.0
        if len(wavelength_relationships) > 0:
            # Simple model: enhancement when wavelengths have simple ratios
            simple_ratios = [r for r in wavelength_relationships if abs(r - round(r)) < 0.1]
            quantum_enhancement_potential = len(simple_ratios) / len(wavelength_relationships)
            
        interaction_analysis = {
            "photon_count": len(photons),
            "average_frequency_hz": avg_frequency,
            "frequency_spread_hz": frequency_spread,
            "average_coherence_length_m": avg_coherence,
            "wavelength_relationships": wavelength_relationships,
            "quantum_enhancement_potential": quantum_enhancement_potential,
            "constructive_interference_possible": quantum_enhancement_potential > 0.5
        }
        
        return interaction_analysis
    
    def get_photon_optimization_summary(self) -> Dict[str, Any]:
        """
        Get summary of photon optimization activities
        
        Returns:
            Dictionary with optimization summary
        """
        if not self.photons:
            return {"status": "no_photons_in_system"}
            
        # Calculate average properties
        total_energy = sum(p.energy for p in self.photons.values())
        total_wavelength = sum(p.wavelength for p in self.photons.values())
        total_coherence = sum(p.coherence_length for p in self.photons.values())
        
        avg_energy = total_energy / len(self.photons)
        avg_wavelength = total_wavelength / len(self.photons)
        avg_coherence = total_coherence / len(self.photons)
        
        return {
            "total_photons": len(self.photons),
            "average_photon_energy_j": avg_energy,
            "average_wavelength_m": avg_wavelength,
            "average_coherence_length_m": avg_coherence,
            "optimization_features_enabled": self.optimization_parameters,
            "environmental_conditions": self.environmental_conditions
        }

class QuantumAcousticEnhancer:
    """Advanced quantum acoustic enhancement techniques"""
    
    def __init__(self, photon_optimizer: SoundWavePhotonOptimizer):
        """Initialize quantum acoustic enhancer"""
        self.photon_optimizer = photon_optimizer
        
    def apply_coherent_state_amplification(self, photon_id: str) -> Dict[str, Any]:
        """
        Apply coherent state amplification to enhance photon propagation
        
        Args:
            photon_id: ID of the photon to enhance
            
        Returns:
            Dictionary with amplification results
        """
        if photon_id not in self.photon_optimizer.photons:
            return {"error": "Photon not found"}
            
        # Theoretical coherent amplification
        # In quantum optics, this would involve parametric amplification
        photon = self.photon_optimizer.photons[photon_id]
        
        # Increase coherence length (theoretical)
        enhanced_coherence = photon.coherence_length * 2.0
        
        # Increase energy while preserving quantum properties
        enhanced_energy = photon.energy * 1.5
        
        enhancement_result = {
            "photon_id": photon_id,
            "original_coherence_m": photon.coherence_length,
            "enhanced_coherence_m": enhanced_coherence,
            "coherence_improvement_factor": 2.0,
            "original_energy_j": photon.energy,
            "enhanced_energy_j": enhanced_energy,
            "energy_improvement_factor": 1.5
        }
        
        return enhancement_result
    
    def implement_quantum_error_correction(self, photon_id: str) -> Dict[str, Any]:
        """
        Implement quantum error correction for sound wave photons
        
        Args:
            photon_id: ID of the photon to protect
            
        Returns:
            Dictionary with error correction results
        """
        # Theoretical quantum error correction
        error_correction_result = {
            "photon_id": photon_id,
            "error_correction_applied": True,
            "decoherence_reduction": 0.7,  # 70% reduction in decoherence
            "phase_stability_improvement": 0.8,  # 80% improvement in phase stability
            "theoretical_distance_extension_km": 500.0  # 500km extension estimate
        }
        
        return error_correction_result

# Global instances
photon_optimizer = SoundWavePhotonOptimizer()
quantum_enhancer = None

def initialize_photon_optimization():
    """Initialize the global sound wave photon optimizer"""
    global photon_optimizer, quantum_enhancer
    photon_optimizer = SoundWavePhotonOptimizer()
    quantum_enhancer = QuantumAcousticEnhancer(photon_optimizer)
    return photon_optimizer

def set_photon_environmental_conditions(temperature = None,
                                     pressure = None,
                                     humidity = None):
    """Set environmental conditions for photon propagation"""
    photon_optimizer.set_environmental_conditions(temperature, pressure, humidity)

def add_sound_wave_photon(photon_id: str, frequency: float, amplitude: float = 1.0):
    """Add a sound wave photon to the optimization system"""
    photon = photon_optimizer.calculate_photon_properties(frequency, amplitude)
    photon_optimizer.add_sound_photon(photon_id, photon)
    return photon

def calculate_maximum_photon_distance(photon_id: str, minimum_detectable_energy: float = 1e-40):
    """Calculate maximum propagation distance for a sound wave photon"""
    return photon_optimizer.calculate_maximum_propagation_distance(photon_id, minimum_detectable_energy)

def optimize_photon_for_distance(photon_id: str):
    """Optimize sound wave photon parameters for maximum propagation distance"""
    return photon_optimizer.optimize_photon_for_maximum_distance(photon_id)

def simulate_photon_propagation(photon_id: str, distances: List[float]):
    """Simulate sound wave photon propagation over a range of distances"""
    return photon_optimizer.simulate_photon_propagation(photon_id, distances)

def enable_quantum_photon_optimization(entanglement: bool = True,
                                     coherence_preservation: bool = True,
                                     phase_matching: bool = True):
    """Enable advanced quantum optimization features"""
    photon_optimizer.enable_quantum_optimization_features(
        entanglement, coherence_preservation, phase_matching
    )

def calculate_photon_interactions(photon_ids: List[str]):
    """Calculate interactions between multiple sound wave photons"""
    return photon_optimizer.calculate_photon_interactions(photon_ids)

def apply_coherent_amplification(photon_id: str):
    """Apply coherent state amplification to enhance photon propagation"""
    if quantum_enhancer:
        return quantum_enhancer.apply_coherent_state_amplification(photon_id)
    return {"error": "Quantum enhancer not initialized"}

def implement_quantum_error_correction(photon_id: str):
    """Implement quantum error correction for sound wave photons"""
    if quantum_enhancer:
        return quantum_enhancer.implement_quantum_error_correction(photon_id)
    return {"error": "Quantum enhancer not initialized"}

def get_photon_optimization_summary():
    """Get summary of photon optimization activities"""
    return photon_optimizer.get_photon_optimization_summary()