<template>
  <AppView>
    <h1>Moje objednávky</h1>
    <table class="table-striped table-hover table-bordered table-sm" v-if="perms.includes('pekarnaApp.add_order')">
      <thead>
        <tr><th>Položky</th><th>Stav</th><th>Doručovací adresa</th><th>Doručit dne</th><th>Poznámky</th><th>Doručeno kdy</th><th>Celková cena</th></tr>
      </thead>
      <tbody>
        <OrderItem v-for="order in orderList" v-bind:item="order" v-bind:key="order.id" :data-id="order.id"></OrderItem>
      </tbody>
    </table>

    <div class="modal fade" id="modal-edit">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Úprava objednávky</h1>
          </div>
          <div class="modal-body">
            <form id="form-edit">
            </form>
          </div>
          <div class="modal-footer" id="edit-footer">
            <button class="btn btn-primary" v-on:click="object_edit">Změnit</button>
          </div>
        </div>
      </div>
    </div>
  </AppView>
</template>


<script>
import AppView from '../components/AppView.vue';
import OrderItem from "../components/OrderItem";
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'MyOrders',
  components: {AppView, OrderItem},
  data() {
    return {
      orderList: [],
      perms: [],
      user: null
    };
  },
  created() {
    this.user = JSON.parse(localStorage.user);
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('pekarnaApp.add_order')) {
      this.$router.push('/')
    }
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$http.get('my_orders/' + this.user.id, {params: {format: 'json'}})
          .then((res) => {
            this.orderList = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async object_edit() {
      const formElement = new FormData(document.querySelector("#form-edit"));
      await this.$http.post('my_orders_view/' + localStorage.edit_item_id, formElement)
          .then(() => {
            document.getElementById("form-edit").innerHTML = 'Objednávka upravena';
            document.getElementById("edit-footer").style.display = "none";
            this.fetchData();
          })
          .catch(error => {
            document.getElementById("form").innerHTML = error.response.data['form'];
          });
    },
  },
};
</script>
