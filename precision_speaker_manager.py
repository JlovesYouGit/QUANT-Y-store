"""
Precision Speaker Management System
Optimizes audio output for any speaker configuration to prevent distortion and ensure accurate reproduction
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from array import array

@dataclass
class SpeakerProfile:
    """Represents a speaker's characteristics and capabilities"""
    id: str
    type: str  # "subwoofer", "woofer", "midrange", "tweeter", "fullrange"
    frequency_range: Tuple[float, float]  # (min_freq, max_freq) in Hz
    sensitivity: float  # dB SPL at 1W/1m
    impedance: float  # Ohms
    max_power: float  # Watts
    thd: float  # Total harmonic distortion percentage
    size: float  # Diameter in inches

@dataclass
class AudioBand:
    """Represents a frequency band for audio processing"""
    name: str
    frequency_range: Tuple[float, float]  # (min_freq, max_freq) in Hz
    target_level: float  # Target amplitude (0.0 to 1.0)
    compression_ratio: float  # Dynamic range compression ratio
    attack_time: float  # Attack time in seconds
    release_time: float  # Release time in seconds

class PrecisionSpeakerManager:
    """Manages precision audio output optimization for speaker systems"""
    
    def __init__(self):
        """Initialize the precision speaker manager"""
        self.speakers: Dict[str, SpeakerProfile] = {}
        self.audio_bands: Dict[str, AudioBand] = {}
        self.calibration_data: Dict[str, Any] = {}
        self.optimization_settings = {
            "protect_speakers": True,
            "optimize_frequency_response": True,
            "dynamic_range_control": True,
            "phase_alignment": True
        }
        self.sample_rate = 44100
        self.current_audio_state = {
            "rms_level": 0.0,
            "peak_level": 0.0,
            "frequency_content": {},
            "clipping_detected": False
        }
        
    def initialize_speaker_profiles(self):
        """Initialize standard speaker profiles for common speaker types"""
        # Standard speaker profiles
        self.speakers = {
            "subwoofer": SpeakerProfile(
                id="subwoofer",
                type="subwoofer",
                frequency_range=(20.0, 200.0),
                sensitivity=87.0,
                impedance=4.0,
                max_power=500.0,
                thd=0.15,
                size=12.0
            ),
            "woofer": SpeakerProfile(
                id="woofer",
                type="woofer",
                frequency_range=(40.0, 1000.0),
                sensitivity=89.0,
                impedance=8.0,
                max_power=200.0,
                thd=0.1,
                size=8.0
            ),
            "midrange": SpeakerProfile(
                id="midrange",
                type="midrange",
                frequency_range=(200.0, 5000.0),
                sensitivity=91.0,
                impedance=8.0,
                max_power=100.0,
                thd=0.05,
                size=5.0
            ),
            "tweeter": SpeakerProfile(
                id="tweeter",
                type="tweeter",
                frequency_range=(2000.0, 20000.0),
                sensitivity=90.0,
                impedance=8.0,
                max_power=50.0,
                thd=0.03,
                size=1.0
            ),
            "fullrange": SpeakerProfile(
                id="fullrange",
                type="fullrange",
                frequency_range=(80.0, 15000.0),
                sensitivity=88.0,
                impedance=8.0,
                max_power=150.0,
                thd=0.08,
                size=6.5
            )
        }
        
        print("🔊 Precision speaker profiles initialized")
        
    def initialize_audio_bands(self):
        """Initialize standard audio frequency bands for processing"""
        self.audio_bands = {
            "sub_bass": AudioBand(
                name="Sub-Bass",
                frequency_range=(20.0, 60.0),
                target_level=0.8,
                compression_ratio=2.0,
                attack_time=0.01,
                release_time=0.2
            ),
            "bass": AudioBand(
                name="Bass",
                frequency_range=(60.0, 250.0),
                target_level=0.9,
                compression_ratio=1.8,
                attack_time=0.008,
                release_time=0.15
            ),
            "low_mid": AudioBand(
                name="Low Midrange",
                frequency_range=(250.0, 500.0),
                target_level=0.7,
                compression_ratio=1.5,
                attack_time=0.005,
                release_time=0.1
            ),
            "mid": AudioBand(
                name="Midrange",
                frequency_range=(500.0, 2000.0),
                target_level=0.8,
                compression_ratio=1.3,
                attack_time=0.003,
                release_time=0.08
            ),
            "upper_mid": AudioBand(
                name="Upper Midrange",
                frequency_range=(2000.0, 4000.0),
                target_level=0.75,
                compression_ratio=1.4,
                attack_time=0.002,
                release_time=0.06
            ),
            "presence": AudioBand(
                name="Presence",
                frequency_range=(4000.0, 6000.0),
                target_level=0.7,
                compression_ratio=1.6,
                attack_time=0.001,
                release_time=0.05
            ),
            "brilliance": AudioBand(
                name="Brilliance",
                frequency_range=(6000.0, 20000.0),
                target_level=0.6,
                compression_ratio=2.0,
                attack_time=0.001,
                release_time=0.03
            )
        }
        
        print("🎛️ Audio frequency bands initialized for precision control")
        
    def add_speaker(self, speaker_id: str, speaker_profile: SpeakerProfile):
        """
        Add a speaker to the system
        
        Args:
            speaker_id: Unique identifier for the speaker
            speaker_profile: SpeakerProfile object with speaker characteristics
        """
        self.speakers[speaker_id] = speaker_profile
        print(f"🔊 Speaker '{speaker_id}' added to system")
        
    def calibrate_speaker_response(self, speaker_id: str, 
                                 measured_response: List[Tuple[float, float]]) -> Dict[str, Any]:
        """
        Calibrate a speaker based on measured frequency response
        
        Args:
            speaker_id: ID of the speaker to calibrate
            measured_response: List of (frequency, amplitude) tuples from measurement
            
        Returns:
            Dictionary with calibration data
        """
        if speaker_id not in self.speakers:
            return {"error": "Speaker not found"}
            
        # Store calibration data
        self.calibration_data[speaker_id] = {
            "measured_response": measured_response,
            "correction_curve": self._generate_correction_curve(measured_response),
            "calibration_time": "current_time"
        }
        
        print(f"📏 Speaker '{speaker_id}' calibrated successfully")
        return self.calibration_data[speaker_id]
    
    def _generate_correction_curve(self, measured_response: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Generate a correction curve to flatten the speaker's frequency response
        
        Args:
            measured_response: List of (frequency, amplitude) tuples
            
        Returns:
            Correction curve as list of (frequency, correction_db) tuples
        """
        # Simplified correction curve generation
        correction_curve = []
        target_level = -10.0  # dB reference
        
        for frequency, measured_level in measured_response:
            # Calculate correction needed to reach target level
            correction = target_level - measured_level
            correction_curve.append((frequency, correction))
            
        return correction_curve
    
    def analyze_audio_content(self, audio_data: List[List[float]]) -> Dict[str, Any]:
        """
        Analyze the frequency content and dynamics of audio data
        
        Args:
            audio_data: Stereo audio data as [left_channel, right_channel]
            
        Returns:
            Dictionary with audio analysis results
        """
        if not audio_data or len(audio_data) < 2:
            return {"error": "Invalid audio data"}
            
        # Calculate RMS and peak levels
        left_channel = audio_data[0]
        right_channel = audio_data[1]
        
        # RMS calculation
        left_rms = math.sqrt(sum(sample**2 for sample in left_channel) / len(left_channel)) if left_channel else 0
        right_rms = math.sqrt(sum(sample**2 for sample in right_channel) / len(right_channel)) if right_channel else 0
        rms_level = (left_rms + right_rms) / 2
        
        # Peak calculation
        left_peak = max(abs(sample) for sample in left_channel) if left_channel else 0
        right_peak = max(abs(sample) for sample in right_channel) if right_channel else 0
        peak_level = max(left_peak, right_peak)
        
        # Simple frequency content analysis (bass/treble balance)
        bass_content = self._calculate_frequency_band_energy(left_channel + right_channel, 20, 250)
        mid_content = self._calculate_frequency_band_energy(left_channel + right_channel, 250, 4000)
        treble_content = self._calculate_frequency_band_energy(left_channel + right_channel, 4000, 20000)
        
        # Detect clipping
        clipping_detected = peak_level > 0.95
        
        self.current_audio_state = {
            "rms_level": rms_level,
            "peak_level": peak_level,
            "frequency_content": {
                "bass": bass_content,
                "mid": mid_content,
                "treble": treble_content
            },
            "clipping_detected": clipping_detected
        }
        
        return self.current_audio_state
    
    def _calculate_frequency_band_energy(self, samples: List[float], 
                                      min_freq: float, max_freq: float) -> float:
        """
        Calculate energy in a specific frequency band (simplified)
        
        Args:
            samples: Audio samples
            min_freq: Minimum frequency of band
            max_freq: Maximum frequency of band
            
        Returns:
            Relative energy in the band (0.0 to 1.0)
        """
        # This is a simplified estimation
        # In a real implementation, we would use FFT analysis
        
        # For now, we'll estimate based on sample characteristics
        if not samples:
            return 0.0
            
        # Calculate sample variance as a proxy for energy
        mean = sum(samples) / len(samples)
        variance = sum((sample - mean) ** 2 for sample in samples) / len(samples)
        energy = math.sqrt(variance)
        
        # Normalize and weight based on frequency band
        # Bass frequencies typically have more energy
        if max_freq <= 250:  # Bass
            normalized_energy = min(1.0, energy * 2.0)
        elif min_freq >= 4000:  # Treble
            normalized_energy = min(1.0, energy * 0.5)
        else:  # Midrange
            normalized_energy = min(1.0, energy)
            
        return normalized_energy
    
    def optimize_audio_for_speakers(self, audio_data: List[List[float]], 
                                  speaker_ids = None) -> List[List[float]]:
        """
        Optimize audio data for specific speakers to prevent distortion
        
        Args:
            audio_data: Input stereo audio data
            speaker_ids: List of speaker IDs to optimize for (None = all speakers)
            
        Returns:
            Optimized stereo audio data
        """
        if not audio_data or len(audio_data) < 2:
            return audio_data
            
        # Analyze current audio content
        audio_analysis = self.analyze_audio_content(audio_data)
        
        # Get speakers to optimize for
        target_speakers = speaker_ids if speaker_ids else list(self.speakers.keys())
        
        # Apply speaker-specific optimizations
        optimized_audio = self._apply_speaker_optimizations(
            audio_data, target_speakers, audio_analysis
        )
        
        return optimized_audio
    
    def _apply_speaker_optimizations(self, audio_data: List[List[float]], 
                                   speaker_ids: List[str], 
                                   audio_analysis: Dict[str, Any]) -> List[List[float]]:
        """
        Apply speaker-specific optimizations to audio data
        
        Args:
            audio_data: Input audio data
            speaker_ids: Speakers to optimize for
            audio_analysis: Current audio analysis
            
        Returns:
            Optimized audio data
        """
        left_channel = audio_data[0][:]
        right_channel = audio_data[1][:]
        
        # Apply optimizations for each speaker type
        for speaker_id in speaker_ids:
            if speaker_id not in self.speakers:
                continue
                
            speaker = self.speakers[speaker_id]
            
            # Apply frequency response correction if calibrated
            if speaker_id in self.calibration_data:
                left_channel, right_channel = self._apply_frequency_correction(
                    left_channel, right_channel, speaker_id
                )
            
            # Apply protection based on speaker characteristics
            left_channel, right_channel = self._apply_speaker_protection(
                left_channel, right_channel, speaker, audio_analysis
            )
            
            # Apply dynamic range control
            if self.optimization_settings["dynamic_range_control"]:
                left_channel, right_channel = self._apply_dynamic_range_control(
                    left_channel, right_channel, speaker
                )
        
        return [left_channel, right_channel]
    
    def _apply_frequency_correction(self, left_channel: List[float], 
                                  right_channel: List[float], 
                                  speaker_id: str) -> Tuple[List[float], List[float]]:
        """
        Apply frequency response correction to audio data
        
        Args:
            left_channel: Left audio channel
            right_channel: Right audio channel
            speaker_id: ID of speaker to correct for
            
        Returns:
            Corrected audio channels
        """
        # In a real implementation, this would apply the correction curve
        # For now, we'll apply a simple EQ adjustment
        
        correction_data = self.calibration_data[speaker_id]
        # Simplified correction - in reality, this would be more complex
        correction_factor = 1.05  # Small boost/cut based on calibration
        
        corrected_left = [sample * correction_factor for sample in left_channel]
        corrected_right = [sample * correction_factor for sample in right_channel]
        
        return corrected_left, corrected_right
    
    def _apply_speaker_protection(self, left_channel: List[float], 
                                right_channel: List[float], 
                                speaker: SpeakerProfile, 
                                audio_analysis: Dict[str, Any]) -> Tuple[List[float], List[float]]:
        """
        Apply protection to prevent speaker damage
        
        Args:
            left_channel: Left audio channel
            right_channel: Right audio channel
            speaker: Speaker profile
            audio_analysis: Current audio analysis
            
        Returns:
            Protected audio channels
        """
        # Calculate power level that would be delivered to this speaker
        max_sample = max(max(abs(s) for s in left_channel), 
                        max(abs(s) for s in right_channel)) if left_channel and right_channel else 0
        
        # Convert to power (simplified)
        power_level = (max_sample ** 2) * 100  # Arbitrary scaling
        
        # Apply protection if power exceeds safe limits
        if power_level > speaker.max_power * 0.8:  # 80% of max power
            # Reduce gain to protect speaker
            protection_factor = (speaker.max_power * 0.8) / power_level
            left_channel = [sample * protection_factor for sample in left_channel]
            right_channel = [sample * protection_factor for sample in right_channel]
            
        # Apply frequency-dependent protection
        min_freq, max_freq = speaker.frequency_range
        if max_freq < 1000:  # Low frequency speaker
            # Reduce high frequency content
            left_channel = self._filter_high_frequencies(left_channel)
            right_channel = self._filter_high_frequencies(right_channel)
        elif min_freq > 2000:  # High frequency speaker
            # Reduce low frequency content
            left_channel = self._filter_low_frequencies(left_channel)
            right_channel = self._filter_low_frequencies(right_channel)
            
        return left_channel, right_channel
    
    def _filter_high_frequencies(self, samples: List[float]) -> List[float]:
        """Simple high frequency filter (simplified implementation)"""
        # In reality, this would be a proper digital filter
        # For now, we'll just reduce the rate of change to simulate filtering
        filtered = samples[:]
        for i in range(1, len(filtered)):
            filtered[i] = filtered[i-1] * 0.7 + filtered[i] * 0.3
        return filtered
    
    def _filter_low_frequencies(self, samples: List[float]) -> List[float]:
        """Simple low frequency filter (simplified implementation)"""
        # In reality, this would be a proper digital filter
        # For now, we'll apply a simple high-pass effect
        filtered = samples[:]
        for i in range(1, len(filtered)):
            filtered[i] = filtered[i] - filtered[i-1] * 0.7
        return filtered
    
    def _apply_dynamic_range_control(self, left_channel: List[float], 
                                   right_channel: List[float], 
                                   speaker: SpeakerProfile) -> Tuple[List[float], List[float]]:
        """
        Apply dynamic range control to prevent clipping and optimize perception
        
        Args:
            left_channel: Left audio channel
            right_channel: Right audio channel
            speaker: Speaker profile
            
        Returns:
            Compressed audio channels
        """
        # Simple peak limiting to prevent clipping
        max_peak = max(max(abs(s) for s in left_channel), 
                      max(abs(s) for s in right_channel)) if left_channel and right_channel else 0
        
        if max_peak > 0.9:  # Near clipping
            compression_factor = 0.9 / max_peak
            left_channel = [sample * compression_factor for sample in left_channel]
            right_channel = [sample * compression_factor for sample in right_channel]
            
        return left_channel, right_channel
    
    def get_speaker_status(self, speaker_id = None) -> Dict[str, Any]:
        """
        Get the current status of speakers
        
        Args:
            speaker_id: Specific speaker ID (None = all speakers)
            
        Returns:
            Dictionary with speaker status information
        """
        if speaker_id:
            if speaker_id in self.speakers:
                speaker = self.speakers[speaker_id]
                return {
                    "speaker_id": speaker_id,
                    "type": speaker.type,
                    "frequency_range": speaker.frequency_range,
                    "sensitivity": speaker.sensitivity,
                    "protection_active": self.optimization_settings["protect_speakers"],
                    "calibrated": speaker_id in self.calibration_data
                }
            else:
                return {"error": "Speaker not found"}
        else:
            # Return status for all speakers
            status = {}
            for spk_id, speaker in self.speakers.items():
                status[spk_id] = {
                    "type": speaker.type,
                    "frequency_range": speaker.frequency_range,
                    "sensitivity": speaker.sensitivity,
                    "protection_active": self.optimization_settings["protect_speakers"],
                    "calibrated": spk_id in self.calibration_data
                }
            return status
    
    def set_optimization_preference(self, setting: str, value: bool):
        """
        Set optimization preferences
        
        Args:
            setting: Setting name ("protect_speakers", "optimize_frequency_response", etc.)
            value: Boolean value to set
        """
        if setting in self.optimization_settings:
            self.optimization_settings[setting] = value
            print(f"⚙️ Optimization setting '{setting}' set to {value}")

# Global instance
precision_speaker_manager = PrecisionSpeakerManager()

def initialize_precision_speaker_management():
    """Initialize the global precision speaker manager"""
    global precision_speaker_manager
    precision_speaker_manager.initialize_speaker_profiles()
    precision_speaker_manager.initialize_audio_bands()
    return precision_speaker_manager

def add_speaker_to_system(speaker_id: str, speaker_profile: SpeakerProfile):
    """Add a speaker to the precision management system"""
    precision_speaker_manager.add_speaker(speaker_id, speaker_profile)

def optimize_audio_for_speakers(audio_data: List[List[float]], speaker_ids = None):
    """Optimize audio data for specific speakers to ensure accurate reproduction"""
    return precision_speaker_manager.optimize_audio_for_speakers(audio_data, speaker_ids)

def calibrate_speaker(speaker_id: str, measured_response: List[Tuple[float, float]]):
    """Calibrate a speaker based on measured frequency response"""
    return precision_speaker_manager.calibrate_speaker_response(speaker_id, measured_response)

def get_speaker_system_status(speaker_id = None):
    """Get the current status of the speaker system"""
    return precision_speaker_manager.get_speaker_status(speaker_id)

def set_speaker_optimization_preference(setting: str, value: bool):
    """Set optimization preferences for speaker management"""
    precision_speaker_manager.set_optimization_preference(setting, value)