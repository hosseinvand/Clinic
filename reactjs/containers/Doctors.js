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
                console.log(response)
                this.setState({doctors: response.data})
                // browserHistory.push(`/notebook/doctors`)
            },
            error => this.setState({error: 'خطا در اتصال به سرور(تلاش مجدد)'})
        )
    }

    render() {
        return (
            <div>
                {
                    this.state.error &&
                    <div className="col-md-4 col-md-offset-4">
                        <div className="alert alert-danger">
                            <strong>{this.state.error}</strong>
                        </div>
                    </div>
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