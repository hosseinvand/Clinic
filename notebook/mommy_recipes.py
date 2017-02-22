from itertools import cycle

from model_mommy import mommy
from model_mommy.recipe import Recipe, seq, foreign_key

from reservation.models import Doctor, EDUCATION_TYPES, Office, SPECIALITY_TYPES, INSURANCE_TYPES, CITY_NAMES, HOURS, \
    Reservation, SystemUser, Patient

RESERVATION_STATUS = {
    'PENDING': 'در دست بررسی',
    'ACCEPTED': 'تعیین شده',
    'REJECTED': 'رد شده',
    'EXPIRED': 'تاریخ گذشته'
}

office_recipe = Recipe(
    Office,
    city=cycle([type[0] for type in CITY_NAMES]),
    phone=seq('0214433221'),
    from_hour=cycle([type[0] for type in HOURS][8:14]),
    to_hour=cycle([type[0] for type in HOURS][15:22]),
    opening_days=['sat', 'sun', 'mon', 'fri'],
    lat_position=seq(35.6929946320988, 0.0001),
    lng_position=seq(51.39129638671875, 0.0001)
)

doctor_recipe = Recipe(
    Doctor,
    doctor_code=seq(10001000, 15),
    education=cycle([type[0] for type in EDUCATION_TYPES]),
    speciality=cycle([type[0] for type in SPECIALITY_TYPES]),
    insurance=cycle([type[0] for type in INSURANCE_TYPES]),
    contract='contracts/',
    price=seq(30000, 2000),
)

patient_recipe = Recipe(
    Patient,
)

system_user_recipe = Recipe(
    SystemUser,
    id_code=seq('333222111'),
    role=foreign_key(patient_recipe)
)

reservation_recipe = Recipe(
    Reservation,
    doctor=foreign_key(doctor_recipe),
    patient=foreign_key(system_user_recipe),
    rejected=False,
    from_time=cycle([type[0] for type in HOURS][8:14]),
    to_time=cycle([type[0] for type in HOURS][15:22]),
)

def create_multiple_doctors(quantity):
    offices = office_recipe.make(_quantity=quantity)
    doctors = doctor_recipe.make(_quantity=quantity, office=cycle(offices))
    system_users = system_user_recipe.make(_quantity=quantity, role=cycle(doctors))
    return system_users
