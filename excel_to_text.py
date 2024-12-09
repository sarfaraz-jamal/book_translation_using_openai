import pandas as pd
import os

def excel_to_formatted_text(excel_file, output_file, sheet_name=0):
    """
    Convert Excel file to a formatted text file with sections and headings,
    preserving pagination and text structure.
    
    :param excel_file: Path to the Excel file
    :param output_file: Path to save the formatted text file
    :param sheet_name: Name or index of the sheet to process (default: 0 for first sheet)
    """
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        # Create a new file or overwrite existing
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write('=' * 80 + '\n')
            f.write('كفية المتحفظ ونهاية المتلفظ\n')  # Arabic title
            f.write(f'Source: {os.path.basename(excel_file)}\n')
            f.write('=' * 80 + '\n\n')
            
            current_page = None
            
            # Process each row
            for index, row in df.iterrows():
                text = row[4] if not pd.isna(row[4]) else ""
                page_num = int(row[5]) if not pd.isna(row[5]) else None
                
                # If we have a new page number, add page marker
                if page_num is not None and page_num != current_page:
                    if current_page is not None:  # Not the first page
                        f.write('\n' + '=' * 40 + '\n')
                    f.write(f'\nPage {page_num}\n')
                    f.write('-' * 40 + '\n\n')
                    current_page = page_num
                
                # Write the text content if it exists
                if text:
                    f.write(str(text) + '\n\n')
            
            # End of document marker
            f.write('\n' + '=' * 80 + '\n')
            f.write('End of Document\n')
            f.write('=' * 80)
            
        print(f"Successfully created formatted text file: {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

def main():
    # Update these paths as needed
    excel_file = "my kafiah-1.xlsx"
    output_file = "kafiah.txt"
    
    try:
        excel_to_formatted_text(excel_file, output_file)
    except Exception as e:
        print(f"Failed to convert Excel file: {str(e)}")

if __name__ == '__main__':
    main()