import React from 'react';
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native';
import { createStackNavigator } from '@react-navigation/stack';
import Home from "./home";
import auth from '@react-native-firebase/auth';

const Stack = createStackNavigator();

export default class Login extends React.Component<Props>{

 constructor(props){
    super(props);
    this.state={
        email:"",
        password:"",
        authenticated:false
    }
  }

  
HomeScreen({ navigation }) {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Home Screen</Text>
      <Button
        title="Go to Details"
        onPress={() => navigation.navigate('Details')}
      />
    </View>
  );
}

DetailsScreen() {
  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text>Details Screen</Text>
    </View>
  );
}


  forgotPassword(){
    auth().sendPasswordResetEmail(this.state.email).then(ret => {
      alert("Jai! Check your mail...");
    })
  }

  authenticateLogin(){
      // alert("Succesfully Logged In!");
    if (this.state.email.length > 5 && this.state.password.length > 8) {
      auth().signInWithEmailAndPassword(this.state.email, this.state.password).then(res => {
        console.log("Login", res);
        if (res) {
          this.setState({authenticated:true})
        }
      },
      res => {
        console.log("Login", res);
        alert("Login unsuccessful");
      }
      )
    }
    else {
      alert("Email or password too short");
    }
  }

  signUp() {
    if (this.state.email.length > 5 && this.state.password.length > 8) {
      auth().createUserWithEmailAndPassword(this.state.email, this.state.password).then(res => {
        console.log("Sign Up", res);
        alert("Sign up successful");
      },
        res => {
          console.log("Sign Up", res);
          alert("Sign up unsuccessful");
        }
      )
    }
    else {
      alert("Email or password too short");
    }
  }

  jumpToHome(){
    //alert('In Home');
    return (
        <Home/>
     );
}

  loginPage(){
    return (
        <View style={styles.container}>
          <Text style={styles.logo}>Park-O-Report</Text>
          <View style={styles.inputView} >
            <TextInput  
              style={styles.inputText}
              placeholder="Email..." 
              placeholderTextColor="#003f5c"
              onChangeText={text => this.setState({email:text})}/>
          </View>
          <View style={styles.inputView} >
            <TextInput  
              secureTextEntry
              style={styles.inputText}
              placeholder="Password..." 
              placeholderTextColor="#003f5c"
              onChangeText={text => this.setState({password:text})}/>
          </View>
          <TouchableOpacity onPress={this.forgotPassword.bind(this)}>
            <Text style={styles.forgot}>Forgot Password?</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.loginBtn} onPress={this.authenticateLogin.bind(this)}>
            <Text style={styles.loginText}>LOGIN</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={this.signUp.bind(this)}>
                        <Text style={styles.loginText}>Signup</Text>
          </TouchableOpacity>
  
    
        </View>
      );
  }

  render(){
    return(
        this.state.authenticated ? this.jumpToHome() : this.loginPage()
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#003f5c',
    alignItems: 'center',
    justifyContent: 'center',
  },
  logo:{
    fontWeight:"bold",
    fontSize:50,
    color:"#fb5b5a",
    marginBottom:40
  },
  inputView:{
    width:"80%",
    backgroundColor:"#465881",
    borderRadius:25,
    height:50,
    marginBottom:20,
    justifyContent:"center",
    padding:20
  },
  inputText:{
    height:50,
    color:"white"
  },
  forgot:{
    color:"white",
    fontSize:11
  },
  loginBtn:{
    width:"80%",
    backgroundColor:"#fb5b5a",
    borderRadius:25,
    height:50,
    alignItems:"center",
    justifyContent:"center",
    marginTop:40,
    marginBottom:10
  },
  loginText:{
    color:"white"
  }
});