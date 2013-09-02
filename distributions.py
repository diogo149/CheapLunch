"""
Module for random distributions and other utility functions.
"""

import random
import numpy as np
from abc import ABCMeta, abstractmethod

from utils import GenericObject


def seed(i):
    """ seeds python random number generators
    """
    assert isinstance(i, int), i
    random.seed(i)
    np.random.seed(i)


def quantize(q, array):
    """ quantize an distribution into discrete values
    """
    return q * np.round(array / q)


class BaseDistribution(GenericObject):

    """ base class for distributions
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def _generate(self):
        pass

    def generate(self):
        if self.size != 1:
            return self._generate(self.size)
        else:
            return self._generate()[0]


class RandIntDistribution(BaseDistribution):

    """ Returns a random integer in the range [0, upper).
    """

    NAME = "randint"
    _required_args = ("size", "high")

    def _generate(self, size=1):
        return np.random.randint(self.high, size=size)


class EnumDistribution(BaseDistribution):

    """ Returns a random value from an input list
    """

    NAME = "enum"
    _required_args = ("enum",)
    _default_args = dict(size=1)

    def _generate(self, size=1):
        return np.array(self.enum)[np.random.randint(len(self.enum), size=size)]


class UniformDistribution(BaseDistribution):

    """ a uniform distribution of floating point numbers
    """

    NAME = "uniform"
    _required_args = ("size", "low", "high")

    def _generate(self, size=1):
        return np.random.uniform(self.low, self.high, size)


class NormalDistribution(BaseDistribution):

    """ a normal distribution with input mean and standard deviation
    """

    NAME = "normal"
    _required_args = ("size", "mean", "std")

    def _generate(self, size=1):
        return np.random.normal(self.mean, self.std, size)


class LogUniformDistribution(BaseDistribution):

    """ a log distribution of floating point numbers
    """

    NAME = "loguniform"
    _required_args = ("size", "low", "high")

    def _post_init(self):
        assert 0 <= self.low <= self.high, (self.low, self.high)

    def _generate(self, size=1):
        return np.random.uniform(self.low, self.high, size)


class LogNormalDistribution(BaseDistribution):

    """ a log normal distribution with input mean and standard deviation
    """

    NAME = "lognormal"
    _required_args = ("size", "mean", "std")

    def _generate(self, size=1):
        return np.random.lognormal(self.mean, self.std, size)


class QUniformDistribution(BaseDistribution):

    """ a quantized uniform distribution of floating point numbers
    """

    NAME = "quniform"
    _required_args = ("size", "low", "high", "q")

    def _generate(self, size=1):
        return quantize(self.q, np.random.uniform(self.low, self.high, size))


class QNormalDistribution(BaseDistribution):

    """ a quantized normal distribution with input mean and standard deviation
    """

    NAME = "qnormal"
    _required_args = ("size", "mean", "std", "q")

    def _generate(self, size=1):
        return quantize(self.q, np.random.normal(self.mean, self.std, size))


class QLogUniformDistribution(BaseDistribution):

    """ a quantized log distribution of floating point numbers
    """

    NAME = "qloguniform"
    _required_args = ("size", "low", "high", "q")

    def _post_init(self):
        assert 0 <= self.low <= self.high, (self.low, self.high)

    def _generate(self, size=1):
        return quantize(self.q, np.random.uniform(self.low, self.high, size))


class QLogNormalDistribution(BaseDistribution):

    """ a quantized log normal distribution with input mean and standard deviation
    """

    NAME = "qlognormal"
    _required_args = ("size", "mean", "std", "q")

    def _generate(self, size=1):
        return quantize(self.q, np.random.lognormal(self.mean, self.std, size))


class DistributionFactory(object):

    """ class for creating distributions
    """
    NAMES = {getattr(cls, "NAME"): cls for cls in BaseDistribution.__subclasses__()}

    @staticmethod
    def create(params):
        assert isinstance(params, dict)
        name = params.pop('name')
        cls = DistributionFactory.NAMES[name]
        return cls(**params)
