import os
import time
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import re
import tiktoken

# Load environment variables from .env file
load_dotenv()

class BookTranslator:
    def __init__(self, api_key=None, model=None):
        """
        Initialize the book translator with OpenAI API.
        
        :param api_key: OpenAI API key (optional, will use env variable if not provided)
        :param model: OpenAI model to use (optional, will use env variable or default)
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key is None:
                raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        self.encoding = tiktoken.encoding_for_model(self.model)
        self.max_tokens = 2000  # Conservative limit for input tokens
        
    def count_tokens(self, text):
        """Count the number of tokens in a text."""
        return len(self.encoding.encode(text))
        
    def _split_text(self, text):
        """
        Split text into pages and chunks while preserving page numbers and keeping within token limits.
        """
        # Split text into pages
        pages = re.split(r'\n=+\n', text)
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for page in pages:
            if not page.strip():
                continue
                
            # Extract page number if present
            page_match = re.search(r'Page (\d+)', page)
            page_num = page_match.group(0) if page_match else None
            
            # Split page content into paragraphs
            content = re.sub(r'Page \d+\n-+\n', '', page).strip()
            if not content:
                continue
            
            paragraphs = content.split('\n\n')
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                    
                # Create chunk with page number and paragraph
                chunk_text = f"{page_num}\n{para}" if page_num else para
                chunk_tokens = self.count_tokens(chunk_text)
                
                if chunk_tokens > self.max_tokens:
                    # If a single paragraph is too long, split it into sentences
                    sentences = re.split(r'([.!?])\s+', para)
                    current_sentence_chunk = []
                    current_sentence_tokens = 0
                    
                    for i in range(0, len(sentences), 2):
                        if i + 1 < len(sentences):
                            sentence = sentences[i] + sentences[i+1]  # Combine with punctuation
                        else:
                            sentence = sentences[i]
                            
                        sentence_text = f"{page_num}\n{sentence}" if page_num else sentence
                        sentence_tokens = self.count_tokens(sentence_text)
                        
                        if current_sentence_tokens + sentence_tokens > self.max_tokens:
                            # Save current chunk and start new one
                            if current_sentence_chunk:
                                chunks.append('\n'.join(current_sentence_chunk))
                            current_sentence_chunk = [sentence_text]
                            current_sentence_tokens = sentence_tokens
                        else:
                            current_sentence_chunk.append(sentence_text)
                            current_sentence_tokens += sentence_tokens
                    
                    if current_sentence_chunk:
                        chunks.append('\n'.join(current_sentence_chunk))
                else:
                    chunks.append(chunk_text)
            
        return chunks

    def translate_text(self, text):
        """
        Translate text using OpenAI's ChatGPT.
        """
        system_prompt = """You are a professional translator specializing in Arabic to English translation.
        Translate the following Arabic text to English, maintaining the original meaning and style.
        If the text contains a page number, preserve it in the translation.
        Focus on accuracy and clarity in the translation."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate this text from Arabic to English:\n\n{text}"}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error during translation: {str(e)}")
            return None

    def translate_book(self, input_file, output_file):
        """
        Translate an entire book from a text file while preserving pagination.
        
        :param input_file: Path to the input Arabic text file
        :param output_file: Path to save the translated text file
        """
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                book_text = f.read()

            # Split into chunks preserving page structure
            chunks = self._split_text(book_text)
            translated_sections = []
            
            # Translate header separately if present
            header_match = re.match(r'(={80}\n.*?\n.*?\n={80})', book_text, re.DOTALL)
            if header_match:
                header = header_match.group(1)
                translated_header = self.translate_text(header)
                if translated_header:
                    translated_sections.append(translated_header)

            # Translate each chunk with progress bar
            for chunk in tqdm(chunks, desc="Translating"):
                chunk_tokens = self.count_tokens(chunk)
                print(f"Processing chunk with {chunk_tokens} tokens")
                
                translated_chunk = self.translate_text(chunk)
                if translated_chunk:
                    translated_sections.append(translated_chunk)
                    # Add a small delay to avoid rate limits
                    time.sleep(2)  # Increased delay to be safer with API limits
                else:
                    print(f"Warning: Failed to translate chunk")

            # Combine all translations
            translated_text = '\n\n'.join(translated_sections)

            # Write translated text to output file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_text)

            print(f"Book translation completed. Output saved to {output_file}")
            
        except Exception as e:
            print(f"Error during book translation: {str(e)}")

def main():
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Please set your OpenAI API key in the OPENAI_API_KEY environment variable")
        return

    translator = BookTranslator(api_key=api_key)
    
    # Example usage
    input_book_path = 'kafiah.txt'
    output_book_path = 'kafiah_english.txt'
    
    translator.translate_book(input_book_path, output_book_path)

if __name__ == '__main__':
    main()
