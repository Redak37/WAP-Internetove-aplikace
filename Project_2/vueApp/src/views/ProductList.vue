<template>
  <AppView>
    <h1 v-if="this.$route.params.category===undefined">Seznam produktů</h1>
    <h1 v-else>Seznam produktů - {{this.$route.params.category}}</h1>
    <router-link v-if="perms.includes('pekarnaApp.add_product')" to="/ProductAdd"  class="btn btn-primary btn-sm" style="margin-bottom: 0.2em">Přidat produkt</router-link>
    <div class="modal fade" id="modal-create">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Dokončit objednávku</h1>
          </div>
          <form>
          <div class="modal-body">

              <table width="450">
                <tr>
                  <th><label for="address" id="address-label">Dodací adresa:</label></th><td><input class="form-control" type="text" id="address" v-model="address"> </td>
                </tr>
                <tr>
                  <th><label for="notes">Poznámka:</label></th><td><textarea class="form-control" type="text" id="notes" v-model="notes"></textarea> </td>
                </tr>
                <tr>
                  <th><label for="deliver_date" id="deliver_date-label">Datum doručení:</label></th><td><input class="form-control" type="date" id="deliver_date" v-model="deliver_date"></td>
                </tr>
              </table>

          </div>
          <div class="modal-footer" id="create-footer">
            <button class="btn btn-primary" v-on:click="orderCreate()">Dokončit</button>
          </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal fade" id="modal-allergens">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Alergeny</h1>
          </div>
          <form>
            <div class="modal-body" id="allergens-body">

              <ul v-if="allergens.length > 0">
                <li v-bind:key="allergen.id" v-for="allergen in allergens">{{allergen.title}}</li>
              </ul>
              <i v-else>Produkt nemá žádné alergeny.</i>

            </div>
            <div class="modal-footer" id="allergens-footer">
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal fade" id="modal-alert">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Dokončit objednávku</h1>
          </div>
          <form>
            <div class="modal-body">
            Nejdříve prosím vyberte nějaké zboží.
            </div>
            <div class="modal-footer" id="alert-footer">
            </div>
          </form>
        </div>
      </div>
    </div>
    <table class="table-striped table-hover table-bordered">
      <thead>
      <tr><th>Název</th><th>Kategorie</th><th v-if="perms.includes('pekarnaApp.add_order')">Množství</th><th>Cena/ kus</th><th>Celková cena</th></tr>
      </thead>
      <tbody>
        <ProductItem v-on:stock="updateSummary" v-on:allergens="showAllergens" v-for="item in itemList" v-bind:item="item" v-bind:stock="item.stock" v-bind:product_id="item.product_id" v-bind:key="item.id"></ProductItem>
      </tbody>
    </table>
    <h2 v-if="perms.includes('pekarnaApp.add_order')">Shrnutí</h2>
    <table v-if="perms.includes('pekarnaApp.add_order')">
      <tr>
        <th>Celková cena: </th><td>{{priceSum}} Kč</td>
      </tr>
      <tr>
        <td></td>
        <td><button class="btn btn-success" @click="next">Pokračovat v objednávce</button></td>
      </tr>
    </table>

  </AppView>
</template>
<script>
import AppView from '../components/AppView.vue';
import ProductItem from '../components/ProductItem.vue';
import $ from 'jquery'
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'ProductList',
  components: {AppView, ProductItem},
  props: ['priceSum'],
  data() {
    return {
      perms: [],
      itemList: [],
      notes: '',
      address: '',
      deliver_date: this.getToday(),
      allergens: [],
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    this.fetchData();
  },
  mounted() {
    const addressInput = document.getElementById('address');
    const suggest = new window.SMap.Suggest(addressInput, {
      provider: new window.SMap.SuggestProvider({
        updateParams: params => {
          params.enableCategories = 1;
          params.type = "municipality|street|address";
          params.bounds = "48.5370786,12.0921668|51.0746358,18.8927040";
          //params.type = 'address|street|municipality';
        },
      }),
      dataParams: (data, requestItem) => {
        console.log(data, requestItem);
        const ud = requestItem.userData;
        data.address = `${ud.suggestFirstRow}, ${ud.zipCode} ${ud.municipality}`;
      }
    });
    suggest.addListener("suggest", (suggestData) => {
      if (suggestData.data.source == 'addr')
        this.address = suggestData.data.address;
      console.log(suggestData);
      console.log(suggestData.data.address);
    });
  },
  watch: {
    $route() {
      this.fetchData();
    }
  },
  methods: {
    next: function () {
      if (this.priceSum < 1) {
        $("#modal-alert").modal('show');
      } else {
        $("#modal-create").modal('show');
      }

    },

    getToday() {
      const today = new Date();
      return today.getFullYear() + '-' + (today.getMonth() + 1).toLocaleString('en-US', {
            minimumIntegerDigits: 2,
            useGrouping: false
          })
          + '-' + today.getDate().toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping: false});
    },

    orderCreate: function () {

      if (this.deliver_date === null || this.deliver_date === "") {
        $("#address-label").css("color", "red");
        return;
      }

      if (this.address === null || this.address === "") {
        $("#deliver_date-label").css("color", "red");
        return;
      }

      this.$http
          .post('/orders', {
            'price': this.priceSum,
            'address': this.address,
            'notes': this.notes,
            "deliver_date": this.deliver_date,
          }).then(response => {

            let order_id = response.data.id;
            let send_data = [];

            for (let i = 0; i < this.itemList.length; i++) {

              if (this.itemList[i].stock > 0) {
                send_data.push({
                  "order": order_id,
                  "product": this.itemList[i].id,
                  "quantity": this.itemList[i].stock,
                });
              }
            }
            $("#modal-create").modal('hide');
            this.$http
                .post('/product_order', send_data).then(
                () =>
                    this.$router.push('/MyOrders')
            )
          }
      )

    },
    updateSummary: function (item) {
      let sum = 0;
      for (let i = 0; i < this.itemList.length; i++) {
        if (this.itemList[i].id === item.id) {
          this.itemList[i].stock = item.stock;
        }
        sum += (this.itemList[i].price * this.itemList[i].stock);
      }

      this.priceSum = "" + sum.toFixed(2);

    },
    async fetchData() {
      const route = this.$route.params.category === undefined ? '/products' : '/products/' + this.$route.params.category;
      await this.$http.get(route, {params: {format: 'json'}})
          .then((res) => {
            this.itemList = res.data;
            for (let i = 0; i < this.itemList.length; i++) {
              this.itemList[i].stock = 0;
            }
          })
          .catch(error => {
            console.log(error);
          });
    },
    showAllergens(id) {
      $("#modal-allergens").modal("show");
      this.$http.get("/product/" + id + "/allergens", {params: {format: 'json'}})
          .then(response => {
            this.allergens = response.data;
          })
    },
  },
};
</script>
