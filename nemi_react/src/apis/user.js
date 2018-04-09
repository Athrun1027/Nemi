import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'

import {message} from 'antd'

let GetUserGroups = (thisApp, user_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/groups/'+user_id,{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      Cookies.set("group", response.data, { expires: 0.1 });
      thisApp.setState({
        load: true
      });
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}


let GetLoginUser = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'auth/login/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      Cookies.set("user", response.data.data, { expires: 0.1 });
      GetUserGroups(thisApp, response.data.data.id)
    }
  ).catch(
    error => {
      message.warning("登录已经过期，请重新登录");
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

let GetUserList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/',{
    headers:{'Nemi-API-KEY': token},
    params:{
      PageSize:50,
      OrderBy:'-join_time',
      Disable:0
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

let UserCreate = (thisApp, post_data) =>{
  let token = Cookies.get("token");
  axios.post(NEMI_URL + 'users/', post_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        create_modal_visible: false,
        create_email: "",
        create_password: "",
        create_role: "admin",
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

let UserEdit = (thisApp, user_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/' + user_id, put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_modal_visible: false,
        edit_nickname: "",
        edit_role: "",
        edit_modal_id: false,
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

let UserResetPassword = (thisApp, user_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/' + user_id+"/password/reset/", put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        password_modal_visible: false,
        password_password: "",
        password_modal_id: false,
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

let UserDisable = (thisApp, user_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'users/' + user_id, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
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

let UserValieUsername = (thisApp, user_name) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/username/', {
    headers:{'Nemi-API-KEY': token},
    params:{
      username: user_name
    }
  }).then(
    response => {
      thisApp.setState({
        edit_username_ok: true,
        load: true
      })
      message.success("可用的用户名！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        edit_username_ok: false,
      })
      message.warning("已经存在的用户名，或者用户名不合法");
    }
  )
}

let UserValieEmail = (thisApp, email) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/email/', {
    headers:{'Nemi-API-KEY': token},
    params:{
      email: email
    }
  }).then(
    response => {
      thisApp.setState({
        edit_email_ok: true,
        load: true
      })
      message.success("可用的邮箱！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        edit_email_ok: false,
      })
      message.warning("已经存在的邮箱，或者邮箱不合法");
    }
  )
}

let UserChangeUsername = (thisApp, user_id, user_name) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/'+user_id+'/username/', {username:user_name},{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_username: user_name,
        edit_username_ok: false,
        load: true
      })
      message.success("修改成功！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        edit_username_ok: false,
      })
      message.warning("修改失败！");
    }
  )
}

let UserChangeEmail = (thisApp, user_id, email) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/'+user_id+'/email/', {email:email},{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_email: email,
        edit_email_ok: false,
        load: true
      })
      message.success("修改成功！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        edit_email_ok: false,
      })
      message.warning("只有一次机会哦");
    }
  )
}

let UserChangeNickname = (thisApp, user_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/' + user_id, put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("修改成功！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      message.warning("修改失败哦");
    }
  )
}

let UserChangePassword = (thisApp, user_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/' + user_id +'/password/', put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        edit_password_old: "",
        edit_password: "",
        edit_password_again: "",
      })
      message.success("修改成功！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        edit_password_old: "",
        edit_password: "",
        edit_password_again: "",
      })
      message.warning("旧密码可能错了哦");
    }
  )
}

let UserChangeClass = (thisApp, user_id, put_data) =>{
  let token = Cookies.get("token");
  axios.put(NEMI_URL + 'users/' + user_id +'/class/', put_data, {
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        load: true
      })
      message.success("修改成功！");
      return true
    }
  ).catch(
    error => {
      // message.warning("登录已经过期，请重新登录");
      // thisApp.props.history.push("/login");
      // Cookies.remove("token");
      thisApp.setState({
        load: true
      })
      message.warning("修改失败了哦！");
    }
  )
}

let GetUserDisList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/',{
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

let UserEnable = (thisApp, user_id) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'users/'+user_id+'/enable/',{
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

let UserDestroy = (thisApp, user_id) =>{
  let token = Cookies.get("token");
  axios.delete(NEMI_URL + 'users/'+user_id+'/destroy/',{
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
  GetLoginUser,
  GetUserGroups,
  UserCreate,
  UserEdit,
  UserResetPassword,
  UserDisable,
  UserValieUsername,
  UserValieEmail,
  UserChangeUsername,
  UserChangeEmail,
  UserChangeNickname,
  UserChangePassword,
  UserChangeClass,
  GetUserDisList,
  UserEnable,
  UserDestroy,
  GetUserList
};