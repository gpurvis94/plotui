import numpy as np

from common import PlotType, DisplayUserOptions
from model.plotfunctions.general import BasePlotFunction


class Conversions:
    """
    A helper class for static conversion methods.
    """
    @staticmethod
    def mph_to_metres(value):
        """
        Converts a miles per hour value into a metres per second value.
        :param float value: The miles per hour value to be converted.
        :return float: The converted value.
        """
        return value*1609.34/3600


class BridgeSide(object):
    """
    A class detailing the properties of a single side of a bridge.
    """
    def __init__(self,
                 arrival_rate=10,
                 initial_queue=10,
                 ):
        self.Q = arrival_rate
        self.n_i = initial_queue
        self.tg = None
        self.tr = None


class GeneralProperties(object):
    """
    A class detailing the general properties pertaining to the bridge
    and both sides of the bridge.
    """
    def __init__(self,
                 bridge_length=20.0,
                 car_length=4.5,
                 separation_distance=2.0,
                 crossing_velocity=20.0,
                 ):
        """
        Sets the values. Default values will be used if not listed.
        :param float bridge_length: The length of the bridge, metres.
        :param float car_length: The length of an average car, metres.
        :param float separation_distance: Distance between cars, metres.
        :param float crossing_velocity: Crossing velocity, miles ph.
        """
        self.L = bridge_length
        self.l = car_length
        self.s = separation_distance
        self.v = Conversions.mph_to_metres(crossing_velocity)


class Model1PlotFunction(BasePlotFunction):  
    """
    A class containing model state information.
    """
    def __init__(self):
        """
        :param BridgeSide side: Both sides of the bridge data.
        :param GeneralProperties props: Non-side specific information.
        """
        super().__init__(
            plot_type=PlotType.MODEL_1,
            user_option_args=DisplayUserOptions(True),
            xvar_strings=['Car Length', 'Bridge Length'],
            yvar_strings=['tg', 'tr'],
            variable_to_func={
                'Car Length': self._var_is_car_length,
                'Bridge Length': self._var_is_bridge_length,
                'tg': self._var_is_tg,
                'tr': self._var_is_tr,
                },
            )

        # Initialize params
        self.i = BridgeSide()
        self.j = BridgeSide()
        self.p = GeneralProperties()

        # Calculate intial values of related params
        self.calc_tg(self.i)
        self.calc_tg(self.j)

    ####################################################################
    #                  Variable calculation functions                  #
    ####################################################################

    # TODO ALL
    def _var_is_car_length(self, var_min, var_max, var_data):
        return np.arange(var_min, var_max, 0.01)

    def _var_is_bridge_length(self, var_min, var_max, var_data):
        return np.arange(var_min, var_max, 0.1)

    def _var_is_tg(self, var_min, var_max, var_data):
        return var_data**2

    def _var_is_tr(self, var_min, var_max, var_data):
        return var_data**4

    ####################################################################
    #                         Model functions                          #
    ####################################################################

    def calc_tg(self, s, p=None):  #TODO
        """
        Calculates tg. Current limits are 30s < tg < 120s.
        :param BridgeSide s: The side for which to calculate tg.
        :param GeneralProperties p: The general data properties to use.
        """
        if p is None:
            p = self.p
        s.tg = np.log(s.n_i) + ((p.l + p.s)/p.v)*(s.n_i - 1)