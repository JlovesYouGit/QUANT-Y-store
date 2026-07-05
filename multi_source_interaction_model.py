"""
Multi-Source Sound Wave Interaction Model
Simulates interactions between multiple simultaneous sound sources and waves
"""

import math
from typing import List, Tuple, Dict, Any
from .acoustic_physics_engine import AcousticPhysicsEngine, SoundSource, SoundWave

class MultiSourceInteractionModel:
    """Models interactions between multiple sound sources and waves"""
    
    def __init__(self, acoustic_engine: AcousticPhysicsEngine):
        """Initialize the multi-source interaction model"""
        self.acoustic_engine = acoustic_engine
        self.interference_patterns = {}
        self.resonance_zones = {}
        self.beat_frequencies = {}
        
    def calculate_wave_interference(self, wave1: SoundWave, wave2: SoundWave) -> Dict[str, float]:
        """
        Calculate interference between two sound waves
        
        Args:
            wave1: First sound wave
            wave2: Second sound wave
            
        Returns:
            Dictionary of interference parameters
        """
        # Calculate distance between waves
        dx = wave1.position[0] - wave2.position[0]
        dy = wave1.position[1] - wave2.position[1]
        dz = wave1.position[2] - wave2.position[2]
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        
        # Calculate path difference
        path_diff = abs(wave1.distance_traveled - wave2.distance_traveled)
        
        # Calculate phase difference
        phase_diff = abs(wave1.phase - wave2.phase)
        
        # Calculate frequency difference (for beat frequencies)
        freq_diff = abs(wave1.frequency - wave2.frequency)
        
        # Determine interference type
        wavelength = self.acoustic_engine.sound_speed / wave1.frequency if wave1.frequency > 0 else 1.0
        path_ratio = path_diff / wavelength if wavelength > 0 else 0.0
        
        # Constructive interference when path difference is integer multiple of wavelength
        # Destructive interference when path difference is half-integer multiple
        constructive = abs(path_ratio - round(path_ratio)) < 0.1
        destructive = abs(path_ratio - (round(path_ratio) + 0.5)) < 0.1
        
        # Calculate interference amplitude effect
        if constructive:
            amplitude_effect = 1.5  # Amplification
        elif destructive:
            amplitude_effect = 0.5   # Attenuation
        else:
            # Partial interference
            amplitude_effect = 1.0 + 0.5 * math.sin(2 * math.pi * path_ratio)
            
        return {
            "distance": distance,
            "path_difference": path_diff,
            "phase_difference": phase_diff,
            "frequency_difference": freq_diff,
            "constructive": constructive,
            "destructive": destructive,
            "amplitude_effect": amplitude_effect,
            "beat_frequency": freq_diff
        }
    
    def analyze_multi_source_interactions(self) -> Dict[str, Any]:
        """
        Analyze interactions between all sound sources and waves
        
        Returns:
            Dictionary of interaction analysis
        """
        waves = self.acoustic_engine.sound_waves
        sources = self.acoustic_engine.sound_sources
        
        if len(waves) < 2:
            return {"interactions": [], "resonance_zones": [], "beat_frequencies": []}
        
        interactions = []
        resonance_zones = []
        beat_frequencies = []
        
        # Analyze pairwise interactions between waves
        for i in range(len(waves)):
            for j in range(i + 1, len(waves)):
                if i != j:
                    wave1, wave2 = waves[i], waves[j]
                    interference = self.calculate_wave_interference(wave1, wave2)
                    interference["wave1_id"] = wave1.source_id
                    interference["wave2_id"] = wave2.source_id
                    interactions.append(interference)
                    
                    # Track beat frequencies
                    if interference["beat_frequency"] > 0:
                        beat_frequencies.append({
                            "sources": (wave1.source_id, wave2.source_id),
                            "frequency": interference["beat_frequency"],
                            "perceptible": interference["beat_frequency"] < 20.0  # Below 20 Hz is perceptible
                        })
        
        # Analyze resonance zones based on source frequencies
        source_frequencies = {}
        for source_id, source in sources.items():
            # Group sources by similar frequencies
            freq_group = round(source.frequency / 100) * 100  # Group by 100 Hz bands
            if freq_group not in source_frequencies:
                source_frequencies[freq_group] = []
            source_frequencies[freq_group].append(source_id)
        
        # Identify resonance zones
        for freq_group, source_ids in source_frequencies.items():
            if len(source_ids) > 1:
                # Multiple sources with similar frequencies create resonance
                avg_frequency = sum(sources[sid].frequency for sid in source_ids) / len(source_ids)
                resonance_zones.append({
                    "frequency": avg_frequency,
                    "sources": source_ids,
                    "strength": len(source_ids) / len(sources),  # Normalized strength
                    "type": "harmonic" if avg_frequency > 200 else "subharmonic"
                })
        
        return {
            "interactions": interactions,
            "resonance_zones": resonance_zones,
            "beat_frequencies": beat_frequencies
        }
    
    def calculate_spatial_interference_pattern(self, listener_position: Tuple[float, float, float]) -> Dict[str, Any]:
        """
        Calculate the spatial interference pattern at a specific listener position
        
        Args:
            listener_position: Position of the listener (x, y, z)
            
        Returns:
            Dictionary describing the interference pattern at that location
        """
        waves = self.acoustic_engine.sound_waves
        
        if not waves:
            return {"amplitude": 0.0, "phase": 0.0, "interference_type": "none"}
        
        # Calculate combined wave effect at listener position
        total_amplitude = 0.0
        total_phase = 0.0
        
        for wave in waves:
            # Calculate distance from wave to listener
            dx = listener_position[0] - wave.position[0]
            dy = listener_position[1] - wave.position[1]
            dz = listener_position[2] - wave.position[2]
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # Calculate time for wave to reach listener
            time_to_listener = distance / self.acoustic_engine.sound_speed if self.acoustic_engine.sound_speed > 0 else 0
            
            # Calculate current phase at listener
            angular_frequency = 2 * math.pi * wave.frequency
            current_phase = wave.phase + angular_frequency * (self.acoustic_engine.current_time - wave.timestamp + time_to_listener)
            
            # Calculate amplitude at listener (with distance attenuation)
            reference_distance = 1.0
            attenuation = (reference_distance / distance) ** 2 if distance > reference_distance else 1.0
            amplitude_at_listener = wave.amplitude * attenuation
            
            # Add to total (phasor addition)
            total_amplitude += amplitude_at_listener * math.cos(current_phase)
            total_phase += current_phase
            
        # Calculate resultant amplitude and phase
        resultant_amplitude = abs(total_amplitude)
        resultant_phase = total_phase / len(waves) if waves else 0.0
        
        # Determine interference type based on amplitude
        if resultant_amplitude > sum(wave.amplitude for wave in waves) * 0.8:
            interference_type = "constructive"
        elif resultant_amplitude < sum(wave.amplitude for wave in waves) * 0.2:
            interference_type = "destructive"
        else:
            interference_type = "partial"
            
        return {
            "amplitude": resultant_amplitude,
            "phase": resultant_phase,
            "interference_type": interference_type,
            "wave_count": len(waves)
        }
    
    def simulate_room_acoustics(self, room_dimensions: Tuple[float, float, float],
                              absorption_coefficients: Dict[str, float]) -> Dict[str, Any]:
        """
        Simulate basic room acoustics with reflections
        
        Args:
            room_dimensions: Room size (width, height, depth)
            absorption_coefficients: Absorption coefficients for room surfaces
            
        Returns:
            Dictionary of room acoustic parameters
        """
        # This is a simplified room acoustics model
        width, height, depth = room_dimensions
        
        # Calculate room volume and surface areas
        volume = width * height * depth
        total_surface_area = 2 * (width * height + width * depth + height * depth)
        
        # Calculate reverberation time using Sabine's formula
        # T60 = 0.161 * V / A (where A is total absorption)
        total_absorption = sum(absorption_coefficients.values()) * total_surface_area / 6
        reverberation_time = 0.161 * volume / total_absorption if total_absorption > 0 else 1.0
        
        # Calculate early reflection patterns (simplified)
        early_reflections = []
        reflection_surfaces = ["front", "back", "left", "right", "ceiling", "floor"]
        
        for surface in reflection_surfaces:
            # Simplified reflection calculation
            reflection_delay = 2 * width / self.acoustic_engine.sound_speed  # Approximate
            early_reflections.append({
                "surface": surface,
                "delay": reflection_delay,
                "attenuation": absorption_coefficients.get(surface, 0.5)
            })
        
        return {
            "reverberation_time": reverberation_time,
            "volume": volume,
            "early_reflections": early_reflections,
            "total_absorption": total_absorption
        }
    
    def get_interaction_summary(self) -> Dict[str, Any]:
        """
        Get a summary of multi-source interactions
        
        Returns:
            Dictionary summarizing interactions
        """
        analysis = self.analyze_multi_source_interactions()
        
        # Count different types of interactions
        constructive_count = sum(1 for interaction in analysis["interactions"] if interaction["constructive"])
        destructive_count = sum(1 for interaction in analysis["interactions"] if interaction["destructive"])
        beat_count = len([beat for beat in analysis["beat_frequencies"] if beat["perceptible"]])
        resonance_count = len(analysis["resonance_zones"])
        
        return {
            "total_interactions": len(analysis["interactions"]),
            "constructive_interactions": constructive_count,
            "destructive_interactions": destructive_count,
            "perceptible_beats": beat_count,
            "resonance_zones": resonance_count,
            "complexity": min(1.0, len(analysis["interactions"]) / 20.0)  # Normalize
        }

