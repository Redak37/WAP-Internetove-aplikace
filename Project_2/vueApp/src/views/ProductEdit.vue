<template>
  <AppView>
    <ProductForm v-bind:id="id" mode="edit" />
  </AppView>
</template>


<script>
import AppView from "@/components/AppView";
import ProductForm from "@/components/ProductForm";

export default {
  name: 'ProductEdit',
  components: {AppView, ProductForm},
  data() {
    return {
      id: this.$route.params.id
    };
  },
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.change_product')) {
      this.$router.push('/')
    }
  },
};
</script>
