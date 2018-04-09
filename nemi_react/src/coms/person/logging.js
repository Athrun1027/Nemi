import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import {LoggingList} from '../../apis/message'
import Cookies from 'js-cookie'

import { NProgress } from '../../utills/loading'

import { Row, Col, Icon, Tooltip, Table } from 'antd';


class Logging extends Component {

  constructor(props) {
    super(props);
    let user_cookie = Cookies.get("user");
    this.state = {
        user: user_cookie?JSON.parse(user_cookie):false,
        selectedRowKeys: [],
        loading: false,
        filteredInfo: null,
        sortedInfo: null,
        filterDropdownVisible: false,
        searchText: '',
        filtered: false,

        data: []
    }
  }

  flash_list=() =>{
    NProgress.start();
    LoggingList(this);
    NProgress.done();
  }

  componentDidMount(){
    this.flash_list()
  }

  render() {
    const columns = [{
      title: '时间',
      dataIndex: 'join_time',
      key: 'join_time'
    },{
      title: '用户',
      dataIndex: 'user.username',
      key: 'user.username'
    },{
      title: '操作',
      dataIndex: 'action',
      key: 'action'
    },{
      title: '对象',
      dataIndex: 'target',
      key: 'target'
    },{
      title: '结果',
      dataIndex: 'result',
      key: 'result'
    }];

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={19}>
              <h3>查看日志</h3>
              <span>只显示一些重要操作的日志，并且只显示最近的200条</span>
            </Col>
            <Col span={5}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">日志条数</span><br/>
                  <Tooltip title="很抱歉，创建是有上限的" placement="bottom" >
                    <h2>{this.state.data.length}<span className="text-gay text-small"> /200</span></h2>
                  </Tooltip>
                </div>
              </div>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <h3><Icon type="rocket" /></h3>
          <Table
          columns={columns}
          loading={!this.state.load}
          dataSource={this.state.data} />
        </div>
      </div>
    );
  }
}

export default withRouter(Logging);
