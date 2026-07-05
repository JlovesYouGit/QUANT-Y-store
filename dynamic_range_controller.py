"""
Dynamic Range Controller and Limiter System
Advanced system for controlling audio dynamic range and preventing clipping
"""

import math
from typing import List, Tuple, Dict, Any
from array import array

class DynamicRangeController:
    """Controls audio dynamic range and prevents clipping through compression and limiting"""
    
    def __init__(self):
        """Initialize the dynamic range controller"""
        self.compression_settings = {
            "threshold": -20.0,  # dB
            "ratio": 4.0,        # 4:1 compression ratio
            "attack": 0.01,      # 10ms attack time
            "release": 0.1,      # 100ms release time
            "knee": 5.0,         # 5dB soft knee
            "makeup_gain": 0.0   # dB makeup gain
        }
        self.limiter_settings = {
            "threshold": -0.5,   # dB (just below 0dBFS)
            "attack": 0.001,     # 1ms attack
            "release": 0.05,     # 50ms release
            "lookahead": 0.005   # 5ms lookahead
        }
        self.sample_rate = 44100
        self.envelope_followers = {}
        self.gain_history = []
        
    def set_compression_parameters(self, threshold = None, ratio = None,
                                 attack = None, release = None,
                                 knee = None, makeup_gain = None):
        """
        Set compression parameters
        
        Args:
            threshold: Compression threshold in dB
            ratio: Compression ratio (e.g., 4.0 for 4:1)
            attack: Attack time in seconds
            release: Release time in seconds
            knee: Soft knee width in dB
            makeup_gain: Makeup gain in dB
        """
        if threshold is not None:
            self.compression_settings["threshold"] = threshold
        if ratio is not None:
            self.compression_settings["ratio"] = ratio
        if attack is not None:
            self.compression_settings["attack"] = attack
        if release is not None:
            self.compression_settings["release"] = release
        if knee is not None:
            self.compression_settings["knee"] = knee
        if makeup_gain is not None:
            self.compression_settings["makeup_gain"] = makeup_gain
            
        print("🎚️ Compression parameters updated")
        
    def set_limiting_parameters(self, threshold = None, attack = None,
                              release = None, lookahead = None):
        """
        Set limiting parameters
        
        Args:
            threshold: Limiter threshold in dB
            attack: Attack time in seconds
            release: Release time in seconds
            lookahead: Lookahead time in seconds
        """
        if threshold is not None:
            self.limiter_settings["threshold"] = threshold
        if attack is not None:
            self.limiter_settings["attack"] = attack
        if release is not None:
            self.limiter_settings["release"] = release
        if lookahead is not None:
            self.limiter_settings["lookahead"] = lookahead
            
        print("🎚️ Limiter parameters updated")
    
    def apply_compression(self, audio_data: List[List[float]], 
                         channel_id: str = "default") -> List[List[float]]:
        """
        Apply dynamic range compression to audio data
        
        Args:
            audio_data: Input stereo audio data
            channel_id: Identifier for envelope follower
            
        Returns:
            Compressed audio data
        """
        if len(audio_data) < 2:
            return audio_data
            
        # Initialize envelope follower for this channel if needed
        if channel_id not in self.envelope_followers:
            self.envelope_followers[channel_id] = {
                "envelope": 0.0,
                "gain": 1.0
            }
            
        envelope_state = self.envelope_followers[channel_id]
        
        # Process each channel
        compressed_channels = []
        for channel in audio_data:
            compressed_channel = self._compress_channel(channel, envelope_state)
            compressed_channels.append(compressed_channel)
            
        return compressed_channels
    
    def _compress_channel(self, samples: List[float], 
                         envelope_state: Dict[str, float]) -> List[float]:
        """
        Compress a single audio channel
        
        Args:
            samples: Audio samples
            envelope_state: Envelope follower state
            
        Returns:
            Compressed audio samples
        """
        compressed_samples = []
        envelope = envelope_state["envelope"]
        gain_linear = envelope_state["gain"]  # Initialize with previous gain
        
        # Convert settings to linear values
        threshold_linear = 10 ** (self.compression_settings["threshold"] / 20.0)
        attack_coeff = math.exp(-1.0 / (self.sample_rate * self.compression_settings["attack"]))
        release_coeff = math.exp(-1.0 / (self.sample_rate * self.compression_settings["release"]))
        
        for sample in samples:
            # Calculate instantaneous level
            instant_level = abs(sample)
            
            # Update envelope follower
            if instant_level > envelope:
                # Attack phase
                envelope = instant_level * (1 - attack_coeff) + envelope * attack_coeff
            else:
                # Release phase
                envelope = instant_level * (1 - release_coeff) + envelope * release_coeff
                
            # Convert envelope to dB
            if envelope > 0:
                envelope_db = 20 * math.log10(envelope)
            else:
                gain_linear = 1.0  # Default gain
            envelope_db = -96.0  # Very low level
                
            # Calculate gain reduction
            gain_db = self._calculate_gain_reduction(envelope_db)
            gain_linear = 10 ** (gain_db / 20.0)
            
            # Apply makeup gain
            makeup_linear = 10 ** (self.compression_settings["makeup_gain"] / 20.0)
            
            # Apply compression
            compressed_sample = sample * gain_linear * makeup_linear
            compressed_samples.append(compressed_sample)
            
        # Update envelope state
        envelope_state["envelope"] = envelope
        envelope_state["gain"] = gain_linear
        
        return compressed_samples
    
    def _calculate_gain_reduction(self, input_level: float) -> float:
        """
        Calculate gain reduction based on input level and compression settings
        
        Args:
            input_level: Input level in dB
            
        Returns:
            Gain reduction in dB
        """
        threshold = self.compression_settings["threshold"]
        ratio = self.compression_settings["ratio"]
        knee = self.compression_settings["knee"]
        
        # Calculate how far above threshold we are
        over_threshold = input_level - threshold
        
        if over_threshold <= 0:
            # Below threshold, no compression
            return 0.0
            
        if over_threshold < knee:
            # Within soft knee, apply gradual compression
            knee_ratio = 1.0 + (ratio - 1.0) * (over_threshold / knee) ** 2
            gain_reduction = -over_threshold * (knee_ratio - 1.0) / knee_ratio
        else:
            # Hard compression above knee
            gain_reduction = -over_threshold * (ratio - 1.0) / ratio
            
        return gain_reduction
    
    def apply_limiting(self, audio_data: List[List[float]]) -> List[List[float]]:
        """
        Apply brickwall limiting to prevent clipping
        
        Args:
            audio_data: Input stereo audio data
            
        Returns:
            Limited audio data
        """
        if len(audio_data) < 2:
            return audio_data
            
        # Apply lookahead if enabled
        if self.limiter_settings["lookahead"] > 0:
            audio_data = self._apply_lookahead(audio_data)
            
        # Process each channel
        limited_channels = []
        for channel in audio_data:
            limited_channel = self._limit_channel(channel)
            limited_channels.append(limited_channel)
            
        return limited_channels
    
    def _apply_lookahead(self, audio_data: List[List[float]]) -> List[List[float]]:
        """
        Apply lookahead processing to improve limiting response
        
        Args:
            audio_data: Input audio data
            
        Returns:
            Audio data with lookahead applied
        """
        # Calculate lookahead buffer size
        lookahead_samples = int(self.sample_rate * self.limiter_settings["lookahead"])
        if lookahead_samples <= 0:
            return audio_data
            
        # Apply delay to audio and advance gain calculation
        delayed_channels = []
        for channel in audio_data:
            # Simple delay implementation
            delayed_channel = [0.0] * lookahead_samples + channel[:-lookahead_samples] if len(channel) > lookahead_samples else [0.0] * len(channel)
            delayed_channels.append(delayed_channel)
            
        return delayed_channels
    
    def _limit_channel(self, samples: List[float]) -> List[float]:
        """
        Apply limiting to a single audio channel
        
        Args:
            samples: Audio samples
            
        Returns:
            Limited audio samples
        """
        limited_samples = []
        
        # Convert threshold to linear
        threshold_linear = 10 ** (self.limiter_settings["threshold"] / 20.0)
        
        # Calculate coefficients
        attack_coeff = math.exp(-1.0 / (self.sample_rate * self.limiter_settings["attack"]))
        release_coeff = math.exp(-1.0 / (self.sample_rate * self.limiter_settings["release"]))
        
        # Initialize gain reduction
        gain_reduction = 1.0
        
        for sample in samples:
            # Calculate sample level
            sample_level = abs(sample)
            
            # Calculate required gain reduction
            if sample_level > threshold_linear:
                required_gain = threshold_linear / sample_level
            else:
                required_gain = 1.0
                
            # Apply attack/release envelope to gain reduction
            if required_gain < gain_reduction:
                # Attack - reduce gain quickly
                gain_reduction = required_gain * (1 - attack_coeff) + gain_reduction * attack_coeff
            else:
                # Release - increase gain slowly
                gain_reduction = required_gain * (1 - release_coeff) + gain_reduction * release_coeff
                
            # Apply limiting
            limited_sample = sample * gain_reduction
            limited_samples.append(limited_sample)
            
        return limited_samples
    
    def apply_adaptive_compression(self, audio_data: List[List[float]], 
                                 analysis_window: int = 1024) -> List[List[float]]:
        """
        Apply adaptive compression based on content analysis
        
        Args:
            audio_data: Input stereo audio data
            analysis_window: Number of samples to analyze for content characteristics
            
        Returns:
            Adaptively compressed audio data
        """
        if len(audio_data) < 2:
            return audio_data
            
        # Analyze content characteristics
        content_analysis = self._analyze_content_characteristics(audio_data, analysis_window)
        
        # Adjust compression settings based on content
        self._adjust_compression_for_content(content_analysis)
        
        # Apply compression with adjusted settings
        return self.apply_compression(audio_data)
    
    def _analyze_content_characteristics(self, audio_data: List[List[float]], 
                                      window_size: int) -> Dict[str, float]:
        """
        Analyze audio content characteristics
        
        Args:
            audio_data: Input audio data
            window_size: Analysis window size
            
        Returns:
            Dictionary with content characteristics
        """
        # Combine channels for analysis
        combined_samples = []
        for i in range(min(len(audio_data[0]), len(audio_data[1]))):
            combined_samples.append((audio_data[0][i] + audio_data[1][i]) / 2)
            
        # Take analysis window
        analysis_samples = combined_samples[:min(window_size, len(combined_samples))]
        
        if not analysis_samples:
            return {"dynamic_range": 0.0, "peak_to_average": 1.0, "transient_content": 0.0}
            
        # Calculate peak and RMS levels
        peak_level = max(abs(sample) for sample in analysis_samples)
        rms_level = math.sqrt(sum(sample ** 2 for sample in analysis_samples) / len(analysis_samples))
        
        # Calculate dynamic range
        if rms_level > 0:
            dynamic_range = 20 * math.log10(peak_level / rms_level)
        else:
            dynamic_range = 0.0
            
        # Calculate peak-to-average ratio
        peak_to_average = peak_level / max(rms_level, 1e-10)
        
        # Estimate transient content (simplified)
        transient_content = self._estimate_transient_content(analysis_samples)
        
        return {
            "dynamic_range": dynamic_range,
            "peak_to_average": peak_to_average,
            "transient_content": transient_content
        }
    
    def _estimate_transient_content(self, samples: List[float]) -> float:
        """
        Estimate the amount of transient content in audio
        
        Args:
            samples: Audio samples
            
        Returns:
            Transient content estimate (0.0 to 1.0)
        """
        if len(samples) < 2:
            return 0.0
            
        # Calculate rate of change as indicator of transients
        changes = [abs(samples[i] - samples[i-1]) for i in range(1, len(samples))]
        avg_change = sum(changes) / len(changes)
        
        # Normalize (simplified)
        transient_estimate = min(1.0, avg_change * 100)
        return transient_estimate
    
    def _adjust_compression_for_content(self, content_analysis: Dict[str, float]):
        """
        Adjust compression settings based on content analysis
        
        Args:
            content_analysis: Content characteristics dictionary
        """
        dynamic_range = content_analysis["dynamic_range"]
        transient_content = content_analysis["transient_content"]
        
        # Adjust compression ratio based on dynamic range
        if dynamic_range > 20:  # High dynamic range content
            new_ratio = max(2.0, self.compression_settings["ratio"] * 0.8)
        elif dynamic_range < 10:  # Low dynamic range content
            new_ratio = min(8.0, self.compression_settings["ratio"] * 1.2)
        else:
            new_ratio = self.compression_settings["ratio"]
            
        # Adjust attack time based on transient content
        if transient_content > 0.5:  # Transient-rich content
            new_attack = max(0.001, self.compression_settings["attack"] * 0.5)  # Faster attack
        else:
            new_attack = min(0.05, self.compression_settings["attack"] * 1.5)  # Slower attack
            
        # Update settings
        self.compression_settings["ratio"] = new_ratio
        self.compression_settings["attack"] = new_attack
        
    def get_compression_metering(self) -> Dict[str, float]:
        """
        Get current compression metering information
        
        Returns:
            Dictionary with metering data
        """
        # Simplified metering - in a real implementation, this would track actual values
        return {
            "input_level": -12.0,  # dB
            "output_level": -10.0,  # dB
            "gain_reduction": -2.0,  # dB
            "compression_ratio": self.compression_settings["ratio"]
        }

