import React from 'react'
import ReservationRow from '../components/ReservationRow'
import renderer from 'react-test-renderer'

test('renders correctly', () => {
  const tree = renderer.create(
    <ReservationRow date="۱۳۹۴/۲/۲" doctor_pk={2} from={14} full_name="علی رادمنش" pk={3} speciality="چشم" status="PENDING" to={16} />
  ).toJSON();
  expect(tree).toMatchSnapshot();
});