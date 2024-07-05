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
        c = m.Maslow(filename=os.path.join("maslow", "data", "smallTest.xlsx"),
                     sheet="supply_TS_smooth_Empa",
                     time="A11:A15",
                     I="D11:D15,E11:E15",
                     P="D11:D15,E11:E15",
                     D="D11:D15,E11:E15",
                     E="D11:D15,E11:E15",
                     L="D11:D15,E11:E15",
                     Sb="D11:D15,E11:E15",
                     Sd="D11:D15,E11:E15",
                     Sto_start = "D11:D11,E11:E11",
                     Sto_end = "D11:D11,E11:E11",
                     c = "D11:D11,E11:E11")
        SPG = c.get_SPG()
        print(f"*** SPG is {SPG}")
        
        SAG = c.get_SAG()
        print(f"*** SAG is {SAG}")

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

if __name__ == '__main__':
    unittest.main()