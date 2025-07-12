import os
import re
from collections import Counter

def extract_translated_titles(file_path):
    titles = []
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith(" Title:"):
            title = line.replace(" Title:", "").strip()
            titles.append(title)
    return titles

def count_repeated_words(titles):
    all_words = []
    for title in titles:
        words = re.findall(r'\b\w+\b', title.lower())
        all_words.extend(words)
    word_counts = Counter(all_words)
    return {word: count for word, count in word_counts.items() if count > 2}

if __name__ == "__main__":
    input_path = r"C:\Users\SWATI\my_python_projects\spanish_Article\translated_results.txt"
    output_path = r"C:\Users\SWATI\my_python_projects\spanish_Article\word_analysis.txt"
    
    print("Extracting translated titles...")
    titles = extract_translated_titles(input_path)

    print("Analyzing repeated words...")
    repeated_words = count_repeated_words(titles)

    with open(output_path, "w", encoding="utf-8") as f:
        if repeated_words:
            f.write("🧠 Words repeated more than twice across translated titles:\n\n")
            for word, count in sorted(repeated_words.items(), key=lambda x: -x[1]):
                f.write(f"- {word}: {count} times\n")
            print("\n✅ Analysis written to word_analysis.txt")
        else:
            f.write("No words were repeated more than twice across headers.\n")
            print("No words were repeated more than twice across headers.")
