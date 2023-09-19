<template>
  <tr>
    <td v-on:click="orderDetail">{{item.user.first_name}} {{item.user.last_name}} ({{item.user.username}})</td>
    <td v-on:click="orderDetail">{{item.created}}</td>
    <td v-on:click="orderDetail" style="text-align: right">{{item.price}},-</td>
    <td v-on:click="orderDetail">{{item.state.title}}</td>
    <td v-if="perms.includes('pekarnaApp.change_resourceorder')&&(item.state.title==='nezpracováno'||item.state.title==='objednáno')">
      <button v-if="item.state.title==='nezpracováno'" v-on:click="confirmOrder" class="btn btn-warning btn-sm">Objednáno</button>
      <button v-if="item.state.title==='objednáno'" v-on:click="orderDelivered" class="btn btn-warning btn-sm">Přijato</button>
    </td>
    <td v-if="perms.includes('pekarnaApp.delete_resourceorder')&&item.state.title!=='zrušeno'&&item.state.title!=='přijato'">
      <button v-on:click="cancelOrder" class="btn btn-danger btn-sm">Zrušit</button>
    </td>
  </tr>
</template>

<script>

export default {
  props: ['item'],
  data() {
    return {
      perms: [],
      res_order: 0,
    };
  },
  created() {
    this.perms = JSON.parse(localStorage.perms);
  },
  methods: {
    orderDetail: function () {
      this.$emit('detail', this.item.id);
    },
    cancelOrder: function () {
      if (confirm("Opravdu chcete zrušit objednávku?")) {
        this.$http.put('resourceOrderChangeState/' + this.item.id + '/zrušeno')
            .then(() => {
              this.$destroy();
              this.$el.parentNode.removeChild(this.$el);
            })
            .catch(error => {
              console.log(error);
            });
      }
    },
    confirmOrder: function () {
      if (confirm("Byla objednávka zaslána?")) {
        this.$http.put('resourceOrderChangeState/' + this.item.id + '/objednáno')
            .then(() => {
              this.item.state.title = "objednáno";
            })
            .catch(error => {
              console.log(error);
            });
      }
    },
    orderDelivered: function () {
      if (confirm("Byla objednávka přijata?")) {
        this.$http.put('resourceOrderDelivered/' + this.item.id)
            .then(() => {
              this.$emit('resDeliver');
            })
            .catch(error => {
              console.log(error);
            });
      }
    },
  },
};
</script>
