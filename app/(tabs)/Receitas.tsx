import React, { useState } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, TextInput, FlatList } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export default function HomeScreen() {
  const [productName, setProductName] = useState('');
  const [products, setProducts] = useState([]);

  // Função para adicionar um novo produto
  const addProduct = () => {
    if (productName.trim()) {
      const newProduct = {
        id: Date.now(),
        name: productName,
        isRecent: true, // Define como "adicionado recentemente"
      };
      setProducts([newProduct, ...products]); // Adiciona o novo produto no topo
      setProductName(''); // Limpa o input
    }
  };

  // Função para alternar a posição do produto
  const toggleProductSection = (id) => {
    setProducts((prevProducts) =>
      prevProducts.map((product) =>
        product.id === id ? { ...product, isRecent: !product.isRecent } : product
      )
    );
  };

  // Renderiza cada item da lista
  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.productItem} onPress={() => toggleProductSection(item.id)}>
      <Text style={styles.productText}>{item.name}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {/* Cabeçalho */}
      <View style={styles.header}>
        <TouchableOpacity>
          <Ionicons name="menu" size={28} color="#FFF" />
        </TouchableOpacity>
        <Text style={styles.title}>Comprei!</Text>
        <TouchableOpacity>
          <Ionicons name="person-circle" size={28} color="#FFF" />
        </TouchableOpacity>,.
      </View>

      {/* Conteúdo principal */}
      <View style={styles.content}>
        <Text style={styles.subtitle}>Lasanha</Text>

        {/* Campo para adicionar produtos */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Adicionar produto..."
            placeholderTextColor="#FFF"
            value={productName}
            onChangeText={(text) => setProductName(text)}
          />
          <TouchableOpacity style={styles.addButton} onPress={addProduct}>
            <Text style={styles.addButtonText}>Adicionar</Text>
          </TouchableOpacity>
        </View>

        {/* Ícone da lista vazia */}
        {products.length === 0 ? (
          <View style={styles.emptyList}>
            <Image
              source={{ uri: 'https://cdn-icons-png.flaticon.com/512/3081/3081559.png' }}
              style={styles.cartImage}
            />
            <Text style={styles.emptyMessage}>Adicione os ingredientes da sua receita.</Text>
          </View>
        ) : (
          <>
            {/* Seção Adicionados Recentemente */}
            <FlatList
              data={products.filter((product) => product.isRecent)}
              renderItem={renderItem}
              keyExtractor={(item) => item.id.toString()}
            />

            {/* Seção Produtos Anteriores */}
            <Text style={styles.sectionTitle}>➤ Adicionado na lista de compras.</Text>
            <FlatList
              data={products.filter((product) => !product.isRecent)}
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
