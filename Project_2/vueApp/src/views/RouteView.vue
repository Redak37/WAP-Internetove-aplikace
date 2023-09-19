<template>
  <AppView>
    <RoutePlan mode="view" />
  </AppView>
</template>

<script>

import AppView from '../components/AppView.vue';
import RoutePlan from '../components/RoutePlan.vue';

export default {
  name: 'RouteView',
  components: {AppView, RoutePlan},
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.view_route')) {
      this.$router.push('/')
    }
  },
};
</script>
