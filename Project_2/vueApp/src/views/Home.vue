<template>
  <AppView>

    <h1>Vítejte v pekarnaIS, {{displayName}}</h1>
    <p>Dnes je <b>{{date}}</b> a svátek má <b>{{nameDay}}</b>.</p>
  </AppView>
</template>

<script>

import AppView from '../components/AppView.vue';
import axios from 'axios';

export default {
  name: 'Home',
  components: {AppView},
  async created() {
    const today = new Date();
    this.date =
        today.getDate().toString()
        + '. ' + (today.getMonth() + 1).toString()
        + '. ' + today.getFullYear();

    let r = await axios.get('https://svatky.adresa.info/json');
    this.nameDay = r.data[0].name;
    await this.fetchData();
  },
  data() {
    return {
      date: '',
      nameDay: '',
      displayName: ''
    };
  },
  methods: {
    async logout() {
      await this.$http.post('logout');
      localStorage.isAuthenticated = 'no';
      await this.$router.push('/login');
    },
    async fetchData() {
      const user = JSON.parse(localStorage.user);
      if (user.first_name && user.last_name)
        this.displayName = `${user.first_name} ${user.last_name} (${user.username})`
      else
        this.displayName = user.username;

    },
  },
};
</script>
