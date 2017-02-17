import React, {Component, PropTypes} from 'react'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

class DoctorCard extends Component {
  constructor(props){
    super(props)
  }

  render(){
    const {
        id,
        education,
        speciality,
        full_name,
        city
    } = this.props

    return(
      <div className="col-md-3">
        <div className="panel panel-default">
            <div className="panel-body">
                <div className="profile-sidebar">
                    <div className="profile-userpic">
                        <img src={require('./doctor.png')} className="img-responsive" alt=""/>
                    </div>
                    <div className="profile-usertitle">
                        <div className="profile-usertitle-education">
                            { education }
                        </div>
                        <div className="profile-usertitle-job">
                            { speciality }
                        </div>
                        <div className="profile-usertitle-name">
                            { full_name }
                        </div>
                        <div className="profile-usertitle-education">
                            { city } &nbsp;
                        </div>
                    </div>
                    <div className="profile-userbuttons">
                        <Link to={`/notebook/doctor/${id}`} className="btn btn-info btn-raised btn-md" role="button"> پروفایل</Link>
                    </div>
                </div>
            </div>
        </div>
      </div>
    )
  }
}

DoctorCard.propTypes = {
    id: PropTypes.number.isRequired,
    education: PropTypes.string.isRequired,
    speciality: PropTypes.string.isRequired,
    full_name: PropTypes.string.isRequired,
    city: PropTypes.string.isRequired
}

export default DoctorCard
