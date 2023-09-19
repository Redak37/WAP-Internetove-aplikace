<template>
  <tr>
    <td>{{item.title}}</td>
    <td v-if="perms.includes('pekarnaApp.add_resourceorder')" style="position: relative">
      <input v-on:change="$emit('recalculate')" :id=item.id :name="item.id" v-model="resOrder" type="number" min="0" class="form-control" style="position: absolute; top: 1px; left: 0; border: none; margin: 0; padding: 0; text-align: right">
    </td>
    <td style="text-align: right">{{item.stock/1000}} kg</td>
    <td style="text-align: right">{{item.price}},-</td>
    <td style="text-align: right">{{item.price * resOrder}},-</td>
    <td v-if="perms.includes('pekarnaApp.change_resource')"><button v-on:click.prevent="showEditForm(item.id)" class="btn btn-warning btn-sm">Upravit</button></td>
    <td v-if="perms.includes('pekarnaApp.delete_resource')"><button v-on:click.prevent="deleteItem" class="btn btn-danger btn-sm">Odstranit</button></td>
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
      resOrder: 0,
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
  },
  methods: {
    deleteItem: function () {
      if (confirm("Opravdu chcete položku smazat?")) {
        this.$http.delete('resource_view/' + this.item.id)
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
      await this.$http.get('resource_view/' + object_id)
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
