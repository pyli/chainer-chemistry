import chainer
from chainer import functions

from chainer_chemistry.links import GraphLinear


class GGNNReadout(chainer.Chain):
    """GGNN submodule for readout part.

    Args:
        out_dim (int): dimension of output feature vector
        hidden_dim (int): dimension of feature vector associated to
            each atom
        n_layers (int): number of layers
        concat_hidden (bool): If set to True, readout is executed in
            each layer and the result is concatenated
        nobias (bool): If ``True``, then this function does not use
            the bias
        activation (~chainer.Function or ~chainer.FunctionNode):
            activate function
            It can be replaced with the functions.identity.
    """

    def __init__(self, out_dim, hidden_dim=16, n_layers=4,
                 concat_hidden=False, nobias=False,
                 activation=functions.tanh):
        super(GGNNReadout, self).__init__()
        n_layer = n_layers if concat_hidden else 1
        with self.init_scope():
            self.i_layers = chainer.ChainList(
                *[GraphLinear(None, out_dim, nobias=nobias)
                  for _ in range(n_layer)])
            self.j_layers = chainer.ChainList(
                *[GraphLinear(None, out_dim, nobias=nobias)
                  for _ in range(n_layer)])
        self.out_dim = out_dim
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        self.concat_hidden = concat_hidden
        self.nobias = nobias
        self.activation = activation

    def __call__(self, h, h0=None, step=0):
        # --- Readout part ---
        index = step if self.concat_hidden else 0
        # h, h0: (minibatch, atom, ch)
        h1 = functions.concat((h, h0), axis=2) if h0 is not None else h

        g1 = functions.sigmoid(self.i_layers[index](h1))
        g2 = self.activation(self.j_layers[index](h1))
        # sum along atom's axis
        g = self.activation(functions.sum(g1 * g2, axis=1))
        return g
