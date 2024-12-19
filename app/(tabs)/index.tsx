import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function LoginScreen() {
  const [nome, setNome] = useState("");
  const [password, setPassword] = useState("");
  const navigation = useNavigation(); // Usando a navegação do React Navigation

  const handleLogin = async () => {
    const userData = {
      nome,
      password,
    };

    console.log("Tentando fazer login com:", userData); // Log de verificação

    try {
      const response = await fetch("http://192.168.0.141:8000/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      console.log("Resposta da requisição:", response); // Log para verificar a resposta

      if (response.ok) {
        // Verifica se a resposta da API é bem-sucedida
        const result = await response.json();
        console.log("Resultado da requisição:", result);

        // Se o login for bem-sucedido, redireciona para a tela inicial
        navigation.navigate("TelaInicial");
      } else {
        // Caso a resposta não seja bem-sucedida
        const result = await response.json();
        console.log("Erro no login:", result); // Log do erro
        Alert.alert("Erro", result.message || "Erro desconhecido");
      }
    } catch (error) {
      console.error("Erro ao fazer a requisição:", error);
      Alert.alert("Erro", "Ocorreu um erro ao tentar fazer o login.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>

      <TextInput
        style={styles.input}
        placeholder="Nome"
        value={nome}
        onChangeText={setNome}
      />
      <TextInput
        style={styles.input}
        placeholder="Senha"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <Button title="Entrar" onPress={handleLogin} color="#FF0000" />

      {/* Link para a tela de cadastro */}
      <Text style={styles.link} onPress={() => navigation.navigate("cadastro")}>
        Não tem conta? Cadastre-se aqui
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FF0000",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#fff",
    marginBottom: 20,
  },
  input: {
    width: "80%",
    height: 40,
    borderColor: "#ddd",
    borderWidth: 1,
    borderRadius: 5,
    backgroundColor: "#fff",
    marginBottom: 15,
    paddingHorizontal: 10,
  },
  link: {
    marginTop: 15,
    color: "#fff",
    textDecorationLine: "underline",
  },
});
