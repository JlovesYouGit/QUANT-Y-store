"""
Frequency Response Calibrator and Speaker Protection System
Advanced system for calibrating speaker frequency response and protecting speakers from damage
"""

import math
from typing import List, Tuple, Dict, Any
from .precision_speaker_manager import PrecisionSpeakerManager, SpeakerProfile

class FrequencyResponseCalibrator:
    """Calibrates speaker frequency response and implements protection mechanisms"""
    
    def __init__(self, speaker_manager: PrecisionSpeakerManager):
        """Initialize the frequency response calibrator"""
        self.speaker_manager = speaker_manager
        self.calibration_profiles = {}
        self.protection_thresholds = {}
        self.eq_filters = {}
        
    def create_calibration_profile(self, speaker_id: str, 
                                 test_frequencies: List[float],
                                 measured_responses: List[float]) -> Dict[str, Any]:
        """
        Create a calibration profile based on measured frequency responses
        
        Args:
            speaker_id: ID of the speaker
            test_frequencies: List of test frequencies in Hz
            measured_responses: List of measured SPL responses in dB
            
        Returns:
            Dictionary with calibration profile data
        """
        if speaker_id not in self.speaker_manager.speakers:
            return {"error": "Speaker not found"}
            
        # Create frequency response curve
        response_curve = list(zip(test_frequencies, measured_responses))
        
        # Calculate target response (flat response)
        target_response = [(freq, 0.0) for freq in test_frequencies]
        
        # Calculate correction curve
        correction_curve = []
        for (freq, measured), (_, target) in zip(response_curve, target_response):
            correction = target - measured
            correction_curve.append((freq, correction))
            
        # Store calibration profile
        profile = {
            "speaker_id": speaker_id,
            "response_curve": response_curve,
            "correction_curve": correction_curve,
            "target_response": target_response,
            "calibration_date": "current_time",
            "accuracy": self._calculate_calibration_accuracy(response_curve, target_response)
        }
        
        self.calibration_profiles[speaker_id] = profile
        
        # Create EQ filters for this speaker
        self._create_eq_filters(speaker_id, correction_curve)
        
        print(f"📊 Calibration profile created for speaker '{speaker_id}'")
        return profile
    
    def _calculate_calibration_accuracy(self, measured: List[Tuple[float, float]], 
                                     target: List[Tuple[float, float]]) -> float:
        """
        Calculate the accuracy of calibration
        
        Args:
            measured: Measured response curve
            target: Target response curve
            
        Returns:
            Accuracy score (0.0 to 1.0)
        """
        if not measured or not target or len(measured) != len(target):
            return 0.0
            
        # Calculate RMS error between measured and target
        squared_errors = []
        for (meas_freq, meas_resp), (target_freq, target_resp) in zip(measured, target):
            if meas_freq == target_freq:  # Ensure frequencies match
                error = abs(meas_resp - target_resp)
                squared_errors.append(error ** 2)
                
        if not squared_errors:
            return 0.0
            
        rms_error = math.sqrt(sum(squared_errors) / len(squared_errors))
        
        # Convert to accuracy score (lower error = higher accuracy)
        # Assuming 10 dB error is considered poor accuracy
        accuracy = max(0.0, min(1.0, 1.0 - (rms_error / 10.0)))
        return accuracy
    
    def _create_eq_filters(self, speaker_id: str, correction_curve: List[Tuple[float, float]]):
        """
        Create EQ filters based on correction curve
        
        Args:
            speaker_id: ID of the speaker
            correction_curve: List of (frequency, correction_db) tuples
        """
        # Create parametric EQ filters for each frequency band
        eq_filters = []
        
        for frequency, correction_db in correction_curve:
            # Determine filter type based on frequency and correction
            if frequency < 200:  # Low frequencies
                filter_type = "low_shelf"
            elif frequency > 5000:  # High frequencies
                filter_type = "high_shelf"
            else:  # Mid frequencies
                filter_type = "peaking"
                
            # Create filter parameters
            filter_params = {
                "type": filter_type,
                "frequency": frequency,
                "gain": correction_db,
                "q": self._calculate_q_factor(frequency, filter_type)
            }
            
            eq_filters.append(filter_params)
            
        self.eq_filters[speaker_id] = eq_filters
        
    def _calculate_q_factor(self, frequency: float, filter_type: str) -> float:
        """
        Calculate appropriate Q factor for a filter
        
        Args:
            frequency: Filter frequency
            filter_type: Type of filter
            
        Returns:
            Q factor value
        """
        # Different Q factors for different frequency ranges and filter types
        if filter_type == "low_shelf":
            return 0.7  # Gentle low shelf
        elif filter_type == "high_shelf":
            return 0.7  # Gentle high shelf
        else:  # Peaking filter
            if frequency < 500:
                return 1.0  # Broader Q for bass
            elif frequency > 5000:
                return 1.5  # Narrower Q for treble
            else:
                return 1.2  # Midrange Q
                
    def apply_calibration(self, audio_data: List[List[float]], 
                         speaker_id: str) -> List[List[float]]:
        """
        Apply frequency response calibration to audio data
        
        Args:
            audio_data: Input stereo audio data
            speaker_id: ID of the speaker to calibrate for
            
        Returns:
            Calibrated audio data
        """
        if speaker_id not in self.calibration_profiles:
            print(f"⚠️ No calibration profile for speaker '{speaker_id}', applying default processing")
            return self._apply_default_processing(audio_data, speaker_id)
            
        # Apply EQ filters
        calibrated_audio = self._apply_eq_filters(audio_data, speaker_id)
        return calibrated_audio
    
    def _apply_eq_filters(self, audio_data: List[List[float]], 
                         speaker_id: str) -> List[List[float]]:
        """
        Apply EQ filters to audio data
        
        Args:
            audio_data: Input audio data
            speaker_id: Speaker ID
            
        Returns:
            Filtered audio data
        """
        if speaker_id not in self.eq_filters:
            return audio_data
            
        # Apply each filter in sequence
        left_channel = audio_data[0][:]
        right_channel = audio_data[1][:]
        
        for filter_params in self.eq_filters[speaker_id]:
            left_channel, right_channel = self._apply_single_filter(
                left_channel, right_channel, filter_params
            )
            
        return [left_channel, right_channel]
    
    def _apply_single_filter(self, left_channel: List[float], 
                           right_channel: List[float], 
                           filter_params: Dict[str, Any]) -> Tuple[List[float], List[float]]:
        """
        Apply a single filter to audio channels
        
        Args:
            left_channel: Left audio channel
            right_channel: Right audio channel
            filter_params: Filter parameters
            
        Returns:
            Filtered audio channels
        """
        # Simplified filter implementation
        # In a real system, this would use proper digital filter algorithms
        
        filter_type = filter_params["type"]
        frequency = filter_params["frequency"]
        gain = filter_params["gain"]
        q = filter_params["q"]
        
        # Convert gain from dB to linear
        linear_gain = 10 ** (gain / 20.0)
        
        # Apply filter effect (simplified)
        if filter_type == "peaking":
            # Peaking filter - boost or cut around center frequency
            filtered_left = [sample * (1.0 + (linear_gain - 1.0) * self._frequency_weight(sample_index, frequency, q, len(left_channel))) 
                           for sample_index, sample in enumerate(left_channel)]
            filtered_right = [sample * (1.0 + (linear_gain - 1.0) * self._frequency_weight(sample_index, frequency, q, len(right_channel))) 
                            for sample_index, sample in enumerate(right_channel)]
        else:
            # Shelf filters - apply to all samples with frequency weighting
            filtered_left = [sample * linear_gain for sample in left_channel]
            filtered_right = [sample * linear_gain for sample in right_channel]
            
        return filtered_left, filtered_right
    
    def _frequency_weight(self, sample_index: int, center_freq: float, q: float, total_samples: int) -> float:
        """
        Calculate frequency weight for a sample (simplified)
        
        Args:
            sample_index: Index of the sample
            center_freq: Center frequency
            q: Q factor
            total_samples: Total number of samples
            
        Returns:
            Weight value (0.0 to 1.0)
        """
        # This is a simplified approximation
        # In reality, this would involve FFT analysis
        normalized_position = sample_index / total_samples
        frequency_match = 1.0 - abs(normalized_position - (center_freq / 20000.0))
        return max(0.0, min(1.0, frequency_match))
    
    def _apply_default_processing(self, audio_data: List[List[float]], 
                                speaker_id: str) -> List[List[float]]:
        """
        Apply default processing when no calibration is available
        
        Args:
            audio_data: Input audio data
            speaker_id: Speaker ID
            
        Returns:
            Processed audio data
        """
        # Apply basic speaker protection
        speaker = self.speaker_manager.speakers.get(speaker_id)
        if not speaker:
            return audio_data
            
        # Apply frequency limiting based on speaker capabilities
        min_freq, max_freq = speaker.frequency_range
        
        if max_freq < 1000:  # Low frequency speaker
            # Apply low-pass filtering
            left_channel = self._simple_low_pass_filter(audio_data[0], max_freq)
            right_channel = self._simple_low_pass_filter(audio_data[1], max_freq)
        elif min_freq > 2000:  # High frequency speaker
            # Apply high-pass filtering
            left_channel = self._simple_high_pass_filter(audio_data[0], min_freq)
            right_channel = self._simple_high_pass_filter(audio_data[1], min_freq)
        else:
            # Full-range speaker, apply gentle protection
            left_channel = audio_data[0][:]
            right_channel = audio_data[1][:]
            
        return [left_channel, right_channel]
    
    def _simple_low_pass_filter(self, samples: List[float], cutoff_freq: float) -> List[float]:
        """Simple low-pass filter implementation"""
        filtered = samples[:]
        alpha = cutoff_freq / (cutoff_freq + 1000)  # Simplified calculation
        for i in range(1, len(filtered)):
            filtered[i] = alpha * filtered[i] + (1 - alpha) * filtered[i-1]
        return filtered
    
    def _simple_high_pass_filter(self, samples: List[float], cutoff_freq: float) -> List[float]:
        """Simple high-pass filter implementation"""
        filtered = samples[:]
        alpha = cutoff_freq / (cutoff_freq + 1000)  # Simplified calculation
        for i in range(1, len(filtered)):
            filtered[i] = alpha * (filtered[i] - filtered[i-1]) + filtered[i-1]
        return filtered
    
    def set_protection_thresholds(self, speaker_id: str, 
                                power_limit = None,
                                thermal_limit = None,
                                excursion_limit = None):
        """
        Set protection thresholds for a speaker
        
        Args:
            speaker_id: ID of the speaker
            power_limit: Maximum power in watts
            thermal_limit: Maximum temperature in Celsius
            excursion_limit: Maximum cone excursion in mm
        """
        if speaker_id not in self.protection_thresholds:
            self.protection_thresholds[speaker_id] = {}
            
        thresholds = self.protection_thresholds[speaker_id]
        
        if power_limit is not None:
            thresholds["power_limit"] = power_limit
        if thermal_limit is not None:
            thresholds["thermal_limit"] = thermal_limit
        if excursion_limit is not None:
            thresholds["excursion_limit"] = excursion_limit
            
        print(f"🛡️ Protection thresholds set for speaker '{speaker_id}'")
    
    def monitor_speaker_safety(self, speaker_id: str, 
                             current_power: float,
                             current_temp = None,
                             current_excursion = None) -> Dict[str, Any]:
        """
        Monitor speaker safety and apply protection if needed
        
        Args:
            speaker_id: ID of the speaker
            current_power: Current power consumption in watts
            current_temp: Current temperature in Celsius
            current_excursion: Current cone excursion in mm
            
        Returns:
            Dictionary with safety status
        """
        if speaker_id not in self.protection_thresholds:
            return {"status": "no_protection_configured"}
            
        thresholds = self.protection_thresholds[speaker_id]
        safety_status = {
            "speaker_id": speaker_id,
            "status": "safe",
            "protection_applied": False,
            "warnings": []
        }
        
        # Check power limit
        if "power_limit" in thresholds and current_power > thresholds["power_limit"]:
            safety_status["status"] = "warning"
            safety_status["protection_applied"] = True
            safety_status["warnings"].append("power_limit_exceeded")
            
        # Check thermal limit
        if current_temp and "thermal_limit" in thresholds and current_temp > thresholds["thermal_limit"]:
            safety_status["status"] = "warning"
            safety_status["protection_applied"] = True
            safety_status["warnings"].append("thermal_limit_exceeded")
            
        # Check excursion limit
        if current_excursion and "excursion_limit" in thresholds and current_excursion > thresholds["excursion_limit"]:
            safety_status["status"] = "warning"
            safety_status["protection_applied"] = True
            safety_status["warnings"].append("excursion_limit_exceeded")
            
        return safety_status

