# dc_cc_analyzer

This project is a tool designed to perform DC/CC coverage analysis for software written in the C programming language.

## How to use

### Dependecies

Python 3.10.12. gcc 11.4.0.

To install all Python libraries, run:

```
pip install -r requirements.txt
```

### How to run

In the source directory of this tool, run:

```
python3  dc-cc-analyzer.py <path-to-sut> <path-to-testvectors>
```

Where \<path-to-sut> is the path in your machine to the sut.c file you want to test and \<path-to-testvectors> is the path to the spreadsheet with the Test Vectors.

## Documentation

Check the [wiki](https://github.com/GabrielSSAraujo/dc_cc_analyzer/wiki) for more informations.

## Authors

* Aline A. Urna - aau@cin.upfe.br
* Bruno A. Colturato - bac2@cin.ufpe.br
* Gabriel S. S. Araújo - gssa@cin.ufpe.br
* Gustavo P. C. Silveira - gpcs@cin.upfe.br
* Moacir F. M. G. de Lima - mfmgl@cin.upfe.br 
