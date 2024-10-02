<template>
  <div>
    <SearchForm />
    <BookDetails />
    <ChapterList />
    <ChapterContent />
  </div>
</template>

<script>
import SearchForm from './components/SearchForm.vue';
import BookDetails from './components/BookDetails.vue';
import ChapterList from './components/ChapterList.vue';
import ChapterContent from './components/ChapterContent.vue';

export default {
  components: {
    SearchForm,
    BookDetails,
    ChapterList,
    ChapterContent
  }
};
</script>