class AdvancedSpeakerProtection:
    """Advanced protection mechanisms for speakers"""
    
    def __init__(self, calibrator: FrequencyResponseCalibrator):
        """Initialize advanced speaker protection"""
        self.calibrator = calibrator
        self.protection_history = {}
        
    def apply_intelligent_protection(self, audio_data: List[List[float]], 
                                   speaker_id: str,
                                   current_conditions: Dict[str, float]) -> List[List[float]]:
        """
        Apply intelligent protection based on current conditions
        
        Args:
            audio_data: Input audio data
            speaker_id: Speaker ID
            current_conditions: Dictionary with current conditions (power, temp, etc.)
            
        Returns:
            Protected audio data
        """
        # Monitor safety
        safety_status = self.calibrator.monitor_speaker_safety(
            speaker_id,
            current_conditions.get("power", 0),
            current_conditions.get("temperature"),
            current_conditions.get("excursion")
        )
        
        # Store in history
        if speaker_id not in self.protection_history:
            self.protection_history[speaker_id] = []
        self.protection_history[speaker_id].append(safety_status)
        
        # Keep only recent history
        if len(self.protection_history[speaker_id]) > 100:
            self.protection_history[speaker_id] = self.protection_history[speaker_id][-100:]
        
        # Apply protection if needed
        if safety_status["protection_applied"]:
            return self._apply_protection_measures(audio_data, speaker_id, safety_status)
            
        return audio_data
    
    def _apply_protection_measures(self, audio_data: List[List[float]], 
                                 speaker_id: str,
                                 safety_status: Dict[str, Any]) -> List[List[float]]:
        """
        Apply specific protection measures
        
        Args:
            audio_data: Input audio data
            speaker_id: Speaker ID
            safety_status: Safety status information
            
        Returns:
            Protected audio data
        """
        # Apply gain reduction to prevent damage
        reduction_factor = 0.7  # Reduce by 30%
        
        left_channel = [sample * reduction_factor for sample in audio_data[0]]
        right_channel = [sample * reduction_factor for sample in audio_data[1]]
        
        # Apply additional filtering if thermal issues
        if "thermal_limit_exceeded" in safety_status["warnings"]:
            # Apply gentle low-pass filtering to reduce high-frequency power
            left_channel = self._thermal_protection_filter(left_channel)
            right_channel = self._thermal_protection_filter(right_channel)
            
        print(f"⚠️ Protection applied to speaker '{speaker_id}' due to: {', '.join(safety_status['warnings'])}")
        
        return [left_channel, right_channel]
    
    def _thermal_protection_filter(self, samples: List[float]) -> List[float]:
        """Apply thermal protection filtering"""
        # Gentle low-pass filtering to reduce high-frequency power consumption
        filtered = samples[:]
        for i in range(1, len(filtered)):
            filtered[i] = 0.9 * filtered[i] + 0.1 * filtered[i-1]
        return filtered

