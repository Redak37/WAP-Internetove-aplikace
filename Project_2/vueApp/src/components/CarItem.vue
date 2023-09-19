<template>
  <tr>
    <td>{{item.title}}</td>
    <td>{{item.spz}}</td>
    <td>{{item.capacity}}</td>
    <td>{{item.driver.first_name}}  {{item.driver.last_name}} ({{item.driver.username}})</td>
    <td v-if="perms.includes('pekarnaApp.change_car')"><button v-on:click="showEditForm(item.id)" class="btn btn-warning btn-sm">Edit</button></td>
    <td v-if="perms.includes('pekarnaApp.delete_car')"><button v-on:click="deleteItem" class="btn btn-danger btn-sm">Delete</button></td>
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
      if (confirm("Opravdu chcete položku smazat?")) {
        this.$http.delete('cars_view/' + this.item.id)
            .then(() => {
              this.$destroy();
              this.$el.parentNode.removeChild(this.$el);
            })
            .catch(error => {
              console.log(error);
            });
      }
    },

    async showEditForm(object_id) {
      localStorage.edit_item_id = object_id;
      await this.$http.get('cars_view/' + object_id)
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
