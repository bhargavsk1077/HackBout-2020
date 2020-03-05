import * as React from 'react';
import { 
    Button,
    Image,
    PixelRatio,
    StyleSheet,
    Text,
    TouchableOpacity,
    View,
 } from 'react-native';
import ImagePicker from 'react-native-image-picker';

function imagePick(){

    const options = {
        title: 'Select an image',
        customButtons:[{name:'choose',title:'choose'}],
        storageOptions:{
            skipBackup:true,
            path:'images',
        },
    };

    ImagePicker.showImagePicker(options,(response) =>{
        console.log('Response = ',response);
        if (response.didCancel) {
            console.log('User cancelled image picker');
        } else if (response.error) {
            console.log('ImagePicker Error: ', response.error);
        } else if (response.customButton) {
            console.log('User tapped custom button: ', response.customButton);
        } else {
            const source = { uri: response.uri };
            //const source = { uri: 'data:image/jpeg;base64,' + response.data };  
        }
    });

}

export default function UploadPage() {
    return(
        <View>
            
            <Button
                title='Upload'
                onPress = {imagePick}
            />
        </View>
    );
}