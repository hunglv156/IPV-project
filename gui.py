"""
VisionSpeak - Adaptive OCR and TTS Desktop Application
Main GUI module using Tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os
import threading

from image_processor import ImageProcessor
from ocr_engine import OCREngine
from tts_engine import TTSEngine


class VisionSpeakApp:
    """
    Main application class for VisionSpeak.
    Provides a GUI for image loading, processing, OCR, and TTS.
    """
    
    def __init__(self, root):
        """
        Initialize the VisionSpeak application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("VisionSpeak - Adaptive OCR & TTS Application")
        self.root.geometry("1200x800")
        
        # Initialize processing engines
        self.image_processor = ImageProcessor()
        self.ocr_engine = OCREngine()
        self.tts_engine = TTSEngine()
        
        # Application state
        self.current_image_path = None
        self.current_text = ""
        self.processing_in_progress = False
        
        # Check if Tesseract is installed
        if not self.ocr_engine.check_tesseract_installed():
            messagebox.showwarning(
                "Tesseract Not Found",
                "Tesseract OCR is not installed or not found in PATH.\n"
                "Please install Tesseract OCR to use this application.\n"
                "See INSTALL.md for installation instructions."
            )
        
        # Setup GUI
        self.setup_ui()
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_ui(self):
        """Setup the user interface."""
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image...", command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Text...", command=self.save_text, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Process menu
        process_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Process", menu=process_menu)
        process_menu.add_command(label="Process Image", command=self.process_image, accelerator="Ctrl+P")
        process_menu.add_command(label="Run OCR", command=self.run_ocr, accelerator="Ctrl+R")
        process_menu.add_separator()
        process_menu.add_command(label="Process & OCR", command=self.process_and_ocr, accelerator="Ctrl+Shift+P")
        
        # Speech menu
        speech_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Speech", menu=speech_menu)
        speech_menu.add_command(label="Speak Text", command=self.speak_text, accelerator="Ctrl+Space")
        speech_menu.add_command(label="Stop Speaking", command=self.stop_speech)
        speech_menu.add_separator()
        speech_menu.add_command(label="TTS Settings...", command=self.show_tts_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_text())
        self.root.bind('<Control-p>', lambda e: self.process_image())
        self.root.bind('<Control-r>', lambda e: self.run_ocr())
        self.root.bind('<Control-P>', lambda e: self.process_and_ocr())
        self.root.bind('<Control-space>', lambda e: self.speak_text())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
    
    def create_toolbar(self):
        """Create the toolbar with main action buttons."""
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Open Image button
        self.btn_open = ttk.Button(
            toolbar,
            text="📁 Open Image",
            command=self.open_image
        )
        self.btn_open.grid(row=0, column=0, padx=2)
        
        # Process Image button
        self.btn_process = ttk.Button(
            toolbar,
            text="🔧 Process Image",
            command=self.process_image
        )
        self.btn_process.grid(row=0, column=1, padx=2)
        
        # Run OCR button
        self.btn_ocr = ttk.Button(
            toolbar,
            text="🔍 Run OCR",
            command=self.run_ocr
        )
        self.btn_ocr.grid(row=0, column=2, padx=2)
        
        # Process & OCR button (combined)
        self.btn_process_ocr = ttk.Button(
            toolbar,
            text="⚡ Process & OCR",
            command=self.process_and_ocr
        )
        self.btn_process_ocr.grid(row=0, column=3, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).grid(row=0, column=4, padx=10, sticky=(tk.N, tk.S))
        
        # Speak button
        self.btn_speak = ttk.Button(
            toolbar,
            text="🔊 Speak",
            command=self.speak_text
        )
        self.btn_speak.grid(row=0, column=5, padx=2)
        
        # Stop button
        self.btn_stop = ttk.Button(
            toolbar,
            text="⏹ Stop",
            command=self.stop_speech
        )
        self.btn_stop.grid(row=0, column=6, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).grid(row=0, column=7, padx=10, sticky=(tk.N, tk.S))
        
        # Deskew checkbox
        self.deskew_var = tk.BooleanVar(value=False)
        self.chk_deskew = ttk.Checkbutton(
            toolbar,
            text="Apply Deskew",
            variable=self.deskew_var
        )
        self.chk_deskew.grid(row=0, column=8, padx=2)
        
        # OCR Language selection
        ttk.Label(toolbar, text="OCR Lang:").grid(row=0, column=9, padx=(10, 2))
        self.ocr_lang_var = tk.StringVar(value="eng+vie")
        self.ocr_lang_combo = ttk.Combobox(
            toolbar,
            textvariable=self.ocr_lang_var,
            values=["eng", "vie", "eng+vie"],
            state='readonly',
            width=10
        )
        self.ocr_lang_combo.grid(row=0, column=10, padx=2)
        
        # Initially disable processing buttons
        self.update_button_states()
    
    def create_main_content(self):
        """Create the main content area with image displays and text output."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Left panel - Original Image
        left_panel = ttk.LabelFrame(main_frame, text="Original Image", padding="5")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Original image canvas with scrollbars
        self.canvas_original = tk.Canvas(left_panel, bg='gray80', width=400, height=400)
        scroll_x_orig = ttk.Scrollbar(left_panel, orient=tk.HORIZONTAL, command=self.canvas_original.xview)
        scroll_y_orig = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.canvas_original.yview)
        self.canvas_original.configure(xscrollcommand=scroll_x_orig.set, yscrollcommand=scroll_y_orig.set)
        
        self.canvas_original.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scroll_x_orig.grid(row=1, column=0, sticky=(tk.W, tk.E))
        scroll_y_orig.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Right panel - Processed Image
        right_panel = ttk.LabelFrame(main_frame, text="Processed Image", padding="5")
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Processed image canvas with scrollbars
        self.canvas_processed = tk.Canvas(right_panel, bg='gray80', width=400, height=400)
        scroll_x_proc = ttk.Scrollbar(right_panel, orient=tk.HORIZONTAL, command=self.canvas_processed.xview)
        scroll_y_proc = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.canvas_processed.yview)
        self.canvas_processed.configure(xscrollcommand=scroll_x_proc.set, yscrollcommand=scroll_y_proc.set)
        
        self.canvas_processed.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scroll_x_proc.grid(row=1, column=0, sticky=(tk.W, tk.E))
        scroll_y_proc.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bottom panel - Recognized Text
        text_panel = ttk.LabelFrame(self.root, text="Recognized Text", padding="5")
        text_panel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        text_panel.grid_rowconfigure(0, weight=1)
        text_panel.grid_columnconfigure(0, weight=1)
        
        # Text widget for OCR output
        self.text_output = scrolledtext.ScrolledText(
            text_panel,
            wrap=tk.WORD,
            width=80,
            height=10,
            font=('Arial', 11)
        )
        self.text_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure row weights for bottom panel
        self.root.grid_rowconfigure(2, weight=0, minsize=200)
    
    def create_status_bar(self):
        """Create the status bar at the bottom."""
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
        
        self.progress_bar = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=100
        )
        self.progress_bar.pack(side=tk.RIGHT, padx=2, pady=2)
    
    def update_status(self, message):
        """
        Update the status bar message.
        
        Args:
            message (str): Status message to display
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_button_states(self):
        """Update button states based on application state."""
        has_image = self.current_image_path is not None
        has_text = len(self.current_text) > 0
        
        state_process = 'normal' if has_image and not self.processing_in_progress else 'disabled'
        state_text = 'normal' if has_text and not self.tts_engine.is_busy() else 'disabled'
        
        self.btn_process.config(state=state_process)
        self.btn_ocr.config(state=state_process)
        self.btn_process_ocr.config(state=state_process)
        self.btn_speak.config(state=state_text)
    
    def open_image(self):
        """Open an image file dialog and load the selected image."""
        file_types = [
            ("Image files", "*.png *.jpg *.jpeg *.tiff *.tif *.bmp *.gif"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("TIFF files", "*.tiff *.tif"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.current_image_path = file_path
                self.display_original_image(file_path)
                self.update_status(f"Loaded: {os.path.basename(file_path)}")
                self.update_button_states()
                
                # Clear previous processed image and text
                self.canvas_processed.delete("all")
                self.text_output.delete(1.0, tk.END)
                self.current_text = ""
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def display_original_image(self, image_path):
        """
        Display the original image on the canvas.
        
        Args:
            image_path (str): Path to the image file
        """
        try:
            # Load and display image
            image = Image.open(image_path)
            
            # Resize if too large (maintain aspect ratio)
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            self.canvas_original.delete("all")
            self.canvas_original.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas_original.image = photo  # Keep a reference
            
            # Update scroll region
            self.canvas_original.config(scrollregion=self.canvas_original.bbox("all"))
        except Exception as e:
            raise RuntimeError(f"Failed to display image: {str(e)}")
    
    def display_processed_image(self, pil_image):
        """
        Display the processed image on the canvas.
        
        Args:
            pil_image: PIL Image object
        """
        try:
            # Resize if too large (maintain aspect ratio)
            image = pil_image.copy()
            max_size = (800, 800)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Update canvas
            self.canvas_processed.delete("all")
            self.canvas_processed.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas_processed.image = photo  # Keep a reference
            
            # Update scroll region
            self.canvas_processed.config(scrollregion=self.canvas_processed.bbox("all"))
        except Exception as e:
            raise RuntimeError(f"Failed to display processed image: {str(e)}")
    
    def process_image(self):
        """Process the current image using the image processor."""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        
        def process_task():
            try:
                self.processing_in_progress = True
                self.update_button_states()
                self.progress_bar.start()
                self.update_status("Processing image...")
                
                # Process image
                apply_deskew = self.deskew_var.get()
                processed = self.image_processor.process_image(
                    self.current_image_path,
                    apply_deskew=apply_deskew
                )
                
                # Display processed image
                pil_image = self.image_processor.get_processed_image_pil()
                self.display_processed_image(pil_image)
                
                self.update_status("Image processing complete")
                messagebox.showinfo("Success", "Image processing completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Image processing failed:\n{str(e)}")
                self.update_status("Image processing failed")
            finally:
                self.processing_in_progress = False
                self.progress_bar.stop()
                self.update_button_states()
        
        # Run in separate thread to keep UI responsive
        thread = threading.Thread(target=process_task, daemon=True)
        thread.start()
    
    def run_ocr(self):
        """Run OCR on the processed image (or original if not processed)."""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        
        # Check if image has been processed
        if self.image_processor.processed_image is None:
            response = messagebox.askyesno(
                "Image Not Processed",
                "The image has not been processed yet.\n"
                "Do you want to process it first?"
            )
            if response:
                self.process_and_ocr()
                return
            else:
                # Use original image
                image_to_ocr = self.current_image_path
        else:
            # Use processed image
            image_to_ocr = self.image_processor.processed_image
        
        def ocr_task():
            try:
                self.processing_in_progress = True
                self.update_button_states()
                self.progress_bar.start()
                self.update_status("Running OCR...")
                
                # Get selected language
                ocr_lang = self.ocr_lang_var.get()
                
                # Run OCR
                text = self.ocr_engine.recognize_text(image_to_ocr, psm=6, lang=ocr_lang)
                
                # Display recognized text
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(1.0, text)
                self.current_text = text
                
                self.update_status(f"OCR complete - {len(text)} characters recognized")
                
                if not text.strip():
                    messagebox.showwarning(
                        "No Text Found",
                        "No text was recognized in the image.\n"
                        "Try processing the image first or check image quality."
                    )
            except Exception as e:
                messagebox.showerror("Error", f"OCR failed:\n{str(e)}")
                self.update_status("OCR failed")
            finally:
                self.processing_in_progress = False
                self.progress_bar.stop()
                self.update_button_states()
        
        # Run in separate thread
        thread = threading.Thread(target=ocr_task, daemon=True)
        thread.start()
    
    def process_and_ocr(self):
        """Process the image and run OCR in one step."""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please open an image first.")
            return
        
        def combined_task():
            try:
                self.processing_in_progress = True
                self.update_button_states()
                self.progress_bar.start()
                
                # Step 1: Process image
                self.update_status("Processing image...")
                apply_deskew = self.deskew_var.get()
                processed = self.image_processor.process_image(
                    self.current_image_path,
                    apply_deskew=apply_deskew
                )
                
                # Display processed image
                pil_image = self.image_processor.get_processed_image_pil()
                self.display_processed_image(pil_image)
                
                # Step 2: Run OCR
                self.update_status("Running OCR...")
                ocr_lang = self.ocr_lang_var.get()
                text = self.ocr_engine.recognize_text(processed, psm=6, lang=ocr_lang)
                
                # Display recognized text
                self.text_output.delete(1.0, tk.END)
                self.text_output.insert(1.0, text)
                self.current_text = text
                
                self.update_status(f"Complete - {len(text)} characters recognized")
                
                if not text.strip():
                    messagebox.showwarning(
                        "No Text Found",
                        "No text was recognized in the image.\n"
                        "Try adjusting processing settings or check image quality."
                    )
                else:
                    messagebox.showinfo("Success", f"Processing and OCR completed!\nRecognized {len(text)} characters.")
            except Exception as e:
                messagebox.showerror("Error", f"Process failed:\n{str(e)}")
                self.update_status("Process failed")
            finally:
                self.processing_in_progress = False
                self.progress_bar.stop()
                self.update_button_states()
        
        # Run in separate thread
        thread = threading.Thread(target=combined_task, daemon=True)
        thread.start()
    
    def speak_text(self):
        """Speak the recognized text using TTS."""
        text = self.text_output.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("No Text", "No text available to speak.")
            return
        
        try:
            self.update_status("Speaking...")
            self.tts_engine.speak_async(text)
            
            # Monitor when speech is done
            def check_speech_done():
                if not self.tts_engine.is_busy():
                    self.update_status("Ready")
                    self.update_button_states()
                else:
                    self.root.after(100, check_speech_done)
            
            self.root.after(100, check_speech_done)
            self.update_button_states()
        except Exception as e:
            messagebox.showerror("Error", f"TTS failed:\n{str(e)}")
            self.update_status("TTS failed")
    
    def stop_speech(self):
        """Stop the current speech."""
        self.tts_engine.stop()
        self.update_status("Speech stopped")
        self.update_button_states()
    
    def save_text(self):
        """Save the recognized text to a file."""
        text = self.text_output.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("No Text", "No text available to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Success", f"Text saved to:\n{file_path}")
                self.update_status(f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save text:\n{str(e)}")
    
    def show_tts_settings(self):
        """Show TTS settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("TTS Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Rate setting
        ttk.Label(settings_window, text="Speaking Rate:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        rate_var = tk.IntVar(value=self.tts_engine.rate)
        rate_scale = ttk.Scale(
            settings_window,
            from_=50,
            to=300,
            variable=rate_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        rate_scale.grid(row=0, column=1, padx=10, pady=10)
        rate_label = ttk.Label(settings_window, text=f"{rate_var.get()} wpm")
        rate_label.grid(row=0, column=2, padx=10, pady=10)
        
        def update_rate_label(*args):
            rate_label.config(text=f"{rate_var.get()} wpm")
        rate_var.trace('w', update_rate_label)
        
        # Volume setting
        ttk.Label(settings_window, text="Volume:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        volume_var = tk.DoubleVar(value=self.tts_engine.volume)
        volume_scale = ttk.Scale(
            settings_window,
            from_=0.0,
            to=1.0,
            variable=volume_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        volume_scale.grid(row=1, column=1, padx=10, pady=10)
        volume_label = ttk.Label(settings_window, text=f"{int(volume_var.get()*100)}%")
        volume_label.grid(row=1, column=2, padx=10, pady=10)
        
        def update_volume_label(*args):
            volume_label.config(text=f"{int(volume_var.get()*100)}%")
        volume_var.trace('w', update_volume_label)
        
        # Voice selection
        ttk.Label(settings_window, text="Voice:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        voices = self.tts_engine.get_available_voices()
        voice_names = [f"{i}: {v.name}" for i, v in enumerate(voices)]
        voice_var = tk.StringVar(value=voice_names[0] if voice_names else "")
        voice_combo = ttk.Combobox(
            settings_window,
            textvariable=voice_var,
            values=voice_names,
            state='readonly',
            width=30
        )
        voice_combo.grid(row=2, column=1, columnspan=2, padx=10, pady=10)
        
        # Auto-detect language checkbox
        auto_detect_var = tk.BooleanVar(value=self.tts_engine.auto_detect_language)
        chk_auto_detect = ttk.Checkbutton(
            settings_window,
            text="Auto-detect language",
            variable=auto_detect_var
        )
        chk_auto_detect.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        
        # Use gTTS for Vietnamese checkbox
        gtts_vi_var = tk.BooleanVar(value=self.tts_engine.use_gtts_for_vietnamese)
        chk_gtts_vi = ttk.Checkbutton(
            settings_window,
            text="Use Google TTS for Vietnamese (better quality)",
            variable=gtts_vi_var
        )
        chk_gtts_vi.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        
        def apply_settings():
            self.tts_engine.set_rate(rate_var.get())
            self.tts_engine.set_volume(volume_var.get())
            
            # Set voice
            if voice_combo.current() >= 0:
                voice_id = voices[voice_combo.current()].id
                self.tts_engine.set_voice(voice_id=voice_id)
            
            # Set language detection settings
            self.tts_engine.set_auto_detect_language(auto_detect_var.get())
            self.tts_engine.set_use_gtts_for_vietnamese(gtts_vi_var.get())
            
            messagebox.showinfo("Success", "TTS settings applied!")
            settings_window.destroy()
        
        def test_settings():
            # Temporarily apply settings
            original_rate = self.tts_engine.rate
            original_volume = self.tts_engine.volume
            original_voice = self.tts_engine.engine.getProperty('voice')
            original_auto_detect = self.tts_engine.auto_detect_language
            original_gtts_vi = self.tts_engine.use_gtts_for_vietnamese
            
            self.tts_engine.set_rate(rate_var.get())
            self.tts_engine.set_volume(volume_var.get())
            if voice_combo.current() >= 0:
                voice_id = voices[voice_combo.current()].id
                self.tts_engine.set_voice(voice_id=voice_id)
            self.tts_engine.set_auto_detect_language(auto_detect_var.get())
            self.tts_engine.set_use_gtts_for_vietnamese(gtts_vi_var.get())
            
            # Speak test phrase (English and Vietnamese)
            test_text = "This is a test. Đây là bài kiểm tra."
            self.tts_engine.speak(test_text, blocking=False)
        
        ttk.Button(button_frame, text="Test", command=test_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Apply", command=apply_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_about(self):
        """Show about dialog."""
        about_text = """VisionSpeak
Adaptive OCR and TTS Desktop Application

Version: 1.1

An advanced application for optical character recognition
with intelligent image pre-processing and text-to-speech
capabilities.

Features:
• Advanced image pre-processing
• Adaptive thresholding for uneven lighting
• Automatic text inversion detection
• Noise reduction and enhancement
• Multi-language OCR (English, Vietnamese)
• Text-to-Speech with automatic language detection
• Google TTS for Vietnamese (high quality)
• Support for multiple image formats

Developed for real-world OCR scenarios with
challenging image conditions.
"""
        messagebox.showinfo("About VisionSpeak", about_text)
    
    def show_instructions(self):
        """Show instructions dialog."""
        instructions = """How to Use VisionSpeak:

1. Open an Image
   Click 'Open Image' or press Ctrl+O to load an image file.

2. Select OCR Language
   Choose the appropriate language from the 'OCR Lang' dropdown:
   • eng - For English text
   • vie - For Vietnamese text
   • eng+vie - For mixed language text

3. Process the Image (Optional but Recommended)
   Click 'Process Image' to apply advanced pre-processing:
   • Noise reduction
   • Adaptive thresholding
   • Automatic text inversion detection
   • Optional deskewing

4. Run OCR
   Click 'Run OCR' to extract text from the image.
   Or use 'Process & OCR' to do both steps at once.

5. Listen to Text
   Click 'Speak' to hear the recognized text.
   • Automatic language detection enabled by default
   • Vietnamese text uses Google TTS for better quality
   • Use 'Stop' to interrupt speech

6. Save Results
   Save recognized text using File > Save Text.

Tips:
• Enable 'Apply Deskew' for rotated images
• Process images before OCR for best results
• Adjust TTS settings in Speech > TTS Settings
• Use keyboard shortcuts for faster workflow
• For Vietnamese: Make sure to install Vietnamese language pack for Tesseract
"""
        messagebox.showinfo("Instructions", instructions)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = VisionSpeakApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

