import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, TextInput, FlatList, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { API_URL } from '../config'; // URL correta do arquivo config.js

export default function HomeScreen({ navigation }) {
  const [productName, setProductName] = useState('');
  const [products, setProducts] = useState([]);
  const [user, setUser] = useState(null);
  const [searchResults, setSearchResults] = useState([]);

  // Função para buscar o usuário logado ao carregar a tela
  useEffect(() => {
    fetchUser();
  }, []);

  // Função para buscar o usuário logado
  const fetchUser = async () => {
    try {
      const response = await fetch(`${API_URL}get_user/`, {
        credentials: 'include',
      });
      const data = await response.json();
      if (data.id) {
        setUser(data);
        fetchProducts(data); // Atualiza os produtos após buscar o usuário
      } else {
        console.log('Usuário não autenticado');
        setUser(null);
        navigation.navigate('Login'); // Redireciona para a tela de login
      }
    } catch (error) {
      console.error('Erro ao buscar o usuário:', error);
      navigation.navigate('Login'); // Redireciona para a tela de login
    }
  };

  // Função para buscar produtos da lista de compras
  const fetchProducts = async (userData) => {
    const userToUse = userData || user;
    if (!userToUse) return;

    try {
      const response = await fetch(`${API_URL}get_itens_lista/${userToUse.shopping_lists[0].id}/`);
      const data = await response.json();
      if (data.success) {
        setProducts(data.itens); // Atualiza a lista de produtos de forma correta
      } else {
        console.log('Erro ao buscar produtos:', data.message);
      }
    } catch (error) {
      console.error('Erro ao buscar os produtos:', error);
    }
  };

  // Função para buscar produtos pelo nome na base de dados
  const searchProduct = async () => {
    if (!productName.trim()) return;

    try {
      const response = await fetch(`${API_URL}buscar_produtos/?query=${productName}`);
      const data = await response.json();
      if (data.produtos && data.produtos.length > 0) {
        setSearchResults(data.produtos); // Mostrando os produtos disponíveis
      } else {
        Alert.alert('Nenhum produto encontrado.');
        setSearchResults([]); // Limpa os resultados de busca se nada for encontrado
      }
    } catch (error) {
      console.error('Erro ao buscar o produto:', error);
    }
  };

  // Função para adicionar um produto selecionado à lista de compras do usuário
  const addProduct = async (productId) => {
    if (!user) return;

    try {
      const response = await fetch(`${API_URL}adicionar_produto/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          produto_id: productId, 
          lista_id: user.shopping_lists[0].id, 
          quantity: 1, 
        }),
      });

      const data = await response.json();

      if (data.success) {
        Alert.alert('Sucesso', data.message);
        setProductName(''); // Limpa o campo de entrada de texto
        setSearchResults([]); // Limpa os resultados de busca
        fetchProducts(); // Atualiza a lista de produtos
      } else {
        Alert.alert('Erro', data.message);
      }
    } catch (error) {
      console.error('Erro ao adicionar o produto:', error);
    }
  };

  // Função para logout
  const logout = async () => {
    try {
      await fetch(`${API_URL}logout/`, {
        method: 'POST',
        credentials: 'include',
      });
      setUser(null);
      setProducts([]);
      setSearchResults([]);
      Alert.alert('Você foi desconectado.');
      navigation.navigate('Login'); // Redireciona para a tela de login
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  };

  const renderSearchItem = ({ item }) => (
    <TouchableOpacity style={styles.productItem} onPress={() => addProduct(item.id)}>
      <Text style={styles.productText}>{item.name}</Text>
    </TouchableOpacity>
  );

  const renderItem = ({ item }) => (
    <View style={styles.productItem}>
      <Text style={styles.productText}>{item.name}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity>
          <Ionicons name="menu" size={28} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.title}>Comprei!</Text>
        <TouchableOpacity onPress={logout}>
          <Ionicons name="log-out" size={28} color="#FFF" />
        </TouchableOpacity>
      </View>

      <View style={styles.content}>
        <Text style={styles.subtitle}>Minha casa</Text>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Buscar produto..."
            placeholderTextColor="#FFF"
            value={productName}
            onChangeText={(text) => setProductName(text)}
          />
          <TouchableOpacity style={styles.addButton} onPress={searchProduct}>
            <Text style={styles.addButtonText}>Buscar</Text>
          </TouchableOpacity>
        </View>

        {searchResults.length > 0 ? (
          <FlatList
            data={searchResults}
            renderItem={renderSearchItem}
            keyExtractor={(item) => item.id.toString()}
          />
        ) : (
          <>
            <Text style={styles.sectionTitle}>➟ Adicionados Recentemente</Text>
            <FlatList
              data={products}
              renderItem={renderItem}
              keyExtractor={(item) => item.id.toString()}
            />
          </>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FF0000',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 40,
    paddingHorizontal: 20,
    backgroundColor: '#D00000',
    paddingBottom: 10,
  },
  title: {
    color: '#FFF',
    fontSize: 24,
    fontWeight: 'bold',
    fontStyle: 'italic',
  },
  content: {
    flex: 1,
    paddingTop: 20,
  },
  subtitle: {
    color: '#FFF',
    fontSize: 20,
    marginLeft: 20,
    marginBottom: 10,
    fontWeight: 'bold',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginHorizontal: 20,
    marginBottom: 20,
  },
  input: {
    flex: 1,
    height: 40,
    borderColor: '#FFF',
    borderWidth: 1,
    paddingHorizontal: 10,
    color: '#FFF',
    borderRadius: 5,
    marginRight: 10,
  },
  addButton: {
    backgroundColor: '#FFF',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 5,
  },
  addButtonText: {
    color: '#D00000',
    fontWeight: 'bold',
  },
  emptyList: {
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 50,
  },
  cartImage: {
    width: 120,
    height: 120,
    marginBottom: 10,
  },
  emptyMessage: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  description: {
    color: '#FFF',
    fontSize: 14,
  },
  sectionTitle: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 20,
    marginTop: 20,
  },
  productItem: {
    backgroundColor: '#FFF',
    padding: 10,
    marginHorizontal: 20,
    marginVertical: 5,
    borderRadius: 5,
  },
  productText: {
    color: '#D00000',
    fontWeight: 'bold',
  },
});
