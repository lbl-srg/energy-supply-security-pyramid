#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######################################################
# Class that implements the energy security metrics
#
#######################################################
import openpyxl
import numpy as np
import pandas as pd

class Maslow(object):
    """ Class that implements the energy security metrics.

        Note that I, P, D, E, L, Sb and Sd must all have the same
        number of energy carriers, and these must be in the same order.
        For example, if the first column of I is electricity, then the first
        column of P must also be electricity, as these energy carriers
        are added, subtracted or compared for each carrier type.

    """

    def __init__(self, filename, sheet, time,
                 I,
                 P,
                 D,
                 E,
                 L,
                 Sb,
                 Sd,
                 Sto_start,
                 Sto_end,
                 c):

        # --------------------------
        # Class variables
        # self._libHome=os.path.abspath(".")
        self._filename = filename
        self._sheet = sheet

        # data frames
        self._time = self._get_pandas_frame(time)
        time = self._time[self._time.columns.to_list()[0]]
        self._time_step = time[1] - time[0]
        self._I = self._get_pandas_frames(I)
        #FIXME
        self._P = self._get_pandas_frames(P)
        self._D = self._get_pandas_frames(D)
        self._E = self._get_pandas_frames(E)
        self._L = self._get_pandas_frames(L)
        self._Sb = self._get_pandas_frames(Sb)
        self._Sd = self._get_pandas_frames(Sd)
        self._Sto_start = self._get_pandas_frames(Sto_start)
        self._Sto_end = self._get_pandas_frames(Sto_end)
        self._c = self._get_pandas_frames(c)

        if self._I.shape != self._P.shape:
            raise RuntimeError("I and P must have the same dimensions.")
        if self._I.shape != self._D.shape:
            raise RuntimeError("I and D must have the same dimensions.")
        if self._I.shape != self._E.shape:
            raise RuntimeError("I and E must have the same dimensions.")
        if self._I.shape != self._L.shape:
            raise RuntimeError("I and L must have the same dimensions.")
        if self._I.shape != self._Sb.shape:
            raise RuntimeError("I and Sb must have the same dimensions.")
        if self._I.shape != self._Sd.shape:
            raise RuntimeError("I and Sd must have the same dimensions.")
        if self._I.shape[1] != self._Sto_start.shape[1]:
            raise RuntimeError("I and Sto_start must have the same number of energy flows.")
        if self._I.shape[1] != self._Sto_end.shape[1]:
            raise RuntimeError("I and Sto_end must have the same number of energy flows.")
        if self._I.shape[1] != self._c.shape[1]:
            raise RuntimeError("I and c must have the same number of energy flows.")
        if self._Sto_start.shape[0] != 1:
            raise RuntimeError("Sto_start must have one row only as it is not a time series.")
        if self._Sto_end.shape[0] != 1:
            raise RuntimeError("Sto_end must have one row only as it is not a time series.")
        if self._c.shape[0] != 1:
            raise RuntimeError("c must have one row only as it is not a time series.")

        #FIXME: Do we need a Sto_start somewhere?

    def _get_pandas_frames(self, range_string):
        """ Low level function to return Pandas data frame.

        :param: range_string: Range of values if xls file, such as "A2:A4", or "A2:A4,"C2:C4"".
        """
        import pandas as pd
        frames = []
        for rs in range_string.split(","):
            fr=self._get_pandas_frame(rs)
            frames.append(fr)
        frame = pd.concat(frames, axis=1)
        return frame

    def _get_pandas_frame(self, range_string):
        """ Low level function to return Pandas data frame.
        """
        from openpyxl import load_workbook
        import pandas

        def load_workbook_range(range_string, ws):
            from openpyxl import load_workbook
            from openpyxl.utils import get_column_interval
            import re

            col_start, col_end = re.findall("[A-Z]+", range_string)

            data_rows = []
            for row in ws[range_string]:
                data_rows.append([cell.value for cell in row])
            return pandas.DataFrame(data_rows, columns=get_column_interval(col_start, col_end))

        wb = load_workbook(filename=self._filename, 
                   read_only=True)
        ws = wb[self._sheet]
        vals = load_workbook_range(range_string, ws)
        return vals

    @staticmethod
    def integrate_by_columns(data_frame, time_step):
        """
        Integrate each column individually and return an array of
        the integral of each column.
        
        Note that this function assumes each entry to have
        the same time step dt
        """
        sums = []
        for c in data_frame.columns.to_list():
            sums.append(time_step * sum(data_frame[c]))
        return sums
    
    @staticmethod
    def integrate_all_columns(data_frame, time_step):
        return sum(Maslow.integrate_by_columns(data_frame, time_step))
        
    def get_SPG(self):
        """
        Returns the self-production grade SPG
        """

        def get_phis(P):
            integrals = Maslow.integrate_by_columns(P, self._time_step)
            denominator = sum(integrals)
            phi = list(np.multiply(1/denominator, integrals))
            for p in phi:
                if abs(1-p) < 1E-8:
                    raise RuntimeError("Data error. Calculated phi for a quantity that is zero. This is not allowed for calculating SPG.")
            return phi
        
        def get_d(P):
            phis = get_phis(P)
            n = len(phis)
            summand = 0
            for phi in phis:
                summand += phi * np.log(phi)

            d = - summand / np.log(n)
            return d
        
        num = []

        P = Maslow.integrate_all_columns(self._P, self._time_step)
        L = Maslow.integrate_all_columns(self._L, self._time_step)
        # Call integrate with a time step of 1, which will get the right data format.
        Sto_end = Maslow.integrate_all_columns(self._Sto_end, 1)
        D = Maslow.integrate_all_columns(self._D, self._time_step)

        SPG = get_d(self._P) * (P-L+Sto_end)/D
        return SPG

    def get_SAG(self):
        """
        Returns the adequacy SAG
        """
        def get_f_i():
            P = self._P.to_numpy()
            I = self._I.to_numpy()
            Sd = self._Sd.to_numpy()
            Sb = self._Sb.to_numpy()
            L = self._L.to_numpy()
            D = self._D.to_numpy()

            lhs = P + I + Sd - Sb - L
            rhs = D

            retB = (lhs >= rhs)
            ret = retB.astype(float)

            return ret

        f = get_f_i()

        D = self._D.to_numpy()
        nFlo = D.shape[1]
        sum_D_over_j = np.zeros(D.shape[0])
        for i in range(nFlo):
            sum_D_over_j += D[:,i]
        # Compute integral, for each energy carrier i
        num = f * D
        # Array with each element being an energy carrier i, and the array contains the integral
        a = np.zeros(nFlo)
        for i in range(nFlo):
            # Integrate over each time step and divide each term by sum_j D_j(t)
            a1 = num[:,i] / sum_D_over_j
            a[i] = sum(a1)

        # sum of all c
        c = self._c.to_numpy()
        sum_c = 0
        for i in range(nFlo):
            sum_c += c[0,i]
        summand = c / sum_c * a
        SAG = 0
        for i in range(nFlo):
            SAG += summand[0, i]

        return SAG



    def ESSI(self, w, SPSG, SAG, AUG, SSG, AUT):
        """
        This functions returns the energy supply security index

        :param w[]: Array of weights w1, ..., w5
        :param SPSG: 
        :param SAG:
        :param AUG:
        :param SSG:
        :param AUT:
        :return: double The energy supply security index

        Usage: Type
            >>> import math.Maslow as c
            >>> m = c.Maslow()
            >>> m.ESSI(w=[0.1, 0.2, 0.3, 0.35, 0.05], \
            SPSG=0.3, \
            SAG=0.5, \
            AUG=0.9, \
            SSG=0.7, \
            AUT=0.1)
            0.65
        """
        return  (w[0] * SPSG + w[1] * SAG + w[2] * AUG + w[3] * SSG + w[4] * AUT)/sum(w)