class WaveInteractionAnalyzer:
    """Analyzer for complex wave interactions"""
    
    def __init__(self, interaction_model: MultiSourceInteractionModel):
        """Initialize the wave interaction analyzer"""
        self.interaction_model = interaction_model
        
    def analyze_frequency_clustering(self) -> List[Dict[str, Any]]:
        """
        Analyze clustering of sound sources by frequency
        
        Returns:
            List of frequency clusters
        """
        sources = self.interaction_model.acoustic_engine.sound_sources
        if not sources:
            return []
        
        # Group sources by frequency ranges
        clusters = {}
        for source_id, source in sources.items():
            # Group into 200 Hz bands
            freq_band = int(source.frequency // 200) * 200
            if freq_band not in clusters:
                clusters[freq_band] = {
                    "center_frequency": freq_band + 100,
                    "sources": [],
                    "total_amplitude": 0.0
                }
            clusters[freq_band]["sources"].append(source_id)
            clusters[freq_band]["total_amplitude"] += source.amplitude
            
        # Convert to list and sort by amplitude
        cluster_list = list(clusters.values())
        cluster_list.sort(key=lambda x: x["total_amplitude"], reverse=True)
        
        return cluster_list
    
    def calculate_spatial_coherence(self) -> float:
        """
        Calculate spatial coherence of sound sources
        
        Returns:
            Coherence value from 0.0 (random) to 1.0 (coherent)
        """
        sources = self.interaction_model.acoustic_engine.sound_sources
        if len(sources) < 2:
            return 1.0
            
        # Calculate centroid of all sources
        total_x = sum(source.position[0] for source in sources.values())
        total_y = sum(source.position[1] for source in sources.values())
        total_z = sum(source.position[2] for source in sources.values())
        count = len(sources)
        
        centroid = (total_x / count, total_y / count, total_z / count)
        
        # Calculate average distance from centroid
        total_distance = 0.0
        for source in sources.values():
            dx = source.position[0] - centroid[0]
            dy = source.position[1] - centroid[1]
            dz = source.position[2] - centroid[2]
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            total_distance += distance
            
        avg_distance = total_distance / count
        
        # Normalize coherence (simplified)
        # In a 10x10x10 space, maximum average distance is about 5.77
        max_avg_distance = 5.77
        coherence = max(0.0, 1.0 - (avg_distance / max_avg_distance))
        
        return coherence

# Global instances
multi_source_model = None
wave_analyzer = None

def initialize_multi_source_interaction(acoustic_engine: AcousticPhysicsEngine):
    """Initialize the global multi-source interaction model"""
    global multi_source_model, wave_analyzer
    multi_source_model = MultiSourceInteractionModel(acoustic_engine)
    wave_analyzer = WaveInteractionAnalyzer(multi_source_model)
    return multi_source_model

def analyze_wave_interactions():
    """Analyze interactions between all sound waves"""
    if multi_source_model:
        return multi_source_model.analyze_multi_source_interactions()
    return {}

def calculate_spatial_interference(listener_position: Tuple[float, float, float]):
    """Calculate spatial interference pattern at listener position"""
    if multi_source_model:
        return multi_source_model.calculate_spatial_interference_pattern(listener_position)
    return {}

def get_interaction_complexity():
    """Get the complexity of multi-source interactions"""
    if multi_source_model:
        return multi_source_model.get_interaction_summary()
    return {"complexity": 0.0}