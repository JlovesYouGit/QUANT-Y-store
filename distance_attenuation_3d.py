"""
Distance-Based Attenuation for 3D Spatial Audio
System for implementing accurate distance-based attenuation in 3D space
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class AttenuationParameters:
    """Parameters for distance-based attenuation"""
    model_type: str  # "inverse", "inverse_square", "exponential", "logarithmic", "custom"
    reference_distance: float  # meters
    rolloff_factor: float  # attenuation factor
    max_distance: float  # meters (beyond this, sound is inaudible)
    min_gain: float  # minimum gain (0.0 to 1.0)
    custom_curve_points: List[Tuple[float, float]]  # (distance, attenuation) pairs

@dataclass
class SpatialAudioSource:
    """3D spatial audio source with attenuation properties"""
    id: str
    position: Tuple[float, float, float]  # (x, y, z) in meters
    initial_gain: float  # 0.0 to 1.0
    attenuation_params: AttenuationParameters
    directivity_pattern: str  # "omnidirectional", "cardioid", etc.
    frequency_content: Tuple[float, float]  # (min_freq, max_freq) in Hz

class DistanceAttenuation3D:
    """Distance-based attenuation system for 3D spatial audio"""
    
    def __init__(self):
        """Initialize the distance attenuation system"""
        self.audio_sources: Dict[str, SpatialAudioSource] = {}
        self.listeners: Dict[str, Tuple[float, float, float]] = {}  # (x, y, z) positions
        self.global_attenuation_settings = {
            "air_absorption": True,
            "atmospheric_attenuation": True,
            "obstacle_occlusion": True,
            "reverberation": True
        }
        self.environmental_conditions = {
            "temperature": 20.0,  # Celsius
            "humidity": 50.0,     # Percent
            "pressure": 101325.0, # Pascals
            "air_density": 1.225  # kg/m³
        }
        
    def add_spatial_audio_source(self, source: SpatialAudioSource):
        """
        Add a spatial audio source with attenuation properties
        
        Args:
            source: SpatialAudioSource object
        """
        self.audio_sources[source.id] = source
        print(f"🔊 Spatial audio source '{source.id}' added at position {source.position}")
        
    def add_listener(self, listener_id: str, position: Tuple[float, float, float]):
        """
        Add a listener position for attenuation calculations
        
        Args:
            listener_id: Unique identifier for the listener
            position: (x, y, z) position in meters
        """
        self.listeners[listener_id] = position
        print(f"👂 Listener '{listener_id}' added at position {position}")
        
    def calculate_3d_distance(self, pos1: Tuple[float, float, float], 
                            pos2: Tuple[float, float, float]) -> float:
        """
        Calculate 3D Euclidean distance between two points
        
        Args:
            pos1: First position (x, y, z)
            pos2: Second position (x, y, z)
            
        Returns:
            Distance in meters
        """
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dz = pos2[2] - pos1[2]
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        return distance
    
    def calculate_inverse_attenuation(self, distance: float, params: AttenuationParameters) -> float:
        """
        Calculate inverse distance attenuation
        
        Args:
            distance: Distance from source in meters
            params: AttenuationParameters object
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if distance <= params.reference_distance:
            return 1.0
            
        # Inverse attenuation: gain = ref_dist / (ref_dist + rolloff * (dist - ref_dist))
        gain = params.reference_distance / (params.reference_distance + 
                                          params.rolloff_factor * (distance - params.reference_distance))
        
        # Apply minimum gain
        gain = max(params.min_gain, gain)
        
        return gain
    
    def calculate_inverse_square_attenuation(self, distance: float, params: AttenuationParameters) -> float:
        """
        Calculate inverse square distance attenuation (physically accurate)
        
        Args:
            distance: Distance from source in meters
            params: AttenuationParameters object
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if distance <= params.reference_distance:
            return 1.0
            
        # Inverse square law: gain = (ref_dist / dist)^2
        gain = (params.reference_distance / distance) ** 2
        
        # Apply rolloff factor
        gain = gain ** params.rolloff_factor
        
        # Apply minimum gain
        gain = max(params.min_gain, gain)
        
        return gain
    
    def calculate_exponential_attenuation(self, distance: float, params: AttenuationParameters) -> float:
        """
        Calculate exponential distance attenuation
        
        Args:
            distance: Distance from source in meters
            params: AttenuationParameters object
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if distance <= params.reference_distance:
            return 1.0
            
        # Exponential attenuation: gain = exp(-rolloff * (dist - ref_dist) / ref_dist)
        gain = math.exp(-params.rolloff_factor * (distance - params.reference_distance) / params.reference_distance)
        
        # Apply minimum gain
        gain = max(params.min_gain, gain)
        
        return gain
    
    def calculate_logarithmic_attenuation(self, distance: float, params: AttenuationParameters) -> float:
        """
        Calculate logarithmic distance attenuation
        
        Args:
            distance: Distance from source in meters
            params: AttenuationParameters object
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if distance <= params.reference_distance:
            return 1.0
            
        # Logarithmic attenuation: gain = 1 / (1 + rolloff * ln(dist / ref_dist))
        if distance > 0 and params.reference_distance > 0:
            gain = 1.0 / (1.0 + params.rolloff_factor * math.log(distance / params.reference_distance))
        else:
            gain = 1.0
            
        # Apply minimum gain
        gain = max(params.min_gain, gain)
        
        return gain
    
    def calculate_custom_attenuation(self, distance: float, params: AttenuationParameters) -> float:
        """
        Calculate custom distance attenuation using defined curve points
        
        Args:
            distance: Distance from source in meters
            params: AttenuationParameters object
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if not params.custom_curve_points:
            return 1.0
            
        # Sort curve points by distance
        sorted_points = sorted(params.custom_curve_points, key=lambda x: x[0])
        
        # If distance is before first point, use first point's value
        if distance <= sorted_points[0][0]:
            return sorted_points[0][1]
            
        # If distance is after last point, use last point's value
        if distance >= sorted_points[-1][0]:
            return sorted_points[-1][1]
            
        # Find surrounding points and interpolate
        for i in range(len(sorted_points) - 1):
            p1, p2 = sorted_points[i], sorted_points[i + 1]
            if p1[0] <= distance <= p2[0]:
                # Linear interpolation
                t = (distance - p1[0]) / (p2[0] - p1[0]) if p2[0] != p1[0] else 0
                gain = p1[1] + t * (p2[1] - p1[1])
                return max(params.min_gain, min(1.0, gain))
                
        return 1.0
    
    def calculate_air_absorption_attenuation(self, distance: float, frequency: float) -> float:
        """
        Calculate air absorption attenuation based on frequency and distance
        
        Args:
            distance: Distance in meters
            frequency: Frequency in Hz
            
        Returns:
            Air absorption attenuation factor (0.0 to 1.0)
        """
        # Simplified air absorption model
        # Based on temperature, humidity, and frequency
        
        temp_factor = 1.0 + (self.environmental_conditions["temperature"] - 20.0) / 100.0
        humidity_factor = 1.0 + (self.environmental_conditions["humidity"] - 50.0) / 200.0
        
        # Frequency-dependent absorption (simplified)
        if frequency < 500:
            base_absorption = 0.00005  # Very low for bass
        elif frequency < 2000:
            base_absorption = 0.0002   # Low for midrange
        elif frequency < 8000:
            base_absorption = 0.001    # Moderate for upper midrange
        else:
            base_absorption = 0.003    # High for treble
            
        # Convert to linear attenuation over distance
        attenuation_db = base_absorption * distance * temp_factor * humidity_factor
        attenuation_linear = 10 ** (-attenuation_db / 10.0)
        
        return max(0.0, min(1.0, attenuation_linear))
    
    def calculate_atmospheric_attenuation(self, distance: float, frequency: float) -> float:
        """
        Calculate detailed atmospheric attenuation
        
        Args:
            distance: Distance in meters
            frequency: Frequency in Hz
            
        Returns:
            Atmospheric attenuation factor (0.0 to 1.0)
        """
        # More detailed model based on ISO 9613-1
        temp_k = self.environmental_conditions["temperature"] + 273.15
        pressure_atm = self.environmental_conditions["pressure"] / 101325.0
        
        # Oxygen relaxation frequency
        fr_o = 24.0 + 4.04e4 * (self.environmental_conditions["humidity"] / 100.0) * (273.15 / temp_k)
        
        # Nitrogen relaxation frequency  
        fr_n = (temp_k / 293.15) ** (-0.5) * (
            9.0 + 280.0 * (self.environmental_conditions["humidity"] / 100.0) * 
            math.exp(-4.17 * ((temp_k / 293.15) ** (-1/3) - 1))
        )
        
        # Absorption coefficient calculation
        alpha_o = 0.0127 * (fr_o / (frequency ** 2 + fr_o ** 2)) * (293.15 / temp_k) ** (5/2)
        alpha_n = 0.1068 * (fr_n / (frequency ** 2 + fr_n ** 2)) * (293.15 / temp_k) ** (5/2)
        
        # Total absorption coefficient (dB/m)
        alpha_total = pressure_atm * (alpha_o + alpha_n) * (frequency ** 2) / 1000.0
        
        # Convert to linear attenuation over distance
        attenuation_db = alpha_total * distance
        attenuation_linear = 10 ** (-attenuation_db / 10.0)
        
        return max(0.0, min(1.0, attenuation_linear))
    
    def calculate_directivity_attenuation(self, source: SpatialAudioSource, 
                                       listener_pos: Tuple[float, float, float]) -> float:
        """
        Calculate directivity-based attenuation
        
        Args:
            source: SpatialAudioSource object
            listener_pos: Listener position (x, y, z)
            
        Returns:
            Directivity attenuation factor (0.0 to 1.0)
        """
        # Calculate angle from source front direction
        source_pos = source.position
        dx = listener_pos[0] - source_pos[0]
        dz = listener_pos[2] - source_pos[2]
        
        # Calculate angle from front (assuming front is along positive Z axis)
        angle_from_front = math.degrees(math.atan2(dx, dz))
        
        if source.directivity_pattern == "omnidirectional":
            return 1.0
            
        elif source.directivity_pattern == "cardioid":
            # Cardioid pattern: D(θ) = 0.5 * (1 + cos(θ))
            angle_rad = math.radians(angle_from_front)
            directivity = 0.5 * (1 + math.cos(angle_rad))
            
        elif source.directivity_pattern == "hypercardioid":
            # Hypercardioid pattern: D(θ) = 0.5 * (1 + 1.5 * cos(θ))
            angle_rad = math.radians(angle_from_front)
            directivity = 0.5 * (1 + 1.5 * math.cos(angle_rad))
            
        elif source.directivity_pattern == "figure8":
            # Figure-8 pattern: D(θ) = |cos(θ)|
            angle_rad = math.radians(angle_from_front)
            directivity = abs(math.cos(angle_rad))
            
        else:
            # Default to omnidirectional
            return 1.0
            
        return max(0.0, min(1.0, directivity))
    
    def calculate_total_attenuation(self, source_id: str, listener_id: str) -> Dict[str, Any]:
        """
        Calculate total attenuation for a source-listener pair
        
        Args:
            source_id: ID of the audio source
            listener_id: ID of the listener
            
        Returns:
            Dictionary with attenuation components and total gain
        """
        if source_id not in self.audio_sources or listener_id not in self.listeners:
            return {"error": "Source or listener not found"}
            
        source = self.audio_sources[source_id]
        listener_pos = self.listeners[listener_id]
        
        # Calculate distance
        distance = self.calculate_3d_distance(source.position, listener_pos)
        
        # Check if beyond maximum distance
        if distance > source.attenuation_params.max_distance:
            return {
                "source_id": source_id,
                "listener_id": listener_id,
                "distance_m": distance,
                "total_gain": 0.0,
                "components": {
                    "distance": 0.0,
                    "air_absorption": 0.0,
                    "atmospheric": 0.0,
                    "directivity": 0.0
                },
                "audible": False
            }
        
        # Calculate distance-based attenuation
        if source.attenuation_params.model_type == "inverse":
            distance_gain = self.calculate_inverse_attenuation(distance, source.attenuation_params)
        elif source.attenuation_params.model_type == "inverse_square":
            distance_gain = self.calculate_inverse_square_attenuation(distance, source.attenuation_params)
        elif source.attenuation_params.model_type == "exponential":
            distance_gain = self.calculate_exponential_attenuation(distance, source.attenuation_params)
        elif source.attenuation_params.model_type == "logarithmic":
            distance_gain = self.calculate_logarithmic_attenuation(distance, source.attenuation_params)
        elif source.attenuation_params.model_type == "custom":
            distance_gain = self.calculate_custom_attenuation(distance, source.attenuation_params)
        else:
            # Default to inverse square
            distance_gain = self.calculate_inverse_square_attenuation(distance, source.attenuation_params)
            
        # Calculate frequency-weighted average for multi-band sources
        min_freq, max_freq = source.frequency_content
        avg_frequency = (min_freq + max_freq) / 2
        
        # Calculate air absorption attenuation
        if self.global_attenuation_settings["air_absorption"]:
            air_absorption_gain = self.calculate_air_absorption_attenuation(distance, avg_frequency)
        else:
            air_absorption_gain = 1.0
            
        # Calculate atmospheric attenuation
        if self.global_attenuation_settings["atmospheric_attenuation"]:
            atmospheric_gain = self.calculate_atmospheric_attenuation(distance, avg_frequency)
        else:
            atmospheric_gain = 1.0
            
        # Calculate directivity attenuation
        directivity_gain = self.calculate_directivity_attenuation(source, listener_pos)
        
        # Calculate total gain
        total_gain = (source.initial_gain * 
                     distance_gain * 
                     air_absorption_gain * 
                     atmospheric_gain * 
                     directivity_gain)
        
        # Ensure gain is within bounds
        total_gain = max(0.0, min(1.0, total_gain))
        
        result = {
            "source_id": source_id,
            "listener_id": listener_id,
            "distance_m": distance,
            "total_gain": total_gain,
            "components": {
                "distance": distance_gain,
                "air_absorption": air_absorption_gain,
                "atmospheric": atmospheric_gain,
                "directivity": directivity_gain
            },
            "audible": total_gain > 0.001,  # Threshold for audibility
            "source_position": source.position,
            "listener_position": listener_pos
        }
        
        return result
    
    def simulate_attenuation_field(self, source_id: str, 
                                listener_positions: List[Tuple[float, float, float]]) -> List[Dict[str, float]]:
        """
        Simulate attenuation field at multiple listener positions
        
        Args:
            source_id: ID of the audio source
            listener_positions: List of (x, y, z) positions to evaluate
            
        Returns:
            List of dictionaries with attenuation at each position
        """
        if source_id not in self.audio_sources:
            return []
            
        field_results = []
        
        for i, position in enumerate(listener_positions):
            # Create temporary listener
            temp_listener_id = f"temp_listener_{i}"
            self.listeners[temp_listener_id] = position
            
            # Calculate attenuation at this position
            attenuation_result = self.calculate_total_attenuation(source_id, temp_listener_id)
            
            if "error" not in attenuation_result:
                field_results.append({
                    "position": position,
                    "distance_m": attenuation_result["distance_m"],
                    "total_gain": attenuation_result["total_gain"],
                    "audible": attenuation_result["audible"],
                    "components": attenuation_result["components"]
                })
            
            # Remove temporary listener
            del self.listeners[temp_listener_id]
            
        return field_results
    
    def optimize_attenuation_parameters(self, source_id: str, 
                                     target_distance: float, 
                                     target_gain: float) -> Dict[str, Any]:
        """
        Optimize attenuation parameters for a target distance and gain
        
        Args:
            source_id: ID of the audio source
            target_distance: Target distance in meters
            target_gain: Target gain (0.0 to 1.0)
            
        Returns:
            Dictionary with optimization results
        """
        if source_id not in self.audio_sources:
            return {"error": "Source not found"}
            
        source = self.audio_sources[source_id]
        params = source.attenuation_params
        
        # Current gain at target distance
        if params.model_type == "inverse":
            current_gain = self.calculate_inverse_attenuation(target_distance, params)
        elif params.model_type == "inverse_square":
            current_gain = self.calculate_inverse_square_attenuation(target_distance, params)
        elif params.model_type == "exponential":
            current_gain = self.calculate_exponential_attenuation(target_distance, params)
        elif params.model_type == "logarithmic":
            current_gain = self.calculate_logarithmic_attenuation(target_distance, params)
        else:
            current_gain = self.calculate_inverse_square_attenuation(target_distance, params)
            
        # Calculate required rolloff factor adjustment
        # This is a simplified approach - in practice, this would be more complex
        if current_gain > 0 and target_gain > 0:
            gain_ratio = target_gain / current_gain
            suggested_rolloff = params.rolloff_factor * gain_ratio
        else:
            suggested_rolloff = params.rolloff_factor
            
        optimization_result = {
            "source_id": source_id,
            "target_distance": target_distance,
            "target_gain": target_gain,
            "current_gain": current_gain,
            "current_rolloff": params.rolloff_factor,
            "suggested_rolloff": suggested_rolloff,
            "adjustment_needed": suggested_rolloff - params.rolloff_factor
        }
        
        return optimization_result
    
    def set_environmental_conditions(self, temperature = None,
                                   humidity = None,
                                   pressure = None):
        """
        Set environmental conditions affecting attenuation
        
        Args:
            temperature: Air temperature in Celsius
            humidity: Relative humidity in percent
            pressure: Atmospheric pressure in Pascals
        """
        if temperature is not None:
            self.environmental_conditions["temperature"] = temperature
        if humidity is not None:
            self.environmental_conditions["humidity"] = humidity
        if pressure is not None:
            self.environmental_conditions["pressure"] = pressure
            
        print(f"🌍 Environmental conditions updated: {temperature}°C, {humidity}% humidity")
    
    def enable_attenuation_features(self, air_absorption: bool = True,
                                 atmospheric_attenuation: bool = True,
                                 obstacle_occlusion: bool = True,
                                 reverberation: bool = True):
        """
        Enable/disable specific attenuation features
        
        Args:
            air_absorption: Enable air absorption attenuation
            atmospheric_attenuation: Enable detailed atmospheric attenuation
            obstacle_occlusion: Enable obstacle occlusion (not implemented)
            reverberation: Enable reverberation effects (not implemented)
        """
        self.global_attenuation_settings["air_absorption"] = air_absorption
        self.global_attenuation_settings["atmospheric_attenuation"] = atmospheric_attenuation
        self.global_attenuation_settings["obstacle_occlusion"] = obstacle_occlusion
        self.global_attenuation_settings["reverberation"] = reverberation
        
        print("⚙️ Attenuation features updated")
        
    def get_attenuation_summary(self) -> Dict[str, Any]:
        """
        Get summary of attenuation system
        
        Returns:
            Dictionary with attenuation summary
        """
        total_sources = len(self.audio_sources)
        total_listeners = len(self.listeners)
        
        return {
            "total_audio_sources": total_sources,
            "total_listeners": total_listeners,
            "environmental_conditions": self.environmental_conditions,
            "attenuation_features": self.global_attenuation_settings
        }

