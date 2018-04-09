import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'

import { message } from 'antd';


let GetGroupList = (thisApp, group_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/groups/'+group_id,{
    headers:{'Nemi-API-KEY': token},
    params:{
      PageSize:50,
      OrderBy:'-join_time',
      Disable:0
    }
  }).then(
    response => {
      response.data.groups_mine.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data: response.data.groups_mine,
        load: true
      })
    }
  ).catch(
    error => {
      // console.log("????");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}


let GroupCreate = (thisApp, post_data) =>{
  let token = Cookies.get("token");
  axios.post(NEMI_URL + 'groups/', post_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        create_modal_visible: false,
        create_name: "",
        load: true
      })
    }
  ).catch(
    error => {
      // console.log("????");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}


let GroupEdit = (thisApp, group_id ,put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'groups/'+group_id, put_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_modal_visible: false,
        edit_nickname: "",
        edit_modal_id: false,
        load: true
      })
    }
  ).catch(
    error => {
      // console.log("????");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}


let GroupDisable = (thisApp, group_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'groups/'+group_id,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
    }
  ).catch(
    error => {
      // console.log("????");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}


let GroupMemberSet = (thisApp, group_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'groups/members/'+group_id, put_data,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        member_modal_visible: false,
        targetKeys: [],
        member_modal_id: false,
        load: true
      })
    }
  ).catch(
    error => {
      // console.log("????");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}


let GetGroupDisList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'groups/',{
    headers:{'Nemi-API-KEY': token},
    params:{
      PageSize:50,
      OrderBy:'-join_time',
      Disable:1
    }
  }).then(
    response => {
      response.data.data.forEach((item)=>{
        item["key"] = item["id"]
      })
      thisApp.setState({
        data:response.data.data,
        load: true
      })
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
    }
  )
}

let GroupEnable = (thisApp, group_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'groups/'+group_id+'/enable/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("恢复成功哦");
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      message.warning("恢复失败哦");
    }
  )
}

let GroupDestroy = (thisApp, group_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'groups/'+group_id+'/destroy/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("彻底删除成功哦");
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      message.warning("彻底删除失败哦");
    }
  )
}



export {
  GetGroupList,
  GroupCreate,
  GroupDisable,
  GroupMemberSet,
  GetGroupDisList,
  GroupEnable,
  GroupDestroy,
  GroupEdit
};