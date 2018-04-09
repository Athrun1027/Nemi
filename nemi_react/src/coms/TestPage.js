import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import { Layout, Upload, Button, Icon, message, Progress } from 'antd';

import { NProgress } from '../utills/loading'
import '../css/test.css';

import axios from 'axios'


class Test extends Component {
  componentWillMount(){
      NProgress.done();
  }

  state = {
    fileList: [],
    defaultFileList: [],
    uploading: false,
    upload: false
  }

  handleUpload = () => {
    const { fileList } = this.state;
    const formData = new FormData();
    fileList.forEach((file) => {
      formData.append(file.uid, file);
    });

    axios.post('http://127.0.0.1:5000/api/v1/files/test/', formData,{
      headers:{'Content-Type': 'multipart/form-data'},
      onUploadProgress:(progressEvent)=>{
        let progress = Math.round(progressEvent.loaded / progressEvent.total * 100);
        this.setState({
          uploading: true,
          upload: progress
        });
      }
    }).then(
      response => {
        this.setState({
          defaultFileList: this.state.defaultFileList.concat(this.state.fileList),
          fileList: [],
          uploading: false,
        });
        console.log(response.data);
        message.success('upload successfully.');
      }
    ).catch(
      error => {
        this.setState({
          uploading: false,
        });
        console.log("????");
        message.error('upload failed.');
      }
    )
  }


  render() {
    const { uploading } = this.state;
    const props = {
      onRemove: (file) => {
        this.setState(({ fileList }) => {
          const index = fileList.indexOf(file);
          const newFileList = fileList.slice();
          newFileList.splice(index, 1);
          return {
            fileList: newFileList,
          };
        });
      },
      beforeUpload: (file) => {
        this.setState(({ fileList }) => ({
          fileList: [...fileList, file],
        }));
        return false;
      },
      fileList: this.state.fileList,
      defaultFileList: this.state.defaultFileList,
    };

    return (
      <Layout>
        <div className="borad-box2">
        </div>
        <div className="borad-box2">
        <Upload.Dragger {...props}>
          {this.state.upload?<Progress type="circle" percent={this.state.upload}/>:<p className="ant-upload-drag-icon"><Icon type="inbox" /></p>}
          <p className="ant-upload-text">Click or drag file to this area to upload</p>
          <p className="ant-upload-hint">Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files</p>
        </Upload.Dragger>
        <Button
          className="upload-demo-start"
          type="primary"
          onClick={this.handleUpload}
          disabled={this.state.fileList.length === 0}
          loading={uploading}
        >
          {uploading ? 'Uploading' : 'Start Upload' }
        </Button>
        </div>
      </Layout>
    );
  }
}

export default withRouter(Test);
