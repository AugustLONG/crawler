# coding=utf8
import os, sys
import xmltodict

alibaba = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if sys.path.count(alibaba) == 0:
    sys.path.insert(0, alibaba)
os.environ['DJANGO_SETTINGS_MODULE'] = 'alibaba.settings'
from alibaba.models import Country, City, Location, Zone, Province
from django.db import transaction


def create_country():
    content = open(u"国家.xml", "r").read()
    content = xmltodict.parse(content)
    # print content["SearchCountryResponse"]["CountryDetails"]
    for country_ in content["SearchCountryResponse"]["CountryDetails"]["CountryDetail"]:
        print country_
        # country_=country_["CountryDetail"]
        country = Country(id=country_["Country"], name=country_["CountryName"], ename=country_["CountryEName"],
                          chart=country_["CountryEName"].lower())
        country.save()


def create_province():
    content = open(u"中国省份.xml", "r").read()
    content = xmltodict.parse(content)
    # print content["SearchCountryResponse"]["CountryDetails"]
    for province_ in content["ProvinceDetails"]["ProvinceDetail"]:
        print province_
        # country_=country_["CountryDetail"]
        province = Province(id=province_["Province"], name=province_["ProvinceName"], ename=province_["ProvinceEName"],
                            chart=province_["ProvinceEName"].lower(), country_id=province_["Country"])
        province.save()


def create_city():
    content = open(u"国内城市.xml", "r").read()
    content = xmltodict.parse(content)
    # City.objects.all().delete()
    # print content["SearchCountryResponse"]["CountryDetails"]
    for province_ in content["CityDetails"]["CityDetail"]:
        print province_
        # country_=country_["CountryDetail"]
        city = City(id=province_["City"], name=province_["CityName"], ename=province_["CityEName"],
                        chart=None if not province_["CityEName"] else province_["CityEName"].lower(),
                        country_id=province_["Country"], province_id=province_["Province"],
                        airport=province_["Airport"], code=province_["CityCode"])
        try:
            with transaction.atomic():
                city.save()
        except:
            import traceback
            traceback.print_exc()
            continue



def create_location():
    # Location.objects.all().delete()
    content = open(u"行政区.xml", "r").read()
    content = xmltodict.parse(content)
    # print content["SearchCountryResponse"]["CountryDetails"]
    for province_ in content["LocationDetails"]["LocationDetail"]:
        print province_
        # country_=country_["CountryDetail"]
        location = Location(id=province_["Location"], name=province_["LocationName"], ename=province_["LocationEName"],
                            chart=None if not province_["LocationEName"] else province_["LocationEName"].lower(),
                            city_id=province_["LocationCity"])
        try:
            with transaction.atomic():
                location.save()
        except:
            import traceback
            traceback.print_exc()
            continue


def create_zone():
    # Zone.objects.all().delete()
    content = open(u"商业区全部.xml", "r").read()
    content = xmltodict.parse(content)
    # print content["SearchCountryResponse"]["CountryDetails"]
    for province_ in content["ZoneDetails"]["ZoneDetail"]:
        # print province_
        # country_=country_["CountryDetail"]
        zone = Zone(id=province_["Zone"], name=province_["ZoneName"], ename=province_["ZoneEName"],
                        chart=province_["ZoneName"].lower() if not province_["ZoneEName"] else province_["ZoneEName"].lower(),
                        city_id1=province_["City"], desc=province_["ZoneDesc"], mapuse=province_["ZoneMapuse"],
                        range=province_["ZoneRange"], mappic=province_["ZoneMapPic"])
        try:
            with transaction.atomic():
                print zone.city_id
                zone.save()
        except:
            import traceback
            traceback.print_exc()
            continue
            # create_Zone()

            # import api
            # results=api.OTA_HotelSearch()
            # # results=xmltodict.parse(results)
            # f=open("1.json","w")
            # f.write(results.encode("utf8"))
            # f.close()

if __name__ == '__main__':
    # create_country()
    # create_province()
    # create_city()
    # create_location()
    create_zone()
