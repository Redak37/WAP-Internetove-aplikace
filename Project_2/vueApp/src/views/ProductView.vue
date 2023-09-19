<template>
  <AppView>
    <h2>{{product.title}}</h2>
    <strong>Váha:</strong> {{product.weight}} g<br>
    <strong>Cena:</strong> {{product.price}} Kč<br>
    <strong>Popis:</strong> <p>{{product.description}}</p><br>
    <strong>Suroviny:</strong>
    <table class="table table-sm" style="width: 300px">
      <tbody>
      <tr v-for="resource in product.resources" v-bind:key="resource.id">
        <td>{{resource.resource.title}}</td>
        <td>{{resource.weight}} g</td>
      </tr>
      </tbody>
    </table>
    <router-link v-if="perms.includes('pekarnaApp.change_product')" v-bind:to="`/ProductEdit/${id}`">Upravit produkt</router-link>
  </AppView>
</template>


<script>
import AppView from "@/components/AppView";

export default {
  name: 'ProductView',
  components: {AppView},
  data() {
    return {
      id: this.$route.params.id,
      perms: [],
      product: {}
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    this.fetchProduct();
  },
  methods: {
    async fetchProduct() {
      await this.$http.get(`product/${this.id}/view`)
          .then((response) => {
            this.product = response.data;
          })
          .catch(error => {
            console.log('error', error);
          });
    },
  },
};
</script>
