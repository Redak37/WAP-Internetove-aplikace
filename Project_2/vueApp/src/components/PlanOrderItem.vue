<template>
  <tr>
    <td>
      <table>
         <tr style="background-color: transparent" v-for="item in this.order_products" v-bind:key="item.id">
           <td>{{item.product.title}}</td>
           <td>{{item.quantity}}x</td>
         </tr>
      </table>
    </td>
    <td>
        <table id="resourceTable" class="table-striped table-hover table-bordered table-sm" v-if="perms.includes('pekarnaApp.view_order')">
          <thead>
            <tr><th>Surovina</th><th>Množství (g)</th></tr>
          </thead>
          <tbody>
            <tr v-for="resourcePair in order_resources" :key="resourcePair.id">
              <td>{{resourcePair[0].title}}</td>
              <td>{{resourcePair[1]}}</td>
            </tr>
          </tbody>
        </table>
    </td>
    <td>{{item.notes}}</td>
    <td v-if="item.state.title === 'Potvrzena'"><button v-on:click="readyOrder" class="btn btn-success btn-sm">Všechny položky připraveny</button></td>
    <td v-else-if="order_acceptable"><button v-on:click="acceptOrder" class="btn btn-success btn-sm">Potvrdit</button></td>
    <td v-else><button v-on:click="acceptOrder" disabled="disabled" class="btn btn-block btn-sm">Nelze potvrdit. Chybí suroviny na skladě.</button></td>
    <td v-if="item.state.title !=='Potvrzena'"><button v-on:click="cancelOrder" class="btn btn-danger btn-sm">Zamítnout</button></td>
  </tr>
</template>


<style scoped>
#resourceTable tr{
    display: block;
    float: left;
}
#resourceTable td th{
    display: block;
}
</style>

<script>
import $ from "jquery";

export default {
  props: ['item', 'order_resources', 'order_acceptable'],
  data() {
    return {
      perms: [],
      order_products: []
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    this.fetchData();
  },
  methods: {
    cancelOrder: function () {
      if (confirm("Opravdu chcete zamítnout objednávku?")) {
        this.$http.get('my_orders_reject/' + this.item.id)
            .then(() => {
              this.$destroy();
              this.$el.parentNode.removeChild(this.$el);
            })
            .catch(error => {
              console.log(error);
            });
      }
    },

    acceptOrder: function () {
      if (confirm("Potvrdit objednávku?")) {
        this.$http.get('my_orders_accept/' + this.item.id)
            .then(() => {
              this.$emit('eventOrderAccepted');
            })
            .catch(error => {
              console.log(error);
            });
      }
    },

    readyOrder: function () {
      if (confirm("Před potvrzením zkontrolujte, zda jsou všechny položky objednávky hotovy a připraveny k doručení.\n" +
          "Jsou všechny položky připraveny?")) {
        this.$http.get('my_orders_complete/' + this.item.id)
            .then(() => {
              this.$emit('eventOrderAccepted');
            })
            .catch(error => {
              console.log(error);
            });
      }
    },

    async fetchData() {
      this.$http.get('orders/' + this.item.id + '/products', {params: {format: 'json'}})
          .then((res) => {
            this.order_products = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async showEditForm(object_id) {
      localStorage.edit_item_id = object_id;
      await this.$http.get('my_orders_view/' + object_id)
          .then((res) => {
            document.getElementById("form-edit").innerHTML = res.data['form'];
            document.getElementById("edit-footer").style.display = "";
            $("#modal-edit").modal('show');
          })
          .catch(error => {
            console.log(error);
          });
    },
  },
};
</script>
