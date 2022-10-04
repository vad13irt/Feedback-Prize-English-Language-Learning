# External data



### IvyPanda
https://ivypanda.com/essays/

Number of essays: ~93k
#### Usage
```
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/1-page-essay-examples/" --output_path "external_data/ivypanda_1pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/2-pages-essay-examples/" --output_path "external_data/ivypanda_2pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/3-pages-essay-examples/" --output_path "external_data/ivypanda_3pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/4-pages-essay-examples/" --output_path "external_data/ivypanda_4pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/5-pages-essay-examples/" --output_path "external_data/ivypanda_5pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/6-pages-essay-examples/" --output_path "external_data/ivypanda_6pages_essays.csv"
```

### StudentShare
https://studentshare.org/free-essays/

Number of essays: ~33.5k

#### Usage
1. SignUp - https://studentshare.org/signup
2. Add password - https://studentshare.org/user/profile -> Change password
```
>>> python parsers/studentshare.py --url "https://studentshare.org/free-essays" --chrome_driver_path "<chrome_driver_path>" --document_types "Essay" "Scholarship Essay" "Admission/Application Essay" --levels "College" "High School" "Undergraduate" --max_pages 6 --email "<email>" --password "<password>" --output_path "studentshare_essays.csv"
```

#### essays.csv
https://www.kaggle.com/datasets/manjarinandimajumdar/essayscsv/

Number of essays: ~2.5k

# Augmentations
- CutOut
- NumberToWords
- Accent
- SlangConverter
- KeywordReplacer

- Google Translate Back Translation

```
>>> python src/transforms/google_translate_back_translation.py --data_frame_path "data/train.csv" --source_language "english" --target_language "french" --output_path "external_data/english_french.csv" --text_column "full_text" 
>>> python src/transforms/google_translate_back_translation.py --data_frame_path "data/train.csv" --source_language "english" --target_language "german" --output_path "external_data/english_german.csv" --text_column "full_text"  
>>> python src/transforms/google_translate_back_translation.py --data_frame_path "data/train.csv" --source_language "english" --target_language "italian" --output_path "external_data/english_italian.csv" --text_column "full_text"  
>>> python src/transforms/google_translate_back_translation.py --data_frame_path "data/train.csv" --source_language "english" --target_language "russian" --output_path "external_data/english_russian.csv" --text_column "full_text" 
>>> python src/transforms/google_translate_back_translation.py --data_frame_path "data/train.csv" --source_language "english" --target_language "chinese (traditional)" --output_path "external_data/english_chinese.csv" --text_column "full_text"
```

# Requirements
- contractions==0.1.72
- pandas==1.5.0
- tqdm==4.64.1
- num2words==0.5.12
- numpy==1.23.3
- nltk==3.7
- torch==1.12.1
- googletrans==4.0.0rc1
- requests==2.28.1
- beautifulsoup4==4.11.1
- ipython==8.5.0
- selenium==4.5.0
