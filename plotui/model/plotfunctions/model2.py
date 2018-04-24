import numpy as np

from common import PlotType, DisplayUserOptions
from model.plotfunctions.general import BasePlotFunction

DEBUG = False


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
            default_N=5, default_tgmax=120):
        self.default_L = default_L
        self.default_l = default_l
        self.default_v = Conversions.kmph_to_metres(default_v)
        self.default_N = default_N
        self.default_tgmax = default_tgmax
        self.h0 = 0.0
        self.trij = 0.0

    def restore_defaults(self):
        self.default_constants()
        self.calc_variables()

    def default_constants(self):
        self.L = self.default_L
        self.l = self.default_l
        self.v = self.default_v
        self.N = self.default_N
        self.tgmax = self.default_tgmax
        self.tc = 0.0
        self.t = 0.0


    def reset_vars(self):
        self.t = 0.0

    def calc_variables(self):
        self.calc_h0()
        self.calc_trij()

    ####################################################################
    #                           Calculations                           #
    ####################################################################

    def calc_trij(self):
        self.trij = ((self.L + self.l)/self.v) * 4/3

    def calc_h0(self):
        self.h0 = (self.l/self.v) + 2

    def return_HT(self, N):
        return np.log(N) + (self.h0 * (N - 1))

class BridgeSide(object):
    """
    A class detailing the properties of a single side of a bridge.
    """
    def __init__(self, general_properties):
        self.p = general_properties
        self.load_defaults()
        self.restore_defaults()

    def load_defaults(self, default_Q=10, default_nq0=0):
        self.default_Q = default_Q
        self.default_nq0 = default_nq0

    def restore_defaults(self):
        self.default_constants()

    def default_constants(self):
        self.Q = self.default_Q
        self.nq0 = self.default_nq0
        self.tg = 0.0
        self.tr = 0.0
        self.tw = 0.0

        self.na = 0.0
        self.na_total = 0.0
        self.nar = 0.0
        self.nag = 0.0
        self.np = 0.0
        self.npmax = 0.0
        self.np_total = 0.0
        self.nq = 0.0

        self.Na = 0.0
        self.Np = 0.0
        self.psi_a = 0.0
        self.psi_c = 0.0
        self.psi_d = 0.0
        self.psi_ar = 0.0
        self.psi_ag = 0.0

    ####################################################################
    #                           Cycle Events                           #
    ####################################################################

    def calc_cycle_events(self, tgz):
        # Order: nq0 tr nar (nq+nar) tg nag na (nq+nag) npM np (nq-np) naT npT
        # Initial queue = queue at the end of the previous cycle
        self.nq0 = self.nq
        # tr, nar, update queue
        self.calc_tr(tgz)
        self.calc_nar()
        self.nq += self.nar
        # tg, nag, na, update queue
        self.calc_tg_nag()
        self.calc_na()
        self.nq += self.nag
        # np, npmax, update queue
        self.calc_npmax_np()
        self.nq -= self.np # 0 check?
        # naT, npT
        self.update_natotal()
        self.update_nptotal()

    def calc_tr(self, tgz):
        self.tr = (2 * self.p.trij) + tgz

    def calc_nar(self):
        self.nar = (int)((self.tr * self.Q) / 60)

    def calc_tg_nag(self):
        nq0 = self.nq
        nq = nq0
        for x in range(1, 10):
            nq = nq0 + (self.p.return_HT(nq) * self.Q / 60)

        self.tg = self.p.return_HT(nq)
        if self.tg > self.p.tgmax:
            self.tg = self.p.tgmax
            self.calc_nag()
        else:
            self.nag = int(nq - nq0)

    def calc_nag(self):
        self.nag = int((self.tg * self.Q) / 60)

    def calc_na(self):
        self.na = self.nar + self.nag

    def calc_npmax_np(self):
        iteration_count = 3
        # Set initial value of np
        self.npmax = 10

        for x in range(1,iteration_count):
            self.npmax = self.npmax - (self.fnpmax()/self.fdnpmax())

        self.npmax = int(self.npmax)
        self.np = self.nq if self.npmax > self.nq else self.npmax

    def fnpmax(self):
        return np.log(self.npmax) + (self.p.h0 * (self.npmax - 1)) - self.tg

    def fdnpmax(self):
        return 1 / self.npmax + self.p.h0

    def update_natotal(self):
        self.na_total += self.na

    def update_nptotal(self):
        self.np_total += self.np

    def reset_vars(self):
        self.na_total = 0.0
        self.np_total = 0.0
        self.nq0 = self.default_nq0
        self.nq = self.nq0
        self.psi_a = 0.0
        self.psi_c = 0.0
        self.psi_d = 0.0
        self.psi_ar = 0.0
        self.psi_ag = 0.0

    ####################################################################
    #                    Waiting time calculations                     #
    ####################################################################

    def calc_Na(self, N):
        self.Na = N - self.na_total + self.na

    def calc_psi_a(self):
        self.psi_a = (1 - (self.Na / self.na)) * self.p.tc

    def calc_Np(self, N):
        Np = N - self.np_total + self.np
        self.Np = self.Na if Np < 1 else Np

    def calc_psi_d(self):
        self.psi_d = self.tr + self.p.return_HT(self.Np)

    def calc_psi_ar(self):
        self.psi_ar = (1 - (self.Na / self.nar)) * self.tr

    def calc_psi_ag(self):
        self.psi_ag = self.p.return_HT(self.Np)

    ####################################################################
    #                              Debug                               #
    ####################################################################

    def print_titles(self):
        print()
        print(' {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} |'
              ' {:<8} | {:<8} | {:<8} | {:<8} | {:<8} | {:<8} |'
              ' {:<8} | {:<8} | {:<8} | {:<8} | '.format(
                'N', 'tr', 'tg', 'Na', 'nar', 'nag', 'na',
                'na_total', 'Np', 'np', 'np_total', 'psi_a', 'psi_c', 'psi_d',
                'psi_ar', 'psi_ag',
                ))
        print()

    def print_vars(self, N):
        print(' {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} |'
              ' {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} |'
              ' {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} | {:<8.2f} |'
              ' {:<8.2f} | '.format(
                N, self.tr, self.tg, self.Na, self.nar, self.nag, self.na,
                self.na_total, self.Np, self.np, self.np_total, self.psi_a,
                self.psi_c, self.psi_d, self.psi_ar, self.psi_ag,
                )
              )


