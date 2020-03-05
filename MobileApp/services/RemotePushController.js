import React, { useEffect } from 'react'
import PushNotification from 'react-native-push-notification'

import database from '@react-native-firebase/database';
import auth from '@react-native-firebase/auth';

const RemotePushController = () => {
  //alert("HIIIJDFLISDJFL");
  useEffect(() => {
    //alert("in useeffect");
    PushNotification.configure({
      
      // (optional) Called when Token is generated (iOS and Android)
      onRegister: function(token) {
        console.log('TOKEN:', token);
        const uid = auth().currentUser.uid;
        const ref_db = database().ref(`/users/${uid}/token`);
        ref_db.set({
          token: token.token
        }).then(res => {
          console.log("Token updated successfully");
        })
      },

      // (required) Called when a remote or local notification is opened or received
      onNotification: function(notification) {
        console.log('REMOTE NOTIFICATION ==>', notification)

        // process the notification here
      },
      // Android only: GCM or FCM Sender ID
      senderID: '929553635554',
      popInitialNotification: true,
      requestPermissions: true
    })
  }, [])

  return null
}

export default RemotePushController