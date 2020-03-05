import React,{Component} from 'react';
import {View,StyleSheet,Text,TouchableOpacity} from 'react-native';
import t from 'tcomb-form-native';
import database from '@react-native-firebase/database';
import auth from '@react-native-firebase/auth';
import Home from './home';

const Form = t.form.Form;
const stylsheeto = Form.stylesheet;
stylsheeto.textbox.color = "#fff";
stylsheeto.controlLabel="#fff";
stylsheeto.LABEL_COLOR="#fff";
stylsheeto.INPUT_COLOR="#fff";
stylsheeto.color="#fff";
stylsheeto.textbox.normal.borderColor="#fff";
stylsheeto.textbox.normal.color = "#fff";
stylsheeto.controlLabel.normal.color="#fff";
var Report = t.enums({
    "Illegal Parking": "Illegal Parking",
    "Abandonment": "Abandonment",
    "Temporary Breakdown": "Temporary Breakdown",
})
var Severity = t.enums({
    1 : "Low",
    2 : "Medium",
    3 : "High"
})
var Vehicle = t.enums({
    "car": "Car",
    "bicycle": "Bicycle",
    "motorcycle": "Motorcycle",
    "bus": "Bus",
    "truck": "Truck"
})
const User = t.struct({
    vehicle: Vehicle,
    severity: Severity,
    numberPlate: t.String,
    vehicleColor: t.maybe(t.String),
    vehicleModel : t.maybe(t.String),
    vehicleCompany : t.maybe(t.String),
    report : Report
});

const apiPrefix = "https://park-o-report.herokuapp.com/"
const api2Prefix = "http://10.42.0.1:5002/"

export default class FormDetails extends Component {

    constructor(props) {
        super(props);
        this.state = {
          value: {
            numberPlate: "XXXXXXXXXX",
            vehicle: props.modelState.recognitions[props.modelState.id_].detectedClass,
          },
          isUploaded: false
        }
    }

    componentDidMount() {
        console.log("Detected class", this.props.modelState.recognitions[this.props.modelState.id_].detectedClass);
        this.setState({ vehicle: this.props.modelState.recognitions[this.props.modelState.id_].detectedClass });
    }

    clearForm() {
        // clear content from all textbox
        this.setState({ value: null });
    }

    onChange(value) {
        console.log("Value", value);
        console.log("State value", this.state);
        let val = value;
        if (val.numberPlate == "XXXXXXXXXX" && this.props.modelState.numberPlate != null)
            val.numberPlate = this.props.modelState.numberPlate;
        this.setState({ value:val });
    }

    uploadData() {
        var value = this._form.getValue();
        console.log("Form value", value);
        console.log("Model State", this.props.modelState);

        const selectedRecog = this.props.modelState.recognitions[this.props.modelState.id_];
        console.log("Selected detection:", selectedRecog);
    
        const uid = auth().currentUser.uid;
    

        const ref_db = database().ref(`/reports/${this.props.modelState.uuid}`);
        ref_db.set({
            confidence: selectedRecog.confidenceInClass,
            class: selectedRecog.detectedClass,
            rect: selectedRecog.rect,
            uid: auth().currentUser.uid,
            numberPlate: value.numberPlate,
            severity: value.severity,
            vehicleColor: value.vehicleColor,
            vehicleCompany: value.vehicleCompany,
            vehicleModel: value.vehicleModel,
            report: value.report,
            lat: this.props.modelState.lat,
            long: this.props.modelState.long,
            timestamp: Date.now()
        }).then(res => {
            console.log("Data uploaded", res);
            alert("Upload successful");
            this.clearForm();
            this.setState({isUploaded:true});
        })
    }

    render(){
        //alert('ola');
        return(
                    <View style={styles.container}>
                        <Form
                            ref={c => this._form = c}
                            type={User}
                            value={this.state.value}
                            onChange={this.onChange.bind(this)}
                            style={styles.container}
                        />
                        <TouchableOpacity style= {styles.uploadButton}
                            onPress={this.uploadData.bind(this)} >
                            <Text>Upload</Text>
                        </TouchableOpacity>
                    </View>
        );
    }
}

const styles = StyleSheet.create({
    container:{
        justifyContent:'center',
        width:400,
        marginTop: 50,
        padding:20,
        backgroundColor:'#003f5c',
        color:'#ffffff',
        textDecorationColor:'#ffffff', 
        borderColor:'#ffffff',
    },
    uploadButton:{
        width:"80%",
        backgroundColor:"#fb5b5a",
        borderRadius:25,
        height:50,
        alignItems:"center",
        justifyContent:"center",
        marginTop:40,
        marginBottom:10
    },
});