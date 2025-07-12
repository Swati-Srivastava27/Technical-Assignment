from deep_translator import GoogleTranslator
import os
import re

def extract_article_sections(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    articles_raw = content.split("=" * 80)

    articles = []
    for article in articles_raw:
        article = article.strip()
        if not article:
            continue

        title_match = re.search(r"Title: (.+)", article)
        content_match = re.search(r" Content:\n(.+)", article, re.DOTALL)

        title = title_match.group(1).strip() if title_match else "[No Title Found]"
        content = content_match.group(1).strip() if content_match else "[No Content Found]"

        articles.append({
            "title": title,
            "content": content
        })

    return articles

def translate_text(text, target='en'):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except Exception as e:
        print(f"Translation failed: {e}")
        return "[Translation Failed]"

def translate_articles(articles):
    translated = []
    for i, article in enumerate(articles, 1):
        print(f"🔁 Translating Article {i}...")
        translated_title = translate_text(article["title"])
        translated_content = translate_text(article["content"])
        translated.append({
            "index": i,
            "title": translated_title,
            "content": translated_content
        })
    return translated

def save_translated_articles(translated, output_path):
    # Clear file first
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("🌍 Translated El País Articles (English)\n\n")

    # Append translations
    with open(output_path, "a", encoding="utf-8") as file:
        for article in translated:
            file.write(f"Article {article['index']}\n")
            file.write(f"Title: {article['title']}\n\n")
            file.write(f"Content:\n{article['content']}\n\n")
            file.write("=" * 80 + "\n\n")

if __name__ == "__main__":
    input_path = r"C:\Users\SWATI\my_python_projects\spanish_Article\scraper_result\results.txt"
    output_path = r"C:\Users\SWATI\my_python_projects\spanish_Article\translated_results.txt"

    print(" Reading original scraped data...")
    articles = extract_article_sections(input_path)

    print(" Translating content to English...")
    translated_articles = translate_articles(articles)

    print(f" Saving translated results to:\n{output_path}")
    save_translated_articles(translated_articles, output_path)

    print("Translation complete and saved.")
