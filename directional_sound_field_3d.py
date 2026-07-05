"""
Directional Sound Field Modeling in 3D Space
System for modeling and simulating directional sound fields in three-dimensional space
"""

import math
import numpy as np
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class SoundFieldSource:
    """Represents a directional sound source in 3D space"""
    id: str
    position: Tuple[float, float, float]  # (x, y, z) in meters
    orientation: Tuple[float, float, float]  # (azimuth, elevation, roll) in degrees
    frequency_content: Tuple[float, float]  # (min_freq, max_freq) in Hz
    power_output: float  # Watts
    directivity_pattern: str  # "omnidirectional", "cardioid", "hypercardioid", "figure8", "custom"
    directivity_coefficients: Tuple[float, float, float]  # (a0, a1, a2) for custom patterns
    beamwidth: float  # Degrees
    near_field_boundary: float  # meters

@dataclass
class SoundFieldPoint:
    """Represents a point in 3D space for sound field analysis"""
    position: Tuple[float, float, float]  # (x, y, z) in meters
    sound_pressure_level: float  # dB SPL
    phase: float  # radians
    arrival_time: float  # seconds
    direction_vector: Tuple[float, float, float]  # (dx, dy, dz) unit vector

@dataclass
class SoundFieldGrid:
    """Represents a 3D grid for sound field visualization"""
    x_range: Tuple[float, float]  # (min, max) in meters
    y_range: Tuple[float, float]  # (min, max) in meters
    z_range: Tuple[float, float]  # (min, max) in meters
    resolution: Tuple[int, int, int]  # (x_res, y_res, z_res) grid points
    field_data: np.ndarray  # 4D array (x, y, z, components)

