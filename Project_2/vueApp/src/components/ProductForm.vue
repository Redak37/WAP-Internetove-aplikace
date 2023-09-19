<template>
  <FormulateForm v-on:submit="submitForm" v-bind:form-errors="errors" v-model="formValues">
    <h1 v-if="mode === 'create'">Přidat produkt</h1>
    <h1 v-if="mode === 'edit'">Upravit produkt #{{id}}</h1>
    <FormulateInput
      type="text"
      name="title"
      label="Titulek"
    />
    <FormulateInput
      type="select"
      name="category"
      label="Kategorie"
      v-bind:options="categories"
    />
    <FormulateInput
      type="number"
      name="price"
      min="0"
      step="0.01"
      label="Cena (Kč)"
    />
    <FormulateInput
      type="number"
      name="weight"
      min="0"
      step="0.01"
      label="Váha (g)"
    />
    <FormulateInput
      type="textarea"
      name="description"
      label="Popis"
    />
    <FormulateInput
      type="group"
      name="resources"
      :repeatable="true"
      label="Suroviny"
      add-label="Přidat další surovinu"
      remove-label="Odstranit"
      >
      <div class="resource">
        <FormulateInput
          type="select"
          name="resource"
          label="Surovina"
          v-bind:options="resources"
        />
        <FormulateInput
          type="number"
          name="weight"
          min="0"
          step="0.01"
          label="Váha (g)"
        />
      </div>
    </FormulateInput>
    <br>
    <FormulateInput
      type="submit"
      label="Potvrdit"
      input-class="btn btn-primary"
    />
  </FormulateForm>
</template>

<style scoped>
.resource {
  margin: 5px;
  padding: 5px;
  border: 1px solid #ddd;
}
</style>

<script>
export default {
  props: ['mode', 'id'],
  data() {
    return {
      categories: [],
      resources: [],
      errors: [],
      formValues: {}
    };
  },
  async created() {
    await this.fetchCategories();
    await this.fetchResources();
    if (this.mode === 'edit')
      await this.fetchProduct();
  },
  methods: {
    async fetchCategories() {
      const r = await this.$http.get('productcategories');
      this.categories = r.data.categories.map(item => {
        return {label: item.title, value: item.id};
      });
    },
    async fetchResources() {
      const r = await this.$http.get('resources');
      this.resources = r.data.map(res => {
        return {label: res.title, value: res.id};
      });
    },
    async submitForm(data) {
      if (this.mode === 'create') {
        await this.$http.post('product/add', data)
            .then((response) => {
              this.$router.push(`/ProductView/${response.data.id}`);
            })
            .catch(error => {
              console.log('error');
              this.errors = [error.response.data.errorMessage];
            });
      } else if (this.mode === 'edit') {
        await this.$http.post(`product/${this.id}/edit`, data)
            .then(() => {
              this.$router.push(`/ProductView/${this.id}`);
            })
            .catch(error => {
              console.log('error');
              this.errors = [error.response.data.errorMessage];
            });
      }
    },
    async fetchProduct() {
      await this.$http.get(`product/${this.id}/view`)
          .then((response) => {
            const data = response.data;
            data.category = data.category.id;
            data.resources = data.resources.map(res => {
              return {resource: res.resource.id, weight: res.weight};
            });
            this.formValues = response.data;
          })
          .catch(error => {
            console.log('error');
            this.errors = [error.response.data.errorMessage];
          });
    },
  },
};
</script>
