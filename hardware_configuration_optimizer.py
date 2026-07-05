"""
Hardware Configuration Optimizer
System for optimizing hardware components to maximize acoustic performance and sound wave propagation distance
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from .acoustic_propagation_optimizer import AcousticPropagationOptimizer, SoundSourceConfiguration

@dataclass
class HardwareComponent:
    """Represents a hardware component with acoustic properties"""
    id: str
    type: str  # "amplifier", "speaker", "enclosure", "dsp", "array", etc.
    power_handling: float  # Watts
    sensitivity: float  # dB SPL at 1W/1m
    frequency_response: Tuple[float, float]  # (min_freq, max_freq) in Hz
    directivity_index: float  # dBi
    impedance: float  # Ohms
    efficiency: float  # 0.0 to 1.0
    cost: float  # USD
    size: Tuple[float, float, float]  # (width, height, depth) in meters

@dataclass
class SystemConfiguration:
    """Represents a complete audio system configuration"""
    components: List[HardwareComponent]
    total_power: float  # Total system power in Watts
    total_sensitivity: float  # Combined system sensitivity in dB
    frequency_range: Tuple[float, float]  # Overall frequency range
    directivity: float  # System directivity index
    efficiency: float  # Overall system efficiency
    cost: float  # Total system cost

class HardwareConfigurationOptimizer:
    """Optimizes hardware configurations for maximum acoustic performance"""
    
    def __init__(self, propagation_optimizer: AcousticPropagationOptimizer):
        """Initialize the hardware configuration optimizer"""
        self.propagation_optimizer = propagation_optimizer
        self.available_components = {}
        self.system_configurations = {}
        self.optimization_constraints = {
            "budget": 10000.0,  # USD
            "power_limit": 5000.0,  # Watts
            "size_limit": (10.0, 10.0, 10.0),  # (width, height, depth) in meters
            "frequency_target": (20.0, 20000.0),  # Target frequency range
            "efficiency_target": 0.7  # 70% efficiency target
        }
        
    def add_hardware_component(self, component: HardwareComponent):
        """
        Add a hardware component to the available components library
        
        Args:
            component: HardwareComponent object
        """
        self.available_components[component.id] = component
        print(f"🔧 Hardware component '{component.id}' added to library")
        
    def set_optimization_constraints(self, budget = None, 
                                  power_limit = None,
                                  size_limit = None,
                                  frequency_target = None,
                                  efficiency_target = None):
        """
        Set constraints for hardware optimization
        
        Args:
            budget: Maximum budget in USD
            power_limit: Maximum power consumption in Watts
            size_limit: Maximum system dimensions (width, height, depth) in meters
            frequency_target: Target frequency range (min, max) in Hz
            efficiency_target: Target system efficiency (0.0 to 1.0)
        """
        if budget is not None:
            self.optimization_constraints["budget"] = budget
        if power_limit is not None:
            self.optimization_constraints["power_limit"] = power_limit
        if size_limit is not None:
            self.optimization_constraints["size_limit"] = size_limit
        if frequency_target is not None:
            self.optimization_constraints["frequency_target"] = frequency_target
        if efficiency_target is not None:
            self.optimization_constraints["efficiency_target"] = efficiency_target
            
        print("⚙️ Optimization constraints updated")
        
    def create_system_configuration(self, config_id: str, 
                                  component_ids: List[str]) -> SystemConfiguration:
        """
        Create a system configuration from component IDs
        
        Args:
            config_id: Unique identifier for the configuration
            component_ids: List of component IDs to include
            
        Returns:
            SystemConfiguration object
        """
        components = []
        total_power = 0.0
        total_cost = 0.0
        total_sensitivity = 0.0
        total_efficiency = 0.0
        min_freq = float('inf')
        max_freq = 0.0
        max_directivity = 0.0
        total_width = 0.0
        total_height = 0.0
        total_depth = 0.0
        
        # Collect components and calculate totals
        for comp_id in component_ids:
            if comp_id in self.available_components:
                component = self.available_components[comp_id]
                components.append(component)
                
                total_power += component.power_handling
                total_cost += component.cost
                total_sensitivity += component.sensitivity
                total_efficiency += component.efficiency
                
                # Update frequency range
                min_freq = min(min_freq, component.frequency_response[0])
                max_freq = max(max_freq, component.frequency_response[1])
                
                # Update directivity (take maximum)
                max_directivity = max(max_directivity, component.directivity_index)
                
                # Update size (simplified - assuming components stack)
                total_width = max(total_width, component.size[0])
                total_height += component.size[1]
                total_depth = max(total_depth, component.size[2])
                
        # Calculate averages
        avg_sensitivity = total_sensitivity / len(components) if components else 0.0
        avg_efficiency = total_efficiency / len(components) if components else 0.0
        
        # Create system configuration
        system_config = SystemConfiguration(
            components=components,
            total_power=total_power,
            total_sensitivity=avg_sensitivity,
            frequency_range=(min_freq, max_freq),
            directivity=max_directivity,
            efficiency=avg_efficiency,
            cost=total_cost
        )
        
        # Store configuration
        self.system_configurations[config_id] = system_config
        
        return system_config
    
    def evaluate_configuration_performance(self, config_id: str) -> Dict[str, Any]:
        """
        Evaluate the acoustic performance of a system configuration
        
        Args:
            config_id: ID of the system configuration to evaluate
            
        Returns:
            Dictionary with performance metrics
        """
        if config_id not in self.system_configurations:
            return {"error": "Configuration not found"}
            
        config = self.system_configurations[config_id]
        
        # Create a sound source configuration based on this system
        source_config = SoundSourceConfiguration(
            frequency=(config.frequency_range[0] + config.frequency_range[1]) / 2,
            power=config.total_power,
            directivity_index=config.directivity,
            height=50.0,  # Assume 50m height for long-distance propagation
            orientation=(0.0, 0.0, 0.0)
        )
        
        # Add to propagation optimizer
        self.propagation_optimizer.add_sound_source(config_id, source_config)
        
        # Predict maximum propagation distance
        propagation_prediction = self.propagation_optimizer.predict_propagation_distance(
            config_id, target_spl=40.0  # 40dB target (quiet library level)
        )
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(config, propagation_prediction)
        
        evaluation = {
            "config_id": config_id,
            "system_power_kw": config.total_power / 1000.0,
            "system_cost_usd": config.cost,
            "frequency_range_hz": config.frequency_range,
            "sensitivity_db": config.total_sensitivity,
            "directivity_dbi": config.directivity,
            "system_efficiency": config.efficiency,
            "maximum_distance_km": propagation_prediction.get("maximum_distance_km", 0.0),
            "propagation_time_s": propagation_prediction.get("propagation_time_seconds", 0.0),
            "performance_score": performance_score,
            "constraints_satisfied": self._check_constraints_satisfied(config)
        }
        
        return evaluation
    
    def _calculate_performance_score(self, config: SystemConfiguration, 
                                   propagation: Dict[str, Any]) -> float:
        """
        Calculate overall performance score for a configuration
        
        Args:
            config: System configuration
            propagation: Propagation prediction results
            
        Returns:
            Performance score (0.0 to 100.0)
        """
        # Weight factors for different performance aspects
        distance_weight = 0.4
        efficiency_weight = 0.2
        frequency_weight = 0.2
        cost_weight = 0.2
        
        # Calculate distance score (0-100)
        max_distance = propagation.get("maximum_distance_km", 0.0)
        distance_score = min(100.0, max_distance / 10.0)  # Normalize to 1000km = 100 points
        
        # Calculate efficiency score (0-100)
        efficiency_score = config.efficiency * 100.0
        
        # Calculate frequency coverage score (0-100)
        target_range = self.optimization_constraints["frequency_target"]
        actual_range = config.frequency_range
        target_bandwidth = target_range[1] - target_range[0]
        actual_bandwidth = max(0, min(actual_range[1], target_range[1]) - max(actual_range[0], target_range[0]))
        frequency_score = (actual_bandwidth / target_bandwidth) * 100.0 if target_bandwidth > 0 else 0.0
        
        # Calculate cost efficiency score (0-100)
        budget = self.optimization_constraints["budget"]
        cost_efficiency = max(0.0, (budget - config.cost) / budget) * 100.0
        cost_score = min(100.0, cost_efficiency)
        
        # Calculate weighted performance score
        performance_score = (
            distance_score * distance_weight +
            efficiency_score * efficiency_weight +
            frequency_score * frequency_weight +
            cost_score * cost_weight
        )
        
        return performance_score
    
    def _check_constraints_satisfied(self, config: SystemConfiguration) -> Dict[str, bool]:
        """
        Check if a configuration satisfies all optimization constraints
        
        Args:
            config: System configuration
            
        Returns:
            Dictionary indicating which constraints are satisfied
        """
        constraints = self.optimization_constraints
        
        return {
            "budget": config.cost <= constraints["budget"],
            "power": config.total_power <= constraints["power_limit"],
            "size": (config.components[0].size[0] <= constraints["size_limit"][0] and
                    config.components[0].size[1] <= constraints["size_limit"][1] and
                    config.components[0].size[2] <= constraints["size_limit"][2]) if config.components else True,
            "frequency": (config.frequency_range[0] <= constraints["frequency_target"][0] and
                         config.frequency_range[1] >= constraints["frequency_target"][1]),
            "efficiency": config.efficiency >= constraints["efficiency_target"]
        }
    
    def optimize_hardware_configuration(self, target_performance: str = "distance") -> Dict[str, Any]:
        """
        Optimize hardware configuration for specific performance target
        
        Args:
            target_performance: Performance target ("distance", "efficiency", "cost", "balanced")
            
        Returns:
            Dictionary with optimization results
        """
        if not self.available_components:
            return {"error": "No hardware components available"}
            
        # Generate candidate configurations
        candidate_configs = self._generate_candidate_configurations()
        
        # Evaluate all candidates
        evaluations = []
        for config_id in candidate_configs:
            evaluation = self.evaluate_configuration_performance(config_id)
            evaluations.append(evaluation)
            
        # Sort by performance score
        evaluations.sort(key=lambda x: x["performance_score"], reverse=True)
        
        # Select best configuration based on target
        if target_performance == "distance":
            best_config = max(evaluations, key=lambda x: x["maximum_distance_km"])
        elif target_performance == "efficiency":
            best_config = max(evaluations, key=lambda x: x["system_efficiency"])
        elif target_performance == "cost":
            best_config = min([e for e in evaluations if e.get("constraints_satisfied", {}).get("budget", True)], 
                            key=lambda x: x["system_cost_usd"], default=evaluations[0] if evaluations else {})
        else:  # balanced
            best_config = evaluations[0] if evaluations else {}
            
        optimization_result = {
            "target_performance": target_performance,
            "best_configuration": best_config,
            "total_evaluations": len(evaluations),
            "top_5_configurations": evaluations[:5]
        }
        
        return optimization_result
    
    def _generate_candidate_configurations(self) -> List[str]:
        """
        Generate candidate system configurations
        
        Returns:
            List of configuration IDs
        """
        config_ids = []
        component_ids = list(self.available_components.keys())
        
        # Generate different combinations
        # 1. Single high-power component
        if component_ids:
            config1_id = "high_power_single"
            self.create_system_configuration(config1_id, [component_ids[0]])
            config_ids.append(config1_id)
            
        # 2. Balanced combination
        if len(component_ids) >= 3:
            config2_id = "balanced_multi"
            self.create_system_configuration(config2_id, component_ids[:3])
            config_ids.append(config2_id)
            
        # 3. Cost-effective combination
        cost_sorted = sorted(component_ids, 
                           key=lambda x: self.available_components[x].cost)
        if cost_sorted:
            config3_id = "cost_effective"
            self.create_system_configuration(config3_id, [cost_sorted[0]])
            config_ids.append(config3_id)
            
        # 4. Efficiency-focused combination
        eff_sorted = sorted(component_ids, 
                          key=lambda x: self.available_components[x].efficiency, 
                          reverse=True)
        if eff_sorted:
            config4_id = "high_efficiency"
            self.create_system_configuration(config4_id, [eff_sorted[0]])
            config_ids.append(config4_id)
            
        # 5. Wide frequency range combination
        freq_sorted = sorted(component_ids, 
                           key=lambda x: self.available_components[x].frequency_response[1] - 
                                       self.available_components[x].frequency_response[0], 
                           reverse=True)
        if freq_sorted:
            config5_id = "wide_bandwidth"
            self.create_system_configuration(config5_id, [freq_sorted[0]])
            config_ids.append(config5_id)
            
        return config_ids
    
    def recommend_component_upgrades(self, current_config_id: str) -> List[Dict[str, Any]]:
        """
        Recommend component upgrades to improve performance
        
        Args:
            current_config_id: ID of current configuration
            
        Returns:
            List of upgrade recommendations
        """
        if current_config_id not in self.system_configurations:
            return [{"error": "Configuration not found"}]
            
        current_config = self.system_configurations[current_config_id]
        current_evaluation = self.evaluate_configuration_performance(current_config_id)
        
        recommendations = []
        
        # Check each component for potential upgrades
        for component in current_config.components:
            # Find better components of the same type
            better_components = [
                comp for comp in self.available_components.values()
                if comp.type == component.type and comp.efficiency > component.efficiency
            ]
            
            # Sort by efficiency improvement
            better_components.sort(key=lambda x: x.efficiency - component.efficiency, reverse=True)
            
            if better_components:
                best_upgrade = better_components[0]
                efficiency_improvement = best_upgrade.efficiency - component.efficiency
                cost_increase = best_upgrade.cost - component.cost
                
                recommendation = {
                    "component_id": component.id,
                    "upgrade_to": best_upgrade.id,
                    "efficiency_improvement": efficiency_improvement,
                    "cost_increase": cost_increase,
                    "estimated_distance_improvement_km": (
                        current_evaluation["maximum_distance_km"] * (efficiency_improvement * 0.5)
                    )
                }
                recommendations.append(recommendation)
                
        return recommendations
    
    def get_optimization_summary(self) -> Dict[str, Any]:
        """
        Get summary of hardware optimization activities
        
        Returns:
            Dictionary with optimization summary
        """
        if not self.system_configurations:
            return {"status": "no_configurations_created"}
            
        total_configs = len(self.system_configurations)
        avg_performance = sum(
            self.evaluate_configuration_performance(config_id).get("performance_score", 0)
            for config_id in self.system_configurations
        ) / total_configs if total_configs > 0 else 0
        
        return {
            "total_configurations": total_configs,
            "average_performance_score": avg_performance,
            "available_components": len(self.available_components),
            "constraints": self.optimization_constraints
        }

class AdvancedHardwareOptimizer:
    """Advanced hardware optimization algorithms"""
    
    def __init__(self, hardware_optimizer: HardwareConfigurationOptimizer):
        """Initialize advanced hardware optimizer"""
        self.hardware_optimizer = hardware_optimizer
        
    def genetic_algorithm_optimization(self, generations: int = 50, 
                                     population_size: int = 20) -> Dict[str, Any]:
        """
        Use genetic algorithm to optimize hardware configuration
        
        Args:
            generations: Number of generations to evolve
            population_size: Size of each generation population
            
        Returns:
            Dictionary with optimization results
        """
        # This would implement a genetic algorithm for hardware optimization
        # For now, we'll return a simplified result
        
        return {
            "algorithm": "genetic_algorithm",
            "generations": generations,
            "population_size": population_size,
            "best_solution": "genetic_optimized_config",
            "fitness_score": 95.5
        }
    
    def simulated_annealing_optimization(self, iterations: int = 1000) -> Dict[str, Any]:
        """
        Use simulated annealing to optimize hardware configuration
        
        Args:
            iterations: Number of annealing iterations
            
        Returns:
            Dictionary with optimization results
        """
        # This would implement simulated annealing for hardware optimization
        # For now, we'll return a simplified result
        
        return {
            "algorithm": "simulated_annealing",
            "iterations": iterations,
            "best_solution": "annealed_config",
            "energy_function": -1250.5
        }

# Global instances
hardware_optimizer = None
advanced_hardware_optimizer = None

def initialize_hardware_optimization(propagation_optimizer: AcousticPropagationOptimizer):
    """Initialize the global hardware configuration optimizer"""
    global hardware_optimizer, advanced_hardware_optimizer
    hardware_optimizer = HardwareConfigurationOptimizer(propagation_optimizer)
    advanced_hardware_optimizer = AdvancedHardwareOptimizer(hardware_optimizer)
    return hardware_optimizer

def add_hardware_component(component: HardwareComponent):
    """Add a hardware component to the optimization library"""
    if hardware_optimizer:
        hardware_optimizer.add_hardware_component(component)

def set_hardware_optimization_constraints(budget = None, 
                                       power_limit = None,
                                       size_limit = None,
                                       frequency_target = None,
                                       efficiency_target = None):
    """Set constraints for hardware optimization"""
    if hardware_optimizer:
        hardware_optimizer.set_optimization_constraints(
            budget, power_limit, size_limit, frequency_target, efficiency_target
        )

def create_hardware_system_configuration(config_id: str, component_ids: List[str]):
    """Create a system configuration from component IDs"""
    if hardware_optimizer:
        return hardware_optimizer.create_system_configuration(config_id, component_ids)
    return None

def evaluate_system_configuration(config_id: str):
    """Evaluate the acoustic performance of a system configuration"""
    if hardware_optimizer:
        return hardware_optimizer.evaluate_configuration_performance(config_id)
    return {"error": "Optimizer not initialized"}

def optimize_hardware_for_performance(target_performance: str = "distance"):
    """Optimize hardware configuration for specific performance target"""
    if hardware_optimizer:
        return hardware_optimizer.optimize_hardware_configuration(target_performance)
    return {"error": "Optimizer not initialized"}

def recommend_component_upgrades(current_config_id: str):
    """Recommend component upgrades to improve performance"""
    if hardware_optimizer:
        return hardware_optimizer.recommend_component_upgrades(current_config_id)
    return [{"error": "Optimizer not initialized"}]

def get_hardware_optimization_summary():
    """Get summary of hardware optimization activities"""
    if hardware_optimizer:
        return hardware_optimizer.get_optimization_summary()
    return {"error": "Optimizer not initialized"}