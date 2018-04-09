import axios from 'axios'
import Cookies from 'js-cookie'

import { NEMI_URL } from './config'


let MessageRecent = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'message/recent',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        message_recent: response.data.data,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}

function getNoticeData(notices) {
  let notices_data = []
  for (var i = notices.length - 1; i >= 0; i--) {
    notices_data.push({
      id:i,
      avatar:notices[i].user_from.img_url,
      title:notices[i].user_from.nickname + "回复了你",
      description:notices[i].contant,
      datetime:notices[i].last_login_time
    })
  }
  return notices_data;
}


let MessageNotRead = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'message/checked',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        data: getNoticeData(response.data.data),
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.props.history.push("/login");
      Cookies.remove("token");
    }
  )
}


let LoggingList = (thisApp) =>{
  let token = Cookies.get("token");
  axios.get(NEMI_URL + 'logs/',{
    headers:{'Nemi-API-KEY': token}
  }).then(
    response => {
      thisApp.setState({
        data: response.data.data,
        load: true
      })
    }
  ).catch(
    error => {
      thisApp.setState({
        load: true
      })
    }
  )
}



export {
  MessageRecent,
  MessageNotRead,
  LoggingList
};