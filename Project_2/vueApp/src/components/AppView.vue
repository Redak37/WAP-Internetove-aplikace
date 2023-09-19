<template>
<div class="app-view">
  <header class="main-header">
    <router-link to="/">
      <img src="../assets/bread.png" alt="bread">
      <span>pekarnaIS</span>
    </router-link>
    <button v-on:click="logout" class="btn btn-warning btn-sm">Odhlásit</button>
    <span id="user-txt" >Přihlášen: <strong>{{user.username}}</strong></span>
  </header>
  <div class="flex-container">
    <nav class="side-nav">
      <ul>
        <li v-if="perms.includes('pekarnaApp.view_product')"><router-link to="/ProductList">Produkty</router-link></li>
        <li v-if="perms.includes('pekarnaApp.add_order')"><router-link to="/MyOrders">Moje objednávky</router-link></li>
        <li v-if="perms.includes('pekarnaApp.view_resource')"><router-link to="/ResourceList">Suroviny</router-link></li>
        <li v-if="perms.includes('pekarnaApp.view_car')"><router-link to="/CarList">Auta</router-link></li>
        <li v-if="perms.includes('auth.view_user')"><router-link to="/UserList">Uživatelé</router-link></li>
        <li v-if="perms.includes('pekarnaApp.view_order')"><router-link to="/OrderList">Všechny objednávky</router-link></li>
        <li v-if="perms.includes('pekarnaApp.view_cookplan')"><router-link to="/ProductionPlan">Plán výroby</router-link></li>
        <li v-if="perms.includes('pekarnaApp.view_route')"><router-link to="/routes">Trasy</router-link></li>
      </ul>
    </nav>
    <main class="main-content">
      <slot></slot>
    </main>
  </div>
</div>
</template>

<script>
export default {
  data() {
    return {
      user: "",
      perms: [],
    };
  },
  async created() {
    if (localStorage.isAuthenticated === 'yes' && localStorage.user === '' && localStorage.perms === '') {
      await this.fetchData();
    } else {
      this.user = JSON.parse(localStorage.user);
      this.perms = JSON.parse(localStorage.perms);
    }
  },
  methods: {
    async logout() {
      await this.$http.post('logout');
      localStorage.isAuthenticated = 'no';
      localStorage.user = '';
      localStorage.perms = '';
      await this.$router.push('/login');
    },
    async fetchData() {
      await this.$http.get('getUser', {params: {format: 'json'}})
          .then((res) => {
            this.user = res.data;
            localStorage.user = JSON.stringify(res.data);
          })
          .catch(error => {
            console.log(error);
          });

      await this.$http.get('getPerms', {params: {format: 'json'}})
          .then((res) => {
            this.perms = res.data;
            localStorage.perms = JSON.stringify(res.data);
          })
          .catch(error => {
            console.log(error);
          });
    },
  },
};
</script>

<style scoped>
.app-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main-header {
  height: 60px;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  vertical-align: center;
  border-bottom: 1px solid #ddd;
  background: #f0f0f0;
  position: relative;
}
.main-header a {
  color: black!important;
  text-decoration: none!important;
  font-size: 22pt;
}
.main-header span {
  top: -10px;
  left: 10px;
  position: relative;
}
.main-header img {
  height: 40px;
}
.main-header button {
  right: 14px;
  top: 14px;
  position: absolute;
}
#user-txt {
  left: unset;
  top: 17px;
  right: 120px;
  position: absolute;
}
.flex-container {
  flex: 1;
  display: flex;
}
.side-nav {
  width: 300px;
  background: #f0f0f0;
  border-right: 1px solid #ddd;
}
.side-nav ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}
.side-nav a {
  border-bottom: 1px solid #ddd;
  font-size: 14pt;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 20px;
  display: block;
  text-decoration: none!important;
  color: black!important;
}
.side-nav a:hover {
  text-decoration: none!important;
  background: #ddd;
}
.side-nav .router-link-active {
  border-left: 5px solid var(--primary);
  background: #ddd;
}
.main-content {
  flex: 1;
  padding: 20px;
  background: #fdfdfd;
}
</style>
