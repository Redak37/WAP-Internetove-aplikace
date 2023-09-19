<template>
  <div>
    <div v-if="errorMessage !== ''" class="alert alert-danger" role="alert">
      {{errorMessage}}
    </div>

    <h1 v-if="mode === 'create'">Naplánovat trasu</h1>
    <h1 v-if="mode === 'view'">Zobrazení trasy #{{id}}</h1>
    <h1 v-if="mode === 'edit'">Upravit trasu #{{id}}</h1>
      <div>
        <label>Datum trasy:&nbsp;</label>
        <input v-if="mode !== 'view'" type="date" v-model="date" v-on:change="dateChanged" />
        <span v-if="mode === 'view'">{{route ? route.date.split(' ')[0] : ''}}</span>
      </div>

      <div>
        <label>Řidič:&nbsp;</label>
        <select v-model="driver" v-if="mode !== 'view'">
          <option disabled value="">Vyberte řidiče</option>
          <option v-for="driver in drivers" v-bind:key="driver.id" v-bind:value="driver.id">{{driver.username}}</option>
        </select>
        <span v-if="mode === 'view'">{{route ? route.driver.username : ''}}</span>
      </div>

      <div>
        <button v-if="mode !== 'view'" class="btn btn-primary" v-on:click="save">Uložit trasu</button>
        <button v-if="mode === 'view'" class="btn btn-primary" v-on:click="$router.push(`/routes/${id}/edit`)">Upravit trasu</button>
        <button v-if="mode !== 'create' && deleteOk" class="btn btn-danger" v-on:click="deleteRoute">Smazat trasu</button>
      </div>


    <div id="map"></div>
    <br>


    <div v-if="mode === 'view'">
      <h4>Příští zastávka</h4>
      <div v-if="goal">
        <strong>Jméno:</strong> {{`${goal.user.first_name} ${goal.user.last_name} ${goal.user.username}`}}<br>
        <strong>Adresa:</strong> {{goal.address}}<br>
        <strong>Poznámka:</strong> {{goal.notes}}<br>
        <strong>Cena:</strong> {{`${goal.price} Kč`}}<br>
      </div>
      <br>
      <h4>Aktuální trasa</h4>
      <table class="table table-sm">
        <thead>
          <tr>
            <th scope="col" style="width: 160px"></th>
            <th scope="col" style="width: 30px;">#</th>
            <th scope="col">Adresa doručení</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in this.routeOrders" v-bind:key="order.id" v-bind:class="goal === order ? 'table-warning' : (order.state.title === 'Doručena' ? 'table-success' : '')">
            <td v-if="order.state.title !== 'Na cestě' && order.state.title !== 'Doručena'">
              <button class="btn btn-primary" v-on:click="onRoute(order)">Na cestě</button>
            </td>
            <td v-if="order.state.title === 'Na cestě'">
              <button class="btn btn-success" v-on:click="delivered(order)">Doručena</button>
            </td>
            <td v-if="order.state.title === 'Doručena'">
            </td>
            <td><span style="background:#a62928;color:white;padding:5px;border-radius:5px">{{order.id}}</span></td>
            <td><a v-on:click.prevent="focusOrder(order)" href="#">{{order.address}}</a></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="mode !== 'view'">
      <h4>Aktuální trasa</h4>
      <table class="table table-sm">
        <thead>
          <tr>
            <th scope="col" style="width: 110px"></th>
            <th scope="col" style="width: 30px">#</th>
            <th scope="col">Adresa doručení</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, i) in this.routeOrders" v-bind:key="order.id">
            <td>
              <button class="btn btn-danger" v-bind:disabled="order.state.title === 'Doručena'" v-on:click="removeOrderFromRoute(i)"><i class="fas fa-minus"></i></button>
              <button class="btn btn-secondary" v-on:click="moveRouteOrder(i, -1)"><i class="fas fa-arrow-up"></i></button>
              <button class="btn btn-secondary" v-on:click="moveRouteOrder(i, 1)"><i class="fas fa-arrow-down"></i></button>
            </td>
            <td><span style="background:#a62928;color:white;padding:5px;border-radius:5px">{{order.id}}</span></td>
            <td><a v-on:click.prevent="focusOrder(order)" href="#">{{order.address}}</a></td>
          </tr>
        </tbody>
      </table>


      <h4>Dostupné objednávky k doručení</h4>
      <table class="table table-sm">
        <thead>
          <tr>
            <th scope="col" style="width: 110px;"></th>
            <th scope="col" style="width: 30px">#</th>
            <th scope="col">Adresa doručení</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(order, i) in this.availableOrders" v-bind:key="order.id" v-on:click="focusOrder(order)">
            <td>
              <button class="btn btn-success" v-on:click="addOrderToRoute(i)"><i class="fas fa-plus"></i></button>
            </td>
            <td><span style="background:#2a4bad;color:white;padding:5px;border-radius:5px">{{order.id}}</span></tD>
            <td><a v-on:click.prevent="focusOrder(order)" href="#">{{order.address}}</a></td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>

