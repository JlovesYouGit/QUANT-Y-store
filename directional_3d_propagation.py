"""
Directional 3D Sound Propagation System
Enhanced system for accurate 3D sound propagation with directional curves and distance calculations
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class SoundSource3D:
    """Represents a 3D sound source with directional characteristics"""
    id: str
    position: Tuple[float, float, float]  # (x, y, z) in meters
    orientation: Tuple[float, float, float]  # (azimuth, elevation, roll) in degrees
    frequency: float  # Hz
    power: float  # Watts
    directivity_pattern: str  # "omnidirectional", "cardioid", "hypercardioid", "figure8", "custom"
    directivity_coefficients: Tuple[float, float, float]  # (a0, a1, a2) for custom patterns
    beamwidth: float  # Degrees (for directional sources)
    near_field_distance: float  # Near field boundary in meters

@dataclass
class Listener3D:
    """Represents a 3D listener with spatial characteristics"""
    position: Tuple[float, float, float]  # (x, y, z) in meters
    orientation: Tuple[float, float, float]  # (azimuth, elevation, roll) in degrees
    head_radius: float  # meters (for head-related transfer functions)

@dataclass
class PropagationPath:
    """Represents a sound propagation path in 3D space"""
    source_id: str
    start_position: Tuple[float, float, float]
    end_position: Tuple[float, float, float]
    distance: float  # meters
    elevation_angle: float  # degrees
    azimuth_angle: float  # degrees
    path_loss: float  # dB
    time_delay: float  # seconds
    phase_shift: float  # radians

class Directional3DPropagation:
    """Enhanced 3D sound propagation with accurate directional curves"""
    
    def __init__(self):
        """Initialize the directional 3D propagation system"""
        self.sound_sources: Dict[str, SoundSource3D] = {}
        self.listeners: Dict[str, Listener3D] = {}
        self.propagation_paths: List[PropagationPath] = []
        self.environmental_factors = {
            "temperature": 20.0,  # Celsius
            "humidity": 50.0,     # Percent
            "pressure": 101325.0, # Pascals
            "air_density": 1.225, # kg/m³
            "sound_speed": 343.0  # m/s
        }
        self.obstacles = []
        self.reflective_surfaces = []
        
    def add_sound_source_3d(self, source: SoundSource3D):
        """
        Add a 3D sound source to the propagation system
        
        Args:
            source: SoundSource3D object
        """
        self.sound_sources[source.id] = source
        print(f"🔊 3D sound source '{source.id}' added at position {source.position}")
        
    def add_listener_3d(self, listener_id: str, listener: Listener3D):
        """
        Add a 3D listener to the propagation system
        
        Args:
            listener_id: Unique identifier for the listener
            listener: Listener3D object
        """
        self.listeners[listener_id] = listener
        print(f"👂 3D listener '{listener_id}' added at position {listener.position}")
        
    def set_environmental_conditions(self, temperature = None,
                                   humidity = None,
                                   pressure = None):
        """
        Set environmental conditions affecting 3D sound propagation
        
        Args:
            temperature: Air temperature in Celsius
            humidity: Relative humidity in percent
            pressure: Atmospheric pressure in Pascals
        """
        if temperature is not None:
            self.environmental_factors["temperature"] = temperature
            # Update sound speed based on temperature
            self.environmental_factors["sound_speed"] = 331.3 + 0.606 * temperature
            
        if humidity is not None:
            self.environmental_factors["humidity"] = humidity
            
        if pressure is not None:
            self.environmental_factors["pressure"] = pressure
            
        print(f"🌍 Environmental conditions updated: {temperature}°C, {humidity}% humidity")
        
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
    
    def calculate_3d_angles(self, source_pos: Tuple[float, float, float], 
                          listener_pos: Tuple[float, float, float]) -> Tuple[float, float]:
        """
        Calculate elevation and azimuth angles from source to listener
        
        Args:
            source_pos: Source position (x, y, z)
            listener_pos: Listener position (x, y, z)
            
        Returns:
            Tuple of (elevation_angle, azimuth_angle) in degrees
        """
        dx = listener_pos[0] - source_pos[0]
        dy = listener_pos[1] - source_pos[1]
        dz = listener_pos[2] - source_pos[2]
        
        # Calculate elevation angle (vertical angle from horizontal plane)
        horizontal_distance = math.sqrt(dx**2 + dz**2)
        elevation_angle = math.degrees(math.atan2(dy, horizontal_distance))
        
        # Calculate azimuth angle (horizontal angle from front direction)
        azimuth_angle = math.degrees(math.atan2(dx, dz))
        
        return (elevation_angle, azimuth_angle)
    
    def calculate_directivity_factor(self, source: SoundSource3D, 
                                   elevation: float, azimuth: float) -> float:
        """
        Calculate directivity factor based on source pattern and angles
        
        Args:
            source: SoundSource3D object
            elevation: Elevation angle in degrees
            azimuth: Azimuth angle in degrees
            
        Returns:
            Directivity factor (0.0 to 1.0)
        """
        # Convert angles to radians
        elev_rad = math.radians(elevation)
        azim_rad = math.radians(azimuth)
        
        if source.directivity_pattern == "omnidirectional":
            return 1.0
            
        elif source.directivity_pattern == "cardioid":
            # Cardioid pattern: D(θ) = 0.5 * (1 + cos(θ))
            angle_from_front = math.sqrt(elev_rad**2 + azim_rad**2)
            directivity = 0.5 * (1 + math.cos(angle_from_front))
            
        elif source.directivity_pattern == "hypercardioid":
            # Hypercardioid pattern: D(θ) = 0.5 * (1 + 1.5 * cos(θ))
            angle_from_front = math.sqrt(elev_rad**2 + azim_rad**2)
            directivity = 0.5 * (1 + 1.5 * math.cos(angle_from_front))
            
        elif source.directivity_pattern == "figure8":
            # Figure-8 pattern: D(θ) = |cos(θ)|
            angle_from_front = math.sqrt(elev_rad**2 + azim_rad**2)
            directivity = abs(math.cos(angle_from_front))
            
        elif source.directivity_pattern == "custom":
            # Custom pattern using spherical harmonics approximation
            a0, a1, a2 = source.directivity_coefficients
            angle_from_front = math.sqrt(elev_rad**2 + azim_rad**2)
            directivity = a0 + a1 * math.cos(angle_from_front) + a2 * math.cos(2 * angle_from_front)
            directivity = max(0.0, min(1.0, directivity))  # Clamp to 0-1
            
        else:
            # Default to omnidirectional
            return 1.0
            
        return max(0.0, min(1.0, directivity))
    
    def calculate_geometric_spreading_loss_3d(self, distance: float, 
                                            source: SoundSource3D) -> float:
        """
        Calculate 3D geometric spreading loss with near-field considerations
        
        Args:
            distance: Distance from source in meters
            source: SoundSource3D object
            
        Returns:
            Spreading loss in dB
        """
        if distance <= 0:
            return 0.0
            
        # Near field vs far field behavior
        if distance < source.near_field_distance:
            # Near field: Spherical spreading with additional complexity
            spreading_loss = 10 * math.log10(distance / 1.0)  # Simplified near field
        else:
            # Far field: Spherical spreading (inverse square law)
            spreading_loss = 20 * math.log10(distance / 1.0)
            
        return spreading_loss
    
    def calculate_atmospheric_absorption_3d(self, distance: float, 
                                          frequency: float) -> float:
        """
        Calculate 3D atmospheric absorption loss
        
        Args:
            distance: Distance in meters
            frequency: Frequency in Hz
            
        Returns:
            Absorption loss in dB
        """
        # Simplified atmospheric absorption model
        # Based on temperature, humidity, and frequency
        
        temp_factor = 1.0 + (self.environmental_factors["temperature"] - 20.0) / 100.0
        humidity_factor = 1.0 + (self.environmental_factors["humidity"] - 50.0) / 200.0
        
        # Frequency-dependent absorption (simplified)
        if frequency < 500:
            base_absorption = 0.0001  # Very low for bass
        elif frequency < 2000:
            base_absorption = 0.0005  # Low for midrange
        elif frequency < 8000:
            base_absorption = 0.002   # Moderate for upper midrange
        else:
            base_absorption = 0.005   # High for treble
            
        # Convert to dB loss over distance (km)
        absorption_loss = base_absorption * distance * temp_factor * humidity_factor
        
        return absorption_loss
    
    def calculate_air_absorption_coefficient(self, frequency: float) -> float:
        """
        Calculate detailed air absorption coefficient for a given frequency
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            Absorption coefficient in dB/m
        """
        # More detailed model based on ISO 9613-1
        temp_k = self.environmental_factors["temperature"] + 273.15
        pressure_atm = self.environmental_factors["pressure"] / 101325.0
        
        # Oxygen relaxation frequency
        fr_o = 24.0 + 4.04e4 * (self.environmental_factors["humidity"] / 100.0) * (273.15 / temp_k)
        
        # Nitrogen relaxation frequency  
        fr_n = (temp_k / 293.15) ** (-0.5) * (
            9.0 + 280.0 * (self.environmental_factors["humidity"] / 100.0) * 
            math.exp(-4.17 * ((temp_k / 293.15) ** (-1/3) - 1))
        )
        
        # Absorption coefficient calculation
        alpha_o = 0.0127 * (fr_o / (frequency ** 2 + fr_o ** 2)) * (293.15 / temp_k) ** (5/2)
        alpha_n = 0.1068 * (fr_n / (frequency ** 2 + fr_n ** 2)) * (293.15 / temp_k) ** (5/2)
        
        # Total absorption coefficient (dB/m)
        alpha_total = pressure_atm * (alpha_o + alpha_n) * (frequency ** 2) / 1000.0
        
        return alpha_total
    
    def trace_propagation_paths(self, source_id: str, listener_id: str) -> List[PropagationPath]:
        """
        Trace propagation paths from source to listener in 3D space
        
        Args:
            source_id: ID of the sound source
            listener_id: ID of the listener
            
        Returns:
            List of PropagationPath objects
        """
        if source_id not in self.sound_sources or listener_id not in self.listeners:
            return []
            
        source = self.sound_sources[source_id]
        listener = self.listeners[listener_id]
        
        # Calculate direct path
        distance = self.calculate_3d_distance(source.position, listener.position)
        elevation, azimuth = self.calculate_3d_angles(source.position, listener.position)
        
        # Calculate path loss components
        spreading_loss = self.calculate_geometric_spreading_loss_3d(distance, source)
        absorption_coeff = self.calculate_air_absorption_coefficient(source.frequency)
        absorption_loss = absorption_coeff * distance
        
        # Total path loss
        total_path_loss = spreading_loss + absorption_loss
        
        # Calculate time delay
        time_delay = distance / self.environmental_factors["sound_speed"]
        
        # Calculate phase shift
        wavelength = self.environmental_factors["sound_speed"] / source.frequency if source.frequency > 0 else 1.0
        phase_shift = (2 * math.pi * distance / wavelength) % (2 * math.pi)
        
        # Create direct path
        direct_path = PropagationPath(
            source_id=source_id,
            start_position=source.position,
            end_position=listener.position,
            distance=distance,
            elevation_angle=elevation,
            azimuth_angle=azimuth,
            path_loss=total_path_loss,
            time_delay=time_delay,
            phase_shift=phase_shift
        )
        
        # TODO: Add reflected paths, diffracted paths, etc.
        paths = [direct_path]
        
        # Store for later reference
        self.propagation_paths.extend(paths)
        
        return paths
    
    def calculate_3d_sound_pressure_level(self, source_id: str, 
                                        listener_id: str) -> Dict[str, Any]:
        """
        Calculate 3D sound pressure level at listener position
        
        Args:
            source_id: ID of the sound source
            listener_id: ID of the listener
            
        Returns:
            Dictionary with SPL calculations
        """
        if source_id not in self.sound_sources or listener_id not in self.listeners:
            return {"error": "Source or listener not found"}
            
        source = self.sound_sources[source_id]
        listener = self.listeners[listener_id]
        
        # Trace propagation paths
        paths = self.trace_propagation_paths(source_id, listener_id)
        
        if not paths:
            return {"error": "No propagation paths found"}
            
        # Calculate SPL for each path
        path_spls = []
        total_power = 0.0
        
        for path in paths:
            # Calculate directivity factor for this path
            directivity = self.calculate_directivity_factor(source, 
                                                          path.elevation_angle, 
                                                          path.azimuth_angle)
            
            # Calculate reference SPL at 1m
            if source.power > 0:
                reference_spl = 10 * math.log10(source.power / 1e-12)  # Assuming reference power
            else:
                reference_spl = 100.0  # Default SPL
                
            # Calculate SPL at listener position
            spl = reference_spl + directivity - path.path_loss
            
            path_spls.append({
                "path": path,
                "directivity": directivity,
                "spl": spl,
                "power_contribution": 10 ** (spl / 10) * 1e-12  # Convert back to power
            })
            
            total_power += 10 ** (spl / 10) * 1e-12
            
        # Calculate combined SPL (coherent or incoherent sum)
        # For simplicity, we'll use incoherent sum (power sum)
        combined_spl = 10 * math.log10(total_power / 1e-12) if total_power > 0 else 0.0
        
        result = {
            "source_id": source_id,
            "listener_id": listener_id,
            "source_position": source.position,
            "listener_position": listener.position,
            "total_paths": len(paths),
            "combined_spl_db": combined_spl,
            "individual_paths": path_spls,
            "direct_path_spl": path_spls[0]["spl"] if path_spls else 0.0,
            "distance_m": paths[0].distance if paths else 0.0,
            "elevation_deg": paths[0].elevation_angle if paths else 0.0,
            "azimuth_deg": paths[0].azimuth_angle if paths else 0.0
        }
        
        return result
    
    def simulate_3d_sound_field(self, source_id: str, 
                              listener_positions: List[Tuple[float, float, float]]) -> List[Dict[str, float]]:
        """
        Simulate 3D sound field at multiple listener positions
        
        Args:
            source_id: ID of the sound source
            listener_positions: List of (x, y, z) positions to evaluate
            
        Returns:
            List of dictionaries with SPL at each position
        """
        if source_id not in self.sound_sources:
            return []
            
        source = self.sound_sources[source_id]
        field_results = []
        
        for i, position in enumerate(listener_positions):
            # Create temporary listener
            temp_listener = Listener3D(
                position=position,
                orientation=(0.0, 0.0, 0.0),
                head_radius=0.0875  # Average human head radius
            )
            
            # Add to system temporarily
            temp_listener_id = f"temp_listener_{i}"
            self.listeners[temp_listener_id] = temp_listener
            
            # Calculate SPL at this position
            spl_result = self.calculate_3d_sound_pressure_level(source_id, temp_listener_id)
            
            if "error" not in spl_result:
                field_results.append({
                    "position": position,
                    "distance_m": spl_result["distance_m"],
                    "spl_db": spl_result["combined_spl_db"],
                    "elevation_deg": spl_result["elevation_deg"],
                    "azimuth_deg": spl_result["azimuth_deg"]
                })
            
            # Remove temporary listener
            del self.listeners[temp_listener_id]
            
        return field_results
    
    def optimize_source_orientation(self, source_id: str, 
                                  target_listener_id: str) -> Dict[str, Any]:
        """
        Optimize source orientation for maximum SPL at target listener
        
        Args:
            source_id: ID of the sound source
            target_listener_id: ID of the target listener
            
        Returns:
            Dictionary with optimization results
        """
        if source_id not in self.sound_sources or target_listener_id not in self.listeners:
            return {"error": "Source or listener not found"}
            
        source = self.sound_sources[source_id]
        listener = self.listeners[target_listener_id]
        
        # Current SPL
        current_spl = self.calculate_3d_sound_pressure_level(source_id, target_listener_id)
        current_spl_value = current_spl.get("combined_spl_db", 0.0)
        
        # Test different orientations
        best_orientation = source.orientation
        best_spl = current_spl_value
        
        # Test orientations in 15-degree increments
        for azimuth in range(0, 360, 15):
            for elevation in range(-90, 91, 15):
                # Create test source with new orientation
                test_source = SoundSource3D(
                    id=f"test_{source_id}",
                    position=source.position,
                    orientation=(azimuth, elevation, source.orientation[2]),
                    frequency=source.frequency,
                    power=source.power,
                    directivity_pattern=source.directivity_pattern,
                    directivity_coefficients=source.directivity_coefficients,
                    beamwidth=source.beamwidth,
                    near_field_distance=source.near_field_distance
                )
                
                # Add temporarily
                self.sound_sources[f"test_{source_id}"] = test_source
                
                # Calculate SPL with new orientation
                test_spl = self.calculate_3d_sound_pressure_level(f"test_{source_id}", target_listener_id)
                test_spl_value = test_spl.get("combined_spl_db", 0.0)
                
                # Check if this is better
                if test_spl_value > best_spl:
                    best_spl = test_spl_value
                    best_orientation = (azimuth, elevation, source.orientation[2])
                
                # Remove test source
                del self.sound_sources[f"test_{source_id}"]
                
        optimization_result = {
            "source_id": source_id,
            "target_listener_id": target_listener_id,
            "current_spl": current_spl_value,
            "optimized_spl": best_spl,
            "spl_improvement_db": best_spl - current_spl_value,
            "current_orientation": source.orientation,
            "optimized_orientation": best_orientation,
            "orientation_change": (
                best_orientation[0] - source.orientation[0],
                best_orientation[1] - source.orientation[1],
                best_orientation[2] - source.orientation[2]
            )
        }
        
        return optimization_result
    
    def get_3d_propagation_summary(self) -> Dict[str, Any]:
        """
        Get summary of 3D propagation activities
        
        Returns:
            Dictionary with propagation summary
        """
        total_sources = len(self.sound_sources)
        total_listeners = len(self.listeners)
        total_paths = len(self.propagation_paths)
        
        # Calculate average distances
        if self.propagation_paths:
            total_distance = sum(path.distance for path in self.propagation_paths)
            avg_distance = total_distance / len(self.propagation_paths)
        else:
            avg_distance = 0.0
            
        return {
            "total_sound_sources": total_sources,
            "total_listeners": total_listeners,
            "total_propagation_paths": total_paths,
            "average_propagation_distance_m": avg_distance,
            "environmental_conditions": self.environmental_factors
        }

class Advanced3DPropagationModel:
    """Advanced 3D propagation modeling with ray tracing and diffraction"""
    
    def __init__(self, propagation_system: Directional3DPropagation):
        """Initialize advanced 3D propagation model"""
        self.propagation_system = propagation_system
        
    def calculate_reflected_paths(self, source_id: str, listener_id: str) -> List[PropagationPath]:
        """
        Calculate reflected propagation paths using ray tracing
        
        Args:
            source_id: ID of the sound source
            listener_id: ID of the listener
            
        Returns:
            List of reflected PropagationPath objects
        """
        # This would implement ray tracing for reflected paths
        # For now, we'll return a simplified result
        
        return []
    
    def calculate_diffracted_paths(self, source_id: str, listener_id: str) -> List[PropagationPath]:
        """
        Calculate diffracted propagation paths around obstacles
        
        Args:
            source_id: ID of the sound source
            listener_id: ID of the listener
            
        Returns:
            List of diffracted PropagationPath objects
        """
        # This would implement diffraction calculations
        # For now, we'll return a simplified result
        
        return []
    
    def apply_atmospheric_turbulence(self, path: PropagationPath) -> float:
        """
        Apply atmospheric turbulence effects to a propagation path
        
        Args:
            path: PropagationPath object
            
        Returns:
            Turbulence-induced loss in dB
        """
        # Simplified turbulence model
        wind_speed = 5.0  # m/s (assumed)
        turbulence_parameter = min(1.0, wind_speed / 20.0)
        frequency_factor = min(1.0, path.distance / 10000.0)
        
        turbulence_loss = turbulence_parameter * frequency_factor * 2.0  # Up to 2dB
        
        return turbulence_loss

# Global instances
directional_3d_propagation = Directional3DPropagation()
advanced_3d_model = None

def initialize_directional_3d_propagation():
    """Initialize the global directional 3D propagation system"""
    global directional_3d_propagation, advanced_3d_model
    directional_3d_propagation = Directional3DPropagation()
    advanced_3d_model = Advanced3DPropagationModel(directional_3d_propagation)
    return directional_3d_propagation

def add_3d_sound_source(source: SoundSource3D):
    """Add a 3D sound source to the propagation system"""
    directional_3d_propagation.add_sound_source_3d(source)

def add_3d_listener(listener_id: str, listener: Listener3D):
    """Add a 3D listener to the propagation system"""
    directional_3d_propagation.add_listener_3d(listener_id, listener)

def set_3d_environmental_conditions(temperature = None,
                                  humidity = None,
                                  pressure = None):
    """Set environmental conditions for 3D sound propagation"""
    directional_3d_propagation.set_environmental_conditions(temperature, humidity, pressure)

def calculate_3d_sound_pressure_level(source_id: str, listener_id: str):
    """Calculate 3D sound pressure level at listener position"""
    return directional_3d_propagation.calculate_3d_sound_pressure_level(source_id, listener_id)

def simulate_3d_sound_field(source_id: str, listener_positions: List[Tuple[float, float, float]]):
    """Simulate 3D sound field at multiple listener positions"""
    return directional_3d_propagation.simulate_3d_sound_field(source_id, listener_positions)

def optimize_3d_source_orientation(source_id: str, target_listener_id: str):
    """Optimize source orientation for maximum SPL at target listener"""
    return directional_3d_propagation.optimize_source_orientation(source_id, target_listener_id)

def trace_3d_propagation_paths(source_id: str, listener_id: str):
    """Trace propagation paths from source to listener in 3D space"""
    return directional_3d_propagation.trace_propagation_paths(source_id, listener_id)

def get_3d_propagation_summary():
    """Get summary of 3D propagation activities"""
    return directional_3d_propagation.get_3d_propagation_summary()