class MultibandCompressor:
    """Multiband compressor for precise frequency-dependent dynamic control"""
    
    def __init__(self, dynamic_controller: DynamicRangeController):
        """Initialize multiband compressor"""
        self.dynamic_controller = dynamic_controller
        self.crossover_frequencies = [120.0, 1200.0, 6000.0]  # Hz
        self.band_settings = {
            "low": {"threshold": -25.0, "ratio": 3.0, "attack": 0.02, "release": 0.2},
            "low_mid": {"threshold": -22.0, "ratio": 2.5, "attack": 0.015, "release": 0.15},
            "high_mid": {"threshold": -20.0, "ratio": 2.0, "attack": 0.01, "release": 0.1},
            "high": {"threshold": -18.0, "ratio": 1.8, "attack": 0.008, "release": 0.08}
        }
        
    def apply_multiband_compression(self, audio_data: List[List[float]]) -> List[List[float]]:
        """
        Apply multiband compression to audio data
        
        Args:
            audio_data: Input stereo audio data
            
        Returns:
            Multiband compressed audio data
        """
        # This is a simplified implementation
        # A real multiband compressor would split the signal into bands,
        # process each band separately, then recombine
        
        # For now, we'll apply different compression settings to different
        # frequency ranges by analyzing the content
        
        # Apply adaptive compression with modified settings for different bands
        return self.dynamic_controller.apply_adaptive_compression(audio_data)

# Global instances
dynamic_range_controller = DynamicRangeController()
multiband_compressor = None

def initialize_dynamic_range_control():
    """Initialize the global dynamic range controller"""
    global dynamic_range_controller, multiband_compressor
    dynamic_range_controller = DynamicRangeController()
    multiband_compressor = MultibandCompressor(dynamic_range_controller)
    return dynamic_range_controller

def apply_audio_compression(audio_data: List[List[float]], channel_id: str = "default"):
    """Apply dynamic range compression to audio data"""
    return dynamic_range_controller.apply_compression(audio_data, channel_id)

def apply_audio_limiting(audio_data: List[List[float]]):
    """Apply brickwall limiting to prevent clipping"""
    return dynamic_range_controller.apply_limiting(audio_data)

def apply_adaptive_compression(audio_data: List[List[float]]):
    """Apply adaptive compression based on content analysis"""
    return dynamic_range_controller.apply_adaptive_compression(audio_data)

def set_compression_parameters(threshold = None, ratio = None,
                             attack = None, release = None,
                             knee = None, makeup_gain = None):
    """Set compression parameters"""
    dynamic_range_controller.set_compression_parameters(
        threshold, ratio, attack, release, knee, makeup_gain
    )

def set_limiting_parameters(threshold = None, attack = None,
                          release = None, lookahead = None):
    """Set limiting parameters"""
    dynamic_range_controller.set_limiting_parameters(
        threshold, attack, release, lookahead
    )

def get_compression_metering():
    """Get current compression metering information"""
    return dynamic_range_controller.get_compression_metering()