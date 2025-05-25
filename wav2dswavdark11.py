import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pydub import AudioSegment
from ttkthemes import ThemedTk
from pathlib import Path

# Словари для перевода
translations = {
    'en': {
        'header_text': "This utility will help you work with segmented WAV files from DiffSinger!\nSpecifically, it is designed to reformat .wav files after batch cleaning from noise, echo, etc., back to the original DiffSinger format.\nIt converts everything to mono 16-bit and can remove extra suffixes after processing in third-party software,\nand optionally applies a smooth fade-in/fade-out to your audio!\nAll modified files are saved to the 'converted' folder.",
        'folder_label': "Folder with WAV files:",
        'browse_button': "Browse...",
        'fade_option': "Apply fade-in/fade-out (0.15 sec)",
        'suffix_option': "Remove suffixes from file names",
        'suffix_label': "Suffixes (comma separated, e.g. _edited, _no_reverb):",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "Start Conversion",
        'no_files': "No .wav files in the folder.",
        'processing_done': "Processed files: ",
        'choose_folder': "Please choose a folder.",
        'error_processing': "Error processing the file: "
    },
    'ru': {
        'header_text': "Эта утилита поможет вам в работе с сегментированными WAV файлами Диффсингера!\nВ частности, она предназначена для форматирования файлов формата .wav после массовой очистки от шумов, эхо и тд в исходный формат Диффсингера.\nОна изменяет всё в формат mono 16-bit, а также может убрать лишние суффиксы после обработки в сторонних программах\nи дополнительно сделать плавный fade-in/fade-out ваших аудио!\nВсе изменённые файлы сохраняются в папку converted.",
        'folder_label': "Папка с WAV файлами:",
        'browse_button': "Обзор...",
        'fade_option': "Добавить fade-in/fade-out (0.15 сек)",
        'suffix_option': "Удалить суффиксы из имени файла",
        'suffix_label': "Суффиксы через запятую (например: _edited, _no_reverb):",
        'prefix_option': "Удалить префиксы из имени файла",
        'prefix_label': "Префиксы через запятую (например: 1_, 2_):",
        'remove_all_prefixes_option': "Удалить все префиксы до первого '_' (например: '1_song.wav' → 'song.wav')",
        'start_button': "Начать конвертацию",
        'no_files': "В папке нет .wav файлов.",
        'processing_done': "Обработано файлов: ",
        'choose_folder': "Выберите папку.",
        'error_processing': "Ошибка при обработке файла: "
    },
    'fr': {
        'header_text': "Cet utilitaire vous aidera à travailler avec les fichiers WAV segmentés de DiffSinger !\nIl est spécialement conçu pour reformater les fichiers .wav après un nettoyage massif du bruit, de l’écho, etc., au format original de DiffSinger.\nIl convertit tout en mono 16 bits, peut supprimer les suffixes superflus ajoutés par d’autres logiciels,\net appliquer un fondu d’entrée/de sortie à vos fichiers audio.\nTous les fichiers modifiés sont enregistrés dans le dossier converted.",
        'folder_label': "Dossier avec des fichiers WAV:",
        'browse_button': "Parcourir...",
        'fade_option': "Appliquer fade-in/fade-out (0.15 sec)",
        'suffix_option': "Supprimer les suffixes des noms de fichiers",
        'suffix_label': "Suffixes (séparés par des virgules, par exemple: _edited, _no_reverb):",
        'prefix_option': "Supprimer les préfixes des noms de fichiers",
        'prefix_label': "Préfixes (séparés par des virgules, par exemple: 1_, 2_):",
        'remove_all_prefixes_option': "Supprimer tous les préfixes avant le premier '_' (ex: '1_song.wav' → 'song.wav')",
        'start_button': "Commencer la conversion",
        'no_files': "Pas de fichiers .wav dans le dossier.",
        'processing_done': "Fichiers traités: ",
        'choose_folder': "Veuillez choisir un dossier.",
        'error_processing': "Erreur lors du traitement du fichier: "
    },
    'ko': {
        'header_text': "이 유틸리티는 DiffSinger의 세분화된 WAV 파일 작업을 도와줍니다!\n특히 노이즈, 에코 등을 일괄 제거한 후 .wav 파일을 DiffSinger의 원래 형식으로 다시 포맷하는 데 사용됩니다.\n모든 오디오를 모노 16비트로 변환하며, 외부 프로그램으로 처리된 파일의 불필요한 접미사를 제거하고\n부드러운 페이드 인/아웃 효과도 적용할 수 있습니다!\n모든 변경된 파일은 'converted' 폴더에 저장됩니다.",
        'folder_label': "WAV 파일이 있는 폴더:",
        'browse_button': "찾아보기...",
        'fade_option': "페이드 인/아웃 적용 (0.15초)",
        'suffix_option': "파일 이름에서 접미사 제거",
        'suffix_label': "접미사 (쉼표로 구분, 예: _edited, _no_reverb):",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "변환 시작",
        'no_files': "폴더에 .wav 파일이 없습니다.",
        'processing_done': "처리된 파일: ",
        'choose_folder': "폴더를 선택하세요.",
        'error_processing': "파일 처리 중 오류 발생: "
    },
    'es': {
        'header_text': "¡Esta utilidad te ayudará a trabajar con archivos WAV segmentados de DiffSinger!\nEstá diseñada para volver a formatear archivos .wav tras una limpieza masiva de ruido, eco, etc., al formato original de DiffSinger.\nConvierte todo a mono 16 bits, puede eliminar sufijos innecesarios añadidos por otros programas\ny aplicar un fundido de entrada/salida suave a tu audio.\nTodos los archivos modificados se guardan en la carpeta converted.",
        'folder_label': "Carpeta con archivos WAV:",
        'browse_button': "Examinar...",
        'fade_option': "Aplicar fade-in/fade-out (0.15 seg)",
        'suffix_option': "Eliminar sufijos de los nombres de los archivos",
        'suffix_label': "Sufijos (separados por comas, p. ej.: _edited, _no_reverb):",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "Comenzar conversión",
        'no_files': "No hay archivos .wav en la carpeta.",
        'processing_done': "Archivos procesados: ",
        'choose_folder': "Por favor, elija una carpeta.",
        'error_processing': "Error al procesar el archivo: "
    },
    'pt': {
        'header_text': "Este utilitário vai te ajudar a trabalhar com arquivos WAV segmentados do DiffSinger!\nÉ projetado para reformatar arquivos .wav após a limpeza em massa de ruídos, ecos, etc., de volta ao formato original do DiffSinger.\nConverte tudo para mono 16-bit, pode remover sufixos extras de programas externos\ne aplicar um fade-in/fade-out suave no seu áudio!\nTodos os arquivos modificados são salvos na pasta converted.",
        'folder_label': "Pasta com arquivos WAV:",
        'browse_button': "Procurar...",
        'fade_option': "Aplicar fade-in/fade-out (0.15 seg)",
        'suffix_option': "Remover sufixos dos nomes dos arquivos",
        'suffix_label': "Sufixos (separados por vírgulas, ex: _edited, _no_reverb):",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "Iniciar conversão",
        'no_files': "Não há arquivos .wav na pasta.",
        'processing_done': "Arquivos processados: ",
        'choose_folder': "Por favor, escolha uma pasta.",
        'error_processing': "Erro ao processar o arquivo: "
    },
    'pl': {
        'header_text': "To narzędzie pomoże ci pracować z segmentowanymi plikami WAV z DiffSingera!\nJest przeznaczone do ponownego formatowania plików .wav po masowym usuwaniu szumów, echa itp., z powrotem do oryginalnego formatu DiffSingera.\nKonwertuje wszystko do formatu mono 16-bit, może usunąć zbędne sufiksy po obróbce w zewnętrznych programach\ni opcjonalnie zastosować łagodne zanikanie (fade-in/fade-out) dźwięku.\nWszystkie zmodyfikowane pliki są zapisywane w folderze converted.",
    	'folder_label': "Folder z plikami WAV:",
    	'browse_button': "Przeglądaj...",
    	'fade_option': "Zastosuj fade-in/fade-out (0.15 sek)",
    	'suffix_option': "Usuń sufiksy z nazw plików",
    	'suffix_label': "Sufiksy (oddzielone przecinkami, np. _edited, _no_reverb):",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
    	'start_button': "Rozpocznij konwersję",
    	'no_files': "Brak plików .wav w folderze.",
    	'processing_done': "Przetworzone pliki: ",
    	'choose_folder': "Wybierz folder.",
    	'error_processing': "Błąd podczas przetwarzania pliku: "
    },
    'zh': {
        'header_text': "此工具可帮助您处理 DiffSinger 的分段 WAV 文件！\n它专为在批量去除噪音、回声等后，将 .wav 文件重新格式化为 DiffSinger 原始格式而设计。\n它会将所有音频转换为单声道 16 位，并可删除第三方软件处理后多余的后缀，\n还可以为音频添加平滑的淡入/淡出效果！\n所有修改后的文件都会保存在 converted 文件夹中。",
        'folder_label': "包含 WAV 文件的文件夹：",
        'browse_button': "浏览...",
        'fade_option': "应用淡入/淡出 (0.15秒)",
        'suffix_option': "从文件名中移除后缀",
        'suffix_label': "后缀（以逗号分隔，例如：_edited, _no_reverb）：",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "开始转换",
        'no_files': "文件夹中没有 .wav 文件。",
        'processing_done': "处理的文件：",
        'choose_folder': "请选择文件夹。",
        'error_processing': "处理文件时出错："
    },
    'ja': {
        'header_text': "このユーティリティは、DiffSinger のセグメント化された WAV ファイルの処理をサポートします！\n特に、ノイズやエコーなどを一括で除去した後、.wav ファイルを元の DiffSinger フォーマットに再フォーマットするために設計されています。\nすべてをモノラル16ビットに変換し、他のソフトで処理されたファイルの不要なサフィックスを削除し、\nオーディオにスムーズなフェードイン/フェードアウトを追加することもできます。\nすべての変更されたファイルは「converted」フォルダに保存されます。",
        'folder_label': "WAV ファイルがあるフォルダー:",
        'browse_button': "参照...",
        'fade_option': "フェードイン/フェードアウトを適用 (0.15秒)",
        'suffix_option': "ファイル名からサフィックスを削除",
        'suffix_label': "サフィックス（カンマ区切り、例：_edited, _no_reverb）：",
        'prefix_option': "Remove prefixes from file names",
        'prefix_label': "Prefixes (comma separated, e.g. 1_, 2_):",
        'remove_all_prefixes_option': "Remove all prefixes before first '_' (e.g. '1_song.wav' → 'song.wav')",
        'start_button': "変換開始",
        'no_files': "フォルダーに .wav ファイルがありません。",
        'processing_done': "処理されたファイル：",
        'choose_folder': "フォルダーを選択してください。",
        'error_processing': "ファイル処理中にエラーが発生しました："
    }
}

# Функция для обновления текста интерфейса в зависимости от выбранного языка
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
        'remove_all_prefixes_option': remove_all_prefixes_option,
        'start_button': start_button,
        'no_files': no_files_message,
        'processing_done': processing_done_message,
        'choose_folder': choose_folder_message,
        'error_processing': error_processing_message
    }

    for key, label in text_vars.items():
        label.config(text=translations[language][key])

# Функция обработки одного файла
def process_wav(filepath, output_folder, apply_fade, suffixes, prefixes, remove_all_prefixes):
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

        if remove_all_prefixes:
            parts = filename_wo_ext.split('_', 1)
            if len(parts) > 1:
                filename_wo_ext = parts[1]
        else:
            for prefix in prefixes:
                if prefix and filename_wo_ext.startswith(prefix):
                    filename_wo_ext = filename_wo_ext[len(prefix):]

        new_filename = filename_wo_ext.strip("_- ") + ".wav"
        output_path = os.path.join(output_folder, new_filename)
        audio.export(output_path, format="wav")
        return True
    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")
        return False

# Основной GUI
def start_gui():
    global header_label
    global folder_label, browse_button, fade_option, suffix_option, suffix_label, start_button
    global prefix_option, prefix_label, remove_all_prefixes_option
    global no_files_message, processing_done_message, choose_folder_message, error_processing_message

    root = ThemedTk()
    root.get_themes()
    root.set_theme("arc")

    root.title("DiffSinger WAV Segments Tool by keirokeer")

    folder_path = tk.StringVar()
    suffix_input = tk.StringVar()
    prefix_input = tk.StringVar()
    apply_fade = tk.BooleanVar()
    apply_suffix_removal = tk.BooleanVar()
    apply_prefix_removal = tk.BooleanVar()
    remove_all_prefixes = tk.BooleanVar()

    def browse_folder():
        path = filedialog.askdirectory()
        if path:
            folder_path.set(path)

    def start_conversion():
        folder = folder_path.get()
        if not folder:
            messagebox.showwarning("Ошибка", choose_folder_message)
            return

        wav_files = list(Path(folder).glob("*.wav"))
        if not wav_files:
            messagebox.showinfo("Нет файлов", no_files_message)
            return

        suffixes = [s.strip() for s in suffix_input.get().split(",")] if apply_suffix_removal.get() else []
        prefixes = [p.strip() for p in prefix_input.get().split(",")] if apply_prefix_removal.get() else []

        output_folder = Path(folder) / "converted"
        output_folder.mkdir(exist_ok=True)

        success_count = sum(process_wav(f, output_folder, apply_fade.get(), suffixes, prefixes, remove_all_prefixes.get()) for f in wav_files)

        messagebox.showinfo("Готово", f"{processing_done_message} {success_count}")

    # Интерфейс
    header_label = ttk.Label(root, text=translations['en']['header_text'], anchor="center", justify="center", font=("Segoe UI", 10))
    header_label.grid(row=0, column=0, columnspan=3, pady=(10, 15))

    folder_label = ttk.Label(root, text=translations['en']['folder_label'])
    folder_label.grid(row=1, column=0, pady=5, sticky="w")
    
    folder_entry = ttk.Entry(root, textvariable=folder_path, width=50)
    folder_entry.grid(row=1, column=1, padx=5)

    browse_button = ttk.Button(root, text=translations['en']['browse_button'], command=browse_folder)
    browse_button.grid(row=1, column=2, padx=5)

    fade_option = ttk.Checkbutton(root, text=translations['en']['fade_option'], variable=apply_fade)
    fade_option.grid(row=2, column=0, columnspan=3, sticky="w")

    suffix_option = ttk.Checkbutton(root, text=translations['en']['suffix_option'], variable=apply_suffix_removal)
    suffix_option.grid(row=3, column=0, columnspan=3, sticky="w")

    suffix_label = ttk.Label(root, text=translations['en']['suffix_label'])
    suffix_label.grid(row=4, column=0, pady=5, sticky="w")

    suffix_input_entry = ttk.Entry(root, textvariable=suffix_input, width=50)
    suffix_input_entry.grid(row=4, column=1, padx=5)

    prefix_option = ttk.Checkbutton(root, text=translations['en']['prefix_option'], variable=apply_prefix_removal)
    prefix_option.grid(row=5, column=0, columnspan=3, sticky="w")

    prefix_label = ttk.Label(root, text=translations['en']['prefix_label'])
    prefix_label.grid(row=6, column=0, pady=5, sticky="w")

    prefix_input_entry = ttk.Entry(root, textvariable=prefix_input, width=50)
    prefix_input_entry.grid(row=6, column=1, padx=5)

    remove_all_prefixes_option = ttk.Checkbutton(root, text=translations['en']['remove_all_prefixes_option'], variable=remove_all_prefixes)
    remove_all_prefixes_option.grid(row=7, column=0, columnspan=3, sticky="w")

    start_button = ttk.Button(root, text=translations['en']['start_button'], command=start_conversion)
    start_button.grid(row=9, column=0, columnspan=3, pady=10)

    # Сообщения
    no_files_message = translations['en']['no_files']
    processing_done_message = translations['en']['processing_done']
    choose_folder_message = translations['en']['choose_folder']
    error_processing_message = translations['en']['error_processing']

    # Выпадающий список для выбора языка
    language_choice = ttk.Combobox(root, values=["English", "Русский", "Français", "한국어", "Español", "Português", "Polski", "中文", "日本語"], state="readonly")
    language_choice.current(0)  # Устанавливаем английский по умолчанию
    language_choice.grid(row=8, column=0, columnspan=3, pady=10)
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
