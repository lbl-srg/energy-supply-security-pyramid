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
                 Sto_end):

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
        self._P = self._I
        self._D = self._I
        self._E = self._I
        self._L = self._I
        self._Sb = self._I
        self._Sd = self._I
        self._Sto_end = [0]
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
       # print(frames)
        frame = pd.concat(frames, axis=1)
        print(frame)
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
            return phi
        
        def get_d(P):
            phis = get_phis(P)
            n = len(phis)
            print(f"*** n = {n}")
            summand = 0
            for phi in phis:
                summand += phi * np.log(phi)
            print(f"*** summand = {summand}")

            d = - summand / np.log(n)
            return d
        
        num = []

        P = Maslow.integrate_all_columns(self._P, self._time_step)
        L = Maslow.integrate_all_columns(self._L, self._time_step)
        Sto_end = sum(self._Sto_end)
        D = Maslow.integrate_all_columns(self._D, self._time_step)

        SPG = get_d(self._P) * (P-L+Sto_end)/D
        print(f"**** d = {get_d(self._P)}")
        return SPG



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
