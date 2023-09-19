<template>
  <AppView>
    <RoutePlan mode="edit" />
  </AppView>
</template>

<script>

import AppView from '../components/AppView.vue';
import RoutePlan from '../components/RoutePlan.vue';

export default {
  name: 'RouteEdit',
  components: {AppView, RoutePlan},
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.change_route')) {
      this.$router.push('/')
    }
  },
};
</script>
