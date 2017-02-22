import React, { Component, PropTypes } from 'react'
import axios from 'axios'
import { getFullUrl } from '../utils'
import DoctorCard from '../components/DoctorCard'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

class DoctorProfile extends Component {
    constructor() {
        super()
        this.state = {
            tab: 'doctor',
            doctor: ''
        }
    }

    componentWillMount() {
        console.log(getFullUrl(`doctor/${this.props.params.id}/`))
        axios.get(getFullUrl(`doctor/${this.props.params.id}/`)).then(
            response => {
                console.log(response)
                this.setState({doctor: response.data})
                // browserHistory.push(`/notebook/doctors`)
            },
            error => this.setState({error: 'خطا در اتصال به سرور(تلاش مجدد)'})
        )
    }

    renderHeaderAndTabs() {
        const doctor = this.state.doctor
        return (
            <div>
            <div className="card hovercard">
                <div className="card-background">
                    <img className="card-bkimg" alt="" src="/static/image/back.png"/>
                </div>
                <div className="useravatar">
                    <img alt="" src="/static/image/doctor.png"/>
                </div>

                <div className="card-info">
                <span className="card-title">
    دکتر
                { doctor.full_name }
                </span>


                </div>
            </div>
            <div className="btn-pref btn-group btn-group-justified btn-group-lg" role="group" aria-label="...">
                <div className="btn-group" role="group">
                    <button type="button" id="doctorinfo" className="btn btn-default btn-raised" onClick={() => this.setState({tab : 'doctor'})}><span className="glyphicon glyphicon-user" aria-hidden="true"></span>
                        <div className="hidden-xs">مشخصات پزشک</div>
                    </button>
                </div>
                <div className="btn-group" role="group">
                    <button type="button" id="officeinfo" className="btn btn-default btn-raised" onClick={() => this.setState({tab : 'office'})}><span className="glyphicon glyphicon-home" aria-hidden="true"></span>
                        <div className="hidden-xs text-p">اطلاعات مطب</div>
                    </button>
                </div>
            </div>
            </div>
        )
    }

    renderDoctorDetail() {
        const doctor = this.state.doctor
        return (
            <div className="fade in active">
                    <dl className="dl-horizontal btn-lg">
                        <dt className="text-primary">نام پزشک</dt>
                        <dd>{ doctor.full_name }</dd>
                        <dt className="text-primary">میزان تحصیلات</dt>
                        <dd>{ doctor.education }   { doctor.speciality }</dd>
                        <dt className="text-primary">بیمه‌ تحت پوشش</dt>
                        <dd>{ doctor.insurance }</dd>
                        <dt className="text-primary">قیمت ویزیت</dt>
                        <dd>{ doctor.price } تومان</dd>
                        <dt className="text-primary">رزومه</dt>
                        <dd>{ doctor.cv}</dd>
                        <dt className="text-primary"></dt>
                        <dd></dd>
                    </dl>
                </div>
        )
    }

    renderOfficeDetail() {
        const office = this.state.doctor.office
        return (
                    <div className="fade in">
                        <dl className="dl-horizontal btn-lg">

                            <dt className="text-primary">شهر</dt>
                            <dd>{ office.city }</dd>
                            <dt className="text-primary"> آدرس </dt>
                            <dd>{ office.address } </dd>
                            <dt className="text-primary"> ساعت کاری </dt>
                            <dd>{ office.from_hour }
                                تا
                                { office.to_hour }</dd>
                            <dt className="text-primary">روزهای کاری </dt>
                            <dd> { office.opening_days}</dd>
                            <dt className="text-primary">تلفن</dt>
                            <dd>{ office.phone}</dd>
                            <dt className="text-primary">تلگرام</dt>
                            <dd>{ office.telegram}</dd>

                            <dt className="text-primary"></dt>
                            <dd></dd>

                            <dt className="text-primary"></dt>
                            <dd></dd>
                        </dl>
                </div>
                )
    }

    renderContent() {
        if(this.state.tab == 'doctor') {
            return this.renderDoctorDetail()
        }
        else {
            if(this.state.doctor.office) {
                return this.renderOfficeDetail()
            } else {
                return (
                    <div className="col-md-offset-1">
                        <h4>اطلاعات مطب پزشک ثبت نشده‌است.</h4>
                    </div>
                )
            }
        }
    }

    render() {
        const doctor = this.state.doctor
        if(!doctor) {
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
            <div className="col-lg-12 col-sm-6">
                {this.renderHeaderAndTabs()}
                <div className="well">
                    <div className="tab-content" id="tabs">
                        {this.renderContent()}
                    </div>
                </div>
            </div>
        )
    }
}

export default DoctorProfile