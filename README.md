# External data



### IvyPanda
https://ivypanda.com/essays/

Number of essays: ~93k
#### Usage
```
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/1-page-essay-examples/" --output_path "ivypanda_1pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/2-pages-essay-examples/" --output_path "ivypanda_2pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/3-pages-essay-examples/" --output_path "ivypanda_3pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/4-pages-essay-examples/" --output_path "ivypanda_4pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/5-pages-essay-examples/" --output_path "ivypanda_5pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/6-pages-essay-examples/" --output_path "ivypanda_6pages_essays.csv"
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


# Requirements
- nltk==3.7
- numpy==1.23.3
- flashtext==2.7
- contractions==0.1.72
- requests==2.28.1
- torch==1.12.1
- googletrans==4.0.0rc1
- tqdm==4.64.1
- pandas==1.5.0
- beautifulsoup4==4.11.1
- ipython==8.5.0
- selenium==4.4.3