class Model2(object):
    """
    The model
    """
    def __init__(self):
        self.p = GeneralProperties()
        self.i = BridgeSide(self.p)
        self.j = BridgeSide(self.p)

    ####################################################################
    #                     Communication Functions                      #
    ####################################################################

    def get_constant_vals(self):
        constant_vals = [
            self.p.default_L, self.p.default_l,
            Conversions.metres_to_kmph(self.p.default_v), self.i.default_Q,
            self.j.default_Q, self.p.default_tgmax, self.p.default_N,
            ]
        return constant_vals

    def set_constant_vals(self, vals):
        self.p.load_defaults(default_L=vals[0], default_l=vals[1],
            default_v=vals[2], default_N=vals[6], default_tgmax=vals[5])
        self.i.load_defaults(default_Q=vals[3])
        self.j.load_defaults(default_Q=vals[4])


    ####################################################################
    #                         Model Functions                          #
    ####################################################################

    def _init_results_lists(self):
        self.tw_l = []
        self.t_l = []
        self.psi_a_l = []
        self.psi_c_l = []
        self.psi_d_l = []
        self.psi_ar_l = []
        self.psi_ag_l = []

    def restore_defaults(self):
        self.p.restore_defaults()
        self.i.restore_defaults()
        self.j.restore_defaults()

    def calc_all_variables(self, calc_tg=True):
        self.p.calc_variables()
        self.i.calc_variables(calc_tg)
        self.j.calc_variables(calc_tg)

    def run_simulation(self, N=None):
        if N is None:
            N = self.p.N

        # Initialise and calculate dummy data for tgj
        self.p.calc_trij()
        self.p.calc_h0()
        self.j.tg = 40
        self.calc_ij_cycle_events()

        if DEBUG and ((N % 20) == 0 or N == 1):
            self.i.print_titles()

        if N < 1:
            return

        # Reset counters, caclulate initial state
        self.i.reset_vars()
        self.j.reset_vars()
        self.p.reset_vars()
        self.calc_ij_cycle_events()

        # Recalclate the cycle events until the car arrives
        while True:
            # If the car hasn't arrived, calculate cycle events
            if N > self.i.na_total:
                self.calc_ij_cycle_events()
                self.p.t += self.p.tc
            # If the car has arrived, calc Na, go onto the next step
            else:
                self.i.calc_Na(N)
                break

        # If the car can leave during the cycle it arrives
        if N <= self.i.np_total:
            # Calculate passing position
            self.i.calc_Np(N)
            # If the car arrives whilst the light is red
            if self.i.Na <= self.i.nar:
                self.i.calc_psi_ar()
                self.i.calc_psi_ag()
                self.i.tw = self.i.psi_ar + self.i.psi_ag
            # If the car arrives whilst the light is green
            else:
                self.i.calc_psi_ag()
                self.i.tw = self.i.psi_ag
        # If the car can't leave during the cycle it arrives
        else:
            # Calculate the arrival delay
            self.i.calc_psi_a()
            # Simulate cycles until the car is able to leave
            while True:
                # Recalculate all events to get to the next cycle
                self.calc_ij_cycle_events()
                # If it can depart during this cycle
                if N <= self.i.np_total:
                    self.i.calc_Np(N)
                    self.i.calc_psi_d()
                    self.i.tw = self.i.psi_a + self.i.psi_c + self.i.psi_d
                    break
                # If it can't depart then increment the cycle time
                else:
                    self.i.psi_c += self.p.tc


        self.p.t += self.i.tw
        self.append_vars()

        if DEBUG:
            self.i.print_vars(N)


    ####################################################################
    #                Independant variable calculations                 #
    ####################################################################

    def _x_is_N(self, var_min, var_max, var_data):
        self.reset_result_lists()

        N_l = np.arange(var_min, var_max + 1, 1)
        for N in N_l:
            self.run_simulation(N)

        return N_l

    def _x_is_t(self, var_min, var_max, var_data):
        self._x_is_N(var_min, var_max, var_data)
        return np.asarray(self.t_l)


    ####################################################################
    #                 Dependant variable calculations                  #
    ####################################################################

    def _y_is_tw(self, var_min, var_max, var_data):
        return np.asarray(self.tw_l)

    def _y_is_psi_a(self, var_min, var_max, var_data):
        return np.asarray(self.psi_a_l)

    def _y_is_psi_c(self, var_min, var_max, var_data):
        return np.asarray(self.psi_c_l)

    def _y_is_psi_d(self, var_min, var_max, var_data):
        return np.asarray(self.psi_d_l)

    def _y_is_psi_ar(self, var_min, var_max, var_data):
        return np.asarray(self.psi_ar_l)

    def _y_is_psi_ag(self, var_min, var_max, var_data):
        return np.asarray(self.psi_ag_l)


    ####################################################################
    #                             Helpers                              #
    ####################################################################

    def calc_ij_cycle_events(self):
        self.i.calc_cycle_events(self.j.tg)
        self.j.calc_cycle_events(self.i.tg)
        self.p.tc = self.i.tg + self.i.tr
        self.p.t += self.p.tc

    def reset_result_lists(self):
        self.tw_l = []
        self.t_l = []
        self.psi_a_l = []
        self.psi_c_l = []
        self.psi_d_l = []
        self.psi_ar_l = []
        self.psi_ag_l = []

    def append_vars(self):
        self.tw_l.append(self.i.tw)
        self.t_l.append(self.p.t / 60)
        self.psi_a_l.append(np.inf if self.i.psi_a == 0 else self.i.psi_a)
        self.psi_c_l.append(np.inf if self.i.psi_c == 0 else self.i.psi_c)
        self.psi_d_l.append(np.inf if self.i.psi_d == 0 else self.i.psi_d)
        self.psi_ar_l.append(np.inf if self.i.psi_ar == 0 else self.i.psi_ar)
        self.psi_ag_l.append(np.inf if self.i.psi_ag == 0 else self.i.psi_ag)


