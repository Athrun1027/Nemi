import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'

import Location from '../public/LocationPage'

import {ResourcesList, ResourcesRoot, ResourcesEdit, FolderCreate, FolderTree, ResourcesMove, ResourcesCopy, ResourcesDisable, FileUpload} from '../../apis/file'

import {ShareFile} from '../../apis/share'
import Cookies from 'js-cookie'

import { NEMI_URL } from '../../apis/config'

import { NProgress, getFileSize } from '../../utills/loading'

import '../../css/space.css';

import { Input, Modal, Transfer, Popconfirm, Upload, Progress, Tree, Breadcrumb, Row, Col, Icon, Tooltip, Button, Table } from 'antd';


const file_type = [
  "pdf", "ppt", "jpg", "markdown", "excel", "word"
]


class SpaceMine extends Component {

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

        folder_root: [],
        folder_id: false,

        edit_modal_visible: false,
        edit_modal_text: "",
        edit_modal_id: false,

        create_modal_visible: false,
        create_modal_text: "",

        move_modal_visible: false,
        move_modal_select: "",
        move_modal_id: false,

        copy_modal_visible: false,
        copy_modal_select: "",
        copy_modal_id: false,

        share_modal_visible: false,
        share_targetKeys: [],
        share_modal_id: false,

        upload_modal_visible: false,

        fileList: [],
        defaultFileList: [],
        uploading: false,
        upload: false,

