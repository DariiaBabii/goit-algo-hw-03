# Напишіть програму на Python, яка рекурсивно копіює файли у вихідній директорії, 
# переміщає їх до нової директорії та сортує в піддиректорії, 
# назви яких базуються на розширенні файлів.

from pathlib import Path
import shutil
import argparse

def parse_arguments():

# аналізуємо дані з командного рядка
    parser = argparse.ArgumentParser(description="Copy files from source to destination sorted by file extension.")
    parser.add_argument('source', type=str, help='Path to the source directory')
    parser.add_argument('-d', '--destination', type=str, default='dist', help='Path to the destination directory (default: dist)')
    
    args = parser.parse_args()
    return args.source, args.destination

def create_target_directory(base_dir: Path, extension: str) -> Path:

# Створюємо цільовий каталог для вказаного розширення файлу, якщо його не існує.

    target_dir = base_dir / extension
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    return target_dir

def process_files(source_dir: Path, target_base_dir: Path) -> None:

# Рекурсивно обробляємо файли у вихідному каталозі, сортуючи їх у підкаталоги на основі розширень файлів.
    
    for item in source_dir.iterdir():
        try:
            if item.is_file():
                extension = item.suffix[1:]  #  Отримуємо розширення файла
                target_dir = create_target_directory(target_base_dir, extension)
                shutil.copy(item, target_dir / item.name)
                print(f"Copied '{item}' to '{target_dir / item.name}'")

            elif item.is_dir():
                print(f"Entering directory '{item}'")
                process_files(item, target_base_dir)
        except Exception as e:
            print(f"Error processing file/directory {item}: {e}")

if __name__ == "__main__":
    source_path, destination_path = parse_arguments()
    source_dir = Path(source_path)
    destination_dir = Path(destination_path)

    if not source_dir.exists() or not source_dir.is_dir():
        print(f"Error: Source directory '{source_dir}' does not exist or is not a directory.")
        exit(1)

    if not destination_dir.exists():
        destination_dir.mkdir(parents=True)

    process_files(source_dir, destination_dir)