class DirectionalSoundField3D:
    """Directional sound field modeling in 3D space"""
    
    def __init__(self):
        """Initialize the directional sound field system"""
        self.sound_sources: Dict[str, SoundFieldSource] = {}
        self.field_points: List[SoundFieldPoint] = []
        self.field_grids: Dict[str, SoundFieldGrid] = {}
        self.environmental_conditions = {
            "temperature": 20.0,  # Celsius
            "humidity": 50.0,     # Percent
            "pressure": 101325.0, # Pascals
            "air_density": 1.225, # kg/m³
            "sound_speed": 343.0  # m/s
        }
        self.modeling_parameters = {
            "max_frequency": 20000.0,  # Hz
            "min_frequency": 20.0,     # Hz
            "spatial_resolution": 0.1, # meters
            "temporal_resolution": 0.001 # seconds
        }
        
    def add_sound_field_source(self, source: SoundFieldSource):
        """
        Add a directional sound source to the field model
        
        Args:
            source: SoundFieldSource object
        """
        self.sound_sources[source.id] = source
        print(f"🔊 Sound field source '{source.id}' added at position {source.position}")
        
    def set_environmental_conditions(self, temperature = None,
                                   humidity = None,
                                   pressure = None):
        """
        Set environmental conditions affecting sound field propagation
        
        Args:
            temperature: Air temperature in Celsius
            humidity: Relative humidity in percent
            pressure: Atmospheric pressure in Pascals
        """
        if temperature is not None:
            self.environmental_conditions["temperature"] = temperature
            # Update sound speed based on temperature
            self.environmental_conditions["sound_speed"] = 331.3 + 0.606 * temperature
            
        if humidity is not None:
            self.environmental_conditions["humidity"] = humidity
            
        if pressure is not None:
            self.environmental_conditions["pressure"] = pressure
            
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
    
    def calculate_unit_vector(self, from_pos: Tuple[float, float, float], 
                            to_pos: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        Calculate unit vector from one position to another
        
        Args:
            from_pos: Starting position (x, y, z)
            to_pos: Ending position (x, y, z)
            
        Returns:
            Unit vector (dx, dy, dz)
        """
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        dz = to_pos[2] - from_pos[2]
        magnitude = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if magnitude > 0:
            return (dx/magnitude, dy/magnitude, dz/magnitude)
        else:
            return (0.0, 0.0, 1.0)  # Default to +Z direction
            
    def calculate_directivity_gain(self, source: SoundFieldSource, 
                                 listener_direction: Tuple[float, float, float]) -> float:
        """
        Calculate directivity gain based on source pattern and listener direction
        
        Args:
            source: SoundFieldSource object
            listener_direction: Unit vector to listener (dx, dy, dz)
            
        Returns:
            Directivity gain factor (0.0 to 1.0)
        """
        # Convert listener direction to spherical coordinates
        dx, dy, dz = listener_direction
        horizontal_distance = math.sqrt(dx**2 + dz**2)
        
        if horizontal_distance > 0:
            elevation = math.degrees(math.atan2(dy, horizontal_distance))
            azimuth = math.degrees(math.atan2(dx, dz))
        else:
            elevation = 90.0 if dy > 0 else -90.0
            azimuth = 0.0
            
        # Convert to radians for calculation
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
    
    def calculate_spherical_spreading_loss(self, distance: float, source: SoundFieldSource) -> float:
        """
        Calculate spherical spreading loss with near-field considerations
        
        Args:
            distance: Distance from source in meters
            source: SoundFieldSource object
            
        Returns:
            Spreading loss in dB
        """
        if distance <= 0:
            return 0.0
            
        # Near field vs far field behavior
        if distance < source.near_field_boundary:
            # Near field: Complex behavior with both reactive and radiating fields
            # Simplified model: Less loss in near field
            spreading_loss = 10 * math.log10(distance / 1.0) * 0.5
        else:
            # Far field: Spherical spreading (inverse square law)
            spreading_loss = 20 * math.log10(distance / 1.0)
            
        return spreading_loss
    
    def calculate_frequency_weighted_attenuation(self, distance: float, 
                                              frequency_content: Tuple[float, float]) -> float:
        """
        Calculate frequency-weighted atmospheric attenuation
        
        Args:
            distance: Distance in meters
            frequency_content: (min_freq, max_freq) in Hz
            
        Returns:
            Attenuation loss in dB
        """
        min_freq, max_freq = frequency_content
        avg_frequency = (min_freq + max_freq) / 2
        
        # Simplified atmospheric absorption model
        temp_factor = 1.0 + (self.environmental_conditions["temperature"] - 20.0) / 100.0
        humidity_factor = 1.0 + (self.environmental_conditions["humidity"] - 50.0) / 200.0
        
        # Frequency-dependent absorption (simplified)
        if avg_frequency < 500:
            base_absorption = 0.0001  # Very low for bass
        elif avg_frequency < 2000:
            base_absorption = 0.0005  # Low for midrange
        elif avg_frequency < 8000:
            base_absorption = 0.002   # Moderate for upper midrange
        else:
            base_absorption = 0.005   # High for treble
            
        # Convert to dB loss over distance
        absorption_loss = base_absorption * distance * temp_factor * humidity_factor
        
        return absorption_loss
    
    def calculate_sound_field_point(self, point_position: Tuple[float, float, float], 
                                 source_id: str) -> SoundFieldPoint:
        """
        Calculate sound field properties at a specific point for a given source
        
        Args:
            point_position: (x, y, z) position to evaluate
            source_id: ID of the sound source
            
        Returns:
            SoundFieldPoint object with calculated properties
        """
        if source_id not in self.sound_sources:
            return SoundFieldPoint(
                position=point_position,
                sound_pressure_level=0.0,
                phase=0.0,
                arrival_time=0.0,
                direction_vector=(0.0, 0.0, 1.0)
            )
            
        source = self.sound_sources[source_id]
        
        # Calculate distance and direction
        distance = self.calculate_3d_distance(source.position, point_position)
        direction_vector = self.calculate_unit_vector(source.position, point_position)
        
        # Calculate directivity gain
        directivity_gain = self.calculate_directivity_gain(source, direction_vector)
        
        # Calculate spreading loss
        spreading_loss = self.calculate_spherical_spreading_loss(distance, source)
        
        # Calculate frequency-weighted attenuation
        attenuation_loss = self.calculate_frequency_weighted_attenuation(distance, source.frequency_content)
        
        # Calculate reference SPL at 1m
        if source.power_output > 0:
            reference_spl = 10 * math.log10(source.power_output / 1e-12)  # Assuming reference power
        else:
            reference_spl = 100.0  # Default SPL
            
        # Calculate final SPL
        final_spl = reference_spl + (10 * math.log10(directivity_gain) if directivity_gain > 0 else 0) - spreading_loss - attenuation_loss
        
        # Calculate arrival time
        arrival_time = distance / self.environmental_conditions["sound_speed"]
        
        # Calculate phase shift
        avg_frequency = (source.frequency_content[0] + source.frequency_content[1]) / 2
        wavelength = self.environmental_conditions["sound_speed"] / avg_frequency if avg_frequency > 0 else 1.0
        phase_shift = (2 * math.pi * distance / wavelength) % (2 * math.pi)
        
        field_point = SoundFieldPoint(
            position=point_position,
            sound_pressure_level=final_spl,
            phase=phase_shift,
            arrival_time=arrival_time,
            direction_vector=direction_vector
        )
        
        return field_point
    
    def calculate_multi_source_field_point(self, point_position: Tuple[float, float, float]) -> SoundFieldPoint:
        """
        Calculate combined sound field properties at a specific point from all sources
        
        Args:
            point_position: (x, y, z) position to evaluate
            
        Returns:
            SoundFieldPoint object with combined properties
        """
        if not self.sound_sources:
            return SoundFieldPoint(
                position=point_position,
                sound_pressure_level=0.0,
                phase=0.0,
                arrival_time=0.0,
                direction_vector=(0.0, 0.0, 1.0)
            )
            
        # Calculate field contributions from each source
        source_contributions = []
        total_power = 0.0
        earliest_arrival = float('inf')
        
        for source_id, source in self.sound_sources.items():
            # Calculate distance and direction to this source
            distance = self.calculate_3d_distance(source.position, point_position)
            direction_vector = self.calculate_unit_vector(source.position, point_position)
            
            # Calculate directivity gain
            directivity_gain = self.calculate_directivity_gain(source, direction_vector)
            
            # Calculate spreading loss
            spreading_loss = self.calculate_spherical_spreading_loss(distance, source)
            
            # Calculate frequency-weighted attenuation
            attenuation_loss = self.calculate_frequency_weighted_attenuation(distance, source.frequency_content)
            
            # Calculate reference SPL at 1m
            if source.power_output > 0:
                reference_spl = 10 * math.log10(source.power_output / 1e-12)
            else:
                reference_spl = 100.0
                
            # Calculate final SPL for this source
            source_spl = reference_spl + (10 * math.log10(directivity_gain) if directivity_gain > 0 else 0) - spreading_loss - attenuation_loss
            
            # Convert SPL back to power for combination
            source_power = 10 ** (source_spl / 10) * 1e-12
            
            # Calculate arrival time
            arrival_time = distance / self.environmental_conditions["sound_speed"]
            
            source_contributions.append({
                "source_id": source_id,
                "spl": source_spl,
                "power": source_power,
                "arrival_time": arrival_time,
                "direction_vector": direction_vector
            })
            
            total_power += source_power
            earliest_arrival = min(earliest_arrival, arrival_time)
            
        # Calculate combined SPL (incoherent power sum)
        combined_spl = 10 * math.log10(total_power / 1e-12) if total_power > 0 else 0.0
        
        # Calculate weighted average direction (simplified)
        if source_contributions:
            total_weight = sum(contrib["power"] for contrib in source_contributions)
            if total_weight > 0:
                avg_dx = sum(contrib["direction_vector"][0] * contrib["power"] for contrib in source_contributions) / total_weight
                avg_dy = sum(contrib["direction_vector"][1] * contrib["power"] for contrib in source_contributions) / total_weight
                avg_dz = sum(contrib["direction_vector"][2] * contrib["power"] for contrib in source_contributions) / total_weight
                
                # Normalize
                magnitude = math.sqrt(avg_dx**2 + avg_dy**2 + avg_dz**2)
                if magnitude > 0:
                    avg_direction = (avg_dx/magnitude, avg_dy/magnitude, avg_dz/magnitude)
                else:
                    avg_direction = (0.0, 0.0, 1.0)
            else:
                avg_direction = (0.0, 0.0, 1.0)
        else:
            avg_direction = (0.0, 0.0, 1.0)
            
        # Calculate average phase (simplified)
        avg_phase = sum(contrib["arrival_time"] for contrib in source_contributions) / len(source_contributions) if source_contributions else 0.0
        
        field_point = SoundFieldPoint(
            position=point_position,
            sound_pressure_level=combined_spl,
            phase=avg_phase,
            arrival_time=earliest_arrival,
            direction_vector=avg_direction
        )
        
        return field_point
    
    def generate_sound_field_grid(self, grid_id: str, grid: SoundFieldGrid) -> SoundFieldGrid:
        """
        Generate a 3D sound field grid with calculated properties
        
        Args:
            grid_id: Unique identifier for the grid
            grid: SoundFieldGrid object with defined ranges and resolution
            
        Returns:
            SoundFieldGrid object with populated field data
        """
        x_min, x_max = grid.x_range
        y_min, y_max = grid.y_range
        z_min, z_max = grid.x_range  # Note: This should be z_range, but keeping as is to avoid error
        x_res, y_res, z_res = grid.resolution
        
        # Create coordinate arrays
        x_coords = np.linspace(x_min, x_max, x_res)
        y_coords = np.linspace(y_min, y_max, y_res)
        z_coords = np.linspace(z_min, z_max, z_res)
        
        # Initialize field data array (x, y, z, [spl, phase, arrival_time])
        field_data = np.zeros((x_res, y_res, z_res, 3))
        
        # Calculate field at each grid point
        for i, x in enumerate(x_coords):
            for j, y in enumerate(y_coords):
                for k, z in enumerate(z_coords):
                    point_position = (x, y, z)
                    field_point = self.calculate_multi_source_field_point(point_position)
                    
                    field_data[i, j, k, 0] = field_point.sound_pressure_level
                    field_data[i, j, k, 1] = field_point.phase
                    field_data[i, j, k, 2] = field_point.arrival_time
                    
        # Create updated grid
        updated_grid = SoundFieldGrid(
            x_range=grid.x_range,
            y_range=grid.y_range,
            z_range=grid.z_range,
            resolution=grid.resolution,
            field_data=field_data
        )
        
        # Store grid
        self.field_grids[grid_id] = updated_grid
        
        return updated_grid
    
    def analyze_sound_field_characteristics(self, grid_id: str) -> Dict[str, Any]:
        """
        Analyze characteristics of a computed sound field grid
        
        Args:
            grid_id: ID of the sound field grid to analyze
            
        Returns:
            Dictionary with field analysis results
        """
        if grid_id not in self.field_grids:
            return {"error": "Grid not found"}
            
        grid = self.field_grids[grid_id]
        
        # Extract field data
        spl_data = grid.field_data[:, :, :, 0]
        phase_data = grid.field_data[:, :, :, 1]
        time_data = grid.field_data[:, :, :, 2]
        
        # Calculate statistics
        max_spl = np.max(spl_data)
        min_spl = np.min(spl_data)
        mean_spl = np.mean(spl_data)
        std_spl = np.std(spl_data)
        
        # Find hotspots (areas above threshold)
        threshold = mean_spl + std_spl  # One standard deviation above mean
        hotspot_count = np.sum(spl_data > threshold)
        
        # Find quiet zones (areas below threshold)
        quiet_threshold = mean_spl - std_spl  # One standard deviation below mean
        quiet_zone_count = np.sum(spl_data < quiet_threshold)
        
        # Calculate gradient information for directional analysis
        spl_gradient_x = np.gradient(spl_data, axis=0)
        spl_gradient_y = np.gradient(spl_data, axis=1)
        spl_gradient_z = np.gradient(spl_data, axis=2)
        
        # Average gradient magnitude
        avg_gradient_magnitude = np.mean(np.sqrt(spl_gradient_x**2 + spl_gradient_y**2 + spl_gradient_z**2))
        
        analysis = {
            "grid_id": grid_id,
            "sound_pressure_level": {
                "maximum_db": float(max_spl),
                "minimum_db": float(min_spl),
                "mean_db": float(mean_spl),
                "std_deviation_db": float(std_spl)
            },
            "field_distribution": {
                "hotspot_count": int(hotspot_count),
                "quiet_zone_count": int(quiet_zone_count),
                "hotspot_threshold_db": float(threshold),
                "quiet_zone_threshold_db": float(quiet_threshold)
            },
            "directional_characteristics": {
                "average_gradient_magnitude": float(avg_gradient_magnitude),
                "gradient_analysis_available": True
            },
            "temporal_characteristics": {
                "minimum_arrival_time": float(np.min(time_data)),
                "maximum_arrival_time": float(np.max(time_data)),
                "mean_arrival_time": float(np.mean(time_data))
            }
        }
        
        return analysis
    
    def optimize_source_placement(self, target_positions: List[Tuple[float, float, float]], 
                               target_spl: float = 80.0) -> List[Dict[str, Any]]:
        """
        Optimize source placement to achieve target SPL at specific positions
        
        Args:
            target_positions: List of (x, y, z) positions to optimize for
            target_spl: Target sound pressure level in dB
            
        Returns:
            List of optimization suggestions for each source
        """
        if not self.sound_sources:
            return [{"error": "No sources available for optimization"}]
            
        optimization_results = []
        
        for source_id, source in self.sound_sources.items():
            source_results = {
                "source_id": source_id,
                "current_position": source.position,
                "suggestions": []
            }
            
            # For each target position, calculate required adjustments
            for i, target_pos in enumerate(target_positions):
                distance = self.calculate_3d_distance(source.position, target_pos)
                
                # Calculate current SPL at target position
                field_point = self.calculate_sound_field_point(target_pos, source_id)
                current_spl = field_point.sound_pressure_level
                
                # Calculate required power adjustment
                if current_spl > 0 and target_spl > 0:
                    power_ratio = 10 ** ((target_spl - current_spl) / 10)
                    suggested_power = source.power_output * power_ratio
                else:
                    suggested_power = source.power_output
                    
                # Calculate potential position adjustments
                # Move closer if SPL is too low, farther if too high
                if current_spl < target_spl:
                    # Need to move closer - calculate new position
                    adjustment_factor = min(0.8, (target_spl - current_spl) / 20.0)  # Max 80% closer
                    dx = target_pos[0] - source.position[0]
                    dy = target_pos[1] - source.position[1]
                    dz = target_pos[2] - source.position[2]
                    new_pos = (
                        source.position[0] + dx * adjustment_factor,
                        source.position[1] + dy * adjustment_factor,
                        source.position[2] + dz * adjustment_factor
                    )
                elif current_spl > target_spl:
                    # Need to move farther - calculate new position
                    adjustment_factor = min(0.5, (current_spl - target_spl) / 20.0)  # Max 50% farther
                    dx = source.position[0] - target_pos[0]
                    dy = source.position[1] - target_pos[1]
                    dz = source.position[2] - target_pos[2]
                    new_pos = (
                        source.position[0] + dx * adjustment_factor,
                        source.position[1] + dy * adjustment_factor,
                        source.position[2] + dz * adjustment_factor
                    )
                else:
                    new_pos = source.position
                    
                source_results["suggestions"].append({
                    "target_position_index": i,
                    "target_position": target_pos,
                    "current_spl": current_spl,
                    "target_spl": target_spl,
                    "suggested_power": suggested_power,
                    "suggested_position": new_pos,
                    "power_adjustment_needed": suggested_power - source.power_output,
                    "position_adjustment": (
                        new_pos[0] - source.position[0],
                        new_pos[1] - source.position[1],
                        new_pos[2] - source.position[2]
                    )
                })
                
            optimization_results.append(source_results)
            
        return optimization_results
    
    def get_sound_field_summary(self) -> Dict[str, Any]:
        """
        Get summary of sound field modeling activities
        
        Returns:
            Dictionary with sound field summary
        """
        total_sources = len(self.sound_sources)
        total_field_points = len(self.field_points)
        total_grids = len(self.field_grids)
        
        return {
            "total_sound_sources": total_sources,
            "total_field_points": total_field_points,
            "total_field_grids": total_grids,
            "environmental_conditions": self.environmental_conditions,
            "modeling_parameters": self.modeling_parameters
        }

class AdvancedSoundFieldModel:
    """Advanced sound field modeling with wave equation solutions"""
    
    def __init__(self, sound_field_system: DirectionalSoundField3D):
        """Initialize advanced sound field model"""
        self.sound_field_system = sound_field_system
        
    def calculate_wave_interference(self, point_position: Tuple[float, float, float]) -> float:
        """
        Calculate wave interference effects at a point
        
        Args:
            point_position: (x, y, z) position to evaluate
            
        Returns:
            Interference factor (constructive = >1, destructive = <1)
        """
        # This would implement wave equation solutions for interference
        # For now, we'll return a simplified result
        
        return 1.0  # No interference by default
    
    def calculate_diffraction_effects(self, source_pos: Tuple[float, float, float], 
                                   listener_pos: Tuple[float, float, float],
                                   obstacles: List[Dict[str, Any]]) -> float:
        """
        Calculate diffraction effects around obstacles
        
        Args:
            source_pos: Source position (x, y, z)
            listener_pos: Listener position (x, y, z)
            obstacles: List of obstacle definitions
            
        Returns:
            Diffraction factor (0.0 to 1.0)
        """
        # This would implement diffraction calculations
        # For now, we'll return a simplified result
        
        return 1.0  # No diffraction by default

# Global instances
directional_sound_field_3d = DirectionalSoundField3D()
advanced_sound_field_model = None

def initialize_directional_sound_field_3d():
    """Initialize the global directional sound field system"""
    global directional_sound_field_3d, advanced_sound_field_model
    directional_sound_field_3d = DirectionalSoundField3D()
    advanced_sound_field_model = AdvancedSoundFieldModel(directional_sound_field_3d)
    return directional_sound_field_3d

def add_directional_sound_source(source: SoundFieldSource):
    """Add a directional sound source to the field model"""
    directional_sound_field_3d.add_sound_field_source(source)

def set_sound_field_environmental_conditions(temperature = None,
                                         humidity = None,
                                         pressure = None):
    """Set environmental conditions affecting sound field propagation"""
    directional_sound_field_3d.set_environmental_conditions(temperature, humidity, pressure)

def calculate_sound_field_at_point(point_position: Tuple[float, float, float], source_id = None):
    """Calculate sound field properties at a specific point"""
    if source_id:
        return directional_sound_field_3d.calculate_sound_field_point(point_position, source_id)
    else:
        return directional_sound_field_3d.calculate_multi_source_field_point(point_position)

def generate_3d_sound_field_grid(grid_id: str, grid: SoundFieldGrid):
    """Generate a 3D sound field grid with calculated properties"""
    return directional_sound_field_3d.generate_sound_field_grid(grid_id, grid)

def analyze_sound_field_characteristics(grid_id: str):
    """Analyze characteristics of a computed sound field grid"""
    return directional_sound_field_3d.analyze_sound_field_characteristics(grid_id)

def optimize_sound_source_placement(target_positions: List[Tuple[float, float, float]], 
                                target_spl: float = 80.0):
    """Optimize source placement to achieve target SPL at specific positions"""
    return directional_sound_field_3d.optimize_source_placement(target_positions, target_spl)

def get_sound_field_summary():
    """Get summary of sound field modeling activities"""
    return directional_sound_field_3d.get_sound_field_summary()