class Model2PlotFunction(BasePlotFunction):
    """
    A class containing model state information.
    """
    def _init_model_data(self):
        self.model = Model2()

    def _init_grapher_data(self):
        self.plot_type = PlotType.MODEL_2
        self.plot_type_string = PlotType.to_string(self.plot_type)
        self.user_option_args = DisplayUserOptions(show_xrange=True,
            show_set_constants=True)
        self.xvar_strings = [
            'N',
            't',
            ]
        self.yvar_strings = [
            'tw',
            'psi_a',
            'psi_c',
            'psi_d',
            'psi_ar',
            'psi_ag',
            ]
        self.constant_strings = [
            'Bridge length (m)', 'Car length (m)', 'Crossing velocity (km/h)',
            'Qi (per min)', 'Qj (per min)', 'tgmax', 'N'
            ]
        self._x_var_to_func = {
            'N': self.model._x_is_N,
            't': self.model._x_is_t,
            }
        self._y_var_to_func = {
            'tw': self.model._y_is_tw,
            'psi_a': self.model._y_is_psi_a,
            'psi_c': self.model._y_is_psi_c,
            'psi_d': self.model._y_is_psi_d,
            'psi_ar': self.model._y_is_psi_ar,
            'psi_ag': self.model._y_is_psi_ag,
            }
