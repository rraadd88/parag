# Example input data

Truncated copies (first 1000 lines, header included) of [BioSNAP](https://snap.stanford.edu/biodata) datasets used in `index.ipynb`. They are stored here so the examples and CI run without downloading from snap.stanford.edu.

| File | Original (gzipped) file | BioSNAP dataset page |
|---|---|---|
| `G-HumanEssential.tsv` | <https://snap.stanford.edu/biodata/datasets/10033/files/G-HumanEssential.tsv.gz> | [10033: Human essential genes](https://snap.stanford.edu/biodata/datasets/10033/10033-G-HumanEssential.html) |
| `PPT-Ohmnet_tissues-combined.edgelist` | <https://snap.stanford.edu/biodata/datasets/10013/files/PPT-Ohmnet_tissues-combined.edgelist.gz> | [10013: Tissue-specific protein-protein interactions](https://snap.stanford.edu/biodata/datasets/10013/10013-PPT-Ohmnet.html) |
| `ChSe-Decagon_monopharmacy.csv` | <https://snap.stanford.edu/biodata/datasets/10018/files/ChSe-Decagon_monopharmacy.csv.gz> | [10018: Drug side effects](https://snap.stanford.edu/biodata/datasets/10018/10018-ChSe-Decagon.html) |

## Effect of truncation on the examples

| File | Rows kept | Consequence |
|---|---|---|
| `PPT-Ohmnet_tissues-combined.edgelist` | 999 interactions | Only one tissue (`urinary_bladder`) is present, so it is also the "smallest network" selected in `index.ipynb` |
| `G-HumanEssential.tsv` | 999 genes (86 essential, 913 non-essential) | 53 of the 864 genes in the interactions above are annotated, so the gene-interaction plot is sparse |
| `ChSe-Decagon_monopharmacy.csv` | 999 drug–side-effect pairs, 7 drugs | The 5 selected side-effects connect to a single drug |

The figures in `examples/outputs` were generated with the full datasets.

## Citations

If you use these data, please cite the original sources:

- **BioSNAP collection:** Zitnik M, Sosič R, Maheshwari S, Leskovec J. BioSNAP Datasets: Stanford Biomedical Network Dataset Collection (2018). <https://snap.stanford.edu/biodata>
- **`PPT-Ohmnet_tissues-combined.edgelist`:** Zitnik M, Leskovec J. Predicting multicellular function through multi-layer tissue networks. *Bioinformatics* 33(14), i190–i198 (2017).
- **`ChSe-Decagon_monopharmacy.csv`:** Zitnik M, Agrawal M, Leskovec J. Modeling polypharmacy side effects with graph convolutional networks. *Bioinformatics* 34(13), i457–i466 (2018). [doi:10.1093/bioinformatics/bty294](https://doi.org/10.1093/bioinformatics/bty294)
- **`G-HumanEssential.tsv`:** essentiality annotations compiled by BioSNAP from the studies listed per gene in its `Data Source` column. PubMed IDs present in this copy: [18239125](https://pubmed.ncbi.nlm.nih.gov/18239125/), [19490893](https://pubmed.ncbi.nlm.nih.gov/19490893/), [21746896](https://pubmed.ncbi.nlm.nih.gov/21746896/), [22585861](https://pubmed.ncbi.nlm.nih.gov/22585861/), [26472758](https://pubmed.ncbi.nlm.nih.gov/26472758/), [26472760](https://pubmed.ncbi.nlm.nih.gov/26472760/), [26627737](https://pubmed.ncbi.nlm.nih.gov/26627737/).

See the dataset pages above for the original data, terms of use and full descriptions.
