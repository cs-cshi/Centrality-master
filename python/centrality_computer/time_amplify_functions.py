import math


class ExponentialFunction:
    def __init__(self, base=2, norm=0.001):
        """"""
        self._base, self._norm = base, norm

    def get_base(self):
        return self._base

    def exponent_fun(self, time):
        """base^(norm * time)"""
        exponent = float(time) * self._norm
        # print('time: ' + str(time) + ', norm: ' + str(self.norm) + ', amplify: ' + str(exponent))
        return math.pow(self._base, exponent)

    def exponent_fun_with_weight(self, time):
        exponent = float(time) * self._norm

        return math.pow(self._base, exponent)

    def amplify(self, time):
        return self.exponent_fun(time)

    def weight(self, time):
        """base^(norm * time)"""
        exponent = float(time) * self._norm
        # print('delta_time: ' + str(time) + ', norm: ' + str(self.norm) + ', weight: ' + str(float(exponent)))
        return math.pow(self._base, exponent)

    def __repr__(self):
        return 'Exp(b_%.3f_n_%.3f)' % (self._base, self._norm)



class LinearFunction:
    def __init__(self, base=2, norm=0.001):
        """"""
        self._base, self._norm = base, norm

    def get_base(self):
        return self._base

    def exponent_fun(self, time):
        """base * (norm * time)"""
        exponent = float(time) * self._norm
        # print('time: ' + str(time) + ', norm: ' + str(self.norm) + ', amplify: ' + str(exponent))
        return self._base * exponent

    def exponent_fun_with_weight(self, time):
        exponent = float(time) * self._norm

        return self._base * exponent

    def amplify(self, time):
        return self.exponent_fun(time)

    def weight(self, time):
        """base *(norm * time)"""
        exponent = float(time) * self._norm
        # print('delta_time: ' + str(time) + ', norm: ' + str(self.norm) + ', weight: ' + str(float(exponent)))
        return self._base * exponent

    def __repr__(self):
        return 'Linear(b_%.3f_n_%.3f)' % (self._base, self._norm)