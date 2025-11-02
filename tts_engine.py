"""
Text-to-Speech Engine Module for VisionSpeak
Handles text-to-speech conversion using pyttsx3 and gTTS.
"""

import pyttsx3
import threading
from gtts import gTTS
import pygame
import tempfile
import os
from langdetect import detect, LangDetectException


class TTSEngine:
    """
    Text-to-Speech Engine wrapper for pyttsx3 and gTTS.
    Provides text-to-speech functionality with configurable voice settings.
    Automatically detects language and uses appropriate TTS engine.
    """
    
    def __init__(self):
        """Initialize the TTS engine."""
        self.engine = pyttsx3.init()
        self.is_speaking = False
        self.speech_thread = None
        self.pygame_available = False
        
        # Default settings
        self.rate = 150  # Speaking rate (words per minute)
        self.volume = 1.0  # Volume (0.0 to 1.0)
        self.use_gtts_for_vietnamese = True  # Use gTTS for Vietnamese by default
        self.auto_detect_language = True  # Auto-detect language
        
        # Apply default settings
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        
        # Initialize pygame mixer for playing gTTS audio
        # Try multiple initialization methods for cross-platform compatibility
        self.pygame_available = False
        
        init_methods = [
            # Method 1: Default settings
            {'frequency': 22050, 'size': -16, 'channels': 2, 'buffer': 512},
            # Method 2: Larger buffer (sometimes helps on macOS)
            {'frequency': 44100, 'size': -16, 'channels': 2, 'buffer': 4096},
            # Method 3: Minimal settings
            {'frequency': 22050, 'size': -16, 'channels': 1, 'buffer': 2048},
        ]
        
        for method_idx, settings in enumerate(init_methods):
            try:
                # Quit first if already initialized
                if pygame.mixer.get_init():
                    pygame.mixer.quit()
                
                pygame.mixer.init(**settings)
                self.pygame_available = True
                # Success - break out of loop
                break
            except Exception as e:
                # Try next method
                if method_idx == len(init_methods) - 1:
                    # All methods failed
                    print(f"Warning: pygame mixer init failed after {len(init_methods)} attempts")
                    print("gTTS will not be available. Using pyttsx3 for all languages.")
                    self.pygame_available = False
                    self.use_gtts_for_vietnamese = False  # Fallback to pyttsx3
    
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
    
    def detect_language(self, text):
        """
        Detect the language of the given text.
        
        Args:
            text (str): Text to detect language from
            
        Returns:
            str: Language code (e.g., 'en', 'vi') or 'en' if detection fails
        """
        if not text or not text.strip():
            return 'en'
        
        try:
            lang = detect(text)
            return lang
        except LangDetectException:
            return 'en'  # Default to English if detection fails
    
    def _split_text_by_punctuation(self, text):
        """
        Split text into sentences based on punctuation marks ONLY.
        KHÔNG ngắt ở xuống dòng - chỉ ngắt ở dấu câu thực sự.
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of sentences
        """
        import re
        
        # Replace newlines with SPACE (không phải dấu chấm)
        # → Xuống dòng KHÔNG tạo pause
        text = text.replace('\n', ' ')
        
        # Split by punctuation marks: . ! ? ; ,
        # Pattern: Split on these punctuation marks but keep them
        sentences = re.split(r'([.!?;,])', text)
        
        # Reconstruct sentences with punctuation
        result = []
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i].strip()
            punct = sentences[i+1] if i+1 < len(sentences) else ''
            
            if sentence:
                result.append(sentence + punct)
        
        # Handle last part if no punctuation
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            result.append(sentences[-1].strip())
        
        return [s.strip() for s in result if s.strip()]
    
    def _speak_with_gtts(self, text, lang='vi'):
        """
        Speak text using Google TTS (gTTS).
        Requires pygame mixer and Internet connection.
        
        Args:
            text (str): Text to speak
            lang (str): Language code (default: 'vi' for Vietnamese)
        """
        if not self.pygame_available:
            # Fallback to pyttsx3
            print("Warning: pygame not available, using pyttsx3 instead")
            self.engine.say(text)
            self.engine.runAndWait()
            return
        
        try:
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.close()
            
            # Generate speech with gTTS
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file.name)
            
            # Reinitialize mixer if needed
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            
            # Play audio with pygame
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Cleanup
            try:
                os.unlink(temp_file.name)
            except Exception:
                pass
                
        except Exception as e:
            # Fallback to pyttsx3 on error
            print(f"Warning: gTTS failed ({e}), falling back to pyttsx3")
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
    
    def speak(self, text, blocking=True, lang=None):
        """
        Convert text to speech and play it.
        Automatically detects language and uses appropriate TTS engine.
        Splits text by punctuation for natural pauses.
        
        Args:
            text (str): Text to speak
            blocking (bool): If True, wait for speech to complete before returning
            lang (str, optional): Force specific language ('en', 'vi', etc.)
        """
        if not text or not text.strip():
            return
        
        # Detect language if not specified
        if lang is None and self.auto_detect_language:
            detected_lang = self.detect_language(text)
        else:
            detected_lang = lang if lang else 'en'
        
        # Split text into sentences for natural pauses
        sentences = self._split_text_by_punctuation(text)
        
        # Decide which engine to use
        use_gtts = (detected_lang == 'vi' and self.use_gtts_for_vietnamese)
        
        if blocking:
            # Blocking mode: speak sentence by sentence with pauses
            self.is_speaking = True
            try:
                for i, sentence in enumerate(sentences):
                    if not sentence.strip():
                        continue
                    
                    if use_gtts:
                        self._speak_with_gtts(sentence, lang=detected_lang)
                    else:
                        self.engine.say(sentence)
                        self.engine.runAndWait()
                    
                    # Add pause between sentences (except last one)
                    if i < len(sentences) - 1:
                        import time
                        time.sleep(0.3)  # 300ms pause between sentences
                        
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
        else:
            # Non-blocking mode: speak in a separate thread
            self.speak_async(text, lang=detected_lang)
    
    def speak_async(self, text, lang=None):
        """
        Speak text asynchronously in a separate thread.
        Automatically detects language and uses appropriate TTS engine.
        Splits text by punctuation for natural pauses.
        
        Args:
            text (str): Text to speak
            lang (str, optional): Force specific language ('en', 'vi', etc.)
        """
        if self.is_speaking:
            self.stop()
        
        # Detect language if not specified
        if lang is None and self.auto_detect_language:
            detected_lang = self.detect_language(text)
        else:
            detected_lang = lang if lang else 'en'
        
        # Split text into sentences for natural pauses
        sentences = self._split_text_by_punctuation(text)
        
        # Decide which engine to use
        use_gtts = (detected_lang == 'vi' and self.use_gtts_for_vietnamese)
        
        def _speak():
            self.is_speaking = True
            try:
                import time
                for i, sentence in enumerate(sentences):
                    if not sentence.strip():
                        continue
                    
                    if use_gtts:
                        self._speak_with_gtts(sentence, lang=detected_lang)
                    else:
                        self.engine.say(sentence)
                        self.engine.runAndWait()
                    
                    # Add pause between sentences (except last one)
                    if i < len(sentences) - 1:
                        time.sleep(0.3)  # 300ms pause
                        
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
            try:
                pygame.mixer.music.stop()
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
        self.use_gtts_for_vietnamese = True
        self.auto_detect_language = True
        # Reset to first available voice
        voices = self.get_available_voices()
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def set_auto_detect_language(self, enabled):
        """
        Enable or disable automatic language detection.
        
        Args:
            enabled (bool): True to enable auto-detection, False to disable
        """
        self.auto_detect_language = enabled
    
    def set_use_gtts_for_vietnamese(self, enabled):
        """
        Enable or disable using gTTS for Vietnamese text.
        
        Args:
            enabled (bool): True to use gTTS for Vietnamese, False to use pyttsx3
        """
        self.use_gtts_for_vietnamese = enabled
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        try:
            if hasattr(self, 'engine'):
                self.stop()
        except Exception:
            pass

