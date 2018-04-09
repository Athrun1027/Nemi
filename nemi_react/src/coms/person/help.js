import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import Cookies from 'js-cookie'

import { Row, Col } from 'antd';


class Help extends Component {

  constructor(props) {
    super(props);
    let user_cookie = Cookies.get("user");
    this.state = {
        user: user_cookie?JSON.parse(user_cookie):false,

    }
  }

  render() {
    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={24}>
              <h3>系统帮助</h3>
              <span>虽然这里是系统帮助，但是开发人员想在论文阶段再写</span>
            </Col>
          </Row>
        </Location>
        <div className="space-body">

        </div>
      </div>
    );
  }
}

export default withRouter(Help);
