<template>
  <tr :class="getStyle(stock)">
    <td>
      <router-link v-bind:to="`/ProductView/${this.item.id}`">{{item.title}}</router-link>
    </td>
    <td>
      <router-link v-bind:to="`/ProductList/${this.item.category.title}`">{{item.category.title}}</router-link>
    </td>
    <td v-if="perms.includes('pekarnaApp.add_order')"><input class="form-control" type="number" v-model="stock" @change="stockChanged"></td>
    <td style="text-align: right">{{item.price}} Kč</td>
    <td style="text-align: right">{{stockChanged(item.price, stock)}} Kč</td>
    <td><button class="btn btn-dark" @click="showAllergens">Alergeny</button></td>
  </tr>
</template>

<script>
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  props: ['item', 'stock'],
  data() {
    return {
      perms: [],
      productId: false
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
  },
  methods: {
    stockChanged: function (price, stock) {
      if (stock < 0) {
        stock = this.stock = 0;
      }
      this.$emit('stock', {stock: this.stock, id: this.item.id});
      return (price * stock).toFixed(2);
    },
    getStyle: function (stock) {
      if (stock > 0) {
        return "table-info";
      } else {
        return "";
      }
    },
    showAllergens() {
      this.$emit('allergens', this.item.id);
    },
  },
};
</script>
