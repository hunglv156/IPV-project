"""
Module Text-to-Speech Engine cho VisionSpeak
Sử dụng pyttsx3 để chuyển đổi văn bản thành giọng nói
"""

import pyttsx3
import threading
import queue
import time
import os


class TTSEngine:
    """
    Lớp xử lý Text-to-Speech với các tính năng nâng cao
    """
    
    def __init__(self):
        """
        Khởi tạo TTS Engine
        """
        self.engine = None
        self.is_speaking = False
        self.is_paused = False
        self.speech_queue = queue.Queue()
        self.current_text = ""
        self.speech_thread = None
        self.stop_flag = False
        
        # Khởi tạo engine
        self._initialize_engine()
        
        # Cài đặt mặc định
        self.set_rate(200)  # Tốc độ nói (từ 50-300)
        self.set_volume(0.8)  # Âm lượng (0.0-1.0)
        
    def _initialize_engine(self):
        """
        Khởi tạo pyttsx3 engine
        """
        try:
            self.engine = pyttsx3.init()
            
            # Lấy danh sách giọng nói có sẵn
            voices = self.engine.getProperty('voices')
            self.available_voices = voices
            
            # Thiết lập giọng nói mặc định (ưu tiên tiếng Việt nếu có)
            self._set_default_voice()
            
        except Exception as e:
            print(f"Lỗi khi khởi tạo TTS engine: {e}")
            self.engine = None
    
    def _set_default_voice(self):
        """
        Thiết lập giọng nói mặc định
        """
        if not self.available_voices:
            return
        
        # Tìm giọng nói tiếng Việt
        vietnamese_voice = None
        for voice in self.available_voices:
            if 'vietnamese' in voice.name.lower() or 'viet' in voice.name.lower():
                vietnamese_voice = voice
                break
        
        # Nếu không có tiếng Việt, sử dụng giọng nói đầu tiên
        if vietnamese_voice:
            self.engine.setProperty('voice', vietnamese_voice.id)
        else:
            self.engine.setProperty('voice', self.available_voices[0].id)
    
    def get_available_voices(self):
        """
        Lấy danh sách giọng nói có sẵn
        
        Returns:
            list: Danh sách thông tin giọng nói
        """
        voices_info = []
        for voice in self.available_voices:
            voices_info.append({
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages,
                'age': voice.age,
                'gender': voice.gender
            })
        return voices_info
    
    def set_voice(self, voice_id):
        """
        Thiết lập giọng nói
        
        Args:
            voice_id (str): ID của giọng nói
        """
        if self.engine:
            try:
                self.engine.setProperty('voice', voice_id)
                return True
            except Exception as e:
                print(f"Lỗi khi thiết lập giọng nói: {e}")
                return False
        return False
    
    def set_rate(self, rate):
        """
        Thiết lập tốc độ nói
        
        Args:
            rate (int): Tốc độ nói (50-300)
        """
        if self.engine:
            try:
                # Giới hạn tốc độ trong khoảng hợp lý
                rate = max(50, min(300, rate))
                self.engine.setProperty('rate', rate)
                return True
            except Exception as e:
                print(f"Lỗi khi thiết lập tốc độ: {e}")
                return False
        return False
    
    def set_volume(self, volume):
        """
        Thiết lập âm lượng
        
        Args:
            volume (float): Âm lượng (0.0-1.0)
        """
        if self.engine:
            try:
                # Giới hạn âm lượng trong khoảng hợp lý
                volume = max(0.0, min(1.0, volume))
                self.engine.setProperty('volume', volume)
                return True
            except Exception as e:
                print(f"Lỗi khi thiết lập âm lượng: {e}")
                return False
        return False
    
    def get_current_settings(self):
        """
        Lấy cài đặt hiện tại
        
        Returns:
            dict: Thông tin cài đặt hiện tại
        """
        if not self.engine:
            return {}
        
        try:
            return {
                'rate': self.engine.getProperty('rate'),
                'volume': self.engine.getProperty('volume'),
                'voice': self.engine.getProperty('voice')
            }
        except Exception as e:
            print(f"Lỗi khi lấy cài đặt: {e}")
            return {}
    
    def speak(self, text, blocking=False):
        """
        Phát âm văn bản
        
        Args:
            text (str): Văn bản cần phát âm
            blocking (bool): Có chặn thread chính hay không
        """
        if not self.engine or not text.strip():
            return False
        
        try:
            self.current_text = text
            
            if blocking:
                # Phát âm đồng bộ
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                # Phát âm bất đồng bộ
                self.is_speaking = True
                self.stop_flag = False
                
                # Tạo thread mới cho việc phát âm
                self.speech_thread = threading.Thread(
                    target=self._speak_thread,
                    args=(text,)
                )
                self.speech_thread.daemon = True
                self.speech_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Lỗi khi phát âm: {e}")
            self.is_speaking = False
            return False
    
    def _speak_thread(self, text):
        """
        Thread xử lý phát âm
        
        Args:
            text (str): Văn bản cần phát âm
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Lỗi trong thread phát âm: {e}")
        finally:
            self.is_speaking = False
    
    def pause(self):
        """
        Tạm dừng phát âm
        """
        if self.engine and self.is_speaking:
            try:
                self.engine.stop()
                self.is_paused = True
                return True
            except Exception as e:
                print(f"Lỗi khi tạm dừng: {e}")
                return False
        return False
    
    def resume(self):
        """
        Tiếp tục phát âm
        """
        if self.is_paused:
            self.is_paused = False
            # Phát lại từ đầu
            if self.current_text:
                self.speak(self.current_text)
            return True
        return False
    
    def stop(self):
        """
        Dừng phát âm
        """
        if self.engine:
            try:
                self.stop_flag = True
                self.engine.stop()
                self.is_speaking = False
                self.is_paused = False
                return True
            except Exception as e:
                print(f"Lỗi khi dừng phát âm: {e}")
                return False
        return False
    
    def is_currently_speaking(self):
        """
        Kiểm tra xem có đang phát âm hay không
        
        Returns:
            bool: True nếu đang phát âm
        """
        return self.is_speaking
    
    def save_to_file(self, text, filename):
        """
        Lưu giọng nói ra file audio
        
        Args:
            text (str): Văn bản cần phát âm
            filename (str): Tên file output
            
        Returns:
            bool: True nếu thành công
        """
        if not self.engine or not text.strip():
            return False
        
        try:
            # Lưu ra file WAV
            if not filename.endswith('.wav'):
                filename += '.wav'
            
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            
            # Kiểm tra file đã được tạo
            if os.path.exists(filename):
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Lỗi khi lưu file audio: {e}")
            return False
    
    def preprocess_text(self, text):
        """
        Tiền xử lý văn bản trước khi phát âm
        
        Args:
            text (str): Văn bản gốc
            
        Returns:
            str: Văn bản đã được xử lý
        """
        if not text:
            return ""
        
        # Loại bỏ các ký tự đặc biệt có thể gây lỗi
        processed_text = text.replace('\n', ' ')
        processed_text = processed_text.replace('\t', ' ')
        
        # Chuẩn hóa khoảng trắng
        processed_text = ' '.join(processed_text.split())
        
        # Thêm dấu chấm câu nếu cần
        if processed_text and not processed_text.endswith(('.', '!', '?')):
            processed_text += '.'
        
        return processed_text
    
    def speak_processed_text(self, text, blocking=False):
        """
        Phát âm văn bản đã được tiền xử lý
        
        Args:
            text (str): Văn bản cần phát âm
            blocking (bool): Có chặn thread chính hay không
        """
        processed_text = self.preprocess_text(text)
        return self.speak(processed_text, blocking)
    
    def cleanup(self):
        """
        Dọn dẹp tài nguyên
        """
        try:
            if self.is_speaking:
                self.stop()
            
            if self.speech_thread and self.speech_thread.is_alive():
                self.speech_thread.join(timeout=1.0)
                
        except Exception as e:
            print(f"Lỗi khi dọn dẹp TTS: {e}")


def test_tts_engine():
    """Hàm test cho TTSEngine"""
    tts = TTSEngine()
    
    # Test các tính năng cơ bản
    print("=== Test TTS Engine ===")
    
    # Lấy thông tin giọng nói
    voices = tts.get_available_voices()
    print(f"Số lượng giọng nói có sẵn: {len(voices)}")
    
    # Lấy cài đặt hiện tại
    settings = tts.get_current_settings()
    print(f"Cài đặt hiện tại: {settings}")
    
    # Test phát âm
    test_text = "Xin chào! Đây là hệ thống VisionSpeak. Tôi có thể đọc văn bản từ hình ảnh."
    print(f"Đang phát âm: {test_text}")
    
    success = tts.speak_processed_text(test_text, blocking=True)
    if success:
        print("Phát âm thành công!")
    else:
        print("Lỗi khi phát âm!")
    
    # Test lưu file
    filename = "test_audio.wav"
    success = tts.save_to_file(test_text, filename)
    if success:
        print(f"Đã lưu file audio: {filename}")
    else:
        print("Lỗi khi lưu file audio!")
    
    # Dọn dẹp
    tts.cleanup()


if __name__ == "__main__":
    test_tts_engine()
