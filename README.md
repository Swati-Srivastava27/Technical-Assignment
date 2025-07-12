# Technical-Assignment
#  El País Opinion Article Scraper & Analyzer

This project automates the process of scraping the latest opinion articles from [El País](https://elpais.com/opinion/), translating their titles and content into English, and analyzing frequently used words in the translated headers.

---

##  Project Overview

###  What it does:

* Scrapes the latest 5 opinion articles from El País (in Spanish)
* Extracts titles, full content, and cover images
* Saves content to `results.txt`
* Translates Spanish titles and content to English using Google Translate
* Stores translated results in `translated_results.txt`
* Analyzes translated titles and reports words repeated more than twice

---

##  Project Structure

```
my_python_projects/
│
├── scraper_result/
│   ├── results.txt                # Scraped Spanish titles and content
│   └── elpais_images/            # Downloaded article images
│
├── translated_results.txt        # English-translated titles and content
├── word_analysis.txt             # Repeated words in translated titles
│
├── scrape_opinion.py             # Scraping script
├── translate_results.py          # Translation script
└── analyze_headers.py             # Title analysis script
```

---

## 🛠️ Requirements

* **Python**: 3.8 to 3.12 (avoid 3.13 for `googletrans`)
* **Google Chrome** installed
* **ChromeDriver** matching your Chrome version

### Install required libraries:

```bash
pip install selenium requests googletrans==4.0.0-rc1
```

Note: Ensure ChromeDriver is in your system's PATH.

---

##  Script Execution Order

### Scrape El País Articles

```bash
python scrape_opinion.py
```

* Visits the El País Opinion section
* Extracts 5 latest articles
* Saves Spanish title, content, and images
* Stores results in `scraper_result/results.txt` and `elpais_images/`

---

Translate Results to English

```bash
python translate_results.py
```

* Reads `results.txt`
* Translates each title and content to English
* Saves to `translated_results.txt`

---

Analyze Translated Titles

```bash
python analyze_titles.py
```

* Reads `translated_results.txt`
* Identifies words repeated more than twice in titles
* Outputs to console and `word_analysis.txt`

---

 Example Output (results.txt)

```
Article 1
Title: Opinión
Content:
[Full Spanish content]

Image Path: scraper_result/elpais_images/article_1.jpg
================================================================================
```

---

##  API Notes

The translation is powered using the unofficial Google Translate API via the `googletrans` library.

---

##  Credits

* Developed by: Swati Srivastava
* Tools used: Selenium, Google Translate API, Python 3

---

##  License

This project is open-source and free to use for educational or research purposes.
