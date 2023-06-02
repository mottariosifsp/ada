from django.test import TestCase

import unittest
from area.models import Area
from .models import Classs

class ClassTestCase(unittest.TestCase):
    def setUp(self):
        self.high_school_area = Area.objects.create(name_area='High School Area', registration_area_id='HS1', is_high_school=True)
        self.college_area = Area.objects.create(name_area='College Area', registration_area_id='COL1', is_high_school=False)

    def test_get_semester_high_school_high_school_area(self):
        class_obj = Classs(area=self.high_school_area, semester=3)
        result = class_obj.get_semester_high_school()
        self.assertEqual(result, 2)

    def test_get_semester_high_school_college_area(self):
        class_obj = Classs(area=self.college_area, semester=4)
        result = class_obj.get_semester_high_school()
        self.assertEqual(result, 4)

if __name__ == '__main__':
    unittest.main()