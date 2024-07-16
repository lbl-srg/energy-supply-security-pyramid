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

        c = m.Maslow(filename=os.path.join("maslow", "data", "Maslow_CH_Ref_exec4.xlsx"),
                     sheet="supply_TS_smooth_Empa")
        SPG = c.get_SPG()
        print(f"*** SPG is {SPG}")

        SAG = c.get_SAG()
        print(f"*** SAG is {SAG}")

        AUG = c.get_AUG()
        print(f"*** AUG is {AUG}")

        SSG = c.get_SSG()
        print(f"*** SSG is {SSG}")

        AUT = c.get_AUT()
        print(f"*** AUT is {AUT}")

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