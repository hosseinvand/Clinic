import React, { Component, PropTypes } from 'react'

class Layout extends Component {
    // renderNavbar() {
    //     return (
    //         <div class="navbar navbar-default">
    //             <div class="container-fluid">
    //                 <div class="navbar-header">
    //                     <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-responsive-collapse">
    //                         <span class="icon-bar"></span>
    //                         <span class="icon-bar"></span>
    //                         <span class="icon-bar"></span>
    //                     </button>
    //                     <a class="active navbar-brand" href="{% url 'react_home' %}">کلینیک</a>
    //                 </div>
    //                 <div class="navbar-collapse collapse navbar-responsive-collapse">
    //                     <div id="navbar-links">
    //                         <ul class="nav navbar-nav">
    //                             <li><a href="/notebook/doctors">پزشکان</a></li>
    //                             <li><a href="/panel">مشاهده نوبت‌ها</a></li>
    //                         </ul>
    //                     </div>
    //                     <ul class="nav navbar-nav navbar-left">
    //                         {% if user.is_authenticated %}
    //                             <li>
    //                                 <a href="#" >
    //                                     {{ user.first_name }}
    //                                     به کلینیک خوش آمدید
    //                                 </a>
    //                             </li>
    //                             <li><a href="{% url "react_logout" %}">خروج</a></li>
    //                         {% else %}
    //                             <li><a href="/notebook/login">ورود</a></li>
    //                         {% endif %}
    //                     </ul>
    //                 </div>
    //             </div>
    //         </div>
    //     )
    // }

    render() {
        return (
            <div>
                {/*{this.renderNavbar()}*/}
                {this.props.children}
            </div>
        )
    }
}

export default Layout
