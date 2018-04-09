import React, { Component } from 'react';
import { withRouter, Link } from 'react-router-dom'

import { Layout, Icon } from 'antd';
import '../../css/footerbar.css';


class FooterBar extends Component {
  render() {
    return (
      <Layout.Footer>
        <div className="home-foot">
          <Link to="/person/help"><Icon type="customer-service" /> 帮助</Link>
          <Link to="/person/help"><Icon type="github" /> 源码</Link>
          <Link to="/person/help"><Icon type="book" /> 详情</Link><br/>
          <p>Copyright <Icon type="copyright" /> 2018 All rights reserved Packet Inc.</p>
        </div>
      </Layout.Footer>
    )
}
}

export default withRouter(FooterBar);