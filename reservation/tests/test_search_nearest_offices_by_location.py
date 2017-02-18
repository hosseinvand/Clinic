from _decimal import Decimal

from django.test.testcases import TestCase

from reservation.models import Office, CITY_NAMES, HOURS
from reservation.tests.test_utils import create_multiple_doctors, create_office
from reservation.views import GetSearchByLocationOfficeResult

"""
unit testing search by location with some kinds of case:
    1.size of expected result [lower and upper bound]
    2.nearest neighbour office[just one]
    3.not far offices in top results
"""
class SearchNearestOfficeByLocation(TestCase):
    COUNT = 10

    def setUp(self):
        self.far_office = create_office('23423546', city=CITY_NAMES[3][0], from_hour=HOURS[3][0], to_hour=HOURS[7][0],
                                        lat_position=10.552800413453546,
                                        lng_position=90.18853759765625)
        create_multiple_doctors(self.COUNT)
        self.far_office = create_office('23423540', city=CITY_NAMES[3][0], from_hour=HOURS[3][0], to_hour=HOURS[7][0],
                                        lat_position=10.552800413453546,
                                        lng_position=90.18853759765625)

        self.search_class = GetSearchByLocationOfficeResult()
        self.position = {'lat': 35.6929946320988, 'lng':51.39129638671875}
        self.offices = Office.objects.all()

    def test_nearest_one_to_sharif_location(self):
        office_id_list = self.search_class.get_list_of_top_office_ids(offices=self.offices, loc_lat=self.position['lat'],
                                                                      loc_lng=self.position['lng'], number=1)

        #lower bound number of results check
        self.assertEqual(len(office_id_list), 1, "1 result for number=1")
        res_office = Office.objects.get(id=office_id_list[0])
        self.assertEqual(res_office.city, CITY_NAMES[0][0], "city index is zero")
        # nearest to this location is itself!

    # check that the far office is not in results - hatta ba in ke ham aval va ham akhar ezafe shod
    def test_not_a_far_location_in_near_offices(self):
        office_id_list = self.search_class.get_list_of_top_office_ids(offices=self.offices, loc_lat=self.position['lat'],
                                                                      loc_lng=self.position['lng'], number=self.COUNT)
        #upper bound number of results check
        self.assertEqual(len(office_id_list), self.COUNT, "correct number of results")
        for id in office_id_list:
            office = Office.objects.get(id=id)
            # print("position of office ", id, " is: ", office.get_position)
            delta_lat = abs(office.lat_position - self.position['lat'])
            delta_lng = abs(office.lng_position - self.position['lng'])
            self.assertLessEqual(delta_lat, self.COUNT/(self.COUNT+1), "lat is not so far")
            self.assertLessEqual(delta_lng, self.COUNT/(self.COUNT+1), "lng is not so far")
