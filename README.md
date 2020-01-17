# knowtox_manuscript_SI

This repository is part of the supporting information to

<b> KnowTox: Pipeline and Case Study for Confident Prediction of Potential Toxic Effects of Compounds in Early Phases of Development </b><br />
A. Morger<sup>1</sup>, M. Mathea<sup>2</sup>, J. H. Achenbach<sup>2</sup>, A. Wolf<sup>2</sup>, R. Buesen<sup>2</sup>, K-J. Schleifer<sup>2</sup>, R. Landsiedel<sup>2</sup>, A. Volkamer<sup>1</sup><br />
<sup>1</sup>: <i>In Silico</i> Toxicology and Structural Bioinformatics, Charité Universitätsmedizin, Berlin, Germany, [volkamerlab.org](https://physiologie-ccm.charite.de/en/research_at_the_institute/volkamer_lab/) <br />
<sup>2</sup>: BASF SE, Ludwigshafen, Germany

Computational tools for toxicity prediction are promising in the process of reducing, refining and
replacing animal testing. In our work, KnowTox was developed, a novel pipeline that combines three
different _in silico_ toxicology approaches to allow for confident prediction of potentially toxic effects of
query compounds, _i.e._ machine learning models, alerts for toxic substructures and computational
support for read-across. When applying machine learning models, applicability and reliability of
predictions for new chemicals are of utmost importance. This was approached using conformal prediction. Several adaptions of the framework were investigated and proposed (_i.e._ KNN normalisation and balancing of proper training set) to improve the model performance. The model set-ups were validated using androgen receptor antagonism datasets.

## Table of contents

* [Objective](#objective)
* [Data and methods](#data-and-methods)
* [Usage](#usage)
* [License](#license)
* [Acknowledgement](#acknowledgement)
* [Citation](#citation)

## Objective
(Back to [Table of contents](#table-of-contents))

In the notebook it is demonstrated how a conformal predictor is built, applied to make predictions for external data, and how to evaluate the internal (crossvalidation) and external predictions. Similar to the model validation process described in the paper, the original, the normalised and the normalised+balanced models for androgen receptor antagonism are built. Comparing the three models, it is demonstrated how normalisation can improve validity on external data while balancing of the proper training and calibration set improves efficiency at significance level 0.2. 

For an exhaustive explanation of conformal prediction and the validation process we refer to the paper. 

## Data and Methods
(Back to [Table of contents](#table-of-contents))

The datasets used in this notebook were downloaded from public databases:
* ToxCast database: https://figshare.com/articles/ToxCast_and_Tox21_Data_Spreadsheet/6062503 
(EPA’s National Center for Computational Toxicology. ToxCast and Tox21 Data Spreadsheet. Download date 23.06.2017)
* External data: https://www.tandfonline.com/doi/full/10.1080/1062936X.2016.1172665 
(Norinder _et al._ SAR and QSAR in Environmental Research 27.4 (2016): 303-316.)

The molecules were standardised as described in the paper (Data and Methods/Dataset Preprocessing/Standardisation)
* Remove duplicates
* Use [`standardiser`](https://github.com/flatkinson/standardiser) library (discard non-organic compounds, apply structure standardisation rules, neutralise, remove salts)
* Remove small fragments and remaining mixtures
* Remove duplicates

Descriptors were generated as specified in the paper (Data and Methods/Dataset Preprocessing/Descriptor calculation)
* MorganMACCS: Calculate Morgan fingerprint (radius `3`, `1024` bits) and MACCS keys using [RDKit](https://www.rdkit.org/) and concatenate
* mmpcReduced: Calculate Morgan fingerprint (radius `3`, `1024` bits), MACCS keys, and physicochemical descriptors using [RDKit](https://www.rdkit.org/)
* Normalise physicochemical descriptors
* Perform feature reduction based on ToxCast data (feature variance threshold `0.01` for binary descriptors (Morgan, MACCS) and `0.001` for continuous descriptors (physicochemical descriptors)
* Concatenate (normalised and) reduced Morgan, MACCS and physicochemial descriptors

All methods and parameters used in this notebook are based on the paper. Note that for this notebook, the newest versions of the python libraries were used. Thus, results may slightly differ. Moreover, due to the randomness of the random forest and stratified splitting, exact numbers cannot be reproduced. However, the magnitude/scale and trend of the improvement steps are consistent.

## Usage
(Back to [Table of contents](#table-of-contents))

The notebook can be used to train aggregated conformal predictors on the ToxCast androgen receptor antagonism endpoint (assay endpoint id 762), to make predictions for an external androgen receptor antagonism dataset, and to evaluate the predictions. Three different set-ups (original, normalised, normalised+balanced) for the conformal predictors are offered. 

The notebook could be adapted to train models for different ToxCast endpoints, as well as to input own dataframes with descriptors.

### Installation

1. Get your local copy of the `KnowTox_manuscript_SI` repository by:
    * Downloading it as a [Zip archive](https://github.com/volkamerlab/KnowTox_manuscript_SI/archive/master.zip) and unzipping it, or
    * Cloning it to your computer using git

    ```
    git clone https://github.com/volkamerlab/KnowTox_manuscript_SI.git
    ``` 

2. Install the [Anaconda](
https://docs.anaconda.com/anaconda/install/) (large download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (lighter) distribution for clean package version management.

3. Use the package manager `conda` to create an environment (called `knowtox_SI`) for the notebooks.
    
    `conda create --name knowtox_SI python=3.6`

4. Activate the conda environment

    `conda activate knowtox_SI`

5. Install packages
    
    `pip install scikit-learn`
    
    `pip install https://github.com/morgeral/nonconformist/archive/master.zip`
    
    `conda install jupyter`
    
Start the jupyter notebook

    `jupyter notebook`

Note: Due to the computational power needed to train the models, you might need to run the notebook with an increased max_buffer_size, _e.g._: 

```
jupyter notebook --NotebookApp.max_buffer_size=2000000000
```
    
## License
(Back to [Table of contents](#table-of-contents))

This work is licensed under the BSD 3-Clause "New" or "Revised" License.

## Acknowledgement
(Back to [Table of contents](#table-of-contents))

AM and AV would like to thank Jaime Rodríguez-Guerra for supporting the set up and reviewing this repository.

## Citation
(Back to [Table of contents](#table-of-contents))

If you make use of the `KnowTox_manuscript_SI` notebook, please cite:

```
@article{KnowTox,
    author = {
        Morger Andrea, 
        Mathea Miriam, 
        Achenbach Janosch Harald, 
        Wolf Antje, 
        Buesen Roland, 
        Schleifer Klaus-Juergen, 
        Landsiedel Robert, 
        Volkamer Andrea},
    title = {KnowTox: Pipeline and Case Study for Confident Prediction of Potential Tox Effects of Compounds in Early Phases of Development},
    journal = {submitted}
}
```
