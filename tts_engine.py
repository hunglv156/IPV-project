"""
Text-to-Speech Engine Module for VisionSpeak
Handles text-to-speech conversion using pyttsx3.
"""

import pyttsx3
import threading


class TTSEngine:
    """
    Text-to-Speech Engine wrapper for pyttsx3.
    Provides text-to-speech functionality with configurable voice settings.
    """
    
    def __init__(self):
        """Initialize the TTS engine."""
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.speech_thread = None
        
        # Default settings
        self.rate = 150  # Speaking rate (words per minute)
        self.volume = 1.0  # Volume (0.0 to 1.0)
        
        # Apply default settings
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
    
    def set_rate(self, rate):
        """
        Set the speaking rate.
        
        Args:
            rate (int): Speaking rate in words per minute (typical: 100-200)
        """
        self.rate = rate
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """
        Set the speaking volume.
        
        Args:
            volume (float): Volume level from 0.0 (silent) to 1.0 (maximum)
        """
        self.volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
        self.engine.setProperty('volume', self.volume)
    
    def set_voice(self, voice_id=None, gender=None):
        """
        Set the voice to use for speech.
        
        Args:
            voice_id (str, optional): Specific voice ID to use
            gender (str, optional): 'male' or 'female' to select voice by gender
        """
        voices = self.engine.getProperty('voices')
        
        if voice_id:
            # Set specific voice by ID
            self.engine.setProperty('voice', voice_id)
        elif gender:
            # Select voice by gender
            for voice in voices:
                if gender.lower() in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def get_available_voices(self):
        """
        Get list of available voices.
        
        Returns:
            list: List of voice objects with id, name, and languages
        """
        return self.engine.getProperty('voices')
    
    def get_voice_info(self):
        """
        Get information about available voices in a readable format.
        
        Returns:
            list: List of dictionaries with voice information
        """
        voices = self.get_available_voices()
        voice_info = []
        
        for i, voice in enumerate(voices):
            info = {
                'index': i,
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages,
                'gender': getattr(voice, 'gender', 'unknown')
            }
            voice_info.append(info)
        
        return voice_info
    
    def speak(self, text, blocking=True):
        """
        Convert text to speech and play it.
        
        Args:
            text (str): Text to speak
            blocking (bool): If True, wait for speech to complete before returning
        """
        if not text or not text.strip():
            return
        
        if blocking:
            # Blocking mode: wait for speech to complete
            self.is_speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        else:
            # Non-blocking mode: speak in a separate thread
            self.speak_async(text)
    
    def speak_async(self, text):
        """
        Speak text asynchronously in a separate thread.
        
        Args:
            text (str): Text to speak
        """
        if self.is_speaking:
            self.stop()
        
        def _speak():
            self.is_speaking = True
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        
        self.speech_thread = threading.Thread(target=_speak, daemon=True)
        self.speech_thread.start()
    
    def stop(self):
        """Stop any ongoing speech."""
        if self.is_speaking:
            try:
                self.engine.stop()
            except Exception:
                pass
            self.is_speaking = False
    
    def save_to_file(self, text, filename):
        """
        Save speech to an audio file.
        
        Args:
            text (str): Text to convert to speech
            filename (str): Output filename (should end with .mp3 or .wav)
        """
        try:
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
        except Exception as e:
            raise RuntimeError(f"Failed to save audio file: {str(e)}")
    
    def is_busy(self):
        """
        Check if the engine is currently speaking.
        
        Returns:
            bool: True if speaking, False otherwise
        """
        return self.is_speaking
    
    def get_current_settings(self):
        """
        Get current TTS settings.
        
        Returns:
            dict: Dictionary with current rate, volume, and voice
        """
        return {
            'rate': self.rate,
            'volume': self.volume,
            'voice': self.engine.getProperty('voice')
        }
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.set_rate(150)
        self.set_volume(1.0)
        # Reset to first available voice
        voices = self.get_available_voices()
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            if hasattr(self, 'engine'):
                self.stop()
        except Exception:
            pass

