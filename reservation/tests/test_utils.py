from django.contrib.auth.models import User

from reservation import models
from reservation.models import Doctor, SystemUser, Office, Patient


def create_test_user(username, password, first_name='ahmad', last_name='ahmadi', email='ahmad@gmail.com', **kwargs):
    return User.objects.create_user(username=username, email=email, password=password,
                                    first_name=first_name, last_name=last_name)

def create_test_system_user(user, id_code):
    patient = Patient()
    patient.save()
    return SystemUser.objects.create(user=user, id_code=id_code, role=patient)


def create_test_doctor(doctor_code,id_code, username, password):
    user = create_test_user(username=username, password=password)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education='S', speciality='Jarahi', insurance='Iran',
                                   price=35000, cv='maybe not the best doc in the world but the happiest one :)',
                                   contract='contracts/')
    return SystemUser.objects.create(user=user, id_code=id_code, role=doctor)


def create_office(phone, city, from_hour, to_hour):
    office = Office.objects.create(city=city, from_hour=from_hour, to_hour=to_hour, address="address",
                                   phone=phone, telegram="telegram", base_time=15, opening_days=None)
    return office


def create_custom_test_doctor(city, from_hour, to_hour, doctor_code, username, password, education, speciality,
                              insurance, price, id_code, first_name, last_name):
    user = create_test_user(username=username, password=password, first_name=first_name, last_name=last_name)
    doctor = Doctor.objects.create(doctor_code=doctor_code, education=education, speciality=speciality,
                                   insurance=insurance,
                                   price=price, cv='maybe not the best doc in the world but the happiest one :)',
                                   contract='contracts/')
    office = create_office(phone=price, city=city, from_hour=from_hour, to_hour=to_hour)
    doctor.office = office
    doctor.save()
    return SystemUser.objects.create(user=user, id_code=id_code, role=doctor)


def create_multiple_doctors(count):
    doctors = []
    for i in range(count):
        education = models.EDUCATION_TYPES[i % len(models.EDUCATION_TYPES)][0]
        speciality = models.SPECIALITY_TYPES[i % len(models.SPECIALITY_TYPES)][0]
        insurance = models.INSURANCE_TYPES[i % len(models.INSURANCE_TYPES)][0]
        city = models.CITY_NAMES[i % len(models.CITY_NAMES)][0]
        from_hour = (i + 8) % len(models.HOURS)
        to_hour = (i + 3 + 8) % len(models.HOURS)
        doctors.append(
            create_custom_test_doctor(city=city, from_hour=from_hour, to_hour=to_hour, doctor_code=i * 10,
                                      username="doctor{}".format(i), password="password{}".format(i),
                                      education=education,
                                      speciality=speciality, insurance=insurance, price=i * 10000, id_code=i * 200,
                                      first_name="first_name{}".format(i), last_name="last_name{}".format(i)))
    return doctors