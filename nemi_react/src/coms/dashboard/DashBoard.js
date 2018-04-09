import React, { Component } from 'react';
import { withRouter, Link } from 'react-router-dom'
import Cookies from 'js-cookie'

import { Breadcrumb, Avatar, Row, Col, Card, Icon, Tooltip, List } from 'antd';

import Location from '../public/LocationPage'

import ReactEcharts from '../../utills/echarts-index';

import {FileRecent} from '../../apis/file'
import {MessageRecent} from '../../apis/message'

import { NProgress } from '../../utills/loading'

import '../../css/dashboard.css';

import {ResourceOption} from './ResourceChart';
import {SpaceOption} from './SpaceUseChart';

const file_type = [
  "pdf", "ppt", "jpg", "markdown", "excel", "word"
]
const color_type = [
  "#52c41a", "#f5222d", "#1890ff", "#faad14", "#4ad5ff", "#7b50b8", "#86a7cf"
]

class DashBoard extends Component {
  constructor(props) {
      super(props);
      let user_cookie = Cookies.get("user");
      user_cookie = user_cookie?JSON.parse(user_cookie):false
      let group_cookie = Cookies.get("group");
      group_cookie = group_cookie?JSON.parse(group_cookie):false
      this.state = {
          collapsed: false,
          user: user_cookie,
          group: group_cookie,
          load: false,
          file_list: [],
          message_recent: []
      }
  }

  OnClickOn=(e)=>{
    console.log(e);
  }

  componentDidMount(){
    NProgress.start();
    FileRecent(this);
    MessageRecent(this);
    NProgress.done();
  }

  render() {
    const fileList = this.state.file_list.map(item => {
        let fileType = "file-text";
        if (file_type.indexOf(item.object_type) !== -1) {
          fileType = "file-" + item.object_type
        };
        let randonmNum = Math.random()*color_type.length;
        randonmNum = parseInt(randonmNum,10);
        return (<Link to="/space/mine" key={item.id}>
          <Card.Grid style={{padding: '24px 0'}}>
            <Card.Meta
              avatar={<Icon className="text-lager" style={{color:color_type[randonmNum]}} type={fileType} />}
              title={item.object_name}
              description="This is the description"
            />
          </Card.Grid>
        </Link>)
    })
    if (!this.state.user) {
      return <div></div>
    }
    let files_types = [];
    for (var i = this.state.user.files_types.length - 1; i >= 0; i--) {
      files_types.push(this.state.user.files_types[i].name)
    }
    console.log(this.state.group);

    return (
      <div>
        <Location>
          <Row gutter={16} className="borad-header">
            <Col span={2}>
              <Tooltip title="嫌丑？嫌丑你自己换啊" placement="bottomLeft" >
                <Avatar
                className="board-img"
                src={this.state.user.img_url}/>
              </Tooltip>
            </Col>
            <Col span={12}>
              <div className="borad-who">
                <span className="borad-hello">下午好，{this.state.user.username}，Coding过程别忘记喝水哦！</span>
                  <Breadcrumb separator=">">
                    <Breadcrumb.Item>{this.state.user.school_in}</Breadcrumb.Item>
                    <Breadcrumb.Item>{this.state.user.college_in}</Breadcrumb.Item>
                    <Breadcrumb.Item>{this.state.user.class_in}</Breadcrumb.Item>
                    <Breadcrumb.Item>
                      <Tooltip title={'你好！'+this.state.user.school_in+' '+this.state.user.college_in+' '+this.state.user.class_in+' '+this.state.user.nick_call} placement="bottomRight" >{this.state.user.nick_call}</Tooltip>
                    </Breadcrumb.Item>
                  </Breadcrumb>
              </div>
            </Col>
            <Col span={10}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">上传的文件数</span><br/>
                  <Tooltip title="嫌少？那就去上传啊" placement="bottom" >
                    <h1>{this.state.user.files_count}</h1>
                  </Tooltip>
                </div>
                <div className="borad-header-inline">
                  <span className="text-gay">加入的群组数</span><br/>
                  <Tooltip title="很抱歉，群组是有上限的" placement="bottom" >
                    <h1>{this.state.group.groups.length}<span className="text-gay text-small"> /24</span></h1>
                  </Tooltip>
                </div>
                <div className="borad-header-inline">
                  <span className="text-gay">分享的文件数</span><br/>
                  <Tooltip title="把你的宝贝给大家分享分享呗" placement="bottomRight" >
                    <h1>_</h1>
                  </Tooltip>
                </div>
              </div>
            </Col>
          </Row>
        </Location>
        <Row className="borad-body">
            <Col span={16}>
              <Card title="最近文件"
              loading={false}
              extra={<Link to="/space/mine">我的空间</Link>}
              className="borad-box1">
                {fileList}
              </Card>
              <Card title="最近动态"
                loading={false}
                className="borad-box1">
                <List
                itemLayout="horizontal"
                dataSource={this.state.message_recent}
                renderItem={item => (
                  <List.Item>
                    <List.Item.Meta
                      avatar={<Avatar src={item.user_from.img_url} />}
                      title={<span>{item.user_from.nickname} <a>{item.contant}</a></span>}
                      description={item.last_login_time}
                    />
                  </List.Item>
                  )}
                  />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="空间使用情况"
              loading={false}
              className="borad-box3">
                <ReactEcharts
                  className="borad-chart"
                  style={{height: '300px', width: '100%', padding: '0'}}
                  option={SpaceOption(this.state.user.files_size / (this.state.user.buckets_count*10*1024*1024))} />
              </Card>
              <Card title="资源的类别"
              loading={false}
              className="borad-box3">
                <ReactEcharts
                  className="borad-chart"
                  style={{height: '300px', width: '100%'}}
                  option={ResourceOption(this.state.user.files_types, files_types)} />
              </Card>
            </Col>
          </Row>
      </div>
    );
  }
}

export default withRouter(DashBoard);
