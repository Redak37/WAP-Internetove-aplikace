<template>
  <AppView>
    <RoutePlan mode="create" />
  </AppView>
</template>

<script>

import AppView from '../components/AppView.vue';
import RoutePlan from '../components/RoutePlan.vue';

export default {
  name: 'RouteAdd',
  components: {AppView, RoutePlan},
  created() {
    const perms = JSON.parse(localStorage.perms);
    if (!perms.includes('pekarnaApp.add_route')) {
      this.$router.push('/')
    }
  },
};
</script>
