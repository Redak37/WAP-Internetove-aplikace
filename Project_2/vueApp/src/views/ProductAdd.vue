<template>
  <AppView>
    <ProductForm mode="create" />
  </AppView>
</template>


<script>
import AppView from "@/components/AppView";
import ProductForm from "@/components/ProductForm";

export default {
  name: 'ProductAdd',
  components: {AppView, ProductForm},
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.add_product')) {
      this.$router.push('/')
    }
  },
};
</script>
