<template>
  <AppView>
   <h1>Přehled objednávek</h1>
    <div class="modal fade" id="modal-state">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Změnit stav</h1>
          </div>
            <div class="modal-body" id="state-body">
            <form>
              <select v-model="stateP" class="form-control">
                <option  v-for="state in this.states" v-bind:key="state.id" :value="state.id">{{state.title}}</option>
              </select>
            </form>
            </div>
            <div class="modal-footer" id="state-footer">
              <button class="btn btn-primary" v-on:click="changeState">Změnit</button>
            </div>

        </div>
      </div>
    </div>
    <div class="modal fade" id="modal-products">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Produkty</h1>
          </div>
          <div class="modal-body" id="product-body">
           <table>
             <tr v-for="item in this.order_products" v-bind:key="item.id">
               <td>*</td>
               <td>{{item.product.title}}</td>
               <td>{{item.quantity}}x</td>
             </tr>
           </table>
          </div>
          <div class="modal-footer" id="product-footer">

          </div>

        </div>
      </div>
    </div>
    <form>
      <table>
        <tr>
          <th>
      Zobrazit:
          </th>
          <td>
      <select v-model="showingMode"  class="form-control" @change="showData">
        <option value="1" selected>Všechny objednávky</option>
        <option value="2">Doručení dnes</option>
        <option value="3">Doručení zítra</option>
      </select>
          </td>
        </tr>
      </table>
    </form>
    <table class="table table-striped table-hover table-responsive table-light">
      <thead>
      <tr>
        <th>Zákazník</th>
        <th>Adresa</th>
        <th>Cena</th>
        <th>Datum vytvoření</th>
        <th>Žádané datum doručení</th>
        <th>Doručeno</th>
        <th>Poznámky</th>
        <th>Stav</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in this.showingList" v-bind:key="item.id">
        <td>{{item.user.first_name}} {{item.user.last_name}}</td>
        <td>{{item.address}}</td>
        <td>{{item.price}} Kč</td>
        <td>{{item.created}}</td>
        <td>{{item.deliver_date}}</td>
        <td>{{item.delivered}}</td>
        <td>{{item.notes}}</td>
        <td><a href="#" @click="showState(item.state.id, item.id)" v-if="item.state != null">{{item.state.title}}</a></td>
        <td><button class="btn btn-dark" @click="showProducts(item.id)">Produkty</button></td>
      </tr>
      </tbody>
    </table>
  </AppView>
</template>

<script>
import AppView from "@/components/AppView";
import $ from "jquery";

export default {
  name: "OrderList",
  props: ['stateP', 'order_products'],
  components: {AppView},
  data() {
    return {
      showingList: [],
      itemList: [],
      states: [],
      orderEdit: 0,
      showingMode: 1,
    }
  },
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.view_order')) {
      this.$router.push('/')
    }
    this.fetchData();
    //   this.$props.showingMode = "1";
    this.showData();
  },
  methods: {
    async fetchData() {
      await this.$http.get('orders', {params: {format: 'json'}})
          .then((res) => {
            this.itemList = res.data;
            this.showingList = this.itemList;
          })
          .catch(error => {
            console.log(error);
          });
      await this.$http.get('states', {params: {format: 'json'}})
          .then((res) => {
            this.states = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },
    async changeState() {
      await this.$http.put('orders/' + this.orderEdit, {'state': this.stateP})
          .then(() => {
            $("#modal-state").modal('toggle');
            this.fetchData();
          })
    },
    showState: function (stateId, orderId) {
      this.orderEdit = orderId;
      this.$props.stateP = stateId;
      $("#modal-state").modal('show');
    },
    showData() {

      this.showingList = this.itemList;
      if (this.showingMode === "2") {
        let d = new Date();
        this.showingList = this.itemList.filter(item => item.deliver_date === d.toISOString().slice(0, 10));
      } else if (this.showingMode === "3") {
        let d = new Date();
        d.setDate(d.getDate() + 1);
        this.showingList = this.itemList.filter(item => item.deliver_date === d.toISOString().slice(0, 10));
      }
    },
    async showProducts(id) {
      this.$http.get('orders/' + id + '/products', {params: {format: 'json'}})
          .then((res) => {
            this.$props.order_products = res.data;
          })
          .catch(error => {
            console.log(error);
          });
      $("#modal-products").modal('show');
    },
  },
};
</script>
