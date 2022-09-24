# External data

### IvyPanda
https://ivypanda.com/essays/
Number of essays: ~85k
#### Usage
```
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/1-page-essay-examples/" --output_path "ivypanda_1pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/2-pages-essay-examples/" --output_path "ivypanda_2pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/3-pages-essay-examples/" --output_path "ivypanda_3pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/4-pages-essay-examples/" --output_path "ivypanda_4pages_essays.csv"
>>> python parsers/ivypanda.py --url "https://ivypanda.com/essays/pages/5-pages-essay-examples/" --output_path "ivypanda_5pages_essays.csv"
```

### StudentShare
https://studentshare.org/free-essays
Number of essays: ~33.5k

#### Usage
1. SignUp - https://studentshare.org/signup
2. Add password - https://studentshare.org/user/profile -> Change password
```
>>> python parsers/studentshare.py --url "https://studentshare.org/free-essays" --chrome_driver_path "<chrome_driver_path>" --document_types "Essay" "Scholarship Essay" "Admission/Application Essay" --levels "College" "High School" "Undergraduate" --max_pages 5 --email "<email>" --password "<password>" --output_path "studentshare_essays.csv"
```

#### essays.csv
https://www.kaggle.com/datasets/manjarinandimajumdar/essayscsv
Number of essays: ~2.5k


# Requirements
- nltk==3.6.2
- googletrans==4.0.0rc1
- tqdm==4.64.0
- pandas==1.1.3
- selenium==3.141.0
- numpy==1.23.0
- requests==2.27.1
- flashtext==2.7
- torch==1.11.0
- contractions==0.1.72
- beautifulsoup4==4.11.1
- ipython==8.5.0