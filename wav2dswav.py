import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pydub import AudioSegment
from ttkthemes import ThemedTk
from pathlib import Path
from languages import translations

def update_text(language):
    text_vars = {
        'header_text': header_label,
        'folder_label': folder_label,
        'browse_button': browse_button,
        'fade_option': fade_option,
        'suffix_option': suffix_option,
        'suffix_label': suffix_label,
        'prefix_option': prefix_option,
        'prefix_label': prefix_label,
        'remove_prefixes_option': remove_prefixes_option,
        'prefix_count_label': prefix_count_label,
        'start_button': start_button,
        'no_files': no_files_message,
        'processing_done': processing_done_message,
        'choose_folder': choose_folder_message,
        'error_processing': error_processing_message
    }

    for key, label in text_vars.items():
        if key in translations[language]:
            label.config(text=translations[language][key])

def remove_n_prefixes(filename, count):
    parts = filename.split('_', count)
    if len(parts) > count:
        return parts[-1]
    return filename

def process_wav(filepath, output_folder, apply_fade, suffixes, prefixes, remove_prefixes, prefix_count):
    try:
        audio = AudioSegment.from_wav(filepath)
        audio = audio.set_channels(1).set_sample_width(2)

        if apply_fade:
            fade_duration = min(len(audio), 150)
            audio = audio.fade_in(fade_duration).fade_out(fade_duration)

        filename = os.path.basename(filepath)
        filename_wo_ext = os.path.splitext(filename)[0]

        for suffix in suffixes:
            if suffix and suffix in filename_wo_ext:
                filename_wo_ext = filename_wo_ext.replace(suffix, "")

        if remove_prefixes:
            filename_wo_ext = remove_n_prefixes(filename_wo_ext, prefix_count)
        else:
            for prefix in prefixes:
                if prefix and filename_wo_ext.startswith(prefix):
                    filename_wo_ext = filename_wo_ext[len(prefix):]

        new_filename = filename_wo_ext.strip("_- ") + ".wav"
        output_path = os.path.join(output_folder, new_filename)
        audio.export(output_path, format="wav")
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def start_gui():
    global header_label, folder_label, browse_button, fade_option, suffix_option, suffix_label
    global prefix_option, prefix_label, remove_prefixes_option, prefix_count_label, start_button
    global no_files_message, processing_done_message, choose_folder_message, error_processing_message

    root = ThemedTk()
    root.get_themes()
    root.set_theme("arc")
    root.title("DiffSinger WAV Segments Tool by keirokeer")

    folder_path = tk.StringVar()
    suffix_input = tk.StringVar()
    prefix_input = tk.StringVar()
    prefix_count = tk.IntVar(value=1)
    apply_fade = tk.BooleanVar()
    apply_suffix_removal = tk.BooleanVar()
    apply_prefix_removal = tk.BooleanVar()
    remove_prefixes = tk.BooleanVar()

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            folder_path.set(path)

    def start_conversion():
        folder = folder_path.get()
        if not folder:
            messagebox.showwarning("Error", choose_folder_message)
            return

        wav_files = list(Path(folder).glob("*.wav"))
        if not wav_files:
            messagebox.showinfo("No files", no_files_message)
            return

        suffixes = [s.strip() for s in suffix_input.get().split(",")] if apply_suffix_removal.get() else []
        prefixes = [p.strip() for p in prefix_input.get().split(",")] if apply_prefix_removal.get() else []
        count = prefix_count.get() if remove_prefixes.get() else 0

        output_folder = Path(folder) / "converted"
        output_folder.mkdir(exist_ok=True)

        success_count = sum(process_wav(f, output_folder, apply_fade.get(), suffixes, prefixes, remove_prefixes.get(), count) for f in wav_files)

        messagebox.showinfo("Done", f"{processing_done_message} {success_count}")

    header_label = ttk.Label(root, text=translations['en']['header_text'], anchor="center", justify="center", font=("Segoe UI", 10))
    header_label.grid(row=0, column=0, columnspan=4, pady=(10, 15))

    folder_label = ttk.Label(root, text=translations['en']['folder_label'])
    folder_label.grid(row=1, column=0, pady=5, sticky="w")
    
    folder_entry = ttk.Entry(root, textvariable=folder_path, width=50)
    folder_entry.grid(row=1, column=1, padx=5, columnspan=2)

    browse_button = ttk.Button(root, text=translations['en']['browse_button'], command=browse_folder)
    browse_button.grid(row=1, column=3, padx=5)

    fade_option = ttk.Checkbutton(root, text=translations['en']['fade_option'], variable=apply_fade)
    fade_option.grid(row=2, column=0, columnspan=4, sticky="w")

    suffix_option = ttk.Checkbutton(root, text=translations['en']['suffix_option'], variable=apply_suffix_removal)
    suffix_option.grid(row=3, column=0, columnspan=4, sticky="w")

    suffix_label = ttk.Label(root, text=translations['en']['suffix_label'])
    suffix_label.grid(row=4, column=0, pady=5, sticky="w")

    suffix_input_entry = ttk.Entry(root, textvariable=suffix_input, width=50)
    suffix_input_entry.grid(row=4, column=1, padx=5, columnspan=3)

    prefix_option = ttk.Checkbutton(root, text=translations['en']['prefix_option'], variable=apply_prefix_removal)
    prefix_option.grid(row=5, column=0, columnspan=4, sticky="w")

    prefix_label = ttk.Label(root, text=translations['en']['prefix_label'])
    prefix_label.grid(row=6, column=0, pady=5, sticky="w")

    prefix_input_entry = ttk.Entry(root, textvariable=prefix_input, width=50)
    prefix_input_entry.grid(row=6, column=1, padx=5, columnspan=3)

    remove_prefixes_option = ttk.Checkbutton(root, text=translations['en']['remove_prefixes_option'], variable=remove_prefixes)
    remove_prefixes_option.grid(row=7, column=0, columnspan=4, sticky="w")

    prefix_count_label = ttk.Label(root, text=translations['en']['prefix_count_label'])
    prefix_count_label.grid(row=8, column=0, pady=5, sticky="w")

    prefix_count_spinbox = ttk.Spinbox(root, from_=1, to=3, textvariable=prefix_count, width=5)
    prefix_count_spinbox.grid(row=8, column=1, sticky="w")

    start_button = ttk.Button(root, text=translations['en']['start_button'], command=start_conversion)
    start_button.grid(row=10, column=0, columnspan=4, pady=10)

    no_files_message = translations['en']['no_files']
    processing_done_message = translations['en']['processing_done']
    choose_folder_message = translations['en']['choose_folder']
    error_processing_message = translations['en']['error_processing']

    language_choice = ttk.Combobox(root, values=["English", "Русский", "Français", "한국어", "Español", "Português", "Polski", "中文", "日本語"], state="readonly")
    language_choice.current(0)  # English default
    language_choice.grid(row=9, column=0, columnspan=4, pady=10)
    language_choice.bind("<<ComboboxSelected>>", lambda event: update_text(
        "en" if language_choice.get() == "English" else
        "ru" if language_choice.get() == "Русский" else
        "fr" if language_choice.get() == "Français" else
        "ko" if language_choice.get() == "한국어" else
        "es" if language_choice.get() == "Español" else
        "pt" if language_choice.get() == "Português" else
        "pl" if language_choice.get() == "Polski" else
        "zh" if language_choice.get() == "中文" else
        "ja" if language_choice.get() == "日本語" else
        "en"))

    root.mainloop()

if __name__ == "__main__":
    start_gui()
