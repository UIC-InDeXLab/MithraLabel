## function-dependency-exploration

A TANE algorithm implementation for function dependency exploration

Command lines in this introduction are fully tested on Ubuntu 16.04 


### Prerequisite

* python3(>=3.5.2)
* pylint3(>=1.5.2), acquired by `sudo apt-get install pylint3`
* coverage(>= 4.3.4), acquired by `sudo pip3 install coverage`

### Project structure

#### utils module

* utils.preprocessor: Handler for command line option
* utils.reader: Input interface for raw data file
* utils.writer: Output interface for function dependency
* utils.slugify: Helper functions

Run

```
pydoc3 -w utils utils.preprocessor utils.reader utils.writer utils.slugify 
```
to generate documents for module details.

#### algorithm module

* algorithm.tane: Implementation for TANE algorithm

Run
```
pydoc3 -w algorithm algorithm.tane
```
to generate documents for module details

#### main.py

* An example of using above modules 

#### test.py

* Test cased

Run
```
pydoc3 -w main
```
to generate documents for details


### How to run

#### Static code analysis
Run
```
pylint3 --rcfile=.pylint main.py algorithm utils > analysis.html
```
to see analysis result in `analysis.html`.

PS: pylint3 is used to meet the requirement of homework, which could be ignored at your convenience.

#### Implement algorithm
Run
```
python3 main.py -i data/data.txt -o output.txt --breaker=,
```
to get function dependencies in `output.txt` for table in `data/data.txt`.
 
#### Run test
Run
```
coverage run test.py
coverage html
```
to get a coverage report of the test.

