import React, { Component, PropTypes } from 'react'
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-router'

class Layout extends Component {
    renderNavbar() {
        const user = localStorage.getItem('user')
        return (
            <div className="navbar navbar-default">
                <div className="container-fluid">
                    <div className="navbar-header">
                        <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-responsive-collapse">
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                            <span className="icon-bar"></span>
                        </button>
                        <a className="active navbar-brand" href="#">کلینیک</a>
                    </div>
                    <div className="navbar-collapse collapse navbar-responsive-collapse">
                        <div id="navbar-links">
                            <ul className="nav navbar-nav">
                                <li><Link to="/notebook/doctors">پزشکان</Link></li>
                                <li><Link to="/notebook/reservations">مشاهده نوبت‌ها</Link></li>
                            </ul>
                        </div>
                        <ul className="nav navbar-nav navbar-left">
                            { user &&
                                <li>
                                    <a href="#" >
                                        { user + ' ' }
                                        به کلینیک خوش آمدید
                                    </a>
                                </li>
                            }
                            {
                                user ? <li><Link href="/notebook/logout/" onClick={() => localStorage.removeItem('user')}>خروج</Link></li> : <li><Link href="/notebook/login">ورود</Link></li>
                            }
                        </ul>
                    </div>
                </div>
            </div>
        )
    }

    render() {
        return (
            <div>
                {this.renderNavbar()}
                {this.props.children}
            </div>
        )
    }
}

export default Layout
