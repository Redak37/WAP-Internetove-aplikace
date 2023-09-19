<template>
  <AppView>
    <h1>Seznam uživatelů</h1>
    <button v-if="perms.includes('auth.add_user')" v-on:click="show_create_form" class="btn btn-primary btn-sm" style="margin-bottom: 0.2em">Přidat uživatele</button>

    <table class="table table-striped table-hover table-responsive table-light">
      <thead>
        <tr><th>Uživatelské jméno</th><th>Email</th><th>Jméno</th><th>Příjmení</th><th>Stav</th></tr>
      </thead>
      <tbody>
        <UserItem v-for="item in itemList" v-bind:item="item" v-bind:key="item.id" :data-id="item.id"></UserItem>
      </tbody>
    </table>
    <div class="modal fade" id="modal-create">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Přidat uživatele</h1>
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
            <h1>Změna profilu</h1>
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
import UserItem from '../components/UserItem.vue';
import $ from "jquery";

export default {
  name: 'UserList',
  components: {AppView, UserItem},
  data() {
    return {
      itemList: [],
      perms: [],
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('auth.view_user')) {
      this.$router.push('/')
    }
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$http.get('users', {params: {format: 'json'}})
          .then((res) => {
            this.itemList = res.data;
          })
          .catch(error => {
            console.log(error);
          });
    },

    async show_create_form() {
      await this.$http.get('user_create_view')
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
      await this.$http.post('user_create_view', formElement)
          .then(() => {
            document.getElementById("form-create").innerHTML = 'Uživatel Přidán';
            document.getElementById("create-footer").style.display = "none";
            this.fetchData();
          })
          .catch(error => {
            document.getElementById("form-create").innerHTML = error.response.data['form'];
          });
    },

    async object_edit() {
      const formElement = new FormData(document.querySelector("#form-edit"));
      await this.$http.post('user_view/' + localStorage.edit_item_id, formElement)
          .then(() => {
            document.getElementById("form-edit").innerHTML = 'Profil upraven';
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
