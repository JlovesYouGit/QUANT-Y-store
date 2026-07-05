"""
Environmental Audio Processor for Quantum Sound Immersion
Enhances quantum audio with natural environmental sound integration
"""

import math
from typing import List, Tuple, Dict, Any
from array import array

class EnvironmentalAudioProcessor:
    """Processes environmental sounds and integrates them with quantum audio for natural 3D immersion"""
    
    def __init__(self):
        """Initialize the environmental audio processor"""
        self.environmental_layers = {}
        self.sound_masks = {}
        self.spatial_filters = {}
        self.ambient_soundscapes = {}
        
    def initialize_environmental_layers(self):
        """Initialize the environmental sound layers for 3D immersion"""
        # Define natural environmental sound layers
        self.environmental_layers = {
            "background_ambient": {
                "type": "ambient",
                "frequency_range": (20, 200),  # Low frequency ambient sounds
                "intensity": 0.3,
                "spatial_spread": 1.0  # Fully distributed
            },
            "midground_texture": {
                "type": "texture",
                "frequency_range": (200, 2000),  # Mid frequency textures
                "intensity": 0.5,
                "spatial_spread": 0.7
            },
            "foreground_detail": {
                "type": "detail",
                "frequency_range": (2000, 20000),  # High frequency details
                "intensity": 0.7,
                "spatial_spread": 0.3
            }
        }
        
        print("🌍 Environmental sound layers initialized for natural 3D immersion")
        
    def add_environmental_sound_layer(self, layer_name: str, sound_type: str, 
                                    frequency_range: Tuple[float, float], 
                                    intensity: float, spatial_spread: float):
        """
        Add a new environmental sound layer
        
        Args:
            layer_name: Name of the sound layer
            sound_type: Type of sound (ambient, texture, detail, etc.)
            frequency_range: Frequency range as (min, max) in Hz
            intensity: Sound intensity (0.0 to 1.0)
            spatial_spread: How spread out the sound is in 3D space (0.0 to 1.0)
        """
        self.environmental_layers[layer_name] = {
            "type": sound_type,
            "frequency_range": frequency_range,
            "intensity": intensity,
            "spatial_spread": spatial_spread
        }
        
    def create_natural_sound_mask(self, environment_type: str) -> Dict[str, Any]:
        """
        Create a sound mask that maps quantum audio to natural environmental counterparts
        
        Args:
            environment_type: Type of environment (forest, ocean, city, space, etc.)
            
        Returns:
            Dictionary of sound mapping parameters
        """
        # Define natural sound mappings for different environments
        environment_mappings = {
            "forest": {
                "quantum_harmonics": "bird_song_harmonics",
                "entanglement_resonance": "wind_through_trees",
                "superposition_texture": "rustling_leaves",
                "measurement_clicks": "dripping_water"
            },
            "ocean": {
                "quantum_harmonics": "wave_harmonics",
                "entanglement_resonance": "deep_ocean_currents",
                "superposition_texture": "surface_ripples",
                "measurement_clicks": "bubble_pops"
            },
            "city": {
                "quantum_harmonics": "traffic_flow_harmonics",
                "entanglement_resonance": "subway_vibrations",
                "superposition_texture": "urban_ambience",
                "measurement_clicks": "keyboard_typing"
            },
            "space": {
                "quantum_harmonics": "cosmic_background_radiation",
                "entanglement_resonance": "solar_wind",
                "superposition_texture": "stellar_dust",
                "measurement_clicks": "pulsar_clicks"
            }
        }
        
        # Create the sound mask
        sound_mask = environment_mappings.get(environment_type, environment_mappings["space"])
        
        # Store for later use
        self.sound_masks[environment_type] = sound_mask
        
        return sound_mask
    
    def apply_spatial_filtering(self, audio_data: List[List[float]], 
                              position: Tuple[float, float, float],
                              layer_name: str) -> List[List[float]]:
        """
        Apply spatial filtering to audio data based on 3D position and layer properties
        
        Args:
            audio_data: Stereo audio data as [left_channel, right_channel]
            position: 3D position (x, y, z)
            layer_name: Name of the environmental layer
            
        Returns:
            Spatially filtered audio data
        """
        if layer_name not in self.environmental_layers:
            return audio_data
            
        layer = self.environmental_layers[layer_name]
        
        # Extract position coordinates
        x, y, z = position
        
        # Apply spatial spread based on layer properties
        spread = layer["spatial_spread"]
        
        # Calculate spatial coefficients
        # X affects left/right balance
        left_coeff = max(0, min(1, (1 - x * spread)))
        right_coeff = max(0, min(1, (1 + x * spread)))
        
        # Y affects front/back positioning (simplified)
        front_coeff = max(0, min(1, (1 + y * spread * 0.5)))
        
        # Z affects vertical positioning and intensity
        vertical_coeff = max(0, min(1, (1 - abs(z) * spread * 0.3)))
        intensity = layer["intensity"] * vertical_coeff
        
        # Apply filtering to audio data
        if len(audio_data) >= 2:
            left_channel = [sample * left_coeff * front_coeff * intensity for sample in audio_data[0]]
            right_channel = [sample * right_coeff * front_coeff * intensity for sample in audio_data[1]]
            return [left_channel, right_channel]
        
        return audio_data
    
    def generate_environmental_ambience(self, environment_type: str, 
                                      duration: float = 5.0) -> List[List[float]]:
        """
        Generate natural environmental ambience for the specified environment
        
        Args:
            environment_type: Type of environment
            duration: Duration in seconds
            
        Returns:
            Stereo audio waveform for environmental ambience
        """
        # Sample rate (simplified for this implementation)
        sample_rate = 44100
        num_samples = int(sample_rate * duration)
        
        # Create base noise for environmental sound
        left_channel = array('d')
        right_channel = array('d')
        
        # Generate different types of environmental sounds based on type
        if environment_type == "forest":
            # Forest ambience - combination of wind and distant bird sounds
            for i in range(num_samples):
                t = i / sample_rate
                # Base wind noise
                wind = math.sin(2 * math.pi * 0.1 * t) * 0.3
                # Bird calls (sporadic high frequencies)
                bird = math.sin(2 * math.pi * (440 + 220 * math.sin(t * 0.5)) * t) * 0.1 if (i % 10000) < 100 else 0
                sample = wind + bird
                left_channel.append(sample)
                right_channel.append(sample * (1 + 0.1 * math.sin(t * 2)))  # Slight stereo variation
                
        elif environment_type == "ocean":
            # Ocean ambience - wave sounds
            for i in range(num_samples):
                t = i / sample_rate
                # Wave sounds with varying frequencies
                wave = math.sin(2 * math.pi * (2 + math.sin(t * 0.2) * 1) * t) * 0.4
                sample = wave
                left_channel.append(sample)
                right_channel.append(sample * (1 + 0.2 * math.sin(t * 1.5)))  # Stereo wave movement
                
        elif environment_type == "city":
            # City ambience - traffic and urban sounds
            for i in range(num_samples):
                t = i / sample_rate
                # Traffic rumble (low frequency)
                traffic = math.sin(2 * math.pi * (1 + 0.5 * math.sin(t * 0.1)) * t) * 0.3
                # Horns and other sounds (sporadic)
                horn = math.sin(2 * math.pi * 880 * t) * 0.1 if (i % 15000) < 200 else 0
                sample = traffic + horn
                left_channel.append(sample)
                right_channel.append(sample * (1 + 0.15 * math.sin(t * 0.8)))
                
        else:  # Space (default)
            # Space ambience - cosmic background
            for i in range(num_samples):
                t = i / sample_rate
                # Cosmic background radiation (very low frequency)
                cosmic = math.sin(2 * math.pi * 0.01 * t) * 0.2
                # Pulsar clicks (sporadic)
                pulsar = 0.3 if (i % 50000) < 50 else 0
                sample = cosmic + pulsar
                left_channel.append(sample)
                right_channel.append(sample)
        
        # Store the generated ambience
        self.ambient_soundscapes[environment_type] = [list(left_channel), list(right_channel)]
        
        return [list(left_channel), list(right_channel)]
    
    def blend_with_environment(self, quantum_audio: List[List[float]], 
                              environment_type: str,
                              blend_ratio: float = 0.7) -> List[List[float]]:
        """
        Blend quantum audio with environmental sounds for natural immersion
        
        Args:
            quantum_audio: Quantum audio data as [left_channel, right_channel]
            environment_type: Type of environment to blend with
            blend_ratio: Ratio of environmental sound to quantum sound (0.0 to 1.0)
            
        Returns:
            Blended audio data
        """
        # Generate or retrieve environmental ambience
        if environment_type not in self.ambient_soundscapes:
            environmental_audio = self.generate_environmental_ambience(environment_type)
        else:
            environmental_audio = self.ambient_soundscapes[environment_type]
        
        # Blend the audio (simplified mixing)
        if len(quantum_audio) >= 2 and len(environmental_audio) >= 2:
            # Ensure both channels have the same length
            min_length = min(len(quantum_audio[0]), len(environmental_audio[0]), 
                           len(quantum_audio[1]), len(environmental_audio[1]))
            
            blended_left = []
            blended_right = []
            
            for i in range(min_length):
                # Blend with specified ratio
                quantum_left = quantum_audio[0][i]
                quantum_right = quantum_audio[1][i]
                env_left = environmental_audio[0][i]
                env_right = environmental_audio[1][i]
                
                blended_sample_left = (quantum_left * (1 - blend_ratio)) + (env_left * blend_ratio)
                blended_sample_right = (quantum_right * (1 - blend_ratio)) + (env_right * blend_ratio)
                
                blended_left.append(blended_sample_left)
                blended_right.append(blended_sample_right)
                
            return [blended_left, blended_right]
        
        # If we can't blend properly, return the quantum audio
        return quantum_audio

# Global instance
environmental_processor = EnvironmentalAudioProcessor()

def initialize_environmental_processing():
    """Initialize the global environmental audio processor"""
    global environmental_processor
    environmental_processor.initialize_environmental_layers()
    return environmental_processor

def create_sound_mask(environment_type: str):
    """Create a sound mask for the specified environment"""
    return environmental_processor.create_natural_sound_mask(environment_type)

def blend_quantum_with_environment(quantum_audio: List[List[float]], 
                                  environment_type: str,
                                  blend_ratio: float = 0.7):
    """Blend quantum audio with environmental sounds"""
    return environmental_processor.blend_with_environment(quantum_audio, environment_type, blend_ratio)