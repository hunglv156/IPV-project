"""
Module GUI cho VisionSpeak
Giao diện người dùng được xây dựng bằng Tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import os
from datetime import datetime

from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine


class VisionSpeakGUI:
    """
    Lớp giao diện chính của ứng dụng VisionSpeak
    """
    
    def __init__(self, root):
        """
        Khởi tạo giao diện
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("VisionSpeak - Hệ Thống OCR và TTS Thích Ứng")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Khởi tạo các engine
        self.image_processor = ImageProcessor()
        self.ocr_engine = OCREngine()
        self.tts_engine = TTSEngine()
        
        # Biến trạng thái
        self.current_image = None
        self.current_image_path = None
        self.processed_image = None
        self.ocr_result = None
        self.is_processing = False
        
        # Thiết lập giao diện
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
        # Thiết lập sự kiện
        self.setup_events()
        
    def setup_ui(self):
        """
        Thiết lập giao diện người dùng
        """
        # Tạo notebook để tổ chức các tab
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab chính - Xử lý ảnh và OCR
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="OCR & TTS")
        
        # Tab cài đặt
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Cài Đặt")
        
        self.setup_main_tab()
        self.setup_settings_tab()
        
    def setup_main_tab(self):
        """
        Thiết lập tab chính
        """
        # Frame chính với 3 cột
        main_container = ttk.Frame(self.main_frame)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Cột trái - Điều khiển
        control_frame = ttk.LabelFrame(main_container, text="Điều Khiển", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Nút tải ảnh
        self.load_image_btn = ttk.Button(
            control_frame, 
            text="Tải Ảnh", 
            command=self.load_image,
            width=20
        )
        self.load_image_btn.pack(pady=5)
        
        # Nút chụp ảnh từ camera
        self.capture_btn = ttk.Button(
            control_frame, 
            text="Chụp Ảnh", 
            command=self.capture_from_camera,
            width=20
        )
        self.capture_btn.pack(pady=5)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Nút xử lý ảnh
        self.process_btn = ttk.Button(
            control_frame, 
            text="Xử Lý Ảnh", 
            command=self.process_image,
            width=20,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=5)
        
        # Nút OCR
        self.ocr_btn = ttk.Button(
            control_frame, 
            text="Nhận Dạng Văn Bản", 
            command=self.perform_ocr,
            width=20,
            state=tk.DISABLED
        )
        self.ocr_btn.pack(pady=5)
        
        # Separator
        ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Điều khiển TTS
        tts_frame = ttk.LabelFrame(control_frame, text="Text-to-Speech", padding=5)
        tts_frame.pack(fill=tk.X, pady=5)
        
        self.speak_btn = ttk.Button(
            tts_frame, 
            text="Phát Âm", 
            command=self.speak_text,
            width=15,
            state=tk.DISABLED
        )
        self.speak_btn.pack(pady=2)
        
        self.stop_speak_btn = ttk.Button(
            tts_frame, 
            text="Dừng", 
            command=self.stop_speaking,
            width=15,
            state=tk.DISABLED
        )
        self.stop_speak_btn.pack(pady=2)
        
        self.save_audio_btn = ttk.Button(
            tts_frame, 
            text="Lưu Audio", 
            command=self.save_audio,
            width=15,
            state=tk.DISABLED
        )
        self.save_audio_btn.pack(pady=2)
        
        # Cột giữa - Hiển thị ảnh
        image_frame = ttk.LabelFrame(main_container, text="Hình Ảnh", padding=10)
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Canvas để hiển thị ảnh
        self.image_canvas = tk.Canvas(image_frame, bg='white', width=400, height=300)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Label hiển thị thông tin ảnh
        self.image_info_label = ttk.Label(image_frame, text="Chưa có ảnh")
        self.image_info_label.pack(pady=5)
        
        # Cột phải - Kết quả OCR
        result_frame = ttk.LabelFrame(main_container, text="Kết Quả OCR", padding=10)
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Text widget để hiển thị văn bản
        self.result_text = scrolledtext.ScrolledText(
            result_frame, 
            wrap=tk.WORD, 
            width=40, 
            height=20,
            font=('Arial', 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame cho thông tin OCR
        info_frame = ttk.Frame(result_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.ocr_info_label = ttk.Label(info_frame, text="Chưa có kết quả OCR")
        self.ocr_info_label.pack()
        
    def setup_settings_tab(self):
        """
        Thiết lập tab cài đặt
        """
        # Frame chính
        main_frame = ttk.Frame(self.settings_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cài đặt TTS
        tts_settings_frame = ttk.LabelFrame(main_frame, text="Cài Đặt Text-to-Speech", padding=10)
        tts_settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Tốc độ nói
        ttk.Label(tts_settings_frame, text="Tốc độ nói:").pack(anchor=tk.W)
        self.rate_var = tk.IntVar(value=200)
        self.rate_scale = ttk.Scale(
            tts_settings_frame, 
            from_=50, 
            to=300, 
            variable=self.rate_var,
            orient=tk.HORIZONTAL,
            command=self.update_rate
        )
        self.rate_scale.pack(fill=tk.X, pady=5)
        self.rate_label = ttk.Label(tts_settings_frame, text="200")
        self.rate_label.pack()
        
        # Âm lượng
        ttk.Label(tts_settings_frame, text="Âm lượng:").pack(anchor=tk.W)
        self.volume_var = tk.DoubleVar(value=0.8)
        self.volume_scale = ttk.Scale(
            tts_settings_frame, 
            from_=0.0, 
            to=1.0, 
            variable=self.volume_var,
            orient=tk.HORIZONTAL,
            command=self.update_volume
        )
        self.volume_scale.pack(fill=tk.X, pady=5)
        self.volume_label = ttk.Label(tts_settings_frame, text="0.8")
        self.volume_label.pack()
        
        # Giọng nói
        ttk.Label(tts_settings_frame, text="Giọng nói:").pack(anchor=tk.W)
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(tts_settings_frame, textvariable=self.voice_var, state="readonly")
        self.voice_combo.pack(fill=tk.X, pady=5)
        self.voice_combo.bind('<<ComboboxSelected>>', self.update_voice)
        
        # Cài đặt OCR
        ocr_settings_frame = ttk.LabelFrame(main_frame, text="Cài Đặt OCR", padding=10)
        ocr_settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Ngôn ngữ OCR
        ttk.Label(ocr_settings_frame, text="Ngôn ngữ:").pack(anchor=tk.W)
        self.language_var = tk.StringVar(value="vie+eng")
        language_combo = ttk.Combobox(
            ocr_settings_frame, 
            textvariable=self.language_var,
            values=["vie", "eng", "vie+eng"],
            state="readonly"
        )
        language_combo.pack(fill=tk.X, pady=5)
        
        # Cài đặt xử lý ảnh
        image_settings_frame = ttk.LabelFrame(main_frame, text="Cài Đặt Xử Lý Ảnh", padding=10)
        image_settings_frame.pack(fill=tk.X)
        
        # Debug mode
        self.debug_var = tk.BooleanVar()
        debug_check = ttk.Checkbutton(
            image_settings_frame, 
            text="Chế độ debug (lưu các bước xử lý)",
            variable=self.debug_var,
            command=self.toggle_debug
        )
        debug_check.pack(anchor=tk.W)
        
        # Nút test
        test_frame = ttk.Frame(main_frame)
        test_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(test_frame, text="Test TTS", command=self.test_tts).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(test_frame, text="Reset Cài Đặt", command=self.reset_settings).pack(side=tk.LEFT)
        
        # Khởi tạo danh sách giọng nói
        self.load_voices()
        
    def setup_menu(self):
        """
        Thiết lập menu bar
        """
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Mở Ảnh...", command=self.load_image)
        file_menu.add_command(label="Chụp Ảnh...", command=self.capture_from_camera)
        file_menu.add_separator()
        file_menu.add_command(label="Lưu Văn Bản...", command=self.save_text)
        file_menu.add_command(label="Lưu Audio...", command=self.save_audio)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self.root.quit)
        
        # Menu Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Hướng Dẫn", command=self.show_help)
        help_menu.add_command(label="Về VisionSpeak", command=self.show_about)
        
    def setup_status_bar(self):
        """
        Thiết lập thanh trạng thái
        """
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Sẵn sàng")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.status_bar, 
            mode='indeterminate',
            length=200
        )
        self.progress.pack(side=tk.RIGHT, padx=10)
        
    def setup_events(self):
        """
        Thiết lập các sự kiện
        """
        # Bind events
        self.root.bind('<Control-o>', lambda e: self.load_image())
        self.root.bind('<Control-s>', lambda e: self.save_text())
        self.root.bind('<F5>', lambda e: self.perform_ocr())
        
    def load_image(self):
        """
        Tải ảnh từ file
        """
        filetypes = [
            ("Tất cả ảnh", "*.jpg *.jpeg *.png *.bmp *.tiff"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff")
        ]
        
        filename = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=filetypes
        )
        
        if filename:
            self.current_image_path = filename
            self.display_image(filename)
            self.update_status("Đã tải ảnh: " + os.path.basename(filename))
            self.process_btn.config(state=tk.NORMAL)
            
    def capture_from_camera(self):
        """
        Chụp ảnh từ camera
        """
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Lỗi", "Không thể mở camera!")
                return
            
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                self.current_image = frame
                self.current_image_path = None
                self.display_image_from_array(frame)
                self.update_status("Đã chụp ảnh từ camera")
                self.process_btn.config(state=tk.NORMAL)
            else:
                messagebox.showerror("Lỗi", "Không thể chụp ảnh!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi chụp ảnh: {e}")
            
    def display_image(self, image_path):
        """
        Hiển thị ảnh từ file
        """
        try:
            # Đọc ảnh
            image = cv2.imread(image_path)
            if image is None:
                messagebox.showerror("Lỗi", "Không thể đọc ảnh!")
                return
            
            self.current_image = image
            self.display_image_from_array(image)
            
            # Cập nhật thông tin ảnh
            height, width = image.shape[:2]
            file_size = os.path.getsize(image_path) / 1024  # KB
            info_text = f"Kích thước: {width}x{height} | Dung lượng: {file_size:.1f} KB"
            self.image_info_label.config(text=info_text)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi hiển thị ảnh: {e}")
            
    def display_image_from_array(self, image_array):
        """
        Hiển thị ảnh từ numpy array
        """
        try:
            # Chuyển đổi BGR sang RGB
            rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            
            # Thay đổi kích thước để vừa với canvas
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = 400
                canvas_height = 300
            
            # Tính tỷ lệ scale
            h, w = rgb_image.shape[:2]
            scale = min(canvas_width/w, canvas_height/h, 1.0)
            
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # Resize ảnh
            resized_image = cv2.resize(rgb_image, (new_w, new_h))
            
            # Chuyển sang PIL Image
            pil_image = Image.fromarray(resized_image)
            
            # Chuyển sang PhotoImage
            self.photo = ImageTk.PhotoImage(pil_image)
            
            # Hiển thị trên canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                canvas_width//2, 
                canvas_height//2, 
                image=self.photo
            )
            
        except Exception as e:
            print(f"Lỗi khi hiển thị ảnh: {e}")
            
    def process_image(self):
        """
        Xử lý ảnh
        """
        if self.current_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải ảnh trước!")
            return
        
        self.start_processing("Đang xử lý ảnh...")
        
        def process_thread():
            try:
                if self.current_image_path:
                    # Xử lý từ file
                    self.processed_image = self.image_processor.process_image(
                        self.current_image_path
                    )
                else:
                    # Xử lý từ array
                    self.processed_image = self.image_processor.process_from_array(
                        self.current_image
                    )
                
                if self.processed_image is not None:
                    self.root.after(0, self.on_image_processed)
                else:
                    self.root.after(0, lambda: self.on_processing_error("Lỗi khi xử lý ảnh!"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_processing_error(f"Lỗi: {e}"))
        
        threading.Thread(target=process_thread, daemon=True).start()
        
    def on_image_processed(self):
        """
        Callback khi xử lý ảnh hoàn thành
        """
        self.stop_processing()
        self.update_status("Đã xử lý ảnh thành công")
        self.ocr_btn.config(state=tk.NORMAL)
        
        # Hiển thị ảnh đã xử lý
        self.display_image_from_array(self.processed_image)
        
    def perform_ocr(self):
        """
        Thực hiện OCR
        """
        if self.processed_image is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng xử lý ảnh trước!")
            return
        
        self.start_processing("Đang nhận dạng văn bản...")
        
        def ocr_thread():
            try:
                language = self.language_var.get()
                
                if self.current_image_path:
                    # OCR từ file
                    self.ocr_result = self.ocr_engine.extract_text_from_image(
                        self.current_image_path, language=language
                    )
                else:
                    # OCR từ array
                    self.ocr_result = self.ocr_engine.extract_text_from_array(
                        self.processed_image, language=language
                    )
                
                self.root.after(0, self.on_ocr_completed)
                    
            except Exception as e:
                self.root.after(0, lambda: self.on_processing_error(f"Lỗi OCR: {e}"))
        
        threading.Thread(target=ocr_thread, daemon=True).start()
        
    def on_ocr_completed(self):
        """
        Callback khi OCR hoàn thành
        """
        self.stop_processing()
        
        if self.ocr_result['success']:
            text = self.ocr_result['text']
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, text)
            
            # Cập nhật thông tin OCR
            config_used = self.ocr_result.get('config_used', 'N/A')
            info_text = f"Cấu hình: {config_used} | Độ dài: {len(text)} ký tự"
            self.ocr_info_label.config(text=info_text)
            
            # Kích hoạt các nút TTS
            if text.strip():
                self.speak_btn.config(state=tk.NORMAL)
                self.save_audio_btn.config(state=tk.NORMAL)
            
            self.update_status("OCR hoàn thành thành công")
        else:
            error_msg = self.ocr_result.get('error', 'Lỗi không xác định')
            self.on_processing_error(f"Lỗi OCR: {error_msg}")
            
    def speak_text(self):
        """
        Phát âm văn bản
        """
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Không có văn bản để phát âm!")
            return
        
        try:
            success = self.tts_engine.speak_processed_text(text)
            if success:
                self.speak_btn.config(state=tk.DISABLED)
                self.stop_speak_btn.config(state=tk.NORMAL)
                self.update_status("Đang phát âm...")
            else:
                messagebox.showerror("Lỗi", "Không thể phát âm!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi phát âm: {e}")
            
    def stop_speaking(self):
        """
        Dừng phát âm
        """
        try:
            self.tts_engine.stop()
            self.speak_btn.config(state=tk.NORMAL)
            self.stop_speak_btn.config(state=tk.DISABLED)
            self.update_status("Đã dừng phát âm")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi dừng phát âm: {e}")
            
    def save_text(self):
        """
        Lưu văn bản ra file
        """
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Không có văn bản để lưu!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Lưu văn bản",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Thành công", f"Đã lưu văn bản vào {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lưu file: {e}")
                
    def save_audio(self):
        """
        Lưu audio ra file
        """
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Không có văn bản để lưu audio!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Lưu audio",
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                success = self.tts_engine.save_to_file(text, filename)
                if success:
                    messagebox.showinfo("Thành công", f"Đã lưu audio vào {filename}")
                else:
                    messagebox.showerror("Lỗi", "Không thể lưu file audio!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lưu audio: {e}")
                
    def load_voices(self):
        """
        Tải danh sách giọng nói
        """
        try:
            voices = self.tts_engine.get_available_voices()
            voice_names = [f"{voice['name']} ({voice['id']})" for voice in voices]
            self.voice_combo['values'] = voice_names
            
            if voice_names:
                self.voice_combo.current(0)
                
        except Exception as e:
            print(f"Lỗi khi tải giọng nói: {e}")
            
    def update_rate(self, value):
        """
        Cập nhật tốc độ nói
        """
        rate = int(float(value))
        self.rate_label.config(text=str(rate))
        self.tts_engine.set_rate(rate)
        
    def update_volume(self, value):
        """
        Cập nhật âm lượng
        """
        volume = float(value)
        self.volume_label.config(text=f"{volume:.1f}")
        self.tts_engine.set_volume(volume)
        
    def update_voice(self, event):
        """
        Cập nhật giọng nói
        """
        selection = self.voice_combo.get()
        if selection:
            # Lấy voice ID từ chuỗi
            voice_id = selection.split('(')[-1].rstrip(')')
            self.tts_engine.set_voice(voice_id)
            
    def toggle_debug(self):
        """
        Bật/tắt chế độ debug
        """
        self.image_processor.set_debug_mode(self.debug_var.get())
        
    def test_tts(self):
        """
        Test TTS
        """
        test_text = "Đây là test hệ thống Text-to-Speech của VisionSpeak."
        try:
            self.tts_engine.speak_processed_text(test_text, blocking=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi test TTS: {e}")
            
    def reset_settings(self):
        """
        Reset cài đặt về mặc định
        """
        self.rate_var.set(200)
        self.volume_var.set(0.8)
        self.language_var.set("vie+eng")
        self.debug_var.set(False)
        
        self.update_rate(200)
        self.update_volume(0.8)
        self.toggle_debug()
        
        messagebox.showinfo("Thông báo", "Đã reset cài đặt về mặc định!")
        
    def start_processing(self, message):
        """
        Bắt đầu hiển thị trạng thái xử lý
        """
        self.is_processing = True
        self.progress.start()
        self.update_status(message)
        
        # Disable các nút
        self.process_btn.config(state=tk.DISABLED)
        self.ocr_btn.config(state=tk.DISABLED)
        
    def stop_processing(self):
        """
        Dừng hiển thị trạng thái xử lý
        """
        self.is_processing = False
        self.progress.stop()
        
        # Enable các nút
        if self.current_image is not None:
            self.process_btn.config(state=tk.NORMAL)
        if self.processed_image is not None:
            self.ocr_btn.config(state=tk.NORMAL)
            
    def on_processing_error(self, error_message):
        """
        Xử lý lỗi trong quá trình xử lý
        """
        self.stop_processing()
        self.update_status(f"Lỗi: {error_message}")
        messagebox.showerror("Lỗi", error_message)
        
    def update_status(self, message):
        """
        Cập nhật thanh trạng thái
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"[{timestamp}] {message}")
        
    def show_help(self):
        """
        Hiển thị hướng dẫn
        """
        help_text = """
VisionSpeak - Hướng Dẫn Sử Dụng

1. Tải ảnh hoặc chụp ảnh từ camera
2. Nhấn "Xử Lý Ảnh" để tối ưu hóa ảnh cho OCR
3. Nhấn "Nhận Dạng Văn Bản" để thực hiện OCR
4. Sử dụng các nút TTS để phát âm văn bản
5. Có thể lưu văn bản hoặc audio ra file

Phím tắt:
- Ctrl+O: Mở ảnh
- Ctrl+S: Lưu văn bản
- F5: Nhận dạng văn bản

Cài đặt:
- Điều chỉnh tốc độ và âm lượng TTS trong tab Cài Đặt
- Chọn ngôn ngữ OCR phù hợp
- Bật debug mode để lưu các bước xử lý ảnh
        """
        messagebox.showinfo("Hướng Dẫn", help_text)
        
    def show_about(self):
        """
        Hiển thị thông tin về ứng dụng
        """
        about_text = """
VisionSpeak v1.0

Hệ Thống Nhận Dạng Ký Tự Quang Học (OCR) và 
Phát Âm Thanh (TTS) Thích Ứng

Phát triển bởi: [Tên sinh viên]
Môn học: Xử Lý Ảnh và Thị Giác Máy Tính

Công nghệ sử dụng:
- Python 3.x
- OpenCV (xử lý ảnh)
- Tesseract OCR
- pyttsx3 (TTS)
- Tkinter (GUI)
        """
        messagebox.showinfo("Về VisionSpeak", about_text)


def main():
    """
    Hàm main để chạy ứng dụng
    """
    root = tk.Tk()
    app = VisionSpeakGUI(root)
    
    try:
        root.mainloop()
    finally:
        # Dọn dẹp tài nguyên
        app.tts_engine.cleanup()


if __name__ == "__main__":
    main()
