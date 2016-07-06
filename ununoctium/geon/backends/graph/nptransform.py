import numpy as np

from geon.backends.graph.transform import Op, Transformer, AllocationOp


class NumPyTransformer(Transformer):
    def __init__(self, **kargs):
        super(NumPyTransformer, self).__init__(**kargs)

    # allocators
    def empty(self, tensor_description):
        return np.empty(tensor_description.sizes, tensor_description.dtype)

    def rng(self, seed=None):
        return np.random.RandomState(seed=seed)

    def tensor_view(self, tensor_description):
        return np.ndarray(shape=tensor_description.shape, dtype=tensor_description.dtype, buffer=tensor_description.buffer.value,
                          offset=tensor_description.offset, strides=tensor_description.strides)

    def rng_uniform_tensor(self, rng, tensor_description, low, high):
        return rng.uniform(low, high, tensor_description.sizes)

    # Side-effects
    def fill(self, out, value):
        out.fill(value)

    def set_item(self, tensor, item, value):
        tensor.__setitem__(item, value)

    # NumPy-specific
    def rng_uniform(self, rng, low, high, out):
        out[:] = rng.uniform(low, high, out.shape)

    # Operations
    def absolute(self, x, out):
        np.abs(x, out=out)

    def add(self, x, y, out):
        np.add(x, y, out=out)

    def argmax(self, x, out):
        np.ndarray.argmax(x, 0, out)

    def argmin(self, x, out):
        np.ndarray.argmin(x, 0, out)

    def cos(self, x, out):
        np.cos(x, out=out)

    def divide(self, x, y, out):
        np.divide(x, y, out=out)

    def dot(self, x, y, out):
        np.dot(x, y, out)

    def equal(self, x, y, out):
        return np.equal(x, y, out=out)

    def exp(self, x, out):
        np.exp(x, out=out)

    def greater(self, x, y, out):
        np.greater(x, y, out=out)

    def greater_equal(self, x, y, out):
        np.greater_equal(x, y, out=out)

    def less(self, x, y, out):
        np.less(x, y, out=out)

    def less_equal(self, x, y, out):
        np.less_equal(x, y, out=out)

    def log(self, x, out):
        np.log(x, out=out)

    def max(self, x, axis, out):
        np.max(x, axis, out=out)

    def maximum(self, x, y, out):
        np.maximum(x, y, out=out)

    def min(self, x, axis, out):
        np.min(x, axis, out=out)

    def minimum(self, x, y, out):
        np.minimum(x, y, out=out)

    def multiply(self, x, y, out):
        np.multiply(x, y, out=out)

    def negative(self, x, out):
        np.negative(x, out=out)

    def not_equal(self, x, y, out):
        np.not_equal(x, y, out=out)

    def reciprocal(self, x, out):
        np.reciprocal(x, out=out)

    def sign(self, x, out):
        np.sign(x, out=out)

    def sin(self, x, out):
        np.sin(x, out=out)

    def sqrt(self, x, out):
        np.sqrt(x, out=out)

    def square(self, x, out):
        np.square(x, out=out)

    def subtract(self, x, y, out):
        np.subtract(x, y, out=out)

    def sum(self, x, axis, out):
        np.sum(x, axis=axis, out=out)

    def tanh(self, x, out):
        np.tanh(x, out=out)


class NPUniform(AllocationOp):
    def __init__(self, rng, low, high, **kargs):
        super(NPUniform, self).__init__(args=(rng,), **kargs)
        self.low = low
        self.high = high

    def compute_tensor_axes_info(self):
        rng, = self.args
        tensor_axes_info = super(NPUniform, self).compute_tensor_axes_info()
        tensor_axes_info.alloc = lambda evaluator, tensor_description: evaluator.rng_uniform_tensor(rng, tensor_description, self.low, self.high)