"""
Acoustic Propagation Optimizer
System for maximizing sound wave travel distance through hardware and environmental optimization
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass

@dataclass
class AcousticEnvironment:
    """Represents acoustic properties of an environment"""
    temperature: float  # Celsius
    humidity: float     # Percent
    pressure: float     # Pascals
    wind_speed: Tuple[float, float, float]  # (vx, vy, vz) in m/s
    obstacles: List[Dict[str, Any]]  # List of obstacles with position and absorption
    reflective_surfaces: List[Dict[str, Any]]  # List of reflective surfaces

@dataclass
class SoundSourceConfiguration:
    """Represents a sound source configuration for optimization"""
    frequency: float           # Hz
    power: float              # Watts
    directivity_index: float  # dB
    height: float             # meters above ground
    orientation: Tuple[float, float, float]  # (azimuth, elevation, roll) in degrees

class AcousticPropagationOptimizer:
    """Optimizes sound wave propagation for maximum distance"""
    
    def __init__(self):
        """Initialize the acoustic propagation optimizer"""
        self.environment = AcousticEnvironment(
            temperature=20.0,
            humidity=50.0,
            pressure=101325.0,
            wind_speed=(0.0, 0.0, 0.0),
            obstacles=[],
            reflective_surfaces=[]
        )
        self.sound_sources = {}
        self.propagation_models = {}
        self.optimization_history = []
        
    def set_environmental_conditions(self, temperature = None, 
                                   humidity = None,
                                   pressure = None,
                                   wind_speed = None):
        """
        Set environmental conditions affecting sound propagation
        
        Args:
            temperature: Air temperature in Celsius
            humidity: Relative humidity in percent
            pressure: Atmospheric pressure in Pascals
            wind_speed: Wind speed vector (vx, vy, vz) in m/s
        """
        if temperature is not None:
            self.environment.temperature = temperature
        if humidity is not None:
            self.environment.humidity = humidity
        if pressure is not None:
            self.environment.pressure = pressure
        if wind_speed is not None:
            self.environment.wind_speed = wind_speed
            
        print(f"🌍 Environmental conditions updated: {temperature}°C, {humidity}% humidity")
        
    def add_sound_source(self, source_id: str, configuration: SoundSourceConfiguration):
        """
        Add a sound source for propagation optimization
        
        Args:
            source_id: Unique identifier for the sound source
            configuration: SoundSourceConfiguration object
        """
        self.sound_sources[source_id] = configuration
        print(f"🔊 Sound source '{source_id}' added for propagation optimization")
        
    def calculate_sound_speed(self) -> float:
        """
        Calculate speed of sound based on environmental conditions
        
        Returns:
            Speed of sound in m/s
        """
        # Simplified formula: c = 331.3 + 0.606 * T (where T is temperature in Celsius)
        speed_of_sound = 331.3 + 0.606 * self.environment.temperature
        
        # Adjust for humidity (simplified)
        humidity_factor = 1.0 + (self.environment.humidity / 100.0) * 0.001
        speed_of_sound *= humidity_factor
        
        # Adjust for wind (component in direction of propagation)
        # For simplicity, we'll use average wind effect
        wind_effect = sum(abs(v) for v in self.environment.wind_speed) / 3
        speed_of_sound += wind_effect * 0.1  # Small adjustment for wind
        
        return speed_of_sound
    
    def calculate_attenuation_coefficient(self, frequency: float) -> float:
        """
        Calculate atmospheric attenuation coefficient for a given frequency
        
        Args:
            frequency: Sound frequency in Hz
            
        Returns:
            Attenuation coefficient in dB/m
        """
        # Simplified atmospheric attenuation model
        # Based on ISO 9613-1 standard (simplified)
        
        # Temperature and humidity effects
        temp_factor = 1.0 + (self.environment.temperature - 20.0) / 100.0
        humidity_factor = 1.0 + (self.environment.humidity - 50.0) / 200.0
        
        # Frequency-dependent attenuation (simplified)
        if frequency < 500:
            base_attenuation = 0.0001  # Very low for bass
        elif frequency < 2000:
            base_attenuation = 0.0005  # Low for midrange
        elif frequency < 8000:
            base_attenuation = 0.002   # Moderate for upper midrange
        else:
            base_attenuation = 0.005   # High for treble
            
        # Apply environmental factors
        attenuation = base_attenuation * temp_factor * humidity_factor
        
        return attenuation
    
    def calculate_geometric_spreading_loss(self, distance: float, spreading_factor: float = 2.0) -> float:
        """
        Calculate geometric spreading loss
        
        Args:
            distance: Distance from source in meters
            spreading_factor: Spreading factor (2.0 for spherical, 1.0 for cylindrical)
            
        Returns:
            Spreading loss in dB
        """
        if distance <= 0:
            return 0.0
            
        # Geometric spreading loss: L = 10 * n * log10(d/d0)
        # where n is spreading factor, d is distance, d0 is reference distance
        reference_distance = 1.0  # 1 meter reference
        spreading_loss = 10 * spreading_factor * math.log10(distance / reference_distance)
        
        return spreading_loss
    
    def calculate_ground_effect(self, frequency: float, height: float, distance: float) -> float:
        """
        Calculate ground effect on sound propagation
        
        Args:
            frequency: Sound frequency in Hz
            height: Source height above ground in meters
            distance: Horizontal distance from source in meters
            
        Returns:
            Ground effect in dB (positive = enhancement, negative = attenuation)
        """
        if height <= 0 or distance <= 0:
            return 0.0
            
        # Calculate angle of propagation to ground
        angle = math.atan2(height, distance)
        
        # Ground effect is more significant at low angles (long distances)
        angle_factor = max(0.0, 1.0 - angle / (math.pi / 2))
        
        # Frequency-dependent ground effect
        if frequency < 200:
            # Bass frequencies are enhanced by ground reflection
            ground_effect = 3.0 * angle_factor
        elif frequency < 1000:
            # Mid frequencies have moderate ground effect
            ground_effect = 1.0 * angle_factor
        else:
            # High frequencies are attenuated by ground absorption
            ground_effect = -2.0 * angle_factor
            
        return ground_effect
    
    def calculate_wind_effect(self, frequency: float, distance: float) -> float:
        """
        Calculate wind effect on sound propagation
        
        Args:
            frequency: Sound frequency in Hz
            distance: Distance from source in meters
            
        Returns:
            Wind effect in dB
        """
        # Calculate effective wind speed in direction of propagation
        wind_speed = math.sqrt(sum(v**2 for v in self.environment.wind_speed))
        
        # Wind effect is more significant for:
        # 1. Higher wind speeds
        # 2. Longer distances
        # 3. Higher frequencies (more directional)
        
        wind_factor = wind_speed * distance / 1000.0  # Normalize by distance
        frequency_factor = min(1.0, frequency / 5000.0)  # Normalize by frequency
        
        wind_effect = wind_factor * frequency_factor * 2.0  # Up to 2dB effect
        
        return wind_effect
    
    def predict_propagation_distance(self, source_id: str, target_spl: float = 40.0) -> Dict[str, Any]:
        """
        Predict maximum propagation distance for a sound source
        
        Args:
            source_id: ID of the sound source
            target_spl: Target sound pressure level in dB (default: 40dB = quiet library)
            
        Returns:
            Dictionary with propagation prediction results
        """
        if source_id not in self.sound_sources:
            return {"error": "Sound source not found"}
            
        source = self.sound_sources[source_id]
        
        # Calculate initial sound power level
        # SPL at 1m = 10 * log10(Power / (4 * π * 1² * 10^-12))
        # Assuming reference power for calculation
        reference_power = 1e-12  # 1 pW reference
        initial_spl = 10 * math.log10(source.power / reference_power) if source.power > 0 else 100.0
        
        # Calculate speed of sound
        sound_speed = self.calculate_sound_speed()
        
        # Calculate attenuation coefficient
        attenuation_coeff = self.calculate_attenuation_coefficient(source.frequency)
        
        # Binary search for maximum distance where SPL >= target_spl
        min_distance = 1.0
        max_distance = 100000.0  # 100 km maximum search
        tolerance = 0.1  # 10cm tolerance
        
        max_distance_found = 0.0
        iterations = 0
        max_iterations = 50
        
        while (max_distance - min_distance) > tolerance and iterations < max_iterations:
            test_distance = (min_distance + max_distance) / 2
            
            # Calculate total losses at test distance
            spreading_loss = self.calculate_geometric_spreading_loss(test_distance)
            atmospheric_loss = attenuation_coeff * test_distance * 1000  # Convert to dB
            ground_effect = self.calculate_ground_effect(source.frequency, source.height, test_distance)
            wind_effect = self.calculate_wind_effect(source.frequency, test_distance)
            directivity_gain = source.directivity_index
            
            # Total SPL at test distance
            total_loss = spreading_loss + atmospheric_loss - ground_effect - wind_effect
            spl_at_distance = initial_spl + directivity_gain - total_loss
            
            if spl_at_distance >= target_spl:
                max_distance_found = test_distance
                min_distance = test_distance
            else:
                max_distance = test_distance
                
            iterations += 1
            
        # Calculate additional metrics
        spreading_loss_final = self.calculate_geometric_spreading_loss(max_distance_found)
        atmospheric_loss_final = attenuation_coeff * max_distance_found * 1000
        ground_effect_final = self.calculate_ground_effect(source.frequency, source.height, max_distance_found)
        wind_effect_final = self.calculate_wind_effect(source.frequency, max_distance_found)
        
        prediction = {
            "source_id": source_id,
            "frequency": source.frequency,
            "initial_spl": initial_spl,
            "maximum_distance_km": max_distance_found / 1000.0,
            "target_spl": target_spl,
            "sound_speed_mps": sound_speed,
            "total_losses_db": spreading_loss_final + atmospheric_loss_final - ground_effect_final - wind_effect_final,
            "spreading_loss_db": spreading_loss_final,
            "atmospheric_loss_db": atmospheric_loss_final,
            "ground_effect_db": ground_effect_final,
            "wind_effect_db": wind_effect_final,
            "directivity_gain_db": source.directivity_index,
            "propagation_time_seconds": max_distance_found / sound_speed if sound_speed > 0 else 0
        }
        
        # Store in history
        self.optimization_history.append(prediction)
        
        return prediction
    
    def optimize_for_maximum_distance(self, source_id: str, 
                                    target_distance = None,
                                    target_spl: float = 40.0) -> Dict[str, Any]:
        """
        Optimize sound source configuration for maximum propagation distance
        
        Args:
            source_id: ID of the sound source
            target_distance: Target distance in meters (None = maximize distance)
            target_spl: Target sound pressure level at distance
            
        Returns:
            Dictionary with optimization results
        """
        if source_id not in self.sound_sources:
            return {"error": "Sound source not found"}
            
        source = self.sound_sources[source_id]
        
        # Current configuration prediction
        current_prediction = self.predict_propagation_distance(source_id, target_spl)
        
        # Optimization parameters
        optimization_results = {
            "source_id": source_id,
            "current_configuration": {
                "frequency": source.frequency,
                "power": source.power,
                "height": source.height,
                "directivity": source.directivity_index
            },
            "current_performance": current_prediction,
            "optimization_suggestions": []
        }
        
        # Suggest optimizations based on current performance
        current_distance = current_prediction["maximum_distance_km"] * 1000  # Convert to meters
        
        # Power optimization
        if source.power < 1000:  # If under 1kW, suggest power increase
            power_multiplier = min(10.0, 1000 / max(source.power, 1.0))
            optimization_results["optimization_suggestions"].append({
                "type": "power",
                "suggestion": f"Increase power by {power_multiplier:.1f}x",
                "expected_improvement_km": current_distance * (math.sqrt(power_multiplier) - 1) / 1000
            })
            
        # Frequency optimization (lower frequencies travel farther)
        if source.frequency > 100:
            optimization_results["optimization_suggestions"].append({
                "type": "frequency",
                "suggestion": "Reduce frequency to sub-bass range (20-100 Hz)",
                "expected_improvement_km": current_distance * 0.5 / 1000  # 50% improvement estimate
            })
            
        # Height optimization (higher = better ground effect)
        if source.height < 50:
            optimization_results["optimization_suggestions"].append({
                "type": "height",
                "suggestion": "Increase height to 50+ meters",
                "expected_improvement_km": current_distance * 0.3 / 1000  # 30% improvement estimate
            })
            
        # Directivity optimization (higher directivity index)
        if source.directivity_index < 10:
            optimization_results["optimization_suggestions"].append({
                "type": "directivity",
                "suggestion": "Use highly directional array (10+ dBi)",
                "expected_improvement_km": current_distance * 0.4 / 1000  # 40% improvement estimate
            })
            
        return optimization_results
    
    def simulate_propagation_path(self, source_id: str, 
                                distances: List[float]) -> List[Dict[str, float]]:
        """
        Simulate sound propagation along a path
        
        Args:
            source_id: ID of the sound source
            distances: List of distances to simulate in meters
            
        Returns:
            List of dictionaries with SPL at each distance
        """
        if source_id not in self.sound_sources:
            return []
            
        source = self.sound_sources[source_id]
        
        # Calculate initial parameters
        reference_power = 1e-12
        initial_spl = 10 * math.log10(source.power / reference_power) if source.power > 0 else 100.0
        attenuation_coeff = self.calculate_attenuation_coefficient(source.frequency)
        sound_speed = self.calculate_sound_speed()
        
        path_simulation = []
        
        for distance in distances:
            if distance <= 0:
                continue
                
            # Calculate all losses
            spreading_loss = self.calculate_geometric_spreading_loss(distance)
            atmospheric_loss = attenuation_coeff * distance * 1000
            ground_effect = self.calculate_ground_effect(source.frequency, source.height, distance)
            wind_effect = self.calculate_wind_effect(source.frequency, distance)
            directivity_gain = source.directivity_index
            
            # Calculate final SPL
            total_loss = spreading_loss + atmospheric_loss - ground_effect - wind_effect
            final_spl = initial_spl + directivity_gain - total_loss
            
            path_simulation.append({
                "distance_m": distance,
                "distance_km": distance / 1000.0,
                "spl_db": final_spl,
                "propagation_time_s": distance / sound_speed if sound_speed > 0 else 0,
                "total_loss_db": total_loss
            })
            
        return path_simulation
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """
        Get summary of all optimization activities
        
        Returns:
            Dictionary with optimization summary
        """
        if not self.optimization_history:
            return {"status": "no_optimizations_performed"}
            
        # Calculate average performance metrics
        total_distance = sum(pred["maximum_distance_km"] for pred in self.optimization_history)
        avg_distance = total_distance / len(self.optimization_history)
        
        total_spl = sum(pred["initial_spl"] for pred in self.optimization_history)
        avg_spl = total_spl / len(self.optimization_history)
        
        return {
            "total_optimizations": len(self.optimization_history),
            "average_maximum_distance_km": avg_distance,
            "average_initial_spl": avg_spl,
            "sources_analyzed": list(self.sound_sources.keys())
        }

class AdvancedPropagationModel:
    """Advanced acoustic propagation modeling"""
    
    def __init__(self, optimizer: AcousticPropagationOptimizer):
        """Initialize advanced propagation model"""
        self.optimizer = optimizer
        
    def calculate_atmospheric_absorption(self, frequency: float, distance: float) -> float:
        """
        Calculate detailed atmospheric absorption
        
        Args:
            frequency: Frequency in Hz
            distance: Distance in meters
            
        Returns:
            Absorption loss in dB
        """
        # More detailed atmospheric absorption model
        # Based on relaxation frequencies of oxygen and nitrogen
        
        # Environmental factors
        temp_k = self.optimizer.environment.temperature + 273.15  # Kelvin
        pressure_atm = self.optimizer.environment.pressure / 101325.0  # Relative to standard
        
        # Oxygen relaxation frequency
        fr_o = 24.0 + 4.04e4 * (self.optimizer.environment.humidity / 100.0) * (273.15 / temp_k)
        
        # Nitrogen relaxation frequency
        fr_n = (temp_k / 293.15) ** (-0.5) * (
            9.0 + 280.0 * (self.optimizer.environment.humidity / 100.0) * math.exp(-4.17 * ((temp_k / 293.15) ** (-1/3) - 1))
        )
        
        # Absorption coefficient calculation
        alpha_o = 0.0127 * (fr_o / (frequency ** 2 + fr_o ** 2)) * (293.15 / temp_k) ** (5/2)
        alpha_n = 0.1068 * (fr_n / (frequency ** 2 + fr_n ** 2)) * (293.15 / temp_k) ** (5/2)
        
        # Total absorption coefficient
        alpha_total = pressure_atm * (alpha_o + alpha_n) * (frequency ** 2) / 1000.0
        
        # Convert to dB loss over distance
        absorption_loss = alpha_total * distance
        
        return absorption_loss
    
    def model_turbulence_effects(self, frequency: float, distance: float) -> float:
        """
        Model effects of atmospheric turbulence
        
        Args:
            frequency: Frequency in Hz
            distance: Distance in meters
            
        Returns:
            Turbulence effect in dB
        """
        # Simplified turbulence model
        # Turbulence causes scattering and fluctuations
        
        # Turbulence strength based on wind speed variations
        wind_magnitude = math.sqrt(sum(v**2 for v in self.optimizer.environment.wind_speed))
        turbulence_parameter = min(1.0, wind_magnitude / 20.0)  # Normalize to 20 m/s
        
        # Frequency-dependent turbulence effect
        # Higher frequencies are more affected by turbulence
        frequency_factor = min(1.0, frequency / 10000.0)
        
        # Distance-dependent effect
        distance_factor = min(1.0, distance / 10000.0)  # Normalize to 10km
        
        turbulence_loss = turbulence_parameter * frequency_factor * distance_factor * 3.0  # Up to 3dB
        
        return turbulence_loss

# Global instances
propagation_optimizer = AcousticPropagationOptimizer()
advanced_propagation_model = None

def initialize_propagation_optimization():
    """Initialize the global acoustic propagation optimizer"""
    global propagation_optimizer, advanced_propagation_model
    propagation_optimizer = AcousticPropagationOptimizer()
    advanced_propagation_model = AdvancedPropagationModel(propagation_optimizer)
    return propagation_optimizer

def set_acoustic_environment(temperature = None, 
                           humidity = None,
                           pressure = None,
                           wind_speed = None):
    """Set environmental conditions for acoustic propagation"""
    propagation_optimizer.set_environmental_conditions(
        temperature, humidity, pressure, wind_speed
    )

def add_sound_source_for_optimization(source_id: str, configuration: SoundSourceConfiguration):
    """Add a sound source for propagation optimization"""
    propagation_optimizer.add_sound_source(source_id, configuration)

def predict_maximum_propagation_distance(source_id: str, target_spl: float = 40.0):
    """Predict maximum propagation distance for a sound source"""
    return propagation_optimizer.predict_propagation_distance(source_id, target_spl)

def optimize_sound_source_for_distance(source_id: str, 
                                    target_distance = None,
                                    target_spl: float = 40.0):
    """Optimize sound source configuration for maximum propagation distance"""
    return propagation_optimizer.optimize_for_maximum_distance(source_id, target_distance, target_spl)

def simulate_propagation_path(source_id: str, distances: List[float]):
    """Simulate sound propagation along a path"""
    return propagation_optimizer.simulate_propagation_path(source_id, distances)

def get_propagation_optimization_summary():
    """Get summary of propagation optimization activities"""
    return propagation_optimizer.get_optimization_summary()