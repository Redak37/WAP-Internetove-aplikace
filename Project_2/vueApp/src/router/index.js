import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ProductList from '../views/ProductList.vue'
import ResourceList from "../views/ResourceList.vue";
import ProductAdd from "../views/ProductAdd";
import ProductEdit from "../views/ProductEdit";
import ProductView from "../views/ProductView";
import CarList from "../views/CarsView";
import CarItem from "../components/CarItem";
import UserList from "../views/UserList";
import UserItem from "../components/UserItem";
import RouteAdd from "../views/RouteAdd";
import RouteEdit from "../views/RouteEdit";
import RouteView from "../views/RouteView";
import RouteList from "../views/RouteList";
import MyOrders from "../views/MyOrders";
import OrderList from "../views/OrderList";
import ProductionPlan from "../views/ProductionPlan";

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/ProductList',
    name: 'ProductList',
    component: ProductList
  },
  {
    path: '/ProductAdd',
    name: 'ProductAdd',
    component: ProductAdd
  },
  {
    path: '/ProductView/:id',
    name: 'ProductView',
    component: ProductView
  },
  {
    path: '/ProductEdit/:id',
    name: 'ProductEdit',
    component: ProductEdit
  },
  {
    path: '/ProductList/:category',
    name: 'ProductListWithCategory',
    component: ProductList
  },
  {
    path: '/ResourceList',
    name: 'ResourceList',
    component: ResourceList
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/CarList',
    name: 'CarList',
    component: CarList
  },
  {
    path: '/CarItem',
    name: 'CarItem',
    component: CarItem
  },
  {
    path: '/UserList',
    name: 'UserList',
    component: UserList
  },
  {
    path: '/UserItem',
    name: 'UserItem',
    component: UserItem
  },
  {
    path: '/routes',
    name: 'RouteList',
    component: RouteList,
  },
  {
    path: '/routes/new',
    name: 'RouteNew',
    component: RouteAdd,
  },
  {
    path: '/routes/:id',
    name: 'RouteView',
    component: RouteView,
  },
  {
    path: '/routes/:id/edit',
    name: 'RouteEdit',
    component: RouteEdit,
  },
  {
    path: '/MyOrders',
    name: 'MyOrders',
    component: MyOrders,
  },
  {
    path: '/OrderList',
    name: 'OrderList',
    component: OrderList,
  },
  {
    path: '/ProductionPlan',
    name: 'ProductionPlan',
    component: ProductionPlan,
  },
];

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (to.name !== 'Login' && localStorage.isAuthenticated !== 'yes')
    next({name: 'Login'});
  else if (to.name === 'Login' && localStorage.isAuthenticated === 'yes')
    next({name: 'Home'});
  else
    next();
});

export default router
