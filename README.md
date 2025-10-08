![PyPI - Version](https://img.shields.io/pypi/v/fcid)

# fcid
*f*low *c*ell *ID*: parse illumina fastq headers to determine machine and flowcell type
Thanks to:

- https://www.biostars.org/p/198143/
- https://github.com/10XGenomics/supernova/blob/master/tenkit/lib/python/tenkit/illumina_instrument.py#L12-L45
- Illumina Techinical Support

> Disclaimer: this is not a replacement for proper sequencing run tracking.
> Disclaimer: PRs welcome to fill gaps!  Instrument IDs are less reliable as those are often changed by the sequencing center.

> Got ONT data? Their flowcells do not follow a naming convention, but they can look up flowcells internally; contact them via the support page on their website.


## Installation

```

pip install fcid
# or, for you devs
git clone <this repo> && cd fcid
pip install --editable .

```

## Usage (CLI)


```
# fcid CABBCANXX
# fcid  K11111 --by-machine
# fcid 22C37GLT3
```


## Usage (package)
```python
>>> from fcid import run
>>> run.get_tech_type("CABBCANXX", run.FCIDs)
[['HiSeq 2500'], 'High Output v3 flow cell']
```

## Test
```
pytest
```

## Deployment

1. Update version pyproject.toml
2. commit and tag
3. push to github and make a release
4. check the package deployment action
