<template>
  <tr>
    <td>{{item.resource.title}}</td>
    <td>{{item.weight/1000}} kg</td>
  </tr>
</template>

<script>

export default {
  props: ['item'],
};
</script>
