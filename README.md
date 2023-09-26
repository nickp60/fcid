# fcid

Thanks to:

- https://www.biostars.org/p/198143/
- https://github.com/10XGenomics/supernova/blob/master/tenkit/lib/python/tenkit/illumina_instrument.py#L12-L45
- Illumina Techinical Support

> Disclaimer: this is not a replacement for proper sequencing run tracking.
> Disclaimer: PRs welcome to fill gaps!  Instrument IDs are less reliable as those are often changed by the sequencing center.


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
