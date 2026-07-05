"""
Vibration Compensation System
System for detecting and compensating for vibration-induced sound output instability
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from collections import deque

@dataclass
class VibrationProfile:
    """Represents vibration characteristics"""
    frequency: float  # Hz
    amplitude: float  # meters
    direction: Tuple[float, float, float]  # (x, y, z) unit vector
    phase: float  # radians
    damping_factor: float  # 0.0 to 1.0

@dataclass
class CompensationAdjuster:
    """Represents a compensation adjuster for vibration effects"""
    id: str
    type: str  # "frequency", "amplitude", "phase", "delay", "filter"
    adjustment_range: Tuple[float, float]  # (min, max) values
    response_time: float  # seconds
    current_value: float  # current adjustment value
    target_value: float  # target adjustment value
    stability_threshold: float  # threshold for stable operation

class VibrationCompensationSystem:
    """System for detecting and compensating for vibration-induced sound instability"""
    
    def __init__(self):
        """Initialize the vibration compensation system"""
        self.vibration_sensors = {}
        self.compensation_adjusters = {}
        self.vibration_profiles = {}
        self.sound_output_monitors = {}
        self.compensation_history = deque(maxlen=1000)  # Last 1000 compensation events
        self.system_parameters = {
            "sampling_rate": 48000.0,  # Hz
            "detection_window": 0.1,   # seconds
            "compensation_delay": 0.005, # 5ms compensation delay
            "stability_threshold": 0.001, # 0.1% stability threshold
            "max_compensation": 0.5,   # 50% maximum compensation
        }
        self.vibration_detection_enabled = True
        self.compensation_active = True
        
    def add_vibration_sensor(self, sensor_id: str, sensor_position: Tuple[float, float, float]):
        """
        Add a vibration sensor to the system
        
        Args:
            sensor_id: Unique identifier for the sensor
            sensor_position: (x, y, z) position in meters
        """
        self.vibration_sensors[sensor_id] = {
            "position": sensor_position,
            "active": True,
            "sensitivity": 1.0,
            "last_reading": 0.0,
            "readings_history": deque(maxlen=100)
        }
        print(f"📡 Vibration sensor '{sensor_id}' added at position {sensor_position}")
        
    def add_compensation_adjuster(self, adjuster: CompensationAdjuster):
        """
        Add a compensation adjuster to the system
        
        Args:
            adjuster: CompensationAdjuster object
        """
        self.compensation_adjusters[adjuster.id] = adjuster
        print(f"🔧 Compensation adjuster '{adjuster.id}' added ({adjuster.type})")
        
    def set_system_parameters(self, sampling_rate = None,
                           detection_window = None,
                           compensation_delay = None,
                           stability_threshold = None,
                           max_compensation = None):
        """
        Set system parameters for vibration compensation
        
        Args:
            sampling_rate: Audio sampling rate in Hz
            detection_window: Vibration detection window in seconds
            compensation_delay: Compensation delay in seconds
            stability_threshold: Stability threshold for compensation
            max_compensation: Maximum compensation factor
        """
        if sampling_rate is not None:
            self.system_parameters["sampling_rate"] = sampling_rate
        if detection_window is not None:
            self.system_parameters["detection_window"] = detection_window
        if compensation_delay is not None:
            self.system_parameters["compensation_delay"] = compensation_delay
        if stability_threshold is not None:
            self.system_parameters["stability_threshold"] = stability_threshold
        if max_compensation is not None:
            self.system_parameters["max_compensation"] = max_compensation
            
        print("⚙️ Vibration compensation parameters updated")
        
    def enable_vibration_detection(self, enabled: bool = True):
        """
        Enable or disable vibration detection
        
        Args:
            enabled: True to enable, False to disable
        """
        self.vibration_detection_enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🔍 Vibration detection {status}")
        
    def enable_compensation(self, enabled: bool = True):
        """
        Enable or disable vibration compensation
        
        Args:
            enabled: True to enable, False to disable
        """
        self.compensation_active = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🛡️ Vibration compensation {status}")
        
    def detect_vibration_frequency(self, sensor_id: str, 
                                time_series: List[float]) -> float:
        """
        Detect dominant vibration frequency from time series data
        
        Args:
            sensor_id: ID of the vibration sensor
            time_series: List of vibration readings
            
        Returns:
            Dominant frequency in Hz
        """
        if len(time_series) < 10:
            return 0.0
            
        # Simple frequency detection using zero-crossing method
        zero_crossings = 0
        for i in range(1, len(time_series)):
            if (time_series[i-1] <= 0 < time_series[i]) or (time_series[i-1] >= 0 > time_series[i]):
                zero_crossings += 1
                
        # Estimate frequency based on zero crossings
        sampling_rate = self.system_parameters["sampling_rate"]
        detection_window = self.system_parameters["detection_window"]
        cycles = zero_crossings / 2.0  # Each cycle has 2 zero crossings
        frequency = cycles / detection_window if detection_window > 0 else 0.0
        
        return frequency
    
    def detect_vibration_amplitude(self, time_series: List[float]) -> float:
        """
        Detect vibration amplitude from time series data
        
        Args:
            time_series: List of vibration readings
            
        Returns:
            Amplitude in meters
        """
        if not time_series:
            return 0.0
            
        # Calculate peak-to-peak amplitude
        max_val = max(time_series)
        min_val = min(time_series)
        amplitude = (max_val - min_val) / 2.0
        
        return amplitude
    
    def detect_vibration_phase(self, time_series: List[float]) -> float:
        """
        Detect vibration phase from time series data
        
        Args:
            time_series: List of vibration readings
            
        Returns:
            Phase in radians
        """
        if len(time_series) < 2:
            return 0.0
            
        # Simple phase detection (first peak position)
        max_index = time_series.index(max(time_series))
        sampling_rate = self.system_parameters["sampling_rate"]
        detection_window = self.system_parameters["detection_window"]
        
        # Calculate phase based on position of first peak
        samples_per_window = int(sampling_rate * detection_window)
        if samples_per_window > 0:
            phase = (2 * math.pi * max_index) / samples_per_window
        else:
            phase = 0.0
            
        return phase
    
    def calculate_damping_factor(self, time_series: List[float]) -> float:
        """
        Calculate vibration damping factor from time series data
        
        Args:
            time_series: List of vibration readings
            
        Returns:
            Damping factor (0.0 to 1.0)
        """
        if len(time_series) < 10:
            return 0.0
            
        # Calculate decay rate
        first_half = time_series[:len(time_series)//2]
        second_half = time_series[len(time_series)//2:]
        
        first_energy = sum(x**2 for x in first_half) / len(first_half)
        second_energy = sum(x**2 for x in second_half) / len(second_half)
        
        if first_energy > 0:
            energy_ratio = second_energy / first_energy
            damping = max(0.0, min(1.0, 1.0 - energy_ratio))
        else:
            damping = 0.0
            
        return damping
    
    def analyze_vibration_profile(self, sensor_id: str, 
                               time_series: List[float]) -> VibrationProfile:
        """
        Analyze complete vibration profile from sensor data
        
        Args:
            sensor_id: ID of the vibration sensor
            time_series: List of vibration readings
            
        Returns:
            VibrationProfile object
        """
        frequency = self.detect_vibration_frequency(sensor_id, time_series)
        amplitude = self.detect_vibration_amplitude(time_series)
        phase = self.detect_vibration_phase(time_series)
        damping = self.calculate_damping_factor(time_series)
        
        # Assume vertical vibration direction for simplicity
        direction = (0.0, 1.0, 0.0)
        
        profile = VibrationProfile(
            frequency=frequency,
            amplitude=amplitude,
            direction=direction,
            phase=phase,
            damping_factor=damping
        )
        
        # Store profile
        self.vibration_profiles[sensor_id] = profile
        
        return profile
    
    def calculate_sound_instability(self, vibration_profile: VibrationProfile) -> float:
        """
        Calculate sound instability factor from vibration profile
        
        Args:
            vibration_profile: VibrationProfile object
            
        Returns:
            Instability factor (0.0 to 1.0)
        """
        # Instability is proportional to amplitude and frequency
        # Higher amplitude and frequency cause more instability
        instability = min(1.0, vibration_profile.amplitude * vibration_profile.frequency * 1000)
        
        # Apply damping factor
        instability *= (1.0 - vibration_profile.damping_factor)
        
        return instability
    
    def determine_compensation_strategy(self, sensor_id: str, 
                                     vibration_profile: VibrationProfile) -> Dict[str, float]:
        """
        Determine compensation strategy based on vibration profile
        
        Args:
            sensor_id: ID of the vibration sensor
            vibration_profile: VibrationProfile object
            
        Returns:
            Dictionary with compensation adjustments
        """
        instability = self.calculate_sound_instability(vibration_profile)
        max_compensation = self.system_parameters["max_compensation"]
        
        # Scale compensation based on instability
        compensation_factor = min(max_compensation, instability)
        
        # Determine adjustments based on vibration characteristics
        adjustments = {}
        
        # Frequency compensation (for high-frequency jitter)
        if vibration_profile.frequency > 50.0:  # Above 50Hz jitter
            adjustments["frequency_compensation"] = compensation_factor * 0.3
        else:
            adjustments["frequency_compensation"] = 0.0
            
        # Amplitude compensation (for vibration amplitude)
        adjustments["amplitude_compensation"] = compensation_factor * 0.4
        
        # Phase compensation (for timing jitter)
        adjustments["phase_compensation"] = compensation_factor * 0.2
        
        # Delay compensation (for timing alignment)
        adjustments["delay_compensation"] = compensation_factor * 0.1
        
        # Store in history
        self.compensation_history.append({
            "sensor_id": sensor_id,
            "timestamp": len(self.compensation_history),
            "instability": instability,
            "adjustments": adjustments
        })
        
        return adjustments
    
    def apply_compensation_adjustments(self, adjustments: Dict[str, float]):
        """
        Apply compensation adjustments to system adjusters
        
        Args:
            adjustments: Dictionary with compensation values
        """
        if not self.compensation_active:
            return
            
        # Apply each adjustment to corresponding adjusters
        for adjuster_id, adjuster in self.compensation_adjusters.items():
            if adjuster.type == "frequency" and "frequency_compensation" in adjustments:
                target = adjuster.current_value * (1.0 + adjustments["frequency_compensation"])
                adjuster.target_value = max(adjuster.adjustment_range[0], 
                                          min(adjuster.adjustment_range[1], target))
                                          
            elif adjuster.type == "amplitude" and "amplitude_compensation" in adjustments:
                target = adjuster.current_value * (1.0 - adjustments["amplitude_compensation"])
                adjuster.target_value = max(adjuster.adjustment_range[0], 
                                          min(adjuster.adjustment_range[1], target))
                                          
            elif adjuster.type == "phase" and "phase_compensation" in adjustments:
                # Phase adjustment (add offset)
                target = adjuster.current_value + adjustments["phase_compensation"] * math.pi
                adjuster.target_value = target % (2 * math.pi)
                
            elif adjuster.type == "delay" and "delay_compensation" in adjustments:
                # Delay adjustment
                target = adjuster.current_value + adjustments["delay_compensation"] * 0.01  # 10ms max
                adjuster.target_value = max(adjuster.adjustment_range[0], 
                                          min(adjuster.adjustment_range[1], target))
        
        print(f"🔧 Applied compensation adjustments: {list(adjustments.keys())}")
    
    def update_adjuster_values(self):
        """
        Update adjuster values toward their target values based on response time
        """
        for adjuster in self.compensation_adjusters.values():
            # Simple first-order low-pass filter for smooth adjustment
            if adjuster.response_time > 0:
                alpha = min(1.0, 1.0 / (adjuster.response_time * 100))  # Simplified
                adjuster.current_value += alpha * (adjuster.target_value - adjuster.current_value)
                
    def monitor_sound_output_stability(self, output_data: List[float]) -> Dict[str, Any]:
        """
        Monitor sound output for stability and jitter
        
        Args:
            output_data: List of sound output samples
            
        Returns:
            Dictionary with stability metrics
        """
        if len(output_data) < 10:
            return {"stability": 1.0, "jitter": 0.0, "dropouts": 0}
            
        # Calculate output statistics
        mean_val = sum(output_data) / len(output_data)
        variance = sum((x - mean_val) ** 2 for x in output_data) / len(output_data)
        std_dev = math.sqrt(variance)
        
        # Detect dropouts (samples near zero)
        dropout_threshold = abs(mean_val) * 0.1  # 10% of mean
        dropouts = sum(1 for x in output_data if abs(x) < dropout_threshold)
        
        # Calculate jitter (sample-to-sample variation)
        differences = [abs(output_data[i] - output_data[i-1]) for i in range(1, len(output_data))]
        avg_jitter = sum(differences) / len(differences) if differences else 0.0
        
        # Stability metric (inverse of jitter)
        stability = max(0.0, min(1.0, 1.0 - (avg_jitter / (abs(mean_val) + 1e-10))))
        
        metrics = {
            "stability": stability,
            "jitter": avg_jitter,
            "dropouts": dropouts,
            "mean_value": mean_val,
            "std_deviation": std_dev
        }
        
        # Store metrics
        self.sound_output_monitors[len(self.sound_output_monitors)] = metrics
        
        return metrics
    
    def process_vibration_data(self, sensor_id: str, vibration_data: List[float]) -> Dict[str, Any]:
        """
        Process vibration data and apply compensation
        
        Args:
            sensor_id: ID of the vibration sensor
            vibration_data: List of vibration readings
            
        Returns:
            Dictionary with processing results
        """
        if not self.vibration_detection_enabled:
            return {"status": "detection_disabled"}
            
        if sensor_id not in self.vibration_sensors:
            return {"error": "Sensor not found"}
            
        # Analyze vibration profile
        vibration_profile = self.analyze_vibration_profile(sensor_id, vibration_data)
        
        # Determine compensation strategy
        adjustments = self.determine_compensation_strategy(sensor_id, vibration_profile)
        
        # Apply compensation
        self.apply_compensation_adjustments(adjustments)
        
        # Update adjuster values
        self.update_adjuster_values()
        
        # Calculate instability
        instability = self.calculate_sound_instability(vibration_profile)
        
        result = {
            "sensor_id": sensor_id,
            "vibration_profile": vibration_profile,
            "instability": instability,
            "adjustments": adjustments,
            "compensation_applied": self.compensation_active
        }
        
        return result
    
    def get_compensation_summary(self) -> Dict[str, Any]:
        """
        Get summary of vibration compensation activities
        
        Returns:
            Dictionary with compensation summary
        """
        total_compensations = len(self.compensation_history)
        
        if total_compensations > 0:
            avg_instability = sum(entry["instability"] for entry in self.compensation_history) / total_compensations
            recent_instability = self.compensation_history[-1]["instability"] if self.compensation_history else 0.0
        else:
            avg_instability = 0.0
            recent_instability = 0.0
            
        return {
            "total_compensations": total_compensations,
            "average_instability": avg_instability,
            "recent_instability": recent_instability,
            "sensors_active": len([s for s in self.vibration_sensors.values() if s["active"]]),
            "compensation_enabled": self.compensation_active,
            "detection_enabled": self.vibration_detection_enabled
        }

class AdaptiveVibrationFilter:
    """Adaptive filter for vibration-induced artifacts"""
    
    def __init__(self, compensation_system: VibrationCompensationSystem):
        """Initialize adaptive vibration filter"""
        self.compensation_system = compensation_system
        self.filter_coefficients = [1.0, 0.0, 0.0]  # Simple FIR filter
        self.adaptation_rate = 0.01  # Learning rate
        
    def adapt_filter_coefficients(self, error_signal: List[float]):
        """
        Adapt filter coefficients based on error signal
        
        Args:
            error_signal: List of error values
        """
        # Simple LMS (Least Mean Squares) adaptation
        for i, error in enumerate(error_signal[:len(self.filter_coefficients)]):
            self.filter_coefficients[i] += self.adaptation_rate * error
            
    def apply_filter(self, input_signal: List[float]) -> List[float]:
        """
        Apply adaptive filter to input signal
        
        Args:
            input_signal: List of input samples
            
        Returns:
            Filtered output signal
        """
        if len(input_signal) < len(self.filter_coefficients):
            return input_signal
            
        output_signal = []
        for i in range(len(self.filter_coefficients), len(input_signal)):
            # FIR filter operation
            filtered_value = sum(input_signal[i-j] * self.filter_coefficients[j] 
                               for j in range(len(self.filter_coefficients)))
            output_signal.append(filtered_value)
            
        return output_signal

class RealTimeJitterDetector:
    """Real-time jitter detection system"""
    
    def __init__(self, compensation_system: VibrationCompensationSystem):
        """Initialize real-time jitter detector"""
        self.compensation_system = compensation_system
        self.jitter_threshold = 0.001  # 0.1% jitter threshold
        self.detection_window = 100  # 100 samples
        self.jitter_history = deque(maxlen=1000)
        
    def detect_jitter(self, signal: List[float]) -> Dict[str, Any]:
        """
        Detect jitter in real-time signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Dictionary with jitter detection results
        """
        if len(signal) < self.detection_window:
            return {"jitter_detected": False, "jitter_level": 0.0}
            
        # Calculate short-term and long-term averages
        recent_samples = signal[-self.detection_window:]
        older_samples = signal[-2*self.detection_window:-self.detection_window]
        
        recent_avg = sum(recent_samples) / len(recent_samples)
        older_avg = sum(older_samples) / len(older_samples) if older_samples else recent_avg
        
        # Calculate jitter level
        if older_avg != 0:
            jitter_level = abs(recent_avg - older_avg) / abs(older_avg)
        else:
            jitter_level = 0.0
            
        # Detect jitter
        jitter_detected = jitter_level > self.jitter_threshold
        
        # Store in history
        self.jitter_history.append({
            "timestamp": len(self.jitter_history),
            "jitter_level": jitter_level,
            "detected": jitter_detected
        })
        
        return {
            "jitter_detected": jitter_detected,
            "jitter_level": jitter_level,
            "recent_average": recent_avg,
            "older_average": older_avg
        }

# Global instances
vibration_compensation_system = VibrationCompensationSystem()
adaptive_filter = None
jitter_detector = None

def initialize_vibration_compensation():
    """Initialize the global vibration compensation system"""
    global vibration_compensation_system, adaptive_filter, jitter_detector
    vibration_compensation_system = VibrationCompensationSystem()
    adaptive_filter = AdaptiveVibrationFilter(vibration_compensation_system)
    jitter_detector = RealTimeJitterDetector(vibration_compensation_system)
    return vibration_compensation_system

def add_vibration_sensor(sensor_id: str, sensor_position: Tuple[float, float, float]):
    """Add a vibration sensor to the system"""
    vibration_compensation_system.add_vibration_sensor(sensor_id, sensor_position)

def add_compensation_adjuster(adjuster: CompensationAdjuster):
    """Add a compensation adjuster to the system"""
    vibration_compensation_system.add_compensation_adjuster(adjuster)

def set_vibration_compensation_parameters(sampling_rate = None,
                                      detection_window = None,
                                      compensation_delay = None,
                                      stability_threshold = None,
                                      max_compensation = None):
    """Set system parameters for vibration compensation"""
    vibration_compensation_system.set_system_parameters(
        sampling_rate, detection_window, compensation_delay, 
        stability_threshold, max_compensation
    )

def enable_vibration_detection(enabled: bool = True):
    """Enable or disable vibration detection"""
    vibration_compensation_system.enable_vibration_detection(enabled)

def enable_compensation(enabled: bool = True):
    """Enable or disable vibration compensation"""
    vibration_compensation_system.enable_compensation(enabled)

def process_vibration_data(sensor_id: str, vibration_data: List[float]):
    """Process vibration data and apply compensation"""
    return vibration_compensation_system.process_vibration_data(sensor_id, vibration_data)

def monitor_sound_output_stability(output_data: List[float]):
    """Monitor sound output for stability and jitter"""
    return vibration_compensation_system.monitor_sound_output_stability(output_data)

def adapt_vibration_filter(error_signal: List[float]):
    """Adapt filter coefficients based on error signal"""
    if adaptive_filter:
        adaptive_filter.adapt_filter_coefficients(error_signal)

def apply_adaptive_filter(input_signal: List[float]) -> List[float]:
    """Apply adaptive filter to input signal"""
    if adaptive_filter:
        return adaptive_filter.apply_filter(input_signal)
    return input_signal

def detect_real_time_jitter(signal: List[float]):
    """Detect jitter in real-time signal"""
    if jitter_detector:
        return jitter_detector.detect_jitter(signal)
    return {"jitter_detected": False, "jitter_level": 0.0}

def get_vibration_compensation_summary():
    """Get summary of vibration compensation activities"""
    return vibration_compensation_system.get_compensation_summary()