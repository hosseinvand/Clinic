import React, { Component, PropTypes } from 'react'
import axios from 'axios'
import { getFullUrl } from '../utils'
import DoctorCard from '../components/DoctorCard'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

class Doctors extends Component {
    constructor() {
        super()
        this.state = {
            doctors: [],
            error: ''
        }
    }

    componentWillMount() {
        axios.get(getFullUrl("doctors/")).then(
            response => {
                this.setState({doctors: response.data})
            },
            error => this.setState({error: 'خطا در اتصال به سرور(تلاش مجدد)'})
        )
    }

    render() {
        return (
            <div>
                {
                    this.state.error &&
                    <ErrorCard error={this.state.error} />
                }
                {
                    this.state.doctors.length > 0 &&
                    <div className="panel panel-default">
                        <div className="panel-body">
                        {this.state.doctors.map(
                            doctor => (<DoctorCard id={doctor.id} education={doctor.education} speciality={doctor.speciality} full_name={doctor.full_name} city={doctor.city}/>))
                        }
                        </div>
                    </div>
                }
            </div>
        )
    }
}

export default Doctors