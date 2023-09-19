<template>
  <tr>
    <td>{{item.username}}</td>
    <td>{{item.email}}</td>
    <td>{{item.first_name}}</td>
    <td>{{item.last_name}}</td>
    <td>{{isActive(item.is_active)}}</td>
    <td v-if="perms.includes('auth.change_user')"><button v-on:click="showEditForm(item.id)" class="btn btn-warning btn-sm">Edit</button></td>
    <td v-if="perms.includes('auth.change_user')"><button v-on:click="deleteItem" class="btn btn-danger btn-sm">Delete</button></td>
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
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
  },
  methods: {
    deleteItem: function () {
      if (confirm("Opravdu chcete uživatele smazat?")) {
        this.$http.delete('user_view/' + this.item.id)
            .then(() => {
              this.$destroy();
              this.$el.parentNode.removeChild(this.$el);
            })
            .catch(error => {
              console.log(error);
            });
      }
    },
    isActive: function (state) {
      return state ? 'aktivní' : 'neaktivní';
    },

    async showEditForm(object_id) {
      localStorage.edit_item_id = object_id;
      await this.$http.get('user_view/' + object_id)
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