        treeData: [],
        data: []
    }
  }

  onSelectChange = (selectedRowKeys) => {
    console.log('selectedRowKeys changed: ', selectedRowKeys);
    this.setState({ selectedRowKeys });
  }

  handleChange = (pagination, filters, sorter) => {
    console.log('Various parameters', pagination, filters, sorter);
    this.setState({
      filteredInfo: filters,
      sortedInfo: sorter,
    });
  }

  clearAll = () => {
    this.setState({
      filteredInfo: null,
      sortedInfo: null,
      searchText: null,
    });
    this.flash_list(this.state.user.space_mine[0].root_folder.id)
  }
  onInputChange = (e) => {
    this.setState({ searchText: e.target.value });
  }
  onSearch = () => {
    const { searchText } = this.state;
    const reg = new RegExp(searchText, 'gi');
    this.setState({
      filterDropdownVisible: false,
      filtered: !!searchText,
      data: this.state.data.map((record) => {
        const match = record.object_name.match(reg);
        if (!match) {
          return null;
        }
        return {
          ...record,
          name: (
            <span>
              {record.object_name.split(reg).map((text, i) => (
                i > 0 ? [<span className="highlight" key={i}>{match[0]}</span>, text] : text
              ))}
            </span>
          ),
        };
      }).filter(record => !!record),
    });
  }

  flash_list=(id) =>{
    NProgress.start();
    ResourcesList(this, id);
    ResourcesRoot(this, id);
    FolderTree(this, this.state.user.space_mine[0].root_folder.id);
    NProgress.done();
  }

  InFolder=(e, record)=>{
    e.preventDefault();
    this.flash_list(record.id)
  }

  componentDidMount(){
    this.flash_list(this.state.user.space_mine[0].root_folder.id)
  }

  edit_modal_Change = (e) => {
    this.setState({ edit_modal_text: e.target.value });
  }
  edit_modal_handleOk = (e) =>{
    e.preventDefault();
    let put_data = {
      object_name:this.state.edit_modal_text
    }
    ResourcesEdit(this, this.state.edit_modal_id, put_data)
    this.flash_list(this.state.folder_id)
  }
  edit_modal_open = (e, item) =>{
    e.preventDefault();
    this.setState({
      edit_modal_visible: true,
      edit_modal_text: item.object_name,
      edit_modal_id:item.id
    });
  }

  create_modal_Change = (e) => {
    this.setState({ create_modal_text: e.target.value });
  }
  create_modal_handleOk = (e) =>{
    e.preventDefault();
    let post_data = {
      object_name:this.state.create_modal_text,
      folder_id:this.state.folder_id
    }
    FolderCreate(this, post_data)
    this.flash_list(this.state.folder_id)
  }

  move_modal_handleOk = (e) =>{
    e.preventDefault();
    let put_data = {
      folder_id: Number.parseInt(this.state.move_modal_select, 10)
    }
    ResourcesMove(this, this.state.move_modal_id, put_data);
    this.flash_list(this.state.folder_id)
  }

  copy_modal_handleOk = (e) =>{
    e.preventDefault();
    let put_data = {
      folder_id: Number.parseInt(this.state.copy_modal_select, 10)
    }
    ResourcesCopy(this, this.state.copy_modal_id, put_data);
    this.flash_list(this.state.folder_id)
  }

  share_handleChange = (nextTargetKeys, direction, moveKeys) => {
    this.setState({ share_targetKeys: nextTargetKeys });
  }

  share_modal_handleOk = (e) =>{
    e.preventDefault();
    let post_data = {
      original_id:this.state.share_modal_id,
      own_id_list:this.state.share_targetKeys,
    }
    ShareFile(this, post_data)
    this.flash_list(this.state.folder_id)
  }

  disabled_resource = (e, item) =>{
    e.preventDefault();
    ResourcesDisable(this, item.id);
    this.flash_list(this.state.folder_id)
  }

  renderTreeNodes = (data) => {
    return data.map((item) => {
      if (item.children) {
        return (
          <Tree.TreeNode title={item.title} key={item.key} dataRef={item}>
            {this.renderTreeNodes(item.children)}
          </Tree.TreeNode>
        );
      }
      return <Tree.TreeNode {...item} disabled/>;
    });
  }

  render() {
    const { selectedRowKeys } = this.state;
    const rowSelection = {
      selectedRowKeys,
      onChange: this.onSelectChange,
    };
    const hasSelected = selectedRowKeys.length > 0;
    let { sortedInfo } = this.state;
    sortedInfo = sortedInfo || {};
    const columns = [{
      title: '名称',
      dataIndex: 'object_name',
      key: 'object_name',
      sorter: (a, b) => a.object_name.length - b.object_name.length,
      sortOrder: sortedInfo.columnKey === 'object_name' && sortedInfo.order,
      filterDropdown: (
        <div className="custom-filter-dropdown">
          <Input
            ref={ele => this.searchInput = ele}
            placeholder="Search name"
            value={this.state.searchText}
            onChange={this.onInputChange}
            onPressEnter={this.onSearch}
          />
          <Button type="primary" onClick={this.onSearch}>Search</Button>
        </div>
      ),
      filterIcon: <Icon type="smile-o" style={{ color: this.state.filtered ? '#108ee9' : '#aaa' }} />,
      filterDropdownVisible: this.state.filterDropdownVisible,
      onFilterDropdownVisibleChange: (visible) => {
        this.setState({
          filterDropdownVisible: visible,
        }, () => this.searchInput && this.searchInput.focus());
      },
      render: (text, record, index) => {
        let fileType = "file-text";
        if (file_type.indexOf(record.object_type) !== -1) {
          fileType = "file-" + record.object_type
        };
        if (record.object_type === "folder") {
          return <a onClick={(e)=>this.InFolder(e, record)}>
            <Icon type="folder" /> {text}
          </a>
        };
        return <a >
        <Icon type={fileType} /> {text}
      </a>
      }
    },{
      title: '下载',
      key: 'download',
      render: (text, record, index) => {
        if (record.object_type === "folder") {
          return <Icon type="minus" style={{ fontSize: 20}}/>
        };
        return <a href={NEMI_URL+"files/download/" + record.id}><Icon type="cloud-download-o" style={{ fontSize: 20}}/></a>
      }
    },{
      title: '大小',
      dataIndex: 'object_size',
      key: 'object_size',
      sorter: (a, b) => a.object_size - b.object_size,
      sortOrder: sortedInfo.columnKey === 'object_size' && sortedInfo.order,
      render: (text, record, index) => {
        if (record.object_type === "folder") {
          return <Icon type="minus" style={{ fontSize: 20}}/>
        };
        return <span>{getFileSize(text)}</span>
      }
    },{
      title: '最近修改时间',
      dataIndex: 'edit_time',
      key: 'edit_time',
      sorter: (a, b) => Date.parse(new Date(a.edit_time)) - Date.parse(new Date(b.edit_time)),
      sortOrder: sortedInfo.columnKey === 'edit_time' && sortedInfo.order,
    },{
      title: '操作',
      key: 'operation',
      render: (text, record, index) => <div>
        <Button type="primary" size="small" onClick={(e)=>this.edit_modal_open(e, record)}>编辑</Button>
        <span> </span>
        <Button type="primary" ghost size="small" onClick={(e)=>this.setState({
            copy_modal_visible: true,
            copy_modal_id:record.id
          })}>复制</Button>
        <span> </span>
        <Button type="primary" ghost size="small" onClick={(e)=>this.setState({
            move_modal_visible: true,
            move_modal_id:record.id
          })}>移动</Button>
        <span> </span>

        <Popconfirm placement="topRight" title="╥﹏╥…确定要删除这个可爱的文件吗" onConfirm={(e)=>this.disabled_resource(e, record)} okText="删除" cancelText="算了">
          <Button type="danger" size="small">删除</Button>
        </Popconfirm>
        <span> </span>
        <Button type="dashed" size="small" onClick={(e)=>this.setState({
            share_modal_visible: true,
            share_modal_id:record.id,
            share_targetKeys:record.share_files.map(item => item.own_id)
          })}>分享</Button>
        <span> </span>
      </div>
    }];

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
        console.log(file)
        return false;
      },
      fileList: this.state.fileList,
      defaultFileList: this.state.defaultFileList,
      multiple: true,
    };

    return (
      <div>
      <Location>
          <Row gutter={16} className="borad-header">
            <Col span={16}>
              <h3>个人空间</h3>
              <span>默认具有文件个数和空间容量的限制，如溢出，请自行联系管理员扩容</span>
            </Col>
            <Col span={8}>
              <div className="gutter-box">
                <div className="borad-header-inline">
                  <span className="text-gay">资源总数</span><br/>
                  <Tooltip title="嫌少？那就去上传啊" placement="bottom" >
                    <h2>{this.state.data.length}<span className="text-gay text-small"> /1000</span></h2>
                  </Tooltip>
                </div>
                <div className="borad-header-inline">
                  <span className="text-gay">空间可用</span><br/>
                  <Tooltip title="很抱歉，空间是有上限的" placement="bottom" >
                    <h2>{getFileSize(this.state.user.files_size)}<span className="text-gay text-small"> /10G</span></h2>
                  </Tooltip>
                </div>
              </div>
            </Col>
          </Row>
        </Location>
        <div className="space-body">
          <div className="space-body-head">
            <Button type="primary" size="small" onClick={()=>{this.flash_list(this.state.folder_id)}}>刷新</Button>
            <Button type="primary" size="small" onClick={()=>{this.setState({upload_modal_visible: true})}}>上传文件</Button>
            <Button type="primary" size="small" onClick={(e)=>this.setState({
              create_modal_visible: true
            })}>新建文件夹</Button>
            <Button type="primary" size="small" onClick={this.clearAll}>清空筛选和排序</Button>
            <span style={{ marginLeft: 8 }}>
            {hasSelected ? `Selected ${selectedRowKeys.length} items` : ''}
          </span>
          <Breadcrumb className="">
            {this.state.folder_root.map((item)=><Breadcrumb.Item key={item.id}>
                <a onClick={(e)=>this.InFolder(e, item)}>{item.object_name}</a>
            </Breadcrumb.Item>)}
          </Breadcrumb>
          </div>
          {this.state.upload?<Progress percent={this.state.upload}/>:""}
          <Table
          rowSelection={rowSelection}
          columns={columns}
          loading={!this.state.load}
          onChange={this.handleChange}
          dataSource={this.state.data} />
          <Modal
            title="修改信息"
            visible={this.state.edit_modal_visible}
            onOk={this.edit_modal_handleOk}
            onCancel={()=>{this.setState({edit_modal_visible: false})}}
          >
            <Input
            onChange={this.edit_modal_Change}
            value={this.state.edit_modal_text} />
          </Modal>
          <Modal
            title="创建文件夹"
            visible={this.state.create_modal_visible}
            onOk={this.create_modal_handleOk}
            onCancel={()=>{this.setState({create_modal_visible: false})}}
          >
            <Input
            onChange={this.create_modal_Change}
            value={this.state.create_modal_text} />
          </Modal>
          <Modal
            title="移动资源"
            visible={this.state.move_modal_visible}
            onOk={this.move_modal_handleOk}
            onCancel={()=>{this.setState({move_modal_visible: false})}}
          >
            <Tree
              showLine
              defaultExpandAll
              onSelect={(selectedKeys)=>{this.setState({
                move_modal_select: selectedKeys[0]
              })}}
            >
              {this.renderTreeNodes(this.state.treeData)}
            </Tree>
          </Modal>
          <Modal
            title="复制资源"
            visible={this.state.copy_modal_visible}
            onOk={this.copy_modal_handleOk}
            onCancel={()=>{this.setState({copy_modal_visible: false})}}
          >
            <Tree
              showLine
              defaultExpandAll
              onSelect={(selectedKeys)=>{this.setState({
                copy_modal_select: selectedKeys[0]
              })}}
            >
              {this.renderTreeNodes(this.state.treeData)}
            </Tree>
          </Modal>
          <Modal
            title="上传文件"
            visible={this.state.upload_modal_visible}
            onOk={()=>{this.setState({upload_modal_visible: false})}}
            onCancel={()=>{this.setState({upload_modal_visible: false})}}
          >
            <Upload.Dragger {...props}>
              {this.state.upload?<Progress type="circle" percent={this.state.upload}/>:<p className="ant-upload-drag-icon"><Icon type="inbox" /></p>}
              <p className="ant-upload-text">Click or drag file to this area to upload</p>
              <p className="ant-upload-hint">Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files</p>
            </Upload.Dragger>
            <Button
              type="primary"
              onClick={(e)=>{FileUpload(this, this.state.user.space_mine[0].bucket_kids[0].id)}}
              disabled={this.state.fileList.length === 0}
              loading={this.state.uploading}
            >
              {this.state.uploading ? 'Uploading' : 'Start Upload' }
            </Button>
          </Modal>
          <Modal
            title="分享文件"
            visible={this.state.share_modal_visible}
            onOk={this.share_modal_handleOk}
            onCancel={()=>{this.setState({share_modal_visible: false})}}
          >
            <Transfer
            dataSource={this.state.user.kids}
            titles={['可选', '已选']}
            targetKeys={this.state.share_targetKeys}
            onChange={this.share_handleChange}
            onSelectChange={this.share_handleSelectChange}
            render={item => item.nickname+'('+item.username+')'}
            rowKey={record => record.id}
            />
          </Modal>
        </div>
      </div>
    );
  }
}

export default withRouter(SpaceMine);
