<template>
  <AppView>
    <h1>Objednávka surovin</h1>
    <button v-if="perms.includes('pekarnaApp.add_resource')" v-on:click="show_create_form" class="btn btn-primary btn-sm" style="margin-bottom: 0.2em">Přidat surovinu</button>
    <form id="order_form">
      <div v-if="perms.includes('pekarnaApp.view_resource')">
        <table class="table-striped table-hover table-bordered table-sm">
          <thead>
            <tr>
              <th>Název</th>
              <th v-if="perms.includes('pekarnaApp.add_resourceorder')">Objednávka (kg)</th>
              <th>Na skladě</th>
              <th>Cena/kg</th>
              <th>Celková cena</th>
            </tr>
          </thead>
          <tbody>
              <ResourceItem v-on:recalculate="priceCalc" v-for="item in itemList" v-bind:item="item" v-bind:key="item.id" :data-id="item.id"/>
          </tbody>
        </table>
      </div>
      <div style="margin-top: 1em">
        <h2>Shrnutí objednávky</h2>
        <table>
          <tr>
            <th>Celková cena:</th><td id="price_summary">{{ priceSum }} Kč</td>
          </tr>
          <tr>
            <td></td>
            <td><button class="btn btn-primary btn-sm" v-on:click.prevent="order">Vytvořit objednávku</button></td>
          </tr>
        </table>
      </div>
    </form>
    <div style="margin-top: 1em" v-if="perms.includes('pekarnaApp.view_resourceorder')">
      <h1>Stav aktuálních objednávek</h1>
      <table class="table-striped table-hover table-bordered table-sm">
        <thead>
          <tr>
            <th>Zadavatel</th>
            <th>Datum</th>
            <th>Cena</th>
            <th>Stav</th>
          </tr>
        </thead>
        <tbody>
            <ResourceOrderItem v-on:resDeliver="fetchData" v-on:detail="resource_detail" v-for="item in orderList" v-bind:item="item" v-bind:key="item.id" :data-id="item.id"/>
        </tbody>
      </table>
    </div>

    <div style="margin-top: 1em" v-if="perms.includes('pekarnaApp.view_resourceorder')">
      <button v-if="!showHistory" class="btn btn-primary" v-on:click="show_history">Zobrazit historii objednávek</button>
      <div v-if="showHistory">
        <h1>Historie objednávek</h1>
        <table class="table-striped table-hover table-bordered table-sm">
          <thead>
            <tr>
              <th>Zadavatel</th>
              <th>Datum</th>
              <th>Cena</th>
              <th>Stav</th>
            </tr>
          </thead>
          <tbody>
              <ResourceOrderItem v-on:detail="resource_detail" v-for="item in historyList" v-bind:item="item" v-bind:key="item.id" :data-id="item.id"/>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="modal-create">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Přidat surovinu</h1>
          </div>
          <div class="modal-body">
            <form id="form-create">
            </form>
          </div>
          <div class="modal-footer" id="create-footer">
            <button class="btn btn-primary" v-on:click.prevent="object_create">Přidat</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modal-edit">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Úpravy suroviny</h1>
          </div>
          <div class="modal-body">
            <form id="form-edit">
            </form>
          </div>
          <div class="modal-footer" id="edit-footer">
            <button class="btn btn-primary" v-on:click.prevent="object_edit">Změnit</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modal-detail">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Detail objednávky</h1>
          </div>
          <div class="modal-body">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Surovina</th>
                  <th>Množství</th>
                </tr>
              </thead>
              <tbody>
                <ResourceDetail v-for="item in orderDetail" v-bind:item="item" v-bind:key="item.id"/>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
          </div>
        </div>
      </div>
    </div>

  </AppView>
</template>


<script>
import AppView from '../components/AppView';
import ResourceDetail from '../components/ResourceDetail';
import ResourceItem from '../components/ResourceItem';
import ResourceOrderItem from '../components/ResourceOrderItem';
import $ from "jquery";

export default {
  name: 'ResourceList',
  components: {ResourceDetail, AppView, ResourceItem, ResourceOrderItem},
  data() {
    return {
      itemList: [],
      orderList: [],
      historyList: [],
      perms: [],
      showHistory: false,
      orderDetail: [],
      priceSum: 0,
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('pekarnaApp.view_resource')) {
      this.$router.push('/');
      return;
    }
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.itemList = [];
      this.orderList = [];
      this.priceSum = 0;
      await this.$http.get('resources', {params: {format: 'json'}})
          .then((res) => {
            this.itemList = res.data;
          })
          .catch(error => {
            console.log(error);
          });
      await this.$http.get('resource_orders', {params: {format: 'json'}})
          .then((res) => {
            this.orderList = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async show_create_form() {
      await this.$http.get('resource_view')
          .then((res) => {
            document.getElementById("form-create").innerHTML = res.data['form'];
            document.getElementById("create-footer").style.display = "";
            $("#modal-create").modal('show');
          })
          .catch(error => {
            console.log(error);
          });
    },

    async object_create() {
      const formElement = new FormData(document.querySelector("#form-create"));
      await this.$http.post('resource_view', formElement)
          .then(() => {
            document.getElementById("form-create").innerHTML = 'Surovina Přidána';
            document.getElementById("create-footer").style.display = "none";
            this.fetchData();
          })
          .catch(error => {
            document.getElementById("form-create").innerHTML = error.response.data['form'];
          });
    },

    async object_edit() {
      const formElement = new FormData(document.querySelector("#form-edit"));
      await this.$http.post('resource_view/' + localStorage.edit_item_id, formElement)
          .then(() => {
            document.getElementById("form-edit").innerHTML = 'Surovina upravena';
            document.getElementById("edit-footer").style.display = "none";
            this.fetchData();
          })
          .catch(error => {
            document.getElementById("form").innerHTML = error.response.data['form'];
          });
    },

    async order() {
      const formElement = new FormData(document.querySelector("#order_form"));
      await this.$http.post('resource_order', formElement)
          .then(() => {
            this.fetchData();
          })
          .catch(error => {
            console.log(error);
            confirm("Nelze zaslat prázdnou objednávku");
          });
    },

    async show_history() {
      await this.$http.get('resource_orders_history', {params: {format: 'json'}})
          .then((res) => {
            this.historyList = res.data;
            this.showHistory = true;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async resource_detail(id) {
      await this.$http.get('resource_order/' + id, {params: {format: 'json'}})
          .then((res) => {
            this.orderDetail = res.data;
            $("#modal-detail").modal('show');
          })
          .catch(error => {
            console.log(error);
          });
    },

    async priceCalc() {
      this.priceSum = 0;
      for (let i = 0; i < this.itemList.length; i++) {
        let input = document.getElementById(this.itemList[i].id);
        if (input !== null)
          this.priceSum += input.value * this.itemList[i].price;
      }
    },
  },
};
</script>
