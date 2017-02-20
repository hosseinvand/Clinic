import React from 'react'
import ErrorCard from '../components/ErrorCard'
import renderer from 'react-test-renderer'

test('renders correctly', () => {
  const tree = renderer.create(
    <ErrorCard error="خطا خطا خطا" />
  ).toJSON();
  expect(tree).toMatchSnapshot();
});