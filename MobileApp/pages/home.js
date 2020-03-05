import * as React from 'react';
import { Button, View, Text,StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import RNLocation from 'react-native-location';
import database from '@react-native-firebase/database';
import auth from '@react-native-firebase/auth';

import Model from '../components/Model';

import RemotePushController from '../services/RemotePushController';
import { TouchableOpacity } from 'react-native-gesture-handler';

RNLocation.configure({
  distanceFilter: 100,
  desiredAccuracy: {
    ios: "best",
    android: "highAccuracy"
  },
  // Android only
  androidProvider: "auto",
  interval: 5000, // Milliseconds
  fastestInterval: 10000, // Milliseconds
  maxWaitTime: 5000, // Milliseconds
})

function HomeScreen({ navigation }) {
  RNLocation.requestPermission({
    ios: "whenInUse",
    android: {
      detail: "fine",
      rationale: {
        title: "We need to access your location",
        message: "We use your location to notify you when there is a new report in your area",
        buttonPositive: "OK",
        buttonNegative: "Cancel"
      }
    }
  }).then(granted => {
      if (granted) {
        this.locationSubscription = RNLocation.subscribeToLocationUpdates(locations => {
          console.log("New location received:", locations);
  
          const uid = auth().currentUser.uid;
          const ref_db = database().ref(`/users/${uid}/location`);
          if (locations.length > 0) {
            ref_db.set({
              lat: locations[0].latitude,
              long: locations[0].longitude,
              timestamp: locations[0].timestamp,
              accuracy: locations[0].accuracy,
              speed: locations[0].speed
            }).then(ret => {
              console.log("Location updated successfully");
            })
          }
          /* Example location returned
          {
            speed: -1,
            longitude: -0.1337,
            latitude: 51.50998,
            accuracy: 5,
            heading: -1,
            altitude: 0,
            altitudeAccuracy: -1
            floor: 0
            timestamp: 1446007304457.029,
            fromMockProvider: false
          }
          */
        })
      }
    },
    res => {
      alert("Location not granted!");
    }
    )
  return (
    <View style={styles.headerColor}>
      {/* <Text>Home Screen</Text> */}
      <TouchableOpacity
        onPress={() => navigation.navigate('Run Model')}
        style={{
            backgroundColor:'#fb5b5a',
            padding:20,
            borderRadius:42,
            width:300,
            alignItems:'center'
        }}>
        <Text style={styles.textButton}>Report an issue</Text>
      </TouchableOpacity>
    </View>
  );
}

function DetailsScreen() {
  return (
    <Model/>
  );
}

const Stack = createStackNavigator();

function Home() {
  return (
    <NavigationContainer>
    <RemotePushController/>
      <Stack.Navigator initialRouteName="Home" >
        <Stack.Screen name="Home" component={HomeScreen} options={{
            title:'Home',
            headerStyle:{
                backgroundColor: '#fb5b5a',
            },
            headerTintColor:'#fff',
            headerTitleStyle: {
                fontWeight: 'bold',
            },
        }}/>
        <Stack.Screen name="Run Model" component={DetailsScreen} options={{
            title:'Run Model',
            headerStyle:{
                backgroundColor: '#fb5b5a',
            },
            headerTintColor:'#fff',
            headerTitleStyle: {
                fontWeight: 'bold',
            },
        }}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default Home;

const styles = StyleSheet.create({
    headerColor:{
        flex: 1,
        backgroundColor: '#003f5c',
        alignItems: 'center',
        justifyContent: 'center',
    },
    textButton:{
        alignContent:'center',
        fontWeight:'bold',
        fontSize:20,
        color:'#fff'
    }
});