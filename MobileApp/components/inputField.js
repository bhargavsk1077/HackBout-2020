import React, { Component } from "react";
import { View, Text, StyleSheet,TextInput,TouchableOpacity } from "react-native";
class InputField extends Component {
    constructor(props) {
        super(props);
        this.state = {
            secureInput: !(props.inputType === "text" || props.inputType === "email")
        };
        this.toggleShowPassword = this.toggleShowPassword.bind(this);
    }

    toggleShowPassword() {
        this.setState({ secureInput: !this.state.secureInput });
    }

    render() {
        const {
            labelText,
            labelTextSize,
            labelColor,
            textColor,
            borderBottomColor,
            inputType,
            customStyle,
            secureInput
        } = this.props;
        const color = labelColor || '#ffffff';
        const fontSize = labelTextSize || 14;
        const inputColor = textColor || '#ffffff';
        const borderBottom = borderBottomColor || "transparent";
        //const { labelText } = this.props;
        return (
            <View style={[customStyle, styles.wrapper]}>
                <Text style={[{ color, fontSize }, styles.label]}>{labelText}</Text>
                {inputType === "password" ? (
                    <TouchableOpacity
                        style={styles.showButton}
                        onPress={this.toggleShowPassword}
                    >
                        <Text style={styles.showButtonText}>
                        {secureInput ? "Show" : "Hide"}
                        </Text>
                    </TouchableOpacity>
                    ) : null}
                <TextInput
                    autoCorrect={false}
                    style={[
                        { color: inputColor, borderBottomColor: borderBottom },
                        styles.inputFiled
                    ]}
                    secureTextEntry={secureInput}
                />
            </View>
        );
    }
}

const styles = StyleSheet.create({
    wrapper: {
      display: "flex"
    },
    label: { fontWeight: "700", marginBottom: 10 },
    inputFiled: {
      borderBottomWidth: 1,
      paddingTop: 5,
      paddingBottom: 5
    },
    showButton: {
        position: "absolute",
        right: 0
      },
      showButtonText: {
        color: '#ffffff',
        fontWeight: "700"
      }
  });

export default InputField;