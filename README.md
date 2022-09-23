# External data

#### IvyPanda
https://ivypanda.com/essays/
Number of essays: ~100k
```
>>> python parsers/ivypanda.py --url https://ivypanda.com/essays/pages/1-page-essay-examples/ --output_path ivypanda_1pages_essays.csv
>>> python parsers/ivypanda.py --url https://ivypanda.com/essays/pages/2-pages-essay-examples/ --output_path ivypanda_2pages_essays.csv
>>> python parsers/ivypanda.py --url https://ivypanda.com/essays/pages/3-pages-essay-examples/ --output_path ivypanda_3pages_essays.csv
>>> python parsers/ivypanda.py --url https://ivypanda.com/essays/pages/4-pages-essay-examples/ --output_path ivypanda_4pages_essays.csv
>>> python parsers/ivypanda.py --url https://ivypanda.com/essays/pages/5-pages-essay-examples/ --output_path ivypanda_5pages_essays.csv
```

#### essays.csv
https://www.kaggle.com/datasets/manjarinandimajumdar/essayscsv
Number of essays: ~2.5k

#### StudentShare
https://studentshare.org/free-essays
Number of essays: unknown

```
>>> python parsers/studentshare.py --url "https://studentshare.org/free-essays" --chrome_driver_path "C:\Users\w13va\drivers\chromedriver" --document_types "Essay" --levels "College" "High School" "Undergraduate" 
```