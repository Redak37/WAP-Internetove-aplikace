<template>
  <AppView>
    <h1>Plán výroby</h1>
    <form>
      <table>
        <tr>
          <td><label for="date">Zobrazit pro den:</label></td>
          <td><input class="form-control" type="date" id="date" v-model="date"></td>
          <td><button class="btn btn-primary" v-on:click="fetchData()">Zobrazit plán</button></td>
        </tr>
      </table>
    </form>
    <div v-if="perms.includes('pekarnaApp.view_order') && (!!newOrderList || newOrderList.length === 0)">
      <h3>Nové objednávky k potvrzení</h3>
      <table class="table-striped table-hover table-bordered table-sm">
        <thead>
          <tr><th>Položky</th><th>Potřebné suroviny</th><th>Poznámky</th></tr>
        </thead>
        <tbody>
          <PlanOrderItem v-on:eventOrderAccepted="fetchData" v-for="order in newOrderList" v-bind:item="order" v-bind:key="order.id"
                         :data-id="order.id" :order_resources="resourcesPerOrder[order.id]" :order_acceptable="newOrdersAcceptable[order.id]"></PlanOrderItem>
        </tbody>
      </table>
      <br>
    </div>
    <br>
    <h3>Objednávky ke zpracování</h3>
    <table class="table-striped table-hover table-bordered table-sm" v-if="perms.includes('pekarnaApp.view_order')">
      <thead>
        <tr><th>Položky</th><th>Potřebné suroviny</th><th>Poznámky</th></tr>
      </thead>
      <tbody>
        <PlanOrderItem v-on:eventOrderAccepted="fetchData" v-for="order in orderList" v-bind:item="order" v-bind:key="order.id"
                       :data-id="order.id" :order_resources="resourcesPerOrder[order.id]" :order_acceptable="true"></PlanOrderItem>
      </tbody>
    </table>
    <br>
    <h3>Souhrn surovin pro potvrzené objednávky</h3>
    <table class="table-striped table-hover table-bordered table-sm" v-if="perms.includes('pekarnaApp.view_order')">
      <thead>
        <tr><th>Surovina</th><th>Množství (g)</th></tr>
      </thead>
      <tbody>
        <tr v-for="resourcePair in resourcesList" :key="resourcePair.id">
          <td>{{resourcePair[0].title}}</td>
          <td>{{resourcePair[1]}}</td>
        </tr>
      </tbody>
    </table>
  </AppView>
</template>

<script>
import AppView from '../components/AppView.vue';
import PlanOrderItem from "../components/PlanOrderItem";
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'ProductionPlan',
  components: {AppView, PlanOrderItem},
  data() {
    return {
      orderList: [],
      newOrderList: [],
      resourcesList: [],
      resourcesPerOrder: {},
      newOrdersAcceptable: {},
      perms: [],
      date: this.getToday()
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('pekarnaApp.view_cookplan')) {
      this.$router.push('/')
    }
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$http.get('orders_plan/' + this.date, {params: {format: 'json'}})
          .then((res) => {
            this.orderList = res.data.orders;
            this.newOrderList = res.data.newOrders;
            this.resourcesList = res.data.resources;
            this.resourcesPerOrder = res.data.resourcesPerOrder;
            this.newOrdersAcceptable = res.data.newOrdersAcceptable;
          })
          .catch(error => {
            console.log(error);
          });
    },

    getToday() {
      const today = new Date();
      return today.getFullYear() + '-' + (today.getMonth() + 1).toLocaleString('en-US', {
            minimumIntegerDigits: 2,
            useGrouping: false
          })
          + '-' + today.getDate().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
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
