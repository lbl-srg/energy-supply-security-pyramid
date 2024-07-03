#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import unittest
import pandas as pd

class Test_Maslow(unittest.TestCase):
    """
       This class contains the unit tests for
       :mod:`maslow.math.Maslow`.
    """

    def test_Maslow(self):
        import os
        import maslow.math.Maslow as m
        c = m.Maslow(filename=os.path.join("maslow", "data", "Maslow_CH_Ref_exec.xlsx"),
                     sheet="supply_TS_smooth_Empa",
                     time="A11:A8770",
                     I="C11:C8770,D11:D8770",
                     P="C11:C8770",
                     D="C11:C8770",
                     E="C11:C8770",
                     L="C11:C8770",
                     Sb="C11:C8770",
                     Sd="C11:C8770",
                     Sto_start = [0],
                     Sto_end = [0])
        SPG = c.get_SPG()
        print(f"*** SPG is {SPG}")

        #c.get_I()

    def test_sum(self):
        import maslow.math.Maslow as m
        df = pd.DataFrame({"AAA": [4, 5, 6, 7], 
                           "BBB": [10, 20, 30, 40], 
                           "CCC": [100, 50, -30, -50]})

        sums = m.Maslow.integrate_by_columns(df, 1)
        self.assertEqual(sums, [22, 100, 70])
        sum = m.Maslow.integrate_all_columns(df, 1)
        self.assertEqual(sum, 192)

