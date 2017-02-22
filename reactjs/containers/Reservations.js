import React, { Component, PropTypes } from 'react'
import axios from 'axios'
import { getFullUrl } from '../utils'
import ReservationRow from '../components/ReservationRow'
import ErrorCard from '../components/ErrorCard'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

class Reservations extends Component {
    constructor() {
        super()
        this.state = {
            reservations: [],
            error: '',
            fetching: false
        }
    }

    componentWillMount() {
        this.setState({fetching: true})
        axios.get(getFullUrl("reservations/")).then(
            response => {
                this.setState({reservations: response.data, fetching:false})
            },
            error => {
                if(error.response.status == 403) {
                    localStorage.removeItem('user')
                    browserHistory.push(`/notebook/login`)
                }
                this.setState({fetching: false, error:'خطا در اتصال به سرور(تلاش مجدد)'})
            }
        )
    }

    render() {
        if(this.state.error) {
            return (
                <ErrorCard error={this.state.error} />
            )
        }
        if(this.state.fetching) {
            return (
                <div className="row">
                 <svg className="loading-svg center-block" width='48px' height='48px' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                    <circle cx="50" cy="50" r="40" stroke="#54c5d0" fill="none" strokeWidth="5" strokeLinecap="round">
                      <animate attributeName="stroke-dashoffset" dur="2s" repeatCount="indefinite" from="0" to="502"></animate>
                      <animate attributeName="stroke-dasharray" dur="2s" repeatCount="indefinite" values="200.8 50.19999999999999;1 250;200.8 50.19999999999999"></animate>
                    </circle>
                  </svg>
                </div>
            )
        }
        return (
            <div className="panel panel-default well col-lg-8 col-lg-offset-2">
                    <table className="table table-stripped table-bordered">
                        <thead>
                        <tr>
                            <th>نام پزشک</th>
                            <th>تخصص پزشک</th>
                            <th>تاریخ</th>
                            <th>زمان تعیین‌شده</th>
                            <th>وضعیت درخواست</th>
                        </tr>
                        </thead>
                        <tbody>
                        {
                            this.state.reservations.map(reservation => (
                                <ReservationRow key={reservation.pk} pk={reservation.pk} doctor_pk={reservation.doctor_pk} speciality={reservation.speciality}
                                date={reservation.date} from={reservation.from} to={reservation.to} status={reservation.status} full_name={reservation.full_name}/>
                            ))
                        }
                        </tbody>
                    </table>
            </div>
        )
    }
}

export default Reservations