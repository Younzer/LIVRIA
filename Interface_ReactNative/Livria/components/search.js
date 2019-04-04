// components/search.js

import books from '../helpers/bookData'
import BookItem from './bookItem'
import React from "react";
import { StyleSheet, View, TextInput, Button, FlatList, Text } from "react-native";

class Search extends React.Component {
  render() {
    return (
      <View style={styles.main_container}>
        <TextInput style={styles.textinput} placeholder="Titre du film" />
        <Button title="rechercher" onPress={() => {}} />
        <FlatList
          data={books}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({item}) => <BookItem/>}
        />
      </View>
    )
  }
}

const styles = StyleSheet.create({
  main_container: {
    flex: 1,
    marginTop: 23
  },

  textinput: {
    marginLeft: 5,
    marginRight: 5,
    height: 50,
    borderColor: "#000000",
    borderWidth: 1,
    paddingLeft: 5
  }
});

export default Search;
