import numpy as np

from common import PlotType, DisplayUserOptions
from model.plotfunctions.general import BasePlotFunction


class Conversions:
    """
    A helper class for static conversion methods.
    """
    @staticmethod
    def mph_to_metres(value):
        return value*1609.34/3600


class GeneralProperties(object):
    """
    Properties shared by both sides of the bridge.
    """
    def __init__(self):
        self.restore_defaults()

    def restore_defaults(self):
        self.init_constants()
        self.calc_variables()

    def init_constants(self):
        self.L = 20.0
        self.l = 4.5
        self.s = 2.0
        self.v = Conversions.mph_to_metres(20.0)
        self.r = 5

    def calc_variables(self):
        self.h0 = self.calc_h0()
        self.trij = self.calc_trij()

    def calc_h0(self):
        return ((self.l + self.s)/self.v)

    def calc_trij(self):
        return ((self.L + self.l)/self.v) + self.r


class BridgeSide(object):
    """
    A class detailing the properties of a single side of a bridge.
    """
    def __init__(self, general_properties):
        self.p = general_properties
        self.restore_defaults()

    def restore_defaults(self):
        self.init_constants()
        self.calc_variables()

    def init_constants(self):
        self.Q = 10
        self.n_i = 10

    def calc_variables(self):
        self.tg = self.calc_tg()
        self.tw = self.calc_tw()

    def calc_tg(self):
        return np.log(self.n_i) + (self.p.h0 *(self.n_i - 1))

    def calc_tw(self):
        return (2*self.p.trij) + self.tg


class Model1PlotFunction(BasePlotFunction):  
    """
    A class containing model state information.
    """
    def _init_grapher_data(self):
        self.plot_type = PlotType.MODEL_1
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = DisplayUserOptions(True)
        self.xvar_strings = [
            'Bridge length', 'Car length', 'Car separation',
            'Crossing velocity', 'Safety factor',
            ]
        self.yvar_strings = [
            'trij', 'tg', 'tw',
            ]
        self._variable_to_func = {
            'Bridge length': self._var_is_bridge_length,
            'Car length': self._var_is_car_length,
            'Car separation': self._var_is_car_separation,
            'Crossing velocity': self._var_is_crossing_velocity,
            'Safety factor': self._var_is_safety_factor,
            'tg': self._var_is_tg,
            'trij': self._var_is_trij,
            'tw': self._var_is_tw,
            }

    def _init_model_data(self):
        self.p = GeneralProperties()
        self.i = BridgeSide(self.p)
        self.j = BridgeSide(self.p)

    def restore_defaults(self):
        self.p.restore_defaults()
        self.i.restore_defaults()
        self.j.restore_defaults()

    def calc_all_variables(self):
        self.p.calc_variables()
        self.i.calc_variables()
        self.j.calc_variables()

    ####################################################################
    #                Independant variable calculations                 #
    ####################################################################

    def _var_is_bridge_length(self, var_min, var_max, var_data):
        self.p.L = np.arange(var_min, var_max + 0.01, 0.01)
        return self.p.L

    def _var_is_car_length(self, var_min, var_max, var_data):
        self.p.l = np.arange(var_min, var_max + 0.01, 0.01)
        return self.p.l

    def _var_is_car_separation(self, var_min, var_max, var_data):
        self.p.s = np.arange(var_min, var_max + 0.01, 0.01)
        return self.p.s

    def _var_is_crossing_velocity(self, var_min, var_max, var_data):
        self.p.v = np.arange(var_min, var_max + 0.01, 0.01)
        return self.p.v

    def _var_is_safety_factor(self, var_min, var_max, var_data):
        self.p.r = np.arange(var_min, var_max + 0.01, 0.01)
        return self.p.r

    ####################################################################
    #                 Dependant variable calculations                  #
    ####################################################################

    def _var_is_tg(self, var_min, var_max, var_data):
        self.calc_all_variables()
        return self.i.tg

    def _var_is_trij(self, var_min, var_max, var_data):
        self.calc_all_variables()
        return self.p.trij

    def _var_is_tw(self, var_min, var_max, var_data):
        self.calc_all_variables()
        return self.i.tw

    ####################################################################
    #                         Model functions                          #
    ####################################################################
