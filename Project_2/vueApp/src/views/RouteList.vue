<template>
  <AppView>
  <h1>Naplánované trasy</h1>
  <router-link to="/routes/new">Naplánovat novou trasu</router-link><br>
  <label>Trasy dne:&nbsp;</label><input type="date" v-model="date" v-on:change="loadRoutes" /><br>
  <label>Zobrazit vše:&nbsp;</label><input type="checkbox" v-model="showAll" v-on:change="loadRoutes" /><br>

  <table class="table table-hover table-responsive table-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Řidič</th>
        <th>Datum</th>
        <th>Počet zastávek</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="route in routes" v-bind:key="route.id" v-on:click="$router.push(`routes/${route.id}`)">
        <td>{{route.id}}</td>
        <td>{{route.driver.username}}</td>
        <td>{{route.date}}</td>
        <td>{{route.orders.length}}</td>
      </tr>
    </tbody>
  </table>
  </AppView>
</template>

<script>

import AppView from '../components/AppView.vue';

export default {
  name: 'RouteList',
  components: {AppView},
  created() {
    this.perms = JSON.parse(localStorage.perms);
    if (!this.perms.includes('pekarnaApp.view_route')) {
      this.$router.push('/')
    }
    const today = new Date();
    this.date = today.getFullYear()
        + '-' + (today.getMonth() + 1).toString().padStart(2, '0')
        + '-' + today.getDate().toString().padStart(2, '0');
    this.loadRoutes();
  },
  data() {
    return {
      perms: [],
      routes: [],
      date: null,
      showAll: false
    };
  },
  methods: {
    async loadRoutes() {
      const r = await this.$http.get('routes');
      this.routes = r.data.filter(r => {
        return this.showAll || this.date === r.date.split(' ')[0];
      });
    },
  },
};
</script>

<style scoped>
tr {
  cursor: pointer;
}
</style>
