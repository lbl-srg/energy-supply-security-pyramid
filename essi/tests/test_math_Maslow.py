#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import unittest
import pandas as pd

class Test_Essi(unittest.TestCase):
    """
       This class contains the unit tests for
       :mod:`essi.math.Essi`.
    """

    def test_Essi(self):
        import os
        import essi.math.Essi as m

        c = m.Essi(filename=os.path.join("essi", "data", "CH_Ref_exec.xlsx"),
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
        import essi.math.Essi as m
        df = pd.DataFrame({"AAA": [4, 5, 6, 7],
                           "BBB": [10, 20, 30, 40],
                           "CCC": [100, 50, -30, -50]})

        sums = m.Essi.integrate_by_columns(df, 1)
        self.assertEqual(sums, [22, 100, 70])
        sum = m.Essi.integrate_all_columns(df, 1)
        self.assertEqual(sum, 192)

if __name__ == '__main__':
    unittest.main()