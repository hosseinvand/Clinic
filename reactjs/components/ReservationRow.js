import React, {Component, PropTypes} from 'react'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

const  statusToString = {
    PENDING : 'در دست بررسی',
    ACCEPTED : 'تعیین شده',
    REJECTED : 'رد شده',
    EXPIRED : 'تاریخ گذشته'
}

const  statusToClass = {
    PENDING : "bg-info text-info",
    ACCEPTED : "bg-success text-success",
    REJECTED : "bg-danger text-danger",
    EXPIRED : "bg-danger text-danger"
}

class ReservationRow extends Component {
  constructor(props){
    super(props)
  }

  render(){
    const {
        pk,
        doctor_pk,
        speciality,
        date,
        from,
        to,
        status,
        full_name
    } = this.props

    return(
      <tr id={pk} className="centered-cells">
        <td><a href={`/notebook/doctor/${doctor_pk}`} className="text-primary">{ full_name }</a></td>
        <td>{ speciality }</td>
        <td>{ date }</td>
        <td>{ from } تا { to }</td>
        <td className={statusToClass[status]}> { statusToString[status] } </td>
      </tr>
    )
  }
}

ReservationRow.propTypes = {
    pk: PropTypes.number,
    colorClass: PropTypes.string,
    full_name: PropTypes.string,
    doctor_pk: PropTypes.number,
    speciality: PropTypes.string,
    date: PropTypes.string,
    from: PropTypes.number,
    to: PropTypes.number,
    status: PropTypes.string
}

export default ReservationRow
