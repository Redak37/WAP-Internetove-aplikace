<template>
  <tr>
    <td>
      <table>
         <tr style="background-color: transparent" v-for="item in this.order_products" v-bind:key="item.id">
           <td>{{item.product.title}}</td>
           <td>{{item.product.price}}Kč</td>
           <td>{{item.quantity}}x</td>
         </tr>
      </table>
    </td>
    <td>{{item.state != null ? item.state.title : '---'}}</td>
    <td>{{item.address}}</td>
    <td>{{item.deliver_date}}</td>
    <td>{{item.notes}}</td>
    <td>{{item.delivered != null ? item.delivered : 'Zatím nedoručeno'}}</td>
    <td>{{item.price}}</td>
    <td v-if="item.state.title === 'Vytvořena'"><button v-on:click="payOrder" class="btn btn-success btn-sm">Zaplatit</button></td>
    <td v-else-if="item.state.title === 'Zrušena zákazníkem' || item.state.title === 'Zamítnuta'"><button disabled="disabled" class="btn btn-block btn-sm">Nelze zaplatit</button></td>
    <td v-else><button disabled="disabled" class="btn btn-block btn-sm">Zaplaceno</button></td>

    <td v-if="item.state.title === 'Vytvořena' || item.state.title === 'Zaplacena'"><button v-on:click="showEditForm(item.id)" class="btn btn-warning btn-sm">Upravit</button></td>
    <td v-else><button disabled="disabled" class="btn btn-block btn-sm">Nelze upravit</button></td>

    <td v-if="item.state.title === 'Vytvořena' || item.state.title === 'Zaplacena'"><button v-on:click="cancelOrder" class="btn btn-danger btn-sm">Zrušit</button></td>
    <td v-else-if="item.state.title === 'Zrušena zákazníkem' || item.state.title === 'Zamítnuta'"><button disabled="disabled" class="btn btn-block btn-sm">Zrušena</button></td>
    <td v-else><button disabled="disabled" class="btn btn-block btn-sm">Nelze již zrušit</button></td>
  </tr>
</template>


<style scoped>

</style>

<script>
import $ from "jquery";

export default {
  props: ['item'],
  data() {
    return {
      perms: [],
      order_products: [],
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    this.fetchData();
  },
  methods: {
    cancelOrder: function () {
      if (confirm("Opravdu chcete zrušit svoji objednávku?")) {
        this.$http.get('my_orders_cancel/' + this.item.id)
            .then((res) => {
              this.$props.item.state = res.data;
            })
            .catch(error => {
              console.log(error);
            });
      }
    },

    payOrder: function () {
      if (confirm("Potvrzujete zaplacení objednávky ve výši " + this.item.price + " Kč?")) {
        this.$http.get('my_orders_pay/' + this.item.id)
            .then((res) => {
              this.$props.item.state = res.data;
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
