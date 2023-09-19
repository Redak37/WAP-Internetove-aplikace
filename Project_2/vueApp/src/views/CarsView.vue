<template>
  <AppView>
    <h1>Seznam aut</h1>

    <button class="btn btn-primary btn-sm" v-on:click="show_create_form" v-if="perms.includes('pekarnaApp.add_car')" style="margin-bottom: 0.2em">Přidat auto</button>

    <table class="table table-striped table-hover table-responsive table-light " v-if="perms.includes('pekarnaApp.view_car')">
      <thead>
        <tr><th>Název</th><th>SPZ</th><th>Kapacita</th><th>Řidič</th></tr>
      </thead>
      <tbody>
        <CarItem v-for="item in itemList" v-bind:item="item" v-bind:key="item.id" :data-id="item.id"></CarItem>
      </tbody>
    </table>
    <div class="modal fade" id="modal-create">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Přidat auto</h1>
          </div>
          <div class="modal-body">
            <form id="form-create">
            </form>
          </div>
          <div class="modal-footer" id="create-footer">
            <button class="btn btn-primary" v-on:click="object_create">Přidat</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="modal-edit">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Změna auta</h1>
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
import CarItem from "@/components/CarItem";
import $ from 'jquery'
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'CarList',
  components: {AppView, CarItem},
  data() {
    return {
      itemList: [],
      perms: [],
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('pekarnaApp.view_car')) {
      this.$router.push('/')
    }
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$http.get('cars', {params: {format: 'json'}})
          .then((res) => {
            this.itemList = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async show_create_form() {
      await this.$http.get('cars_view')
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
      await this.$http.post('cars_view', formElement)
          .then(() => {
            document.getElementById("form-create").innerHTML = 'Auto Přidáno';
            document.getElementById("create-footer").style.display = "none";
            this.fetchData();
          })
          .catch(error => {
            document.getElementById("form-create").innerHTML = error.response.data['form'];
          });
    },

    async object_edit() {
      const formElement = new FormData(document.querySelector("#form-edit"));
      await this.$http.post('cars_view/' + localStorage.edit_item_id, formElement)
          .then(() => {
            document.getElementById("form-edit").innerHTML = 'Auto změněno';
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
