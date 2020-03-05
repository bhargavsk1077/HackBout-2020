import React, { Component } from 'react';
import { Platform, StyleSheet, Image, Text, View, TouchableOpacity, Button } from 'react-native';
import Tflite from 'tflite-react-native';
import ImagePicker from 'react-native-image-picker';
import { firebase } from '@react-native-firebase/storage';
import database from '@react-native-firebase/database';
import auth from '@react-native-firebase/auth';
import FormDetails from '../pages/form';
import Overlay from 'react-native-modal-overlay';
import RNLocation from 'react-native-location';

let tflite = new Tflite();

const height = 350;
const width = 350;
const blue = "#25d5fd";
//const mobile = "MobileNet";
const ssd = "SSD MobileNet";
//const yolo = "Tiny YOLOv2";
//const deeplab = "Deeplab";
//const posenet = "PoseNet";
const validClasses = ["car", "bicycle", "motorcycle", "bus", "truck"]

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

const apiPrefix = "https://park-o-report.herokuapp.com/"
const api2Prefix = "http://10.42.0.1:5002/"

type Props = {};
export default class Model extends Component<Props> {
  constructor(props) {
    super(props);
    this.state = {
      model: null,
      source: null,
      imageHeight: height,
      imageWidth: width,
      recognitions: [],
      token: null,
      filePath: null,
      uuid: null,
      modalVisible: false,
      uploadClick: false,
      id_: null,
      numberPlate: null,
      bgcolor:'#fb5b5a',
      lat: null,
      long: null
    };
  }


  onSelectImage() {
    this.setState({bgcolor:'#003f5c'});
    const options = {
      title: 'Select Avatar',
      customButtons: [{ name: 'fb', title: 'Choose Photo from Facebook' }],
      storageOptions: {
        skipBackup: true,
        path: 'images',
      },
    };
    ImagePicker.launchImageLibrary(options, (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        let filePath = 'file://' + response.path;
        var uuid = uuidv4();
        this.setState({ filePath, uuid });

        var path = Platform.OS === 'ios' ? response.uri : 'file://' + response.path;
        var w = response.width;
        var h = response.height;
        this.setState({
          source: { uri: path },
          imageHeight: h * width / w,
          imageWidth: width
        });

        tflite.detectObjectOnImage({
          path,
          threshold: 0.2,
          numResultsPerClass: 1,
        },
          (err, res) => {
            if (err)
              console.log(err);
            else
              this.setState({ recognitions: res });
        });
      }
    });
  }

  selectedBox(id_) {
    // Upload here for now
    console.log("Box clicked", id_);
    this.setState({modalVisible:true});
  }

  goBack(){
    this.setState({modalVisible:false});
  }

  uploadImage(id_) {
    const selectedRecog = this.state.recognitions[id_];
    console.log("Selected detection:", selectedRecog);

    const uid = auth().currentUser.uid;

    const ref = firebase.storage().ref('images/'+this.state.uuid);
    const path = this.state.filePath; //`${firebase.utils.FilePath.DOCUMENT_DIRECTORY}/new-logo.png`;
    const task = ref.putFile(path); 
    task.resume();
    task.then(res => {
      console.log("Task complete:", res);
      var lat = 0.0;
      var long = 0.0;
      RNLocation.getLatestLocation({ timeout: 60000 }).then(latestLocation => {
        // Use the location here
        console.log("Got location:", latestLocation);
        lat = latestLocation.latitude;
        long = latestLocation.longitude;
        this.setState({ lat });
        this.setState({ long });
          
        const ref_db = database().ref(`/reports/${this.state.uuid}`);
        ref_db.set({
          confidence: selectedRecog.confidenceInClass,
          class: selectedRecog.detectedClass,
          rect: selectedRecog.rect,
          uid: auth().currentUser.uid,
          lat: lat,
          long: long
        }).then(res => {
          console.log("Data uploaded", res);
          alert("Upload successful");

          let formdata = new FormData();
          formdata.append("uid", uid)
          fetch(apiPrefix + "api/location/notifyNearby", {
            method: 'POST',
            headers: {
              'Content-Type': 'multipart/form-data',
            },
            body: formdata
          }).then((resp) => {
            console.log("Sent notification", resp);
          }, (resp) => {
            console.log("Fail notfication", resp)
          }
          )

          formdata = new FormData();
            formdata.append("uuid", this.state.uuid);
            fetch(api2Prefix + "api/number-plate/detectFromDB", {
              method: 'POST',
              headers: {
                'Content-Type': 'multipart/form-data',
              },
              body: formdata
            }).then((resp) => {
              console.log("Got detection");
              return resp.json()
            }, (resp) => {
              console.log("Did not get detection");
              throw resp;
            }).catch(e => {
              console.log("Did not get detection (caught error:", e, ")");
              if (e != null) throw e;
            }).then(
              (data) => {
                console.log("Number plate", data);
                alert("Number plate is " + data["number"]);
                this.setState({ numberPlate: data["number"] });
              },
              (data) => {
                console.log("Could not get number plate", data);
              }
            ).catch(e => {
              console.log("Could not get number plate", e);
            })
          })
      })
    })
    this.setState({uploadClick:true, id_:id_});
  }

  renderResults() {
    const { model, recognitions, imageHeight, imageWidth } = this.state;
    return recognitions.map((res, id) => {
      if (validClasses.includes(res["detectedClass"])) {
        var left = res["rect"]["x"] * imageWidth;
        var top = res["rect"]["y"] * imageHeight;
        var width = res["rect"]["w"] * imageWidth;
        var height = res["rect"]["h"] * imageHeight;
        return (
          <View key={id}>
                <TouchableOpacity style={[styles.box, { top, left, width, height }]} onPress={this.selectedBox.bind(this, id)}>
                  <Text style={{ color: 'white', backgroundColor: blue }}>
                    {res["detectedClass"] + " " + (res["confidenceInClass"] * 100).toFixed(0) + "%"}
                  </Text>
                </TouchableOpacity>
                <Overlay visible={this.state.modalVisible} onClose={this.onClose} closeOnTouchOutside style={styles.container}>
                    <Text>Would You Like to upload this image?</Text>
                    <Button
                      title="Go Back"
                      onPress={this.goBack.bind(this)}
                      style={styles.button1}
                    />
                    <Button
                      title="Upload"
                      onPress={this.uploadImage.bind(this,id)}
                      style={styles.button2}
                    />
                </Overlay>
          </View>
      )}
    });
  }
  
  render() {
    const { model, source, imageHeight, imageWidth,bgcolor } = this.state;
    // var renderButton = (m) => {
    //   return (
    //     <TouchableOpacity style={styles.button} onPress={this.onSelectModel.bind(this, m)}>
    //       <Text style={styles.buttonText}>{m}</Text>
    //     </TouchableOpacity>
    //   );
    // }
    
    return (
      <View style={styles.container}>
            {this.state.uploadClick ?
                  <FormDetails modelState={this.state} />
            :
            <TouchableOpacity style={{
                backgroundColor:bgcolor,
                padding:20,
                borderRadius:42,
                width:300,
                alignItems:'center'
              }}
                onPress={source ? null : this.onSelectImage.bind(this,ssd)}
                activeOpacity={source ? 1 : 0}
              >
              {
                source ?
                  <Image source={source} style={{
                    height: imageHeight, width: imageWidth
                  }} resizeMode="contain" /> :
                  <Text style={styles.text}>Select Picture</Text>
              }
              <View style={styles.boxes}>
                {this.renderResults()}              
              </View>
            </TouchableOpacity>  
            }   
      </View>

    );
  }
}


function onSelectModel(model) {
  console.log(model+'this has been accepted');
  var modelFile = 'models/ssd_mobilenet.tflite';
  var labelsFile = 'models/ssd_mobilenet.txt';
  tflite.loadModel({
    model: modelFile,
    labels: labelsFile,
  },
    (err, res) => {
      if (err)
        console.log(err);
      else
        console.log(res);
    });
}


onSelectModel(ssd);
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#003f5c',
    padding:12
  },

  buttonContainer: {
    flex: 1,
    flexDirection:('row'),
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
    padding:12
  },

  imageContainer: {
    borderColor: blue,
    borderRadius: 5,
    alignItems: "center"
  },
  text: {
    alignContent:'center',
    fontWeight:'bold',
    fontSize:20,
    color:'#fff'
  },
  button: {
    width: 200,
    backgroundColor: blue,
    borderRadius: 10,
    height: 40,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10
  },
  buttonText: {
    color: 'white',
    fontSize: 15
  },
  box: {
    position: 'absolute',
    borderColor: blue,
    borderWidth: 2,
    zIndex: 5,
    opacity: 0.8
  },
  boxes: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    top: 0,
  },
  button1:{
    flex:1,
    flexDirection:'row',
    margin:20,
    justifyContent:'center'
  },
  button2:{
    flex:1,
    alignSelf:'center',
    margin:20,
    justifyContent:'center'
  }
});
