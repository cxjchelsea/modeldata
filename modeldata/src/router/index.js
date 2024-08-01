import { createRouter, createWebHashHistory } from 'vue-router'
import Content from '@/components/ContentPage.vue';
import Search from '@/components/SearchPage.vue';
import First from '@/components/FirstPage.vue';
import Detail from '@/components/DetailPage.vue';
import Weihu from '@/components/WeihuPage.vue';
import Line from '@/components/LinePage.vue';
import Material from '@/components/MaterialPage.vue';
import Product from '@/components/ProductPage.vue';

const routes = [
  {
    path: '/',
    component: First,
  },
  {
    path: '/model',
    component: Content,
  },
  {
    path: '/model/:model',
    component: Content,
  },
  {
    path: '/model/:model?/modelname/:chineseName',
    component: Detail,
  },
  {
    path: '/model/:model?/search/:searchKeyword/modelname/:chineseName',
    component: Detail,
  },
  {
    path: '/model/:model?/search/:searchKeyword',
    name: 'search',
    component: Search,
  },
  {
    path: '/weihu',
    component: Weihu,
  },
  {
    path: '/line',
    component: Line,
  },
  {
    path: '/material',
    component: Material,
  },    
  {
    path: '/product',
    component: Product,
  }

]

const router = createRouter({
  history: createWebHashHistory(),
  routes
});
export default router
