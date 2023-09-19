<template>
  <div>
    <div class="login">
      <h1>Přihlášení</h1>
      <form v-on:submit.prevent="login" method="post">
        <div class="error" v-if="error">{{ error }}</div>
        <label for="username">Přihlašovací jméno:</label><br>
        <input type="text" id="username" v-model="form.username" /><br><br>
        <label for="password">Heslo:</label><br>
        <input type="password" id="password" v-model="form.password" /><br><br>
        <button type="submit" class="btn btn-primary">Přihlásit</button>
      </form>
      <a class="navbar-link" v-on:click="register_show">Nemáte ještě účet? (registrovat)</a>
    </div>
    <div class="modal fade" id="modal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1>Registrace</h1>
          </div>
          <div class="modal-body">
            <form id="form">
            </form>
          </div>
          <div class="modal-footer" id="modal-footer">
            <button class="btn btn-primary" v-on:click="register">Registrovat</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login {
  text-align: center;
}
.error {
  color: red;
  font-weight: bold;
}
</style>

<script>
import $ from 'jquery'
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: ''
    };
  },
  methods: {
    async login() {
      await this.$http.get('csrf');
      await this.$http.post('login', this.form)
          .then(async () => {
            localStorage.isAuthenticated = 'yes';
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

            await this.$router.push('/');
          })
          .catch(error => {
            this.error = error.response.data.errorMessage;
          });
    },

    async register_show() {
      await this.$http.get('register')
          .then((res) => {
            document.getElementById('form').innerHTML = res.data['form'];
            document.getElementById('modal-footer').style.display = '';
            $("#modal").modal('show');
          })
          .catch(error => {
            console.log(error);
          });
    },

    async register() {
      const formElement = new FormData(document.querySelector("#form"));
      await this.$http.post('register', formElement)
          .then(() => {
            document.getElementById('form').innerHTML = 'Registrace úspěšná!';
            document.getElementById('modal-footer').style.display = 'none';
          })
          .catch(error => {
            document.getElementById('form').innerHTML = error.response.data['form'];
          });
    },
  },
};
</script>