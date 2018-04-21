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

    @staticmethod
    def metres_to_mph(value):
        return value*3600/1609.34

    @staticmethod
    def kmph_to_metres(value):
        return value*5/18

    @staticmethod
    def metres_to_kmph(value):
        return value*18/5


class GeneralProperties(object):
    """
    Properties shared by both sides of the bridge.
    """
    def __init__(self):
        self.load_defaults()
        self.restore_defaults()

    def load_defaults(self, default_L=200, default_l=4.8, default_v=40.0,
            default_c=5):
        self.default_L = default_L
        self.default_l = default_l
        self.default_v = Conversions.kmph_to_metres(default_v)
        self.default_c = default_c

    def restore_defaults(self):
        self.default_constants()
        self.calc_variables()

    def default_constants(self):
        self.L = self.default_L
        self.l = self.default_l
        self.v = self.default_v
        self.c = self.default_c

    def calc_variables(self):
        self.h0 = 0
        self.trij = 0
        self.calc_h0()
        self.calc_trij()

    def calc_h0(self):
        self.h0 = (self.l/self.v) + 2

    def calc_trij(self):
        self.trij = ((self.L + self.l)/self.v) * 4/3


class BridgeSide(object):
    """
    A class detailing the properties of a single side of a bridge.
    """
    def __init__(self, general_properties):
        self.p = general_properties
        self.load_defaults()
        self.restore_defaults()

    def load_defaults(self, default_Q=10, default_n0=0):
        self.default_Q = default_Q
        self.default_n0 = default_n0
        self.tg = 0
        self.tr = 0
        self.na = 0
        self.np = 0
        self.nq = 0
        self.r = 0
        self.tw = 0

    def restore_defaults(self):
        self.default_constants()

    def default_constants(self):
        self.Q = self.default_Q
        self.n0 = self.default_n0

    def calc_tg(self, n_p):
        return np.log(n_p) + (self.p.h0 *(n_p - 1))

    def calc_tr(self, tg=None):
        if tg is None:
            tg = self.tg
        self.tr = (2*self.p.trij) + tg

    def calc_na(self, tg):
        self.na = np.floor(((self.tr + tg) * self.Q) / 60)

    def calc_np(self, tg):
        tg_out = 0.0
        n_p = 0

        while(True):
            if tg < tg_out:
                self.np = n_p - 1
                return
            n_p += 1
            tg_out = self.calc_tg(n_p)

    def calc_nq(self):
        nq = (self.p.c * self.na) - (self.p.c * self.np)
        if nq < 0:
            nq = 0
        self.nq = nq

    def calc_r(self):
        self.r = np.floor(self.nq / self.np)

    def calc_tw(self, tg):
        self.tw = ((self.r + 1) * self.tr) + (self.r * tg)


class Model1PlotFunction(BasePlotFunction):
    """
    A class containing model state information.
    """
    def _init_grapher_data(self):
        self.plot_type = PlotType.MODEL_1
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = DisplayUserOptions(show_xrange=True,
            show_set_constants=True)
        self.xvar_strings = [
            'tg',
            ]
        self.yvar_strings = [
            'tw',
            ]
        self.constant_strings = [
            'Bridge length (m)', 'Car length (m)', 'Crossing velocity (km/h)',
            'Arrival rate (per min)', 'Cycle',
            ]
        self._x_var_to_func = {
            'tg': self._x_is_tg,
            }
        self._y_var_to_func = {
            'tw': self._y_is_tw,
            }

    def _init_model_data(self):
        self.p = GeneralProperties()
        self.i = BridgeSide(self.p)
        self.j = BridgeSide(self.p)

    def get_constant_vals(self):
        constant_vals = [
            self.p.default_L, self.p.default_l,
            Conversions.metres_to_kmph(self.p.default_v), self.i.default_Q,
            self.p.default_c
            ]
        return constant_vals

    def set_constant_vals(self, vals):
        self.p.load_defaults(default_L=vals[0], default_l=vals[1],
            default_v=vals[2], default_c=vals[4])
        self.i.load_defaults(default_Q=vals[3])
        self.j.load_defaults(default_Q=vals[3])

    def restore_defaults(self):
        self.p.restore_defaults()
        self.i.restore_defaults()
        self.j.restore_defaults()

    def calc_all_variables(self, calc_tg=True):
        self.p.calc_variables()
        self.i.calc_variables(calc_tg)
        self.j.calc_variables(calc_tg)


    ####################################################################
    #                Independant variable calculations                 #
    ####################################################################

    def _x_is_tg(self, var_min, var_max, var_data):
        self.i.tg = np.arange(var_min, var_max + 0.1, 0.1)
        return self.i.tg


    ####################################################################
    #                 Dependant variable calculations                  #
    ####################################################################

    def _y_is_tw(self, var_min, var_max, var_data):
        tw = []
        self.p.calc_trij()

        for tg in self.i.tg.tolist():
            self.i.calc_tr(tg)
            self.i.calc_np(tg)
            self.i.calc_na(tg)
            self.i.calc_nq()
            self.i.calc_r()
            self.i.calc_tw(tg)
            tw.append(self.i.tw)

        return np.asarray(tw)
