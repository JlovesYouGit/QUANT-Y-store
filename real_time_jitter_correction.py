"""
Real-Time Jitter Correction System
System for detecting and correcting real-time jitter in sound output
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from collections import deque

@dataclass
class JitterCorrectionProfile:
    """Represents a jitter correction profile"""
    correction_type: str  # "interpolation", "prediction", "smoothing", "buffering"
    aggressiveness: float  # 0.0 to 1.0
    latency_tolerance: float  # seconds
    frequency_response: Tuple[float, float]  # (min_freq, max_freq) Hz
    effectiveness: float  # 0.0 to 1.0

@dataclass
class JitterEvent:
    """Represents a detected jitter event"""
    timestamp: float  # seconds
    magnitude: float  # relative magnitude
    frequency: float  # Hz
    duration: float  # seconds
    correction_applied: bool
    correction_type: str

class RealTimeJitterCorrection:
    """System for real-time jitter detection and correction"""
    
    def __init__(self):
        """Initialize the real-time jitter correction system"""
        self.jitter_detectors = {}
        self.correction_profiles = {}
        self.jitter_events = deque(maxlen=1000)
        self.correction_history = deque(maxlen=1000)
        self.system_parameters = {
            "sampling_rate": 48000.0,  # Hz
            "buffer_size": 1024,       # samples
            "detection_threshold": 0.001,  # 0.1% threshold
            "correction_latency": 0.005,   # 5ms max latency
            "max_correction": 0.5,     # 50% max correction
        }
        self.jitter_detection_enabled = True
        self.correction_enabled = True
        self.real_time_buffer = deque(maxlen=4096)  # Real-time audio buffer
        
    def add_jitter_detector(self, detector_id: str, detector_type: str):
        """
        Add a jitter detector to the system
        
        Args:
            detector_id: Unique identifier for the detector
            detector_type: Type of detector ("amplitude", "frequency", "phase", "timing")
        """
        self.jitter_detectors[detector_id] = {
            "type": detector_type,
            "active": True,
            "sensitivity": 1.0,
            "last_detection": 0.0,
            "detection_history": deque(maxlen=100)
        }
        print(f"🔍 Jitter detector '{detector_id}' added ({detector_type})")
        
    def add_correction_profile(self, profile_id: str, profile: JitterCorrectionProfile):
        """
        Add a jitter correction profile to the system
        
        Args:
            profile_id: Unique identifier for the profile
            profile: JitterCorrectionProfile object
        """
        self.correction_profiles[profile_id] = profile
        print(f"🔧 Correction profile '{profile_id}' added ({profile.correction_type})")
        
    def set_system_parameters(self, sampling_rate = None,
                           buffer_size = None,
                           detection_threshold = None,
                           correction_latency = None,
                           max_correction = None):
        """
        Set system parameters for jitter correction
        
        Args:
            sampling_rate: Audio sampling rate in Hz
            buffer_size: Buffer size in samples
            detection_threshold: Jitter detection threshold
            correction_latency: Maximum correction latency in seconds
            max_correction: Maximum correction factor
        """
        if sampling_rate is not None:
            self.system_parameters["sampling_rate"] = sampling_rate
        if buffer_size is not None:
            self.system_parameters["buffer_size"] = buffer_size
        if detection_threshold is not None:
            self.system_parameters["detection_threshold"] = detection_threshold
        if correction_latency is not None:
            self.system_parameters["correction_latency"] = correction_latency
        if max_correction is not None:
            self.system_parameters["max_correction"] = max_correction
            
        print("⚙️ Jitter correction parameters updated")
        
    def enable_jitter_detection(self, enabled: bool = True):
        """
        Enable or disable jitter detection
        
        Args:
            enabled: True to enable, False to disable
        """
        self.jitter_detection_enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🔍 Jitter detection {status}")
        
    def enable_correction(self, enabled: bool = True):
        """
        Enable or disable jitter correction
        
        Args:
            enabled: True to enable, False to disable
        """
        self.correction_enabled = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🛡️ Jitter correction {status}")
        
    def detect_amplitude_jitter(self, signal: List[float]) -> float:
        """
        Detect amplitude jitter in signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Jitter magnitude (0.0 to 1.0)
        """
        if len(signal) < 10:
            return 0.0
            
        # Calculate short-term and long-term amplitude variations
        window_size = min(len(signal) // 4, 100)
        if window_size < 5:
            return 0.0
            
        # Short-term amplitude (recent window)
        recent_window = signal[-window_size:]
        recent_amplitude = max(abs(x) for x in recent_window) if recent_window else 0.0
        
        # Long-term amplitude (previous window)
        previous_window = signal[-2*window_size:-window_size] if len(signal) >= 2*window_size else signal[:-window_size]
        previous_amplitude = max(abs(x) for x in previous_window) if previous_window else recent_amplitude
        
        # Calculate jitter magnitude
        if previous_amplitude > 0:
            jitter_magnitude = abs(recent_amplitude - previous_amplitude) / previous_amplitude
        else:
            jitter_magnitude = 0.0
            
        return min(1.0, jitter_magnitude)
    
    def detect_frequency_jitter(self, signal: List[float]) -> float:
        """
        Detect frequency jitter in signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Jitter magnitude (0.0 to 1.0)
        """
        if len(signal) < 20:
            return 0.0
            
        # Simple frequency estimation using zero-crossing rate
        sampling_rate = self.system_parameters["sampling_rate"]
        window_size = min(len(signal) // 2, 200)
        
        # Estimate frequency in recent window
        recent_window = signal[-window_size:]
        recent_crossings = self._count_zero_crossings(recent_window)
        recent_frequency = (recent_crossings / 2.0) * (sampling_rate / window_size)
        
        # Estimate frequency in previous window
        previous_window = signal[-2*window_size:-window_size]
        previous_crossings = self._count_zero_crossings(previous_window)
        previous_frequency = (previous_crossings / 2.0) * (sampling_rate / window_size)
        
        # Calculate jitter magnitude
        if previous_frequency > 0:
            jitter_magnitude = abs(recent_frequency - previous_frequency) / previous_frequency
        else:
            jitter_magnitude = 0.0
            
        return min(1.0, jitter_magnitude)
    
    def detect_phase_jitter(self, signal: List[float]) -> float:
        """
        Detect phase jitter in signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Jitter magnitude (0.0 to 1.0)
        """
        if len(signal) < 10:
            return 0.0
            
        # Simple phase detection using peak positions
        window_size = min(len(signal) // 2, 100)
        recent_window = signal[-window_size:]
        previous_window = signal[-2*window_size:-window_size]
        
        # Find peak positions
        recent_peak_idx = self._find_peak_index(recent_window)
        previous_peak_idx = self._find_peak_index(previous_window)
        
        # Calculate phase difference
        if window_size > 0:
            recent_phase = (2 * math.pi * recent_peak_idx) / window_size
            previous_phase = (2 * math.pi * previous_peak_idx) / window_size
            phase_diff = abs(recent_phase - previous_phase)
            # Normalize to 0-2π range
            phase_diff = min(phase_diff, 2 * math.pi - phase_diff)
            jitter_magnitude = phase_diff / math.pi  # Normalize to 0-1
        else:
            jitter_magnitude = 0.0
            
        return jitter_magnitude
    
    def detect_timing_jitter(self, timestamps: List[float]) -> float:
        """
        Detect timing jitter in signal timestamps
        
        Args:
            timestamps: List of sample timestamps
            
        Returns:
            Jitter magnitude (0.0 to 1.0)
        """
        if len(timestamps) < 10:
            return 0.0
            
        # Calculate inter-sample intervals
        intervals = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
        
        # Calculate mean and standard deviation of intervals
        mean_interval = sum(intervals) / len(intervals) if intervals else 0.0
        if mean_interval <= 0:
            return 0.0
            
        variance = sum((interval - mean_interval) ** 2 for interval in intervals) / len(intervals)
        std_dev = math.sqrt(variance)
        
        # Jitter magnitude as coefficient of variation
        jitter_magnitude = std_dev / mean_interval if mean_interval > 0 else 0.0
        
        return min(1.0, jitter_magnitude)
    
    def _count_zero_crossings(self, signal: List[float]) -> int:
        """
        Count zero crossings in signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Number of zero crossings
        """
        crossings = 0
        for i in range(1, len(signal)):
            if (signal[i-1] <= 0 < signal[i]) or (signal[i-1] >= 0 > signal[i]):
                crossings += 1
        return crossings
    
    def _find_peak_index(self, signal: List[float]) -> int:
        """
        Find index of maximum absolute value in signal
        
        Args:
            signal: List of signal samples
            
        Returns:
            Index of peak value
        """
        if not signal:
            return 0
            
        max_idx = 0
        max_val = abs(signal[0])
        
        for i in range(1, len(signal)):
            if abs(signal[i]) > max_val:
                max_val = abs(signal[i])
                max_idx = i
                
        return max_idx
    
    def detect_jitter_events(self, signal: List[float], 
                          timestamps = None) -> List[JitterEvent]:
        """
        Detect jitter events in signal
        
        Args:
            signal: List of signal samples
            timestamps: List of sample timestamps (optional)
            
        Returns:
            List of detected JitterEvent objects
        """
        if not self.jitter_detection_enabled or len(signal) < 10:
            return []
            
        detected_events = []
        current_time = len(self.jitter_events) * 0.1  # Simplified timestamp
        
        # Detect using all active detectors
        for detector_id, detector in self.jitter_detectors.items():
            if not detector["active"]:
                continue
                
            jitter_magnitude = 0.0
            jitter_frequency = 0.0
            
            if detector["type"] == "amplitude":
                jitter_magnitude = self.detect_amplitude_jitter(signal)
                jitter_frequency = 10.0  # Simplified
            elif detector["type"] == "frequency":
                jitter_magnitude = self.detect_frequency_jitter(signal)
                # Estimate frequency from sampling rate and buffer size
                jitter_frequency = self.system_parameters["sampling_rate"] / len(signal)
            elif detector["type"] == "phase":
                jitter_magnitude = self.detect_phase_jitter(signal)
                jitter_frequency = 50.0  # Simplified
            elif detector["type"] == "timing" and timestamps:
                jitter_magnitude = self.detect_timing_jitter(timestamps)
                jitter_frequency = 100.0  # Simplified
                
            # Check if jitter exceeds threshold
            if jitter_magnitude > self.system_parameters["detection_threshold"]:
                event = JitterEvent(
                    timestamp=current_time,
                    magnitude=jitter_magnitude,
                    frequency=jitter_frequency,
                    duration=0.01,  # Simplified duration
                    correction_applied=False,
                    correction_type=""
                )
                detected_events.append(event)
                
                # Store in history
                self.jitter_events.append(event)
                
                # Update detector
                detector["last_detection"] = current_time
                detector["detection_history"].append({
                    "time": current_time,
                    "magnitude": jitter_magnitude
                })
                
        return detected_events
    
    def select_correction_profile(self, jitter_event: JitterEvent) -> str:
        """
        Select appropriate correction profile for jitter event
        
        Args:
            jitter_event: JitterEvent object
            
        Returns:
            ID of selected correction profile
        """
        if not self.correction_profiles:
            return ""
            
        best_profile_id = ""
        best_match_score = 0.0
        
        for profile_id, profile in self.correction_profiles.items():
            # Calculate match score based on jitter characteristics
            frequency_match = 1.0 - abs(profile.frequency_response[0] - jitter_event.frequency) / \
                             max(profile.frequency_response[0], jitter_event.frequency, 1.0)
            
            magnitude_match = 1.0 - abs(profile.aggressiveness - jitter_event.magnitude)
            
            # Combined score (weighted)
            match_score = 0.6 * frequency_match + 0.4 * magnitude_match
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_profile_id = profile_id
                
        return best_profile_id
    
    def apply_interpolation_correction(self, signal: List[float], 
                                    jitter_event: JitterEvent) -> List[float]:
        """
        Apply interpolation-based correction to signal
        
        Args:
            signal: List of signal samples
            jitter_event: JitterEvent object
            
        Returns:
            Corrected signal
        """
        if len(signal) < 5:
            return signal
            
        # Simple linear interpolation to smooth jitter
        corrected_signal = signal.copy()
        window_size = min(len(signal) // 4, 50)
        
        # Apply smoothing around the jitter event
        start_idx = max(0, len(signal) - window_size)
        end_idx = min(len(signal), start_idx + window_size)
        
        if end_idx - start_idx > 2:
            # Linear interpolation between first and last points
            start_val = signal[start_idx]
            end_val = signal[end_idx - 1]
            
            for i in range(start_idx, end_idx):
                t = (i - start_idx) / (end_idx - start_idx - 1) if end_idx > start_idx + 1 else 0
                corrected_signal[i] = start_val + t * (end_val - start_val)
                
        return corrected_signal
    
    def apply_prediction_correction(self, signal: List[float], 
                                 jitter_event: JitterEvent) -> List[float]:
        """
        Apply prediction-based correction to signal
        
        Args:
            signal: List of signal samples
            jitter_event: JitterEvent object
            
        Returns:
            Corrected signal
        """
        if len(signal) < 10:
            return signal
            
        # Simple prediction using recent trend
        corrected_signal = signal.copy()
        prediction_window = min(len(signal) // 3, 30)
        
        # Calculate trend from recent samples
        recent_samples = signal[-prediction_window:]
        if len(recent_samples) >= 2:
            # Linear trend
            x_vals = list(range(len(recent_samples)))
            y_vals = recent_samples
            
            # Simple linear regression
            n = len(x_vals)
            sum_x = sum(x_vals)
            sum_y = sum(y_vals)
            sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
            sum_xx = sum(x * x for x in x_vals)
            
            if n * sum_xx - sum_x * sum_x != 0:
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
                intercept = (sum_y - slope * sum_x) / n
                
                # Apply correction to recent samples
                correction_start = max(0, len(signal) - prediction_window // 2)
                for i in range(correction_start, len(signal)):
                    predicted_val = slope * (i - len(signal) + prediction_window) + intercept
                    # Blend original and predicted values
                    blend_factor = min(1.0, (i - correction_start) / (len(signal) - correction_start))
                    corrected_signal[i] = (1 - blend_factor) * signal[i] + blend_factor * predicted_val
                    
        return corrected_signal
    
    def apply_smoothing_correction(self, signal: List[float], 
                                jitter_event: JitterEvent) -> List[float]:
        """
        Apply smoothing-based correction to signal
        
        Args:
            signal: List of signal samples
            jitter_event: JitterEvent object
            
        Returns:
            Corrected signal
        """
        if len(signal) < 5:
            return signal
            
        # Simple moving average smoothing
        corrected_signal = signal.copy()
        window_size = min(len(signal) // 5, 10)
        window_size = max(3, window_size)  # Minimum window size
        
        # Apply moving average
        for i in range(window_size, len(signal)):
            window_sum = sum(signal[max(0, i-window_size):i])
            corrected_signal[i] = window_sum / min(i, window_size)
            
        return corrected_signal
    
    def correct_jitter_events(self, signal: List[float], 
                           jitter_events: List[JitterEvent]) -> List[float]:
        """
        Apply corrections for detected jitter events
        
        Args:
            signal: List of signal samples
            jitter_events: List of JitterEvent objects
            
        Returns:
            Corrected signal
        """
        if not self.correction_enabled or not jitter_events:
            return signal
            
        corrected_signal = signal.copy()
        
        for event in jitter_events:
            # Select appropriate correction profile
            profile_id = self.select_correction_profile(event)
            if not profile_id or profile_id not in self.correction_profiles:
                continue
                
            profile = self.correction_profiles[profile_id]
            
            # Apply correction based on profile type
            if profile.correction_type == "interpolation":
                corrected_signal = self.apply_interpolation_correction(corrected_signal, event)
                event.correction_type = "interpolation"
            elif profile.correction_type == "prediction":
                corrected_signal = self.apply_prediction_correction(corrected_signal, event)
                event.correction_type = "prediction"
            elif profile.correction_type == "smoothing":
                corrected_signal = self.apply_smoothing_correction(corrected_signal, event)
                event.correction_type = "smoothing"
                
            event.correction_applied = True
            
            # Store correction in history
            self.correction_history.append({
                "event": event,
                "profile_id": profile_id,
                "timestamp": len(self.correction_history)
            })
            
        return corrected_signal
    
    def process_real_time_signal(self, signal_chunk: List[float], 
                             timestamps = None) -> List[float]:
        """
        Process real-time signal chunk for jitter detection and correction
        
        Args:
            signal_chunk: List of signal samples
            timestamps: List of sample timestamps (optional)
            
        Returns:
            Processed signal chunk
        """
        # Add to real-time buffer
        self.real_time_buffer.extend(signal_chunk)
        
        # Detect jitter events
        jitter_events = self.detect_jitter_events(list(self.real_time_buffer), timestamps)
        
        # Apply corrections
        if jitter_events:
            corrected_buffer = self.correct_jitter_events(list(self.real_time_buffer), jitter_events)
            # Return only the new chunk
            return corrected_buffer[-len(signal_chunk):]
        else:
            return signal_chunk
    
    def get_jitter_correction_summary(self) -> Dict[str, Any]:
        """
        Get summary of jitter correction activities
        
        Returns:
            Dictionary with correction summary
        """
        total_events = len(self.jitter_events)
        corrected_events = sum(1 for event in self.jitter_events if event.correction_applied)
        
        if total_events > 0:
            correction_rate = corrected_events / total_events
        else:
            correction_rate = 0.0
            
        # Calculate average jitter magnitude
        if self.jitter_events:
            avg_magnitude = sum(event.magnitude for event in self.jitter_events) / len(self.jitter_events)
        else:
            avg_magnitude = 0.0
            
        return {
            "total_jitter_events": total_events,
            "corrected_events": corrected_events,
            "correction_rate": correction_rate,
            "average_jitter_magnitude": avg_magnitude,
            "active_detectors": len([d for d in self.jitter_detectors.values() if d["active"]]),
            "correction_profiles": len(self.correction_profiles),
            "detection_enabled": self.jitter_detection_enabled,
            "correction_enabled": self.correction_enabled
        }

class AdaptiveJitterPredictor:
    """Adaptive predictor for future jitter events"""
    
    def __init__(self, jitter_correction_system: RealTimeJitterCorrection):
        """Initialize adaptive jitter predictor"""
        self.jitter_correction_system = jitter_correction_system
        self.prediction_model = None
        self.learning_rate = 0.01
        self.prediction_history = deque(maxlen=500)
        
    def train_prediction_model(self, training_data: List[Dict[str, Any]]):
        """
        Train prediction model on historical jitter data
        
        Args:
            training_data: List of jitter event data
        """
        # This would implement machine learning for jitter prediction
        # For now, we'll keep it as a placeholder
        print("🤖 Jitter prediction model training initiated")
        
    def predict_next_jitter(self) -> Dict[str, Any]:
        """
        Predict next jitter event based on historical patterns
        
        Returns:
            Dictionary with predicted jitter characteristics
        """
        # Simple prediction based on recent history
        if len(self.jitter_correction_system.jitter_events) >= 10:
            recent_events = list(self.jitter_correction_system.jitter_events)[-10:]
            avg_magnitude = sum(event.magnitude for event in recent_events) / len(recent_events)
            avg_frequency = sum(event.frequency for event in recent_events) / len(recent_events)
            
            prediction = {
                "predicted_magnitude": avg_magnitude,
                "predicted_frequency": avg_frequency,
                "confidence": 0.7,  # Simplified confidence
                "time_to_event": 0.05  # 50ms prediction
            }
        else:
            prediction = {
                "predicted_magnitude": 0.0,
                "predicted_frequency": 0.0,
                "confidence": 0.0,
                "time_to_event": 0.0
            }
            
        # Store prediction
        self.prediction_history.append(prediction)
        
        return prediction
    
    def pre_compensate_signal(self, signal: List[float], prediction: Dict[str, Any]) -> List[float]:
        """
        Pre-compensate signal based on jitter prediction
        
        Args:
            signal: List of signal samples
            prediction: Jitter prediction dictionary
            
        Returns:
            Pre-compensated signal
        """
        if prediction["confidence"] < 0.5:
            return signal
            
        # Apply pre-compensation based on prediction
        compensated_signal = signal.copy()
        
        # Simple pre-emphasis based on predicted jitter
        pre_emphasis_factor = 1.0 + prediction["predicted_magnitude"] * 0.1
        
        for i in range(len(compensated_signal)):
            compensated_signal[i] *= pre_emphasis_factor
            
        return compensated_signal

# Global instances
jitter_correction_system = RealTimeJitterCorrection()
adaptive_predictor = None

def initialize_jitter_correction():
    """Initialize the global jitter correction system"""
    global jitter_correction_system, adaptive_predictor
    jitter_correction_system = RealTimeJitterCorrection()
    adaptive_predictor = AdaptiveJitterPredictor(jitter_correction_system)
    return jitter_correction_system

def add_jitter_detector(detector_id: str, detector_type: str):
    """Add a jitter detector to the system"""
    jitter_correction_system.add_jitter_detector(detector_id, detector_type)

def add_jitter_correction_profile(profile_id: str, profile: JitterCorrectionProfile):
    """Add a jitter correction profile to the system"""
    jitter_correction_system.add_correction_profile(profile_id, profile)

def set_jitter_correction_parameters(sampling_rate = None,
                                 buffer_size = None,
                                 detection_threshold = None,
                                 correction_latency = None,
                                 max_correction = None):
    """Set system parameters for jitter correction"""
    jitter_correction_system.set_system_parameters(
        sampling_rate, buffer_size, detection_threshold,
        correction_latency, max_correction
    )

def enable_jitter_detection(enabled: bool = True):
    """Enable or disable jitter detection"""
    jitter_correction_system.enable_jitter_detection(enabled)

def enable_jitter_correction(enabled: bool = True):
    """Enable or disable jitter correction"""
    jitter_correction_system.enable_correction(enabled)

def detect_jitter_events(signal: List[float], timestamps = None) -> List[JitterEvent]:
    """Detect jitter events in signal"""
    return jitter_correction_system.detect_jitter_events(signal, timestamps)

def correct_jitter_events(signal: List[float], jitter_events: List[JitterEvent]) -> List[float]:
    """Apply corrections for detected jitter events"""
    return jitter_correction_system.correct_jitter_events(signal, jitter_events)

def process_real_time_signal(signal_chunk: List[float], timestamps = None) -> List[float]:
    """Process real-time signal chunk for jitter detection and correction"""
    return jitter_correction_system.process_real_time_signal(signal_chunk, timestamps)

def predict_next_jitter() -> Dict[str, Any]:
    """Predict next jitter event based on historical patterns"""
    if adaptive_predictor:
        return adaptive_predictor.predict_next_jitter()
    return {}

def pre_compensate_signal(signal: List[float], prediction: Dict[str, Any]) -> List[float]:
    """Pre-compensate signal based on jitter prediction"""
    if adaptive_predictor:
        return adaptive_predictor.pre_compensate_signal(signal, prediction)
    return signal

def get_jitter_correction_summary() -> Dict[str, Any]:
    """Get summary of jitter correction activities"""
    return jitter_correction_system.get_jitter_correction_summary()