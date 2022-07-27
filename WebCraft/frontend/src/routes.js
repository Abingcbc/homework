import Vue from "vue";
import Router from "vue-router";

import HomePage from "@/components/HomePage";
import MainScene from "@/components/MainScene";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: '',
    routes: [
        {path: '/', component: HomePage, name: 'homepage'},
        {path: '/main', component: MainScene, name: 'main'},
    ]
})
