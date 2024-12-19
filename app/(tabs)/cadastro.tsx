/*
Universidade de São Paulo
SSC0621 - Modelagem Orientada a Objetos
*/

import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Image } from "react-native";

export default function CadastroScreen() {
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleCadastro = async () => {
    // Exibir os valores antes do envio
    console.log("Dados enviados:", { nome, email, password, confirmPassword });
  
    // Verificar se as senhas coincidem
    if (password !== confirmPassword) {
      alert("As senhas não coincidem!");
      console.log("Erro: As senhas não coincidem.");
      return;
    }
  
    // Dados que serão enviados ao backend
    const userData = {
      nome,
      email,
      password,
      confirm_password: confirmPassword,
    };
  
    try {
      console.log("Enviando requisição para o backend...");
      
      const response = await fetch("http://192.168.0.141:8000/cadastro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });
  
      const result = await response.json();
      console.log("Dados retornados pelo backend:", result);
  
      if (response.ok) {
        alert(result.message); // Cadastro realizado com sucesso
      } else {
        alert(result.message); // Exibe erro, como nome de usuário ou email já cadastrados
      }
    } catch (error) {
      alert("Erro ao cadastrar. Tente novamente.");
      console.error("Erro durante a requisição:", error);
    }
  };
  

  return (
    <View style={styles.container}>
      <Image
        style={styles.logo}
        source={{ uri: 'https://example.com/logo.png' }}  // Aqui você pode colocar a URL do logo
      />
      <Text style={styles.title}>Criar Conta</Text>

      <TextInput
        style={styles.input}
        placeholder="Nome Completo"
        value={nome}
        onChangeText={setNome}
      />
      <TextInput
        style={styles.input}
        placeholder="Email"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Senha"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />
      <TextInput
        style={styles.input}
        placeholder="Confirmar Senha"
        secureTextEntry
        value={confirmPassword}
        onChangeText={setConfirmPassword}
      />

      <Button title="Criar Conta" onPress={handleCadastro} color="#FF0000" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#FF0000", // Mantém o padrão vermelho
  },
  logo: {
    width: 100,
    height: 100,
    marginBottom: 20,
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
});
