import numpy
import pytest

from chainer_chemistry.dataset.splitters.stratified_splitter import StratifiedSplitter # NOQA
from chainer_chemistry.datasets import NumpyTupleDataset


@pytest.fixture
def cls_dataset():
    a = numpy.random.random((30, 10))
    b = numpy.random.random((30, 8))
    c = numpy.concatenate([numpy.zeros(20), numpy.ones(10)]).astype(numpy.int)
    return NumpyTupleDataset(a, b, c)


@pytest.fixture
def reg_dataset():
    a = numpy.random.random((100, 10))
    b = numpy.random.random((100, 8))
    c = numpy.arange(100).astype(numpy.float)
    return NumpyTupleDataset(a, b, c)


def test_classification_split(cls_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind, test_ind = splitter._split(cls_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 24
    assert valid_ind.shape[0] == 3
    assert test_ind.shape[0] == 3

    train_ind, valid_ind, test_ind = splitter._split(cls_dataset,
                                                     frac_train=0.5,
                                                     frac_valid=0.3,
                                                     frac_test=0.2)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 15
    assert valid_ind.shape[0] == 9
    assert test_ind.shape[0] == 6


def test_regression_split(reg_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind, test_ind = splitter._split(reg_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 80
    assert valid_ind.shape[0] == 10
    assert test_ind.shape[0] == 10

    train_ind, valid_ind, test_ind = splitter._split(reg_dataset,
                                                     frac_train=0.5,
                                                     frac_valid=0.3,
                                                     frac_test=0.2)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 50
    assert valid_ind.shape[0] == 30
    assert test_ind.shape[0] == 20


def test_classification_split_fix_seed(cls_dataset):
    splitter = StratifiedSplitter()
    train_ind1, valid_ind1, test_ind1 = splitter._split(cls_dataset, seed=44)
    train_ind2, valid_ind2, test_ind2 = splitter._split(cls_dataset, seed=44)

    assert numpy.array_equal(train_ind1, train_ind2)
    assert numpy.array_equal(valid_ind1, valid_ind2)
    assert numpy.array_equal(test_ind1, test_ind2)


def test_regression_split_fix_seed(reg_dataset):
    splitter = StratifiedSplitter()
    train_ind1, valid_ind1, test_ind1 = splitter._split(reg_dataset, seed=44)
    train_ind2, valid_ind2, test_ind2 = splitter._split(reg_dataset, seed=44)

    assert numpy.array_equal(train_ind1, train_ind2)
    assert numpy.array_equal(valid_ind1, valid_ind2)
    assert numpy.array_equal(test_ind1, test_ind2)


def test_train_valid_test_classification_split(cls_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind, test_ind =\
        splitter.train_valid_test_split(cls_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 24
    assert valid_ind.shape[0] == 3
    assert test_ind.shape[0] == 3


def test_train_valid_test_classification_split_return_dataset(cls_dataset):
    splitter = StratifiedSplitter()
    train, valid, test = splitter.train_valid_test_split(cls_dataset,
                                                         return_index=False)
    assert type(train) == NumpyTupleDataset
    assert type(valid) == NumpyTupleDataset
    assert type(test) == NumpyTupleDataset
    assert len(train) == 24
    assert len(valid) == 3
    assert len(test) == 3
    assert (train.features[:, -1] == 1).sum() == 8
    assert (valid.features[:, -1] == 1).sum() == 1
    assert (test.features[:, -1] == 1).sum() == 1


def test_train_valid_test_regression_split(reg_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind, test_ind =\
        splitter.train_valid_test_split(reg_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 80
    assert valid_ind.shape[0] == 10
    assert test_ind.shape[0] == 10


def test_train_valid_test_regression_split_return_dataset(reg_dataset):
    splitter = StratifiedSplitter()
    train, valid, test = splitter.train_valid_test_split(reg_dataset,
                                                         return_index=False)
    assert type(train) == NumpyTupleDataset
    assert type(valid) == NumpyTupleDataset
    assert type(test) == NumpyTupleDataset
    assert len(train) == 80
    assert len(valid) == 10
    assert len(test) == 10
    assert 47.5 < train.features[:, -1].mean() < 52.5
    assert 47.5 < valid.features[:, -1].mean() < 52.5
    assert 47.5 < test.features[:, -1].mean() < 52.5


def test_train_valid_classification_split(cls_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind = splitter.train_valid_split(cls_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 27
    assert valid_ind.shape[0] == 3


def test_train_valid_classification_split_return_dataset(cls_dataset):
    splitter = StratifiedSplitter()
    train, valid = splitter.train_valid_split(cls_dataset, return_index=False)
    assert type(train) == NumpyTupleDataset
    assert type(valid) == NumpyTupleDataset
    assert len(train) == 27
    assert len(valid) == 3
    assert (train.features[:, -1] == 1).sum() == 9
    assert (valid.features[:, -1] == 1).sum() == 1


def test_train_valid_regression_split(reg_dataset):
    splitter = StratifiedSplitter()
    train_ind, valid_ind = splitter.train_valid_split(reg_dataset)
    assert type(train_ind) == numpy.ndarray
    assert train_ind.shape[0] == 90
    assert valid_ind.shape[0] == 10


def test_train_valid_regression_split_return_dataset(reg_dataset):
    splitter = StratifiedSplitter()
    train, valid = splitter.train_valid_split(reg_dataset, return_index=False)
    assert type(train) == NumpyTupleDataset
    assert type(valid) == NumpyTupleDataset
    assert len(train) == 90
    assert len(valid) == 10
    assert 47.5 < train.features[:, -1].mean() < 52.5
    assert 47.5 < valid.features[:, -1].mean() < 52.5
