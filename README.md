# synthpop-model-eval
A collection of tests to allow for comparison between Galactic models and observational data.

The basic set up right now is that each test category is a python module, and each individual test is a function. Each function takes in specific data columns from the Galactic model output and compares it to an observed data set. An example Jupyter notebook shows how an example test can be run on a SynthPop catalog.

The current test categories, and test data sets for each are:
- Color-magnitude diagrams (cmds.py)
- Luminosity functions (lumfuncs.py)
  - V, I, J, H - band luminosity functions from HST data in the Stanek Window (Reference: [Terry et al., 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...889..126T/abstract))
- Microlensing statistics (mulensstats.py)
- Proper motions (propermotions.py)
- Radial velocities (radvels.py)
- Star counts (starcounts.py)
