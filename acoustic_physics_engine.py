"""
Acoustic Physics Engine for Realistic Sound Wave Simulation
Simulates sound wave physics including direction, intensity, distance, and multi-source interactions
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from array import array

@dataclass
class SoundSource:
    """Represents a sound source in 3D space"""
    id: str
    position: Tuple[float, float, float]  # (x, y, z)
    frequency: float  # Hz
    amplitude: float  # 0.0 to 1.0
    phase: float  # radians
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # (vx, vy, vz)
    type: str = "point"  # point, plane, spherical
    direction: Tuple[float, float, float] = (0.0, 0.0, 1.0)  # direction vector for directional sources

@dataclass
class SoundListener:
    """Represents a listener in 3D space"""
    position: Tuple[float, float, float]  # (x, y, z)
    orientation: Tuple[float, float, float] = (0.0, 0.0, 1.0)  # facing direction
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)  # (vx, vy, vz)

@dataclass
class SoundWave:
    """Represents a sound wave propagating through space"""
    source_id: str
    frequency: float
    amplitude: float
    phase: float
    position: Tuple[float, float, float]
    direction: Tuple[float, float, float]
    speed: float  # m/s (speed of sound in medium)
    distance_traveled: float
    timestamp: float

class AcousticPhysicsEngine:
    """Simulates realistic acoustic physics for 3D sound immersion"""
    
    def __init__(self, sound_speed: float = 343.0, air_density: float = 1.225):
        """
        Initialize the acoustic physics engine
        
        Args:
            sound_speed: Speed of sound in m/s (default: 343 m/s for air at 20°C)
            air_density: Density of air in kg/m³ (default: 1.225 kg/m³ for air at sea level)
        """
        self.sound_speed = sound_speed  # Speed of sound in medium (m/s)
        self.air_density = air_density  # Air density (kg/m³)
        self.sound_sources: Dict[str, SoundSource] = {}
        self.sound_waves: List[SoundWave] = []
        self.listener = SoundListener((0.0, 0.0, 0.0))
        self.environment_properties = {
            "absorption_coefficients": {},  # Frequency-dependent absorption
            "reflection_properties": {},    # Surface reflection characteristics
            "temperature": 20.0,            # Celsius
            "humidity": 50.0,               # Percent
            "pressure": 101325.0            # Pascals
        }
        self.sample_rate = 44100
        self.time_step = 1.0 / self.sample_rate
        self.current_time = 0.0
        
    def initialize_environment_properties(self, temperature: float = 20.0, 
                                       humidity: float = 50.0, 
                                       pressure: float = 101325.0):
        """
        Initialize environmental properties that affect sound propagation
        
        Args:
            temperature: Air temperature in Celsius
            humidity: Relative humidity in percent
            pressure: Atmospheric pressure in Pascals
        """
        self.environment_properties["temperature"] = temperature
        self.environment_properties["humidity"] = humidity
        self.environment_properties["pressure"] = pressure
        
        # Update sound speed based on environmental conditions
        # Simplified formula: c = 331.3 + 0.606 * T (where T is temperature in Celsius)
        self.sound_speed = 331.3 + 0.606 * temperature
        
        # Initialize frequency-dependent absorption coefficients
        # These are simplified values for typical indoor environments
        self.environment_properties["absorption_coefficients"] = {
            125: 0.25,    # 125 Hz
            250: 0.45,    # 250 Hz
            500: 0.65,    # 500 Hz
            1000: 0.75,   # 1000 Hz
            2000: 0.85,   # 2000 Hz
            4000: 0.90,   # 4000 Hz
            8000: 0.95    # 8000 Hz
        }
        
        print(f"🔊 Acoustic environment initialized: {temperature}°C, {humidity}% humidity")
        
    def add_sound_source(self, source_id: str, position: Tuple[float, float, float],
                        frequency: float, amplitude: float, phase: float = 0.0,
                        velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0),
                        source_type: str = "point",
                        direction: Tuple[float, float, float] = (0.0, 0.0, 1.0)):
        """
        Add a sound source to the simulation
        
        Args:
            source_id: Unique identifier for the sound source
            position: 3D position (x, y, z)
            frequency: Sound frequency in Hz
            amplitude: Sound amplitude (0.0 to 1.0)
            phase: Initial phase in radians
            velocity: Source velocity (vx, vy, vz)
            source_type: Type of source ("point", "plane", "spherical")
            direction: Direction vector for directional sources
        """
        source = SoundSource(
            id=source_id,
            position=position,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            velocity=velocity,
            type=source_type,
            direction=direction
        )
        self.sound_sources[source_id] = source
        
        # Create initial sound waves from this source
        wave = SoundWave(
            source_id=source_id,
            frequency=frequency,
            amplitude=amplitude,
            phase=phase,
            position=position,
            direction=direction,
            speed=self.sound_speed,
            distance_traveled=0.0,
            timestamp=self.current_time
        )
        self.sound_waves.append(wave)
        
    def set_listener_position(self, position: Tuple[float, float, float],
                           orientation: Tuple[float, float, float] = (0.0, 0.0, 1.0),
                           velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        """
        Set the listener's position and orientation
        
        Args:
            position: Listener position (x, y, z)
            orientation: Listener facing direction
            velocity: Listener velocity (vx, vy, vz)
        """
        self.listener = SoundListener(position, orientation, velocity)
        
    def calculate_distance_attenuation(self, distance: float, reference_distance: float = 1.0) -> float:
        """
        Calculate distance-based attenuation using the inverse square law
        
        Args:
            distance: Distance from source to listener
            reference_distance: Reference distance where no attenuation occurs
            
        Returns:
            Attenuation factor (0.0 to 1.0)
        """
        if distance <= reference_distance:
            return 1.0
            
        # Inverse square law: I ∝ 1/r²
        attenuation = (reference_distance / distance) ** 2
        return max(0.0, min(1.0, attenuation))
    
    def calculate_air_absorption(self, frequency: float, distance: float) -> float:
        """
        Calculate frequency-dependent air absorption
        
        Args:
            frequency: Sound frequency in Hz
            distance: Distance sound travels in meters
            
        Returns:
            Absorption factor (0.0 to 1.0)
        """
        # Get closest frequency band for absorption coefficient
        freq_bands = sorted(self.environment_properties["absorption_coefficients"].keys())
        closest_freq = min(freq_bands, key=lambda x: abs(x - frequency))
        absorption_coeff = self.environment_properties["absorption_coefficients"][closest_freq]
        
        # Exponential decay due to absorption: A = e^(-αd)
        # Where α is the absorption coefficient and d is distance
        absorption_factor = math.exp(-absorption_coeff * distance / 1000)  # Normalize distance
        return max(0.0, min(1.0, absorption_factor))
    
    def calculate_directional_attenuation(self, source_direction: Tuple[float, float, float],
                                        listener_position: Tuple[float, float, float],
                                        source_position: Tuple[float, float, float]) -> float:
        """
        Calculate attenuation based on source directionality
        
        Args:
            source_direction: Source emission direction vector
            listener_position: Listener position
            source_position: Source position
            
        Returns:
            Directional attenuation factor (0.0 to 1.0)
        """
        # Calculate vector from source to listener
        dx = listener_position[0] - source_position[0]
        dy = listener_position[1] - source_position[1]
        dz = listener_position[2] - source_position[2]
        
        # Normalize vectors
        listener_distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if listener_distance == 0:
            return 1.0
            
        # Normalize direction to listener
        dir_to_listener = (dx/listener_distance, dy/listener_distance, dz/listener_distance)
        
        # Normalize source direction
        dir_length = math.sqrt(source_direction[0]**2 + source_direction[1]**2 + source_direction[2]**2)
        if dir_length == 0:
            return 1.0
            
        norm_source_dir = (source_direction[0]/dir_length, source_direction[1]/dir_length, source_direction[2]/dir_length)
        
        # Calculate dot product (cosine of angle between vectors)
        dot_product = (dir_to_listener[0] * norm_source_dir[0] + 
                      dir_to_listener[1] * norm_source_dir[1] + 
                      dir_to_listener[2] * norm_source_dir[2])
        
        # Convert to attenuation (1.0 for same direction, 0.0 for opposite)
        # Using cosine pattern for directional attenuation
        directional_attenuation = max(0.0, dot_product)
        return directional_attenuation
    
    def calculate_doppler_effect(self, source_velocity: Tuple[float, float, float],
                               listener_velocity: Tuple[float, float, float],
                               source_position: Tuple[float, float, float],
                               listener_position: Tuple[float, float, float]) -> float:
        """
        Calculate Doppler effect frequency shift
        
        Args:
            source_velocity: Source velocity vector (vx, vy, vz)
            listener_velocity: Listener velocity vector (vx, vy, vz)
            source_position: Source position
            listener_position: Listener position
            
        Returns:
            Frequency scaling factor
        """
        # Calculate vector from source to listener
        dx = listener_position[0] - source_position[0]
        dy = listener_position[1] - source_position[1]
        dz = listener_position[2] - source_position[2]
        
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        if distance == 0:
            return 1.0
            
        # Normalize direction vector
        dir_x, dir_y, dir_z = dx/distance, dy/distance, dz/distance
        
        # Calculate radial velocities (velocity components along the line of sight)
        source_radial_velocity = (source_velocity[0] * dir_x + 
                                source_velocity[1] * dir_y + 
                                source_velocity[2] * dir_z)
        
        listener_radial_velocity = (listener_velocity[0] * dir_x + 
                                  listener_velocity[1] * dir_y + 
                                  listener_velocity[2] * dir_z)
        
        # Doppler effect formula: f' = f * (c + v_listener) / (c + v_source)
        # Where c is speed of sound, v is radial velocity
        observed_frequency_factor = (self.sound_speed + listener_radial_velocity) / (self.sound_speed + source_radial_velocity)
        
        # Clamp to reasonable values to prevent extreme shifts
        return max(0.5, min(2.0, observed_frequency_factor))
    
    def simulate_sound_propagation(self, time_delta: float):
        """
        Simulate sound wave propagation over a time step
        
        Args:
            time_delta: Time step in seconds
        """
        self.current_time += time_delta
        
        # Update sound wave positions
        waves_to_remove = []
        for i, wave in enumerate(self.sound_waves):
            # Calculate distance traveled in this time step
            distance_step = wave.speed * time_delta
            wave.distance_traveled += distance_step
            
            # Update wave position based on direction
            dx = wave.direction[0] * distance_step
            dy = wave.direction[1] * distance_step
            dz = wave.direction[2] * distance_step
            
            wave.position = (wave.position[0] + dx, wave.position[1] + dy, wave.position[2] + dz)
            
            # Remove waves that have traveled too far (simple cleanup)
            if wave.distance_traveled > 1000.0:  # 1000 meters limit
                waves_to_remove.append(i)
        
        # Remove old waves
        for i in reversed(waves_to_remove):
            if i < len(self.sound_waves):
                del self.sound_waves[i]
        
        # Update moving sound sources
        for source in self.sound_sources.values():
            if source.velocity != (0.0, 0.0, 0.0):
                dx = source.velocity[0] * time_delta
                dy = source.velocity[1] * time_delta
                dz = source.velocity[2] * time_delta
                source.position = (source.position[0] + dx, source.position[1] + dy, source.position[2] + dz)
    
    def calculate_sound_at_listener(self) -> Dict[str, Any]:
        """
        Calculate the combined sound at the listener's position from all sources
        
        Returns:
            Dictionary containing sound parameters at listener position
        """
        if not self.sound_sources:
            return {"amplitude": 0.0, "frequency": 0.0, "phase": 0.0, "components": []}
        
        listener_pos = self.listener.position
        total_amplitude = 0.0
        frequency_weighted_sum = 0.0
        total_weight = 0.0
        sound_components = []
        
        for source in self.sound_sources.values():
            # Calculate distance to listener
            dx = listener_pos[0] - source.position[0]
            dy = listener_pos[1] - source.position[1]
            dz = listener_pos[2] - source.position[2]
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # Calculate various attenuation factors
            distance_attenuation = self.calculate_distance_attenuation(distance)
            air_absorption = self.calculate_air_absorption(source.frequency, distance)
            directional_attenuation = self.calculate_directional_attenuation(
                source.direction, listener_pos, source.position
            )
            doppler_factor = self.calculate_doppler_effect(
                source.velocity, self.listener.velocity, source.position, listener_pos
            )
            
            # Combined attenuation
            total_attenuation = distance_attenuation * air_absorption * directional_attenuation
            
            # Apply Doppler effect to frequency
            observed_frequency = source.frequency * doppler_factor
            
            # Calculate final amplitude at listener
            final_amplitude = source.amplitude * total_attenuation
            
            # Add to totals for mixing
            total_amplitude += final_amplitude
            frequency_weighted_sum += observed_frequency * final_amplitude
            total_weight += final_amplitude
            
            # Store component information
            sound_components.append({
                "source_id": source.id,
                "distance": distance,
                "amplitude": final_amplitude,
                "frequency": observed_frequency,
                "attenuation": total_attenuation,
                "doppler_factor": doppler_factor
            })
        
        # Calculate mixed parameters
        mixed_frequency = frequency_weighted_sum / total_weight if total_weight > 0 else 0.0
        mixed_amplitude = min(1.0, total_amplitude)  # Clamp to prevent clipping
        
        return {
            "amplitude": mixed_amplitude,
            "frequency": mixed_frequency,
            "components": sound_components
        }
    
    def generate_3d_audio_frame(self) -> List[List[float]]:
        """
        Generate a stereo audio frame based on current sound field
        
        Returns:
            Stereo audio frame as [left_channel, right_channel]
        """
        # Calculate sound at listener position
        sound_params = self.calculate_sound_at_listener()
        amplitude = sound_params["amplitude"]
        
        if amplitude <= 0:
            # Return silence
            return [[0.0], [0.0]]
        
        # For simplicity, generate a single sample per frame
        # In a real implementation, this would generate a full buffer
        sample = amplitude * math.sin(2 * math.pi * sound_params["frequency"] * self.current_time)
        
        # Apply basic stereo positioning based on sound sources
        left_sum = 0.0
        right_sum = 0.0
        total_sources = len(sound_params["components"])
        
        if total_sources > 0:
            for component in sound_params["components"]:
                source = self.sound_sources.get(component["source_id"])
                if source:
                    # Simple left/right positioning based on X coordinate
                    x_pos = source.position[0]
                    # Normalize to -1 to 1 range (assuming space width of 20 units)
                    normalized_x = max(-1.0, min(1.0, x_pos / 10.0))
                    
                    # Convert to left/right balance (0 = center, -1 = left, 1 = right)
                    left_balance = max(0.0, 1.0 - normalized_x)  # 1.0 when x=-1, 0.0 when x=1
                    right_balance = max(0.0, 1.0 + normalized_x)  # 0.0 when x=-1, 1.0 when x=1
                    
                    left_sum += sample * left_balance * component["amplitude"]
                    right_sum += sample * right_balance * component["amplitude"]
        
        # Normalize if we have multiple sources
        if total_sources > 1:
            left_sum /= total_sources
            right_sum /= total_sources
            
        return [[left_sum], [right_sum]]

# Global instance
acoustic_engine = AcousticPhysicsEngine()

def initialize_acoustic_physics(sound_speed: float = 343.0, air_density: float = 1.225):
    """Initialize the global acoustic physics engine"""
    global acoustic_engine
    acoustic_engine = AcousticPhysicsEngine(sound_speed, air_density)
    acoustic_engine.initialize_environment_properties()
    return acoustic_engine

def add_physics_sound_source(source_id: str, position: Tuple[float, float, float],
                           frequency: float, amplitude: float, phase: float = 0.0):
    """Add a sound source to the physics simulation"""
    acoustic_engine.add_sound_source(source_id, position, frequency, amplitude, phase)

def update_acoustic_simulation(time_delta: float = 1.0/44100.0):
    """Update the acoustic physics simulation"""
    acoustic_engine.simulate_sound_propagation(time_delta)

def get_sound_at_listener():
    """Get the calculated sound at the listener position"""
    return acoustic_engine.calculate_sound_at_listener()

def generate_physics_based_audio():
    """Generate audio based on acoustic physics simulation"""
    return acoustic_engine.generate_3d_audio_frame()