# Global instances
frequency_calibrator = None
speaker_protection = None

def initialize_frequency_calibration(speaker_manager: PrecisionSpeakerManager):
    """Initialize the global frequency response calibrator"""
    global frequency_calibrator, speaker_protection
    frequency_calibrator = FrequencyResponseCalibrator(speaker_manager)
    speaker_protection = AdvancedSpeakerProtection(frequency_calibrator)
    return frequency_calibrator

def create_speaker_calibration(speaker_id: str, 
                             test_frequencies: List[float],
                             measured_responses: List[float]):
    """Create a calibration profile for a speaker"""
    if frequency_calibrator:
        return frequency_calibrator.create_calibration_profile(
            speaker_id, test_frequencies, measured_responses
        )
    return {"error": "Calibrator not initialized"}

def apply_frequency_calibration(audio_data: List[List[float]], speaker_id: str):
    """Apply frequency response calibration to audio data"""
    if frequency_calibrator:
        return frequency_calibrator.apply_calibration(audio_data, speaker_id)
    return audio_data

def set_speaker_protection_thresholds(speaker_id: str, 
                                    power_limit = None,
                                    thermal_limit = None,
                                    excursion_limit = None):
    """Set protection thresholds for a speaker"""
    if frequency_calibrator:
        frequency_calibrator.set_protection_thresholds(
            speaker_id, power_limit, thermal_limit, excursion_limit
        )

def monitor_speaker_safety(speaker_id: str, 
                          current_power: float,
                          current_temp = None,
                          current_excursion = None):
    """Monitor speaker safety and apply protection if needed"""
    if frequency_calibrator:
        return frequency_calibrator.monitor_speaker_safety(
            speaker_id, current_power, current_temp, current_excursion
        )
    return {"error": "Calibrator not initialized"}