# CSUS 2018 Reversi AI Project

An attempted implementation of n-step q-learning detailed @ https://coach.nervanasys.com/algorithms/value_optimization/n_step/index.html

I made this in a week lol please don't be hard on me.

## Requirements for this project:

numpy

tensorflow

keras

## To play text-based game:

```
python wytest.py
```

## To train:

```
python wytrain.py
```

The model is saved as reversi3.h5

## Misc Notes

Currently, the model has trained for ~150,000 games on my shitty macbook.

In this state it managed to barely beat a more traditional AI. However, take this with a grain of salt, as that AI was also written by a high school comp-sci student.

I would have liked to get 80M, which is a nice number for our model to converge to a good approximation.
