import numpy as np
import os
import string
import torch
import pytest

from itertools import chain

from torch import nn
from pytorch_widedeep.models.wide import Wide
from pytorch_widedeep.models.deep_dense import DeepDense
from pytorch_widedeep.models.deep_text import DeepText
from pytorch_widedeep.models.deep_image import DeepImage

from pytorch_widedeep.models.wide_deep import WideDeep
from pytorch_widedeep.optimizers import Adam, RAdam, SGD, RMSprop
from pytorch_widedeep.lr_schedulers import (StepLR, MultiStepLR, ExponentialLR,
	ReduceLROnPlateau, CyclicLR, OneCycleLR)
from pytorch_widedeep.callbacks import ModelCheckpoint, EarlyStopping, LRHistory

import pdb

# Wide array
X_wide=np.random.choice(2, (100, 100), p = [0.8, 0.2])

# Deep Array
colnames    = list(string.ascii_lowercase)[:10]
embed_cols  = [np.random.choice(np.arange(5), 100) for _ in range(5)]
embed_input = [(u,i,j) for u,i,j in zip(colnames[:5], [5]*5, [16]*5)]
cont_cols   = [np.random.rand(100) for _ in range(5)]
deep_column_idx={k:v for v,k in enumerate(colnames)}
X_deep = np.vstack(embed_cols+cont_cols).transpose()

# Text Array
padded_sequences = np.random.choice(np.arange(1,100), (100, 48))
vocab_size = 1000
X_text = np.hstack((np.repeat(np.array([[0,0]]), 100, axis=0), padded_sequences))

# target
target = np.random.choice(2, 100)

###############################################################################
# Test that history saves the information adequately
###############################################################################
optimizers_1 = { 'wide': Adam, 'deepdense': Adam}
lr_schedulers_1 = { 'wide': StepLR(step_size=4), 'deepdense': CyclicLR(base_lr=0.001, max_lr=0.01, step_size_up=10, cycle_momentum=False)}

optimizers_2 = { 'wide': Adam, 'deepdense':RAdam}
lr_schedulers_2 = {'wide': StepLR(step_size=4),'deepdense': StepLR(step_size=4)}
@pytest.mark.parametrize(
    'optimizers, schedulers, len_loss_output, len_lr_output',
    [
    (optimizers_1, lr_schedulers_1, 5, 21),
    (optimizers_2, lr_schedulers_2, 5, 6)
    ]
    )
def test_history_callback(optimizers, schedulers, len_loss_output, len_lr_output):
	wide = Wide(100, 1)
	deepdense = DeepDense(hidden_layers=[32,16], dropout=[0.5], deep_column_idx=deep_column_idx,
	    embed_input=embed_input, continuous_cols=colnames[-5:], output_dim=1)
	model = WideDeep(wide=wide, deepdense=deepdense)
	model.compile(method='logistic', optimizers=optimizers, lr_schedulers=schedulers,
		callbacks=[LRHistory], verbose=0)
	model.fit(X_wide=X_wide, X_deep=X_deep, X_text=X_text, target=target, n_epochs=5)
	out = []
	out.append(len(model.history._history['train_loss'])==len_loss_output)
	try:
		lr_list = list(chain.from_iterable(model.lr_history['lr_deepdense']))
	except TypeError:
		lr_list = model.lr_history['lr_deepdense']
	out.append(len(lr_list)==len_lr_output)
	assert all(out)

###############################################################################
# Test that EarlyStopping stops as expected
###############################################################################
def test_early_stop():
	wide = Wide(100, 1)
	deepdense = DeepDense(hidden_layers=[32,16], dropout=[0.5], deep_column_idx=deep_column_idx,
	    embed_input=embed_input, continuous_cols=colnames[-5:], output_dim=1)
	model = WideDeep(wide=wide, deepdense=deepdense)
	model.compile(method='logistic', callbacks=[EarlyStopping(min_delta=0.1, patience=3,
		restore_best_weights=True, verbose=1)], verbose=1)
	model.fit(X_wide=X_wide, X_deep=X_deep, target=target, val_split=0.2, n_epochs=5)
	# length of history = patience+1
	assert len(model.history._history['train_loss']) == 3+1

###############################################################################
# Test that ModelCheckpoint behaves as expected
###############################################################################
@pytest.mark.parametrize(
    'save_best_only, max_save, n_files',
    [
    (True, 2, 2),
    (False, 2, 2),
    (False, 0, 5)
    ]
    )
def test_model_checkpoint(save_best_only, max_save, n_files):
	wide = Wide(100, 1)
	deepdense = DeepDense(hidden_layers=[32,16], dropout=[0.5], deep_column_idx=deep_column_idx,
	    embed_input=embed_input, continuous_cols=colnames[-5:], output_dim=1)
	model = WideDeep(wide=wide, deepdense=deepdense)
	model.compile(method='logistic', callbacks=[ModelCheckpoint("weights/test_weights",
		save_best_only=save_best_only, max_save=max_save)], verbose=0)
	model.fit(X_wide=X_wide, X_deep=X_deep, target=target, n_epochs=5, val_split=0.2)
	n_saved = len(os.listdir('weights/'))
	for f in os.listdir('weights/'): os.remove('weights/'+f)
	assert n_saved <= n_files