class AdvancedAttenuationModel:
    """Advanced attenuation modeling with physics-based calculations"""
    
    def __init__(self, attenuation_system: DistanceAttenuation3D):
        """Initialize advanced attenuation model"""
        self.attenuation_system = attenuation_system
        
    def calculate_obstacle_occlusion(self, source_pos: Tuple[float, float, float], 
                                   listener_pos: Tuple[float, float, float],
                                   obstacles: List[Dict[str, Any]]) -> float:
        """
        Calculate obstacle occlusion attenuation
        
        Args:
            source_pos: Source position (x, y, z)
            listener_pos: Listener position (x, y, z)
            obstacles: List of obstacle definitions
            
        Returns:
            Occlusion attenuation factor (0.0 to 1.0)
        """
        # This would implement ray casting and occlusion calculations
        # For now, we'll return a simplified result
        
        return 1.0  # No occlusion by default
    
    def calculate_reverberation_effects(self, source_pos: Tuple[float, float, float], 
                                     listener_pos: Tuple[float, float, float],
                                     room_parameters: Dict[str, float]) -> float:
        """
        Calculate reverberation effects on attenuation
        
        Args:
            source_pos: Source position (x, y, z)
            listener_pos: Listener position (x, y, z)
            room_parameters: Room acoustic parameters
            
        Returns:
            Reverberation factor (0.0 to 1.0)
        """
        # This would implement room acoustics and reverberation modeling
        # For now, we'll return a simplified result
        
        return 1.0  # No additional reverberation by default

