"""
Adaptive Sound Layer System for Automatic Sound Adjustment
Automatically adapts sound layers based on acoustic physics and environmental conditions
"""

import math
from typing import List, Tuple, Dict, Any
from .acoustic_physics_engine import AcousticPhysicsEngine, SoundSource

class AdaptiveSoundLayerSystem:
    """Automatically adjusts sound layers based on acoustic physics and environmental conditions"""
    
    def __init__(self, acoustic_engine: AcousticPhysicsEngine):
        """Initialize the adaptive sound layer system"""
        self.acoustic_engine = acoustic_engine
        self.sound_layers = {}
        self.adaptation_rules = {}
        self.layer_priorities = {}
        self.adaptation_history = []
        
    def initialize_sound_layers(self):
        """Initialize the adaptive sound layer system with default layers"""
        self.sound_layers = {
            "quantum_core": {
                "priority": 100,
                "adaptive": True,
                "base_amplitude": 1.0,
                "base_frequency": 440.0,
                "adaptation_sensitivity": 1.0,
                "environmental_response": "enhance"
            },
            "environmental_background": {
                "priority": 30,
                "adaptive": True,
                "base_amplitude": 0.3,
                "base_frequency": 100.0,
                "adaptation_sensitivity": 0.5,
                "environmental_response": "blend"
            },
            "spatial_effects": {
                "priority": 70,
                "adaptive": True,
                "base_amplitude": 0.6,
                "base_frequency": 880.0,
                "adaptation_sensitivity": 0.8,
                "environmental_response": "modulate"
            },
            "quantum_detail": {
                "priority": 80,
                "adaptive": True,
                "base_amplitude": 0.8,
                "base_frequency": 2200.0,
                "adaptation_sensitivity": 0.9,
                "environmental_response": "enhance"
            }
        }
        
        # Set layer priorities
        for layer_name, layer_info in self.sound_layers.items():
            self.layer_priorities[layer_name] = layer_info["priority"]
            
        print("🎛️ Adaptive sound layers initialized for automatic adjustment")
        
    def add_adaptation_rule(self, rule_name: str, condition_function, adaptation_function):
        """
        Add a rule for adaptive sound layer adjustment
        
        Args:
            rule_name: Name of the adaptation rule
            condition_function: Function that determines when rule applies
            adaptation_function: Function that applies the adaptation
        """
        self.adaptation_rules[rule_name] = {
            "condition": condition_function,
            "adaptation": adaptation_function
        }
        
    def analyze_acoustic_environment(self) -> Dict[str, Any]:
        """
        Analyze the current acoustic environment for adaptation decisions
        
        Returns:
            Dictionary of environmental analysis parameters
        """
        # Get sound information at listener position
        sound_info = self.acoustic_engine.calculate_sound_at_listener()
        
        # Calculate environmental metrics
        total_amplitude = sound_info["amplitude"]
        component_count = len(sound_info["components"])
        
        # Analyze component distribution
        average_distance = 0.0
        if sound_info["components"]:
            total_distance = sum(comp["distance"] for comp in sound_info["components"])
            average_distance = total_distance / len(sound_info["components"])
            
        # Analyze frequency content
        average_frequency = sound_info["frequency"] if component_count > 0 else 0.0
        
        # Determine environmental complexity
        complexity = min(1.0, component_count / 10.0)  # Normalize to 0-1
        
        # Determine spatial distribution
        spatial_spread = 0.0
        if len(sound_info["components"]) > 1:
            positions = []
            for comp in sound_info["components"]:
                source = self.acoustic_engine.sound_sources.get(comp["source_id"])
                if source:
                    positions.append(source.position)
                    
            if positions:
                # Calculate spread based on position variance
                center_x = sum(pos[0] for pos in positions) / len(positions)
                center_y = sum(pos[1] for pos in positions) / len(positions)
                center_z = sum(pos[2] for pos in positions) / len(positions)
                
                distances_from_center = [
                    math.sqrt((pos[0]-center_x)**2 + (pos[1]-center_y)**2 + (pos[2]-center_z)**2)
                    for pos in positions
                ]
                
                avg_distance_from_center = sum(distances_from_center) / len(distances_from_center)
                max_distance = max(distances_from_center) if distances_from_center else 1.0
                spatial_spread = avg_distance_from_center / max_distance if max_distance > 0 else 0.0
        
        return {
            "total_amplitude": total_amplitude,
            "component_count": component_count,
            "average_distance": average_distance,
            "average_frequency": average_frequency,
            "complexity": complexity,
            "spatial_spread": spatial_spread,
            "needs_adaptation": total_amplitude > 0.8 or component_count > 5
        }
    
    def adapt_sound_layers(self) -> Dict[str, Dict[str, float]]:
        """
        Automatically adapt sound layers based on acoustic environment analysis
        
        Returns:
            Dictionary of adapted layer parameters
        """
        # Analyze current environment
        env_analysis = self.analyze_acoustic_environment()
        
        # Store adaptation history
        self.adaptation_history.append({
            "timestamp": self.acoustic_engine.current_time,
            "analysis": env_analysis
        })
        
        # Keep only recent history (last 100 adaptations)
        if len(self.adaptation_history) > 100:
            self.adaptation_history = self.adaptation_history[-100:]
        
        # Calculate adaptation factors for each layer
        adapted_parameters = {}
        
        for layer_name, layer_info in self.sound_layers.items():
            if not layer_info["adaptive"]:
                # Non-adaptive layers keep base parameters
                adapted_parameters[layer_name] = {
                    "amplitude": layer_info["base_amplitude"],
                    "frequency": layer_info["base_frequency"]
                }
                continue
                
            # Calculate adaptation based on environmental analysis
            sensitivity = layer_info["adaptation_sensitivity"]
            
            # Amplitude adaptation based on total sound level
            amplitude_factor = 1.0
            if env_analysis["total_amplitude"] > 0.7:
                # Reduce amplitude in loud environments
                amplitude_factor = max(0.3, 1.0 - (env_analysis["total_amplitude"] - 0.7) * sensitivity)
            elif env_analysis["total_amplitude"] < 0.3:
                # Increase amplitude in quiet environments
                amplitude_factor = min(1.5, 1.0 + (0.3 - env_analysis["total_amplitude"]) * sensitivity * 0.5)
                
            # Frequency adaptation based on complexity
            frequency_factor = 1.0
            if env_analysis["complexity"] > 0.5:
                # Shift frequencies to reduce masking in complex environments
                if layer_info["base_frequency"] < 1000:
                    frequency_factor = 1.1  # Shift low frequencies up
                else:
                    frequency_factor = 0.9   # Shift high frequencies down
                    
            # Spatial adaptation based on spread
            spatial_factor = 1.0
            if env_analysis["spatial_spread"] > 0.7:
                # Enhance spatial effects in distributed sound fields
                if layer_name == "spatial_effects":
                    spatial_factor = 1.2
            elif env_analysis["spatial_spread"] < 0.3:
                # Reduce spatial effects in concentrated sound fields
                if layer_name == "spatial_effects":
                    spatial_factor = 0.8
                    
            # Apply environmental response strategy
            response = layer_info["environmental_response"]
            if response == "blend":
                # Blend with environment
                amplitude_factor *= (1.0 - env_analysis["complexity"] * 0.3)
            elif response == "enhance":
                # Enhance in response to environment
                amplitude_factor *= (1.0 + env_analysis["complexity"] * 0.2)
            elif response == "modulate":
                # Modulate based on environmental changes
                amplitude_factor *= (1.0 + math.sin(self.acoustic_engine.current_time * 2) * 0.1)
                
            # Calculate final adapted parameters
            adapted_amplitude = max(0.0, min(1.0, 
                layer_info["base_amplitude"] * amplitude_factor))
            adapted_frequency = max(20.0, min(20000.0,
                layer_info["base_frequency"] * frequency_factor))
                
            adapted_parameters[layer_name] = {
                "amplitude": adapted_amplitude,
                "frequency": adapted_frequency,
                "spatial_factor": spatial_factor
            }
            
        # Apply priority-based mixing
        adapted_parameters = self._apply_priority_mixing(adapted_parameters)
        
        return adapted_parameters
    
    def _apply_priority_mixing(self, layer_parameters: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
        """
        Apply priority-based mixing to ensure important layers are heard
        
        Args:
            layer_parameters: Dictionary of layer parameters
            
        Returns:
            Adjusted layer parameters with priority mixing applied
        """
        # Sort layers by priority (highest first)
        sorted_layers = sorted(
            self.layer_priorities.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Apply priority-based adjustments
        total_priority = sum(priority for _, priority in sorted_layers)
        if total_priority == 0:
            return layer_parameters
            
        for layer_name, priority in sorted_layers:
            if layer_name in layer_parameters:
                # Normalize priority influence
                priority_influence = priority / total_priority
                
                # Adjust amplitude based on priority and existing parameters
                current_amp = layer_parameters[layer_name]["amplitude"]
                priority_adjusted_amp = current_amp * (0.7 + 0.3 * priority_influence)
                
                layer_parameters[layer_name]["amplitude"] = max(0.0, min(1.0, priority_adjusted_amp))
                
        return layer_parameters
    
    def apply_layer_adaptations(self, layer_parameters: Dict[str, Dict[str, float]]):
        """
        Apply the calculated adaptations to the acoustic engine
        
        Args:
            layer_parameters: Dictionary of adapted layer parameters
        """
        # Update sound sources in the acoustic engine based on adapted parameters
        for layer_name, params in layer_parameters.items():
            # In a real implementation, this would update actual sound sources
            # For now, we'll just log the adaptations
            pass
            
    def get_adaptation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current adaptation state
        
        Returns:
            Dictionary summarizing the adaptation state
        """
        if not self.adaptation_history:
            return {"status": "no_adaptations_yet"}
            
        latest_analysis = self.adaptation_history[-1]["analysis"]
        
        return {
            "status": "active",
            "total_adaptations": len(self.adaptation_history),
            "current_amplitude": latest_analysis["total_amplitude"],
            "component_count": latest_analysis["component_count"],
            "environmental_complexity": latest_analysis["complexity"],
            "spatial_distribution": latest_analysis["spatial_spread"],
            "adaptation_needed": latest_analysis["needs_adaptation"]
        }

class SoundLayerAdaptationRules:
    """Predefined rules for sound layer adaptation"""
    
    @staticmethod
    def loud_environment_condition(analyzer):
        """Condition: Environment is too loud"""
        analysis = analyzer.analyze_acoustic_environment()
        return analysis["total_amplitude"] > 0.8
        
    @staticmethod
    def loud_environment_adaptation(system, layer_params):
        """Adaptation: Reduce overall amplitude in loud environments"""
        for layer_name in layer_params:
            layer_params[layer_name]["amplitude"] *= 0.7
        return layer_params
        
    @staticmethod
    def complex_environment_condition(analyzer):
        """Condition: Environment is acoustically complex"""
        analysis = analyzer.analyze_acoustic_environment()
        return analysis["component_count"] > 5
        
    @staticmethod
    def complex_environment_adaptation(system, layer_params):
        """Adaptation: Enhance spatial separation in complex environments"""
        for layer_name in layer_params:
            if layer_name == "spatial_effects":
                layer_params[layer_name]["amplitude"] *= 1.3
            else:
                layer_params[layer_name]["amplitude"] *= 0.9
        return layer_params

# Global instance
adaptive_layer_system = None

def initialize_adaptive_sound_layers(acoustic_engine: AcousticPhysicsEngine):
    """Initialize the global adaptive sound layer system"""
    global adaptive_layer_system
    adaptive_layer_system = AdaptiveSoundLayerSystem(acoustic_engine)
    adaptive_layer_system.initialize_sound_layers()
    
    # Add predefined adaptation rules
    adaptive_layer_system.add_adaptation_rule(
        "loud_environment",
        SoundLayerAdaptationRules.loud_environment_condition,
        SoundLayerAdaptationRules.loud_environment_adaptation
    )
    
    adaptive_layer_system.add_adaptation_rule(
        "complex_environment",
        SoundLayerAdaptationRules.complex_environment_condition,
        SoundLayerAdaptationRules.complex_environment_adaptation
    )
    
    return adaptive_layer_system

def adapt_sound_layers_automatically():
    """Automatically adapt sound layers based on acoustic environment"""
    if adaptive_layer_system:
        adapted_params = adaptive_layer_system.adapt_sound_layers()
        adaptive_layer_system.apply_layer_adaptations(adapted_params)
        return adapted_params
    return {}

def get_adaptation_status():
    """Get the current status of the adaptive sound layer system"""
    if adaptive_layer_system:
        return adaptive_layer_system.get_adaptation_summary()
    return {"status": "not_initialized"}