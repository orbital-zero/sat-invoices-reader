![CI](https://github.com/orbital-zero/sat-invoices-reader/actions/workflows/build.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/orbital-zero/sat-invoices-reader/badge.svg)](https://coveralls.io/github/orbital-zero/sat-invoices-reader) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=orbital-zero_sat-invoices-reader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=orbital-zero_sat-invoices-reader)


# sat-invoices-reader
Sat invoices reader, the ones used in Mexico

## Requirements

This project is builded on python > 3.X, please consider to create and activate a virtual python environment before to start:

```bash
# Create and activate python enironment
python -m venv pyenv

## Linux
.\pyenv\Scripts\activate

## Windows powershell
.\pyenv\Scripts\Activate.ps1

## Windows cmd
.\pyenv\Scripts\activate.cmd
```

In order to leave the virtual environment execute:

```bash
## Linux
.\pyenv\Scripts\deactivate

## Windows powershell
.\pyenv\Scripts\dectivate.ps1

## Windows cmd
.\pyenv\Scripts\deactivate.bat
```

The required packages are defined on `requirements.txt` file, and it could be installed as follow:

```bash
pip install -r requirements.txt
```

**note:** If new packages are installed the `requiremts.txt` file must be updated using the virtual environment:
```bash
pip freeze > requirements.txt
```


## Usage

There are two scripts:

- `main.py` to read payroll or deduction invoices from terminal
- `classify.py` to sort invoices by issuer and their year of creation

Use option -h for get help of each one.

output:
```
$ main.py -h

usage: main.py [-h] -p path [-t [P,D]] [-x]

Process to read invoce files from a specified directory (xml or zipped files)

options:
  -h, --help            show this help message and exit
  -p path, --sourcesPath path
                        Path to directory with files, the nestted directories are included in the processing.
  -t [P,D], --type [P,D]
                        Invoice type, P for payroll (by default) or D for deductions.
  -x, --extract         Extract xml from zipped files.


These are an examples to execute the command:

    # read xml files from directory
        ./main.py -p <sourcesPath>

    # read zipped xml files from directory
        ./main.py -p <sourcesPath> -x

-----------------------------------------------------------

$ classify.py -h

usage: classify.py [-h] -p source_path -o target_path [-x]

Classify invoices by issuer and year of creation

options:
  -h, --help            show this help message and exit
  -p source_path, --sourcesPath source_path
                        source directory to read xml files
  -o target_path, --targetPath target_path
                        target directory to put sorted xml files
  -x, --extract         Extract xml from zipped files.
  -u, --uuid_names      The output file will be renamed by their invoice uuid

These are an examples to execute the command:

    # sort xml files by invoice year and issuer from source directory, then leave it in another directory
        ./classify.py -p <sourcesPath> -o <targetPath>

    # sort xml files by invoice year and issuer from source directory, then leave it in another directory changing names by uuid value
        ./classify.py -p <sourcesPath> -o <targetPath> -u

    # extract and sort xml zipped files from a directory and leave it in another one
        ./classify.py -p <sourcesPath> -o <targetPath> -x

    # extract and sort xml zipped files from a directory and leave it in another one changing their names by uuid value
        ./classify.py -p <sourcesPath> -o <targetPath> -xu
```

## Testing and code coverage

### Running unit tests

    $ python -m unittest discover -s ./test -p "*Test.py"

### Code coverage

```sh
# Clean coverage data
python -m coverage erase

# Create coverage report executing unit tests
python -m coverage run --source=classes -m unittest discover -s ./test -p "*Test.py"

# Create coverage report for coveralls
python -m coverage lcov -o ./coverage/lcov.info

# Show coverage report in terminal (text output)
python -m coverage report

# Create coverage report in html format
python -m coverage html

# help
python -m coverage help

```

### Coveralls report

Publish report on coverralls.io:

    $ python -m coveralls

# Enforcement style guide

```sh
# Show issues and statistics on sepecific path
python -m flake8 path/to/sources --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Show issues and statistics on sepecific file, showing source code
python -m flake8 path/to/file.py --count --show-source  --statistics

```
For more deteil of errors and violations, see here [violation codes](https://flake8.pycqa.org/en/latest/user/error-codes.html) and [error codes](https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes)

## Format code to conform style guide

Some issues can be automatically fixed using the module autopep8 style guide:

```sh
# Show list fix codes
python -m autopep8 --list-fixes

# Fix blank a few white spaces
python -m autopep8 -i <filename>

# Select subset of fixes
python -m autopep8 --select=E225,E231,E301,E302,E303,E305,E265,W291,W292,W293,W391,E271,E275,E306,E271,E251,E111,E117,E128,E203,F401,F811 <filename>

# Fix issues in a file using aggresive level 1
python -m autopep8 --in-place --aggressive --ignore=E731,E275 <filename>

# Show help
python -m autopep8 -h

```

See also **autopep8** docs [here](https://pypi.org/project/autopep8/) to get more detailed instructions and error codes description.
    