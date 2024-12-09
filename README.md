# Arabic Book Translation Script using ChatGPT

## Overview
This Python script uses OpenAI's ChatGPT API to translate Arabic books into English. It handles long texts by breaking them into manageable chunks and translating each chunk separately.

## Prerequisites
- Python 3.7+
- OpenAI API key

## Installation
1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your environment variables:
   - Copy `.env.example` to `.env`:
     ```
     # On Windows
     copy .env.example .env
     
     # On Unix/MacOS
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key
   - Optionally configure the model (GPT-3.5-turbo or GPT-4)

## Usage
1. Place your Arabic book text file in the project directory
2. Update `input_book_path` and `output_book_path` in `book_translator.py`
3. Run the script:
   ```
   python book_translator.py
   ```

## Features
- Uses ChatGPT for high-quality translations
- Handles large texts by splitting into chunks
- Progress tracking with tqdm
- Built-in rate limiting to avoid API errors
- Error handling and logging

## Notes
- Translation costs will depend on your OpenAI API plan and text length
- Default model is gpt-3.5-turbo (you can change to gpt-4 in the code)
- Includes automatic retry logic for failed translations