export default {
  created() {
    const today = new Date();
    this.date = today.getFullYear()
        + '-' + (today.getMonth() + 1).toString().padStart(2, '0')
        + '-' + today.getDate().toString().padStart(2, '0');
    this.user = JSON.parse(localStorage.user);
    this.driver = this.user.id;
    this.load();

  },
  data() {
    return {
      orders: [],
      routeOrders: [],
      availableOrders: [],
      map: null,
      id: this.$route.params.id,
      date: '',
      driver: '',
      drivers: [],
      route: null,
      goal: null,
      deleteOk: false,
      errorMessage: ''
    }
  },
  props: ['mode'],
  mounted() {
    const mid = window.SMap.Coords.fromWGS84(14.41, 50.08);
    this.map = new window.SMap(window.JAK.gel('map'), mid, 10);
    this.map.addDefaultLayer(window.SMap.DEF_BASE).enable();
    this.map.addDefaultControls();

    this.markersLayer = new window.SMap.Layer.Marker();
    this.map.addLayer(this.markersLayer);
    this.markersLayer.enable();

    this.routeLayer = new window.SMap.Layer.Geometry();
    this.map.addLayer(this.routeLayer).enable();

    this.map.setCenterZoom(mid, 16);

    this.redrawMap();
    this.focusMapOverview();
  },
  watch: {
    routeOrders() {
      this.redrawMap();
    },
    availableOrders() {
      this.redrawMap();
    }
  },
  methods: {
    getNumDelivered() {
      let n = 0;
      for (const o of this.routeOrders) {
        if (o.state && o.state.title === 'Doručena')
          n++;
      }
      return n;
    },
    async getCoords(address) {
      return new Promise((resolve, reject) => {
        const geocoder = new window.SMap.Geocoder(address, () => {
          const o = geocoder.getResults()[0];
          if (o.results.length === 0) {
            console.log('No results found!');
            reject();
            return;
          }
          const result = o.results[0];
          resolve(result.coords);
        });
      });
    },
    async loadOrderCoords(orders) {
      let result = await Promise.all(orders.map(async order => {
        let coord;
        try {
          coord = await this.getCoords(order.address);
        } catch {
          coord = null;
        }
        return {
          ...order,
          coord: coord
        };
      }));
      return result.filter(o => o.coord != null);
    },
    async loadDrivers() {
      const driversRes = await this.$http.get('users/drivers');
      this.drivers = driversRes.data;
    },
    async loadOrders() {
      const ordersRes = await this.$http.get('orders');
      this.availableOrders =
          await this.loadOrderCoords(ordersRes.data.filter(order => {
            return !order.route && order.deliver_date === this.date
                &&
                (!order.state || (
                    order.state.title !== 'Doručena' &&
                    order.state.title !== 'Zrušena' &&
                    order.state.title !== 'Zrušena zákazníkem'
                ));
          }));
      this.routeOrders = this.routeOrders.filter(order => {
        return order.deliver_date === this.date;
      });
    },
    async loadRoute() {
      const routeRes = await this.$http.get(`routes/${this.id}`);
      const route = routeRes.data;
      this.routeOrders =
          await this.loadOrderCoords(
              route.orders.sort((a, b) => a.route_index - b.route_index)
          );
      this.driver = routeRes.data.driver.id;
      this.date = routeRes.data.date.split(' ')[0];
      this.route = route;
    },
    async load() {
      if (this.mode !== 'view')
        await this.loadDrivers();
      if (this.mode === 'edit' || this.mode === 'view')
        await this.loadRoute();
      if (this.mode !== 'view')
        await this.loadOrders();
      this.redrawMap();
      this.focusMapOverview();
      if (this.mode === 'view') {
        this.setNextGoal();
      }
      this.deleteOk = (this.getNumDelivered() === 0);
    },
    async dateChanged() {
      await this.loadOrders();
      this.redrawMap();
      this.focusMapOverview();
    },
    focusOrder(order) {
      this.map.setCenter(order.coord);
    },
    moveRouteOrder(i, offset) {
      const j = i + offset;
      if (j < 0 || j >= this.routeOrders.length)
        return;
      let newRouteOrders = [...this.routeOrders];
      const tmp = newRouteOrders[i];
      newRouteOrders[i] = newRouteOrders[j];
      newRouteOrders[j] = tmp;
      this.routeOrders = newRouteOrders;
    },
    addOrderToRoute(i) {
      this.routeOrders.splice(this.routeOrders.length, 0, this.availableOrders[i]);
      this.availableOrders.splice(i, 1);
      //this.routeOrders[this.routeOrders.length - 1].obrazek.src = window.SMap.CONFIG.img+"/marker/drop-red.png";
    },
    removeOrderFromRoute(i) {
      this.availableOrders.splice(this.availableOrders.length, 0, this.routeOrders[i]);
      this.routeOrders.splice(i, 1);
      //this.availableOrders[this.availableOrders.length - 1].obrazek.src = window.SMap.CONFIG.img+"/marker/drop-blue.png";
    },
    async save() {
      const data = {
        orders: this.routeOrders.map(order => {
          return {order: order.id};
        }),
        date: this.date,
        driver: this.driver
      };
      if (!this.id) {
        await this.$http.post('routes/add', data)
            .then(response => {
              this.$router.push(`/routes/${response.data.id}`);
            })
            .catch(error => {
              if (error.response.data.errorMessage)
                this.errorMessage = error.response.data.errorMessage;
              else
                this.errorMessage = `Chyba ${error.response.status}`;
            });
      } else {
        await this.$http.post(`routes/${this.id}`, data)
            .then(response => {
              this.$router.push(`/routes/${response.data.id}`);
            })
            .catch(error => {
              if (error.response.data.errorMessage)
                this.errorMessage = error.response.data.errorMessage;
              else
                this.errorMessage = `Chyba ${error.response.status}`;
            });
      }
    },
    redrawMap() {
      if (!this.map) {
        return;
      }
      this.markersLayer.removeAll();
      this.routeLayer.removeAll();

      const addMarker = (order, color) => {
        const znacka = window.JAK.mel("div");
        const obrazek = window.JAK.mel("img", {src: window.SMap.CONFIG.img + `/marker/drop-${color}.png`});
        znacka.appendChild(obrazek);

        const popisek = window.JAK.mel("div", {}, {
          position: "absolute",
          left: "0px",
          top: "2px",
          textAlign: "center",
          width: "22px",
          color: "white",
          fontWeight: "bold"
        });
        popisek.innerHTML = order.id;
        znacka.appendChild(popisek);

        const marker = new window.SMap.Marker(order.coord, order.address, {url: znacka});
        this.markersLayer.addMarker(marker);
      };

      this.availableOrders.forEach(order => {
        addMarker(order, 'blue');
      });
      this.routeOrders.forEach(order => {
        addMarker(order, 'red');
      });

      let routeCoords = this.routeOrders.map(o => o.coord);
      let tmp = [];
      let prev = null;
      for (const coord of routeCoords) {
        if (prev == null || (prev.x !== coord.x && prev.y !== coord.y))
          tmp.push(coord);
        prev = coord;
      }
      routeCoords = tmp;

      if (routeCoords.length > 1) {
        new window.SMap.Route(routeCoords, (route) => {
          const routeCoords = route.getResults().geometry;
          const g = new window.SMap.Geometry(window.SMap.GEOMETRY_POLYLINE, null, routeCoords);
          this.routeLayer.addGeometry(g);
        });
      }
    },
    focusMapOverview() {
      const coords = this.routeOrders.concat(this.availableOrders).map(o => o.coord);
      const cz = this.map.computeCenterZoom(coords);
      this.map.setCenterZoom(cz[0], cz[1]);
    },
    async setGoal(order) {
      this.goal = order;
      this.focusOrder(order);
    },
    async onRoute(order) {
      order.state.title = 'Na cestě';
      await this.$http.get(`orders/${order.id}/setstate/Na cestě`);
    },
    async delivered(order) {
      order.state.title = 'Doručena';
      await this.$http.get(`orders/${order.id}/setstate/Doručena`);
      this.setNextGoal();
    },
    setNextGoal() {
      for (const order of this.routeOrders) {
        if (order.state.title !== 'Doručena') {
          this.setGoal(order);
          return;
        }
      }
      this.goal = null;
    },
    async deleteRoute() {
      await this.$http.delete(`routes/${this.id}`)
          .then(() => {
            this.$router.push('/routes');
          })
          .catch(error => {
            if (error.response.data.errorMessage)
              this.errorMessage = error.response.data.errorMessage;
            else
              this.errorMessage = `Chyba ${error.response.status}`;
          });
    },
  },
};
</script>

<style scoped>
#map {
  width: 100%;
  height: 500px;
}
button {
  font-size: 11pt;
  padding: 1px 5px;
  margin: 0 1px 0 0;
}
</style>
