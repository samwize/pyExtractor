pyExtractor
===========

A python tool to extract data types such as email, URL, domains and phone numbers.

# Usage 

```
usage: extract.py [-h] [-e] [-u] [-d] [-m] [-a] [-v VERBOSITY] [--version]
                  filename

Extract useful data from a file!

positional arguments:
  filename              The filename to extract data from

optional arguments:
  -h, --help            show this help message and exit
  -e, --emails          Extract emails
  -u, --urls            Extract URLs
  -d, --domains         Extract domain names
  -m, --mobile          Extract mobile phone numbers (for Singapore only)
  -a, --all             Extract emails, URLS and domain names
  -v VERBOSITY, --verbosity VERBOSITY
                        Increase output verbosity
  --version             show program's version number and exit
```


# Example

The repository includes a test file that contains some garbage. Clone the repository and run the following command to extract the mobile numbers:

	python extract.py -m test.txt 

A `test - mobile.csv` containing the results will be generated.