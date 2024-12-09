def merge_translations(arabic_file, english_file, output_file):
    """
    Merge Arabic and English translations, with Arabic text followed by its English translation.
    Preserves page numbers and formatting.
    """
    try:
        # Read both files
        with open(arabic_file, 'r', encoding='utf-8') as f:
            arabic_lines = f.readlines()
        with open(english_file, 'r', encoding='utf-8') as f:
            english_lines = f.readlines()

        # Process lines and merge
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write('=' * 80 + '\n')
            f.write('Arabic-English Translation\n')
            f.write('=' * 80 + '\n\n')

            ar_idx = 0
            en_idx = 0

            while ar_idx < len(arabic_lines) and en_idx < len(english_lines):
                ar_line = arabic_lines[ar_idx].strip()
                en_line = english_lines[en_idx].strip()

                # Skip empty lines
                if not ar_line:
                    ar_idx += 1
                    continue
                if not en_line:
                    en_idx += 1
                    continue

                # Handle page markers
                if ar_line.startswith('Page '):
                    f.write('\n' + '=' * 40 + '\n')
                    f.write(ar_line + '\n')
                    f.write('-' * 40 + '\n\n')
                    ar_idx += 1
                    # Find and skip corresponding English page marker
                    while en_idx < len(english_lines) and not english_lines[en_idx].strip().startswith('Page '):
                        en_idx += 1
                    en_idx += 1
                    continue

                # Write Arabic text with [Arabic] marker
                f.write('[Arabic]\n')
                f.write(ar_line + '\n\n')

                # Write English translation with [English] marker
                f.write('[English]\n')
                f.write(en_line + '\n')
                f.write('-' * 40 + '\n\n')

                ar_idx += 1
                en_idx += 1

        print(f"Successfully merged translations into: {output_file}")

    except Exception as e:
        print(f"Error merging translations: {str(e)}")

def main():
    arabic_file = 'kafiah.txt'
    english_file = 'kafiah_english.txt'
    output_file = 'kafiah_merged.txt'
    
    merge_translations(arabic_file, english_file, output_file)

if __name__ == '__main__':
    main()