# Global instances
distance_attenuation_3d = DistanceAttenuation3D()
advanced_attenuation_model = None

def initialize_distance_attenuation_3d():
    """Initialize the global distance attenuation system"""
    global distance_attenuation_3d, advanced_attenuation_model
    distance_attenuation_3d = DistanceAttenuation3D()
    advanced_attenuation_model = AdvancedAttenuationModel(distance_attenuation_3d)
    return distance_attenuation_3d

def add_spatial_audio_source(source: SpatialAudioSource):
    """Add a spatial audio source with attenuation properties"""
    distance_attenuation_3d.add_spatial_audio_source(source)

def add_3d_listener(listener_id: str, position: Tuple[float, float, float]):
    """Add a listener position for attenuation calculations"""
    distance_attenuation_3d.add_listener(listener_id, position)

def calculate_3d_attenuation(source_id: str, listener_id: str):
    """Calculate total attenuation for a source-listener pair"""
    return distance_attenuation_3d.calculate_total_attenuation(source_id, listener_id)

def simulate_attenuation_field(source_id: str, listener_positions: List[Tuple[float, float, float]]):
    """Simulate attenuation field at multiple listener positions"""
    return distance_attenuation_3d.simulate_attenuation_field(source_id, listener_positions)

def optimize_attenuation_parameters(source_id: str, target_distance: float, target_gain: float):
    """Optimize attenuation parameters for a target distance and gain"""
    return distance_attenuation_3d.optimize_attenuation_parameters(source_id, target_distance, target_gain)

def set_attenuation_environmental_conditions(temperature = None,
                                         humidity = None,
                                         pressure = None):
    """Set environmental conditions affecting attenuation"""
    distance_attenuation_3d.set_environmental_conditions(temperature, humidity, pressure)

def enable_3d_attenuation_features(air_absorption: bool = True,
                                atmospheric_attenuation: bool = True,
                                obstacle_occlusion: bool = True,
                                reverberation: bool = True):
    """Enable/disable specific attenuation features"""
    distance_attenuation_3d.enable_attenuation_features(
        air_absorption, atmospheric_attenuation, obstacle_occlusion, reverberation
    )

def get_attenuation_summary():
    """Get summary of attenuation system"""
    return distance_attenuation_3d.get_attenuation_summary()