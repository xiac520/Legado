<template>
  <div>
    <input v-model="searchKeyword" placeholder="输入搜索关键词">
    <button @click="searchBooks">搜索</button>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      searchKeyword: ''
    };
  },
  methods: {
    searchBooks() {
      axios.post('/api/search', { keyword: this.searchKeyword })
      .then(response => {
          // 处理搜索结果
        })
      .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>