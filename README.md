# Epherousa [![Build Status](https://travis-ci.com/Sinderella/epherousa.svg?token=8Z4yehRhLixppVCDLLLp&branch=master)](https://travis-ci.com/Sinderella/epherousa) [![codecov](https://codecov.io/gh/Sinderella/epherousa/branch/master/graph/badge.svg?token=cD3Vt8lGow)](https://codecov.io/gh/Sinderella/epherousa) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/42926095c43b41a294fa8bb8ad183dd5/badge.svg)](https://www.quantifiedcode.com/app/project/42926095c43b41a294fa8bb8ad183dd5)

Epherousa (or Ephe in short) provides an automatic way of searching for available exploits and vulnerability information. Ultimately it should present the information in such a way that will help researchers and penetration testers with their day to day job. Both CVE and text-based searches are supported.

Ephe's name stems from the Greek mythology. Pherousa (Φέρουσα) is the name of 2 different figures, one being a Nereid (sea female spirit) and the other being a Horae (godness of the seasons and time). Pherousa in Greek stands for "she who brings or carries", which hopefully in this case makes sense as ephe carries or brings your exploit and vulnerability information.

## INSTALLATION

### via git

```
$ git clone $URL
$ python epherousa/setup.py install
```

## Usage

Epherousa can be invoked with both `epherousa` and `ephe`, for short.

```
$ ephe -h
usage: ephe [-h] [-d DISABLE] [-e ENABLE] [-v] [-p] [-l LIMIT] [-q] cve

Search multiple sources for exploits for CVEs or software versions

positional arguments:
  cve                   The cve to find exploits for.

optional arguments:
  -h, --help            show this help message and exit
  -d DISABLE, --disable DISABLE
                        Disable only these scanners. Input is interpreted as a
                        series of comma-seperated case-insensitive regexes.
  -e ENABLE, --enable ENABLE
                        Enable only these scanners. Input is interpreted as a
                        series of comma-seperated case-insensitive regexes.
  -v, --verbose         Enable verbose logging.
  -p, --phrase          Force interpreting the search argument as a search
                        string rather than a CVE
  -l LIMIT, --limit LIMIT
                        Limit the results of the exploits returned for each
                        Scanner. Default value is set to 0 for no limit.
  -q, --quiet           Do not display ephe's banner.
```
