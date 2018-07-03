from collections import defaultdict

import numpy
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

from chainer_chemistry.dataset.splitters.base_splitter import BaseSplitter


def generate_scaffold(smiles, include_chirality=False):
    """return scaffold string of target molecule"""
    mol = Chem.MolFromSmiles(smiles)
    scaffold = MurckoScaffold\
        .MurckoScaffoldSmiles(mol=mol, includeChirality=include_chirality)
    return scaffold


# Refer to Deepchem
# https://git.io/fXzF4
class ScaffoldSplitter(BaseSplitter):
    """Class for doing data splits by chemical scaffold."""
    def _split(self, dataset, frac_train=0.8, frac_valid=0.1, frac_test=0.1,
               **kwargs):
        numpy.testing.assert_almost_equal(frac_train + frac_valid + frac_test,
                                          1.)
        seed = kwargs.get('seed', None)
        smiles_list = kwargs.get('smiles_list')
        include_chirality = kwargs.get('include_chirality')
        if len(dataset) != len(smiles_list):
            raise ValueError("The lengths of dataset and smiles_list are "
                             "different")

        rng = numpy.random.RandomState(seed)

        scaffolds = defaultdict(list)
        for ind, smiles in enumerate(smiles_list):
            scaffold = generate_scaffold(smiles, include_chirality)
            scaffolds[scaffold].append(ind)

        scaffold_sets = rng.permutation(list(scaffolds.values()))

        n_total_valid = int(numpy.floor(frac_valid * len(dataset)))
        n_total_test = int(numpy.floor(frac_test * len(dataset)))

        train_index = []
        valid_index = []
        test_index = []

        for scaffold_set in scaffold_sets:
            if len(valid_index) + len(scaffold_set) <= n_total_valid:
                valid_index.extend(scaffold_set)
            elif len(test_index) + len(scaffold_set) <= n_total_test:
                test_index.extend(scaffold_set)
            else:
                train_index.extend(scaffold_set)

        return numpy.array(train_index), numpy.array(valid_index),\
            numpy.array(test_index),\


    def train_valid_test_split(self, dataset, smiles_list, frac_train=0.8,
                               frac_valid=0.1, frac_test=0.1, converter=None,
                               return_index=True, seed=None,
                               include_chirality=False, **kwargs):
        """Generate indices by splittting based on the scaffold of small
        molecules into train, valid and test set.

        Args:
            dataset(NumpyTupleDataset, numpy.ndarray):
                Dataset.
            smiles_list(list):
                SMILES list corresponding to datset.
            seed (int):
                Random seed.
            frac_train(float):
                Fraction of dataset put into training data.
            frac_valid(float):
                Fraction of dataset put into validation data.
            converter(callable):
            return_index(bool):
                If `True`, this function returns only indices. If `False`, this
                function returns splitted dataset.

        Returns:
            SplittedDataset(tuple):
                splitted dataset or indices
        """
        return super(ScaffoldSplitter, self)\
            .train_valid_test_split(dataset, frac_train, frac_valid, frac_test,
                                    converter, return_index, seed=seed,
                                    smiles_list=smiles_list,
                                    include_chirality=include_chirality,
                                    **kwargs)

    def train_valid_split(self, dataset, smiles_list, frac_train=0.9,
                          frac_valid=0.1, converter=None, return_index=True,
                          seed=None, include_chirality=False, **kwargs):
        """Generate indices by splittting based on the scaffold of small
        molecules into train and valid set.

        Args:
            dataset(NumpyTupleDataset, numpy.ndarray):
                Dataset.
            smiles_list(list):
                SMILES list corresponding to datset.
            seed (int):
                Random seed.
            frac_train(float):
                Fraction of dataset put into training data.
            frac_valid(float):
                Fraction of dataset put into validation data.
            converter(callable):
            return_index(bool):
                If `True`, this function returns only indices. If `False`, this
                function returns splitted dataset.

        Returns:
            SplittedDataset(tuple):
                splitted dataset or indices
        """
        return super(ScaffoldSplitter, self)\
            .train_valid_split(dataset, frac_train, frac_valid, converter,
                               return_index, seed=seed,
                               smiles_list=smiles_list,
                               include_chirality=include_chirality, **kwargs)
