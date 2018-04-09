import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import {UserValieUsername, UserValieEmail, UserChangeEmail, UserChangeUsername, UserChangeNickname, UserChangePassword, UserChangeClass} from '../../apis/user'
import Cookies from 'js-cookie'

import { Input, Modal, message, Upload, Row, Col, Icon, Button } from 'antd';


class Info extends Component {

  constructor(props) {
    super(props);
    let user_cookie = Cookies.get("user");
    user_cookie = user_cookie?JSON.parse(user_cookie):false
    this.state = {
        user: user_cookie,
        img_previewVisible: false,
        img_previewImage: '',
        img_fileList: [],

        edit_username: user_cookie.username,
        edit_username_ok: false,
        edit_email: user_cookie.email,
        edit_email_ok: false,
        edit_nickname: user_cookie.nickname,
        edit_password_old: "",
        edit_password: "",
        edit_password_again: "",

        edit_info_1: user_cookie.school_in,
        edit_info_2: user_cookie.college_in,
        edit_info_3: user_cookie.class_in,
        edit_info_4: user_cookie.nick_call
    }
  }


  onChangeCreate = (e, value_type) => {
    e.preventDefault();
    let obj={};
    obj[value_type] = e.target.value;
    this.setState(obj);
  }

  img_handleCancel = () => this.setState({ img_previewVisible: false })

  img_handlePreview = (file) => {
    this.setState({
      img_previewImage: file.url || file.thumbUrl,
      img_previewVisible: true,
    });
  }

  img_handleChange = ({ fileList }) => this.setState({ fileList })

  username_valie = () =>{
    if(this.state.user.is_changed){
      message.info("您已经没有机会再修改用户名了");
      return true
    }
    UserValieUsername(this, this.state.edit_username);
  }

  email_valie = () =>{
    if(this.state.user.is_changed){
      message.info("您已经没有机会再修改用户名了");
      return true
    }
    UserValieEmail(this, this.state.edit_email);
  }

  password_change = () =>{
    if(this.state.edit_password !== this.state.edit_password_again){
      message.info("两次密码不匹配");
      return true
    }
    if (this.state.edit_password_old === "") {
      message.info("旧密码未输入啊");
      return true
    }
    UserChangePassword(this, this.state.user.id, {
      old_password: this.state.edit_password_old,
      new_password: this.state.edit_password
    });
  }


  render() {
    const uploadButton = (
      <div>
        <Icon type="plus" />
        <div className="ant-upload-text">Upload</div>
      </div>
    );

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={24}>
              <h3>个人信息</h3>
              <span>您可以修改如下的个人信息</span>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <div style={{ padding: '1rem', margin: '0 3rem'  }}>
            <h2>修改您的信息</h2>
            <Input
              placeholder="请输入用户名"
              addonBefore="用户名"
              prefix={<Icon type="slack" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_username}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_username")}
            />
            <span> </span>
            <Button type="primary" icon="question-circle"
            onClick={this.username_valie}>是否可用</Button>
            <span> </span>
            <Button type="primary" disabled={!this.state.edit_username_ok}
            onClick={()=>UserChangeUsername(this, this.state.user.id, this.state.edit_username)}>更改</Button>
            <br />
            <h6>注意：您只能修改一次用户名</h6>
          </div>
          <div style={{ padding: '1rem', margin: '0 3rem'  }}>
            <Input
              placeholder="请输入邮箱"
              addonBefore="邮箱"
              prefix={<Icon type="slack" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_email}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_email")}
            />
            <span> </span>
            <Button type="primary" icon="question-circle"
            onClick={this.email_valie}>是否可用</Button>
            <span> </span>
            <Button type="primary" disabled={!this.state.edit_email_ok}
            onClick={()=>UserChangeEmail(this, this.state.user.id, this.state.edit_email)}>更改</Button>
            <br />
            <h6>注意：邮箱必须唯一</h6>
          </div>
          <div style={{ padding: '1rem', margin: '0 3rem'  }}>
            <Input
              placeholder="请输入昵称"
              addonBefore="昵称"
              prefix={<Icon type="slack" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_nickname}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_nickname")}
            />
            <span> </span>
            <Button type="primary"
            onClick={()=>UserChangeNickname(this, this.state.user.id, {nickname:this.state.edit_nickname, role:this.state.user.role})}>更改</Button>
            <br />
            <h6>注意：昵称随意</h6>
          </div>
          <div style={{ padding: '1rem', margin: '0 3rem'  }}>
            <h3>更换头像:</h3>
            <Upload
              action="//jsonplaceholder.typicode.com/posts/"
              listType="picture-card"
              fileList={this.state.img_fileList}
              onPreview={this.img_handlePreview}
              onChange={this.img_handleChange}
            >
              {this.state.img_fileList.length >= 3 ? null : uploadButton}
            </Upload>
            <Modal visible={this.state.img_previewVisible} footer={null} onCancel={this.img_handleCancel}>
              <img alt="example" style={{ width: '100%' }} src={this.state.img_previewImage} />
            </Modal>
          </div>
          <div style={{ padding: '1rem', margin: '0 3rem'  }}>
            <h3>密码:</h3>
            <Input
              placeholder="请输入旧密码"
              addonBefore="旧密码"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_password_old}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_password_old")}
              type="password"
            />
            <br /><br />
            <Input
              placeholder="请输入新密码"
              addonBefore="新密码"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_password}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_password")}
              type="password"
            />
            <br /><br />
            <Input
              placeholder="再次输入密码"
              addonBefore="确认"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_password_again}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_password_again")}
              type="password"
            />
            <span> </span>
            <Button type="primary"
            onClick={this.password_change}>更改</Button>
          </div>
          <div style={{ padding: '1rem', margin: '0 3rem' }}>
            <h3>其他信息:</h3>
            <Input
              placeholder="请输入学校"
              addonBefore="学校"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_info_1}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_info_1")}
            />
            <br /><br />
            <Input
              placeholder="请输入学院"
              addonBefore="学院"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_info_2}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_info_2")}
            />
            <br /><br />
            <Input
              placeholder="请输入班级"
              addonBefore="班级"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_info_3}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_info_3")}
            />
            <br /><br />
            <Input
              placeholder="请输入称呼"
              addonBefore="称呼"
              prefix={<Icon type="layout" style={{ color: 'rgba(0,0,0,.25)' }} />}
              value={this.state.edit_info_4}
              style={{ width: 300 }}
              onChange={(e) => this.onChangeCreate(e, "edit_info_4")}
            />
            <span> </span>
            <Button type="primary"
            onClick={()=>UserChangeClass(this, this.state.user.id, {
              school_in: this.state.edit_info_1,
              college_in: this.state.edit_info_2,
              class_in: this.state.edit_info_3,
              nick_call: this.state.edit_info_4
            })}>更改</Button>
          </div>
        </div>
      </div>
    );
  }
}

export default withRouter(Info);
