import Vue from 'vue';
import Router from 'vue-router';

import HomePage from "@/components/HomePage";
import Login from '@/components/Login'
import Register from "@/components/Register";
import Lab from '@/components/Lab'
import Community from "@/components/Community";
import CreatePost from "@/components/CreatePost";
import PostDetail from "@/components/PostDetail";
import Profile from "@/components/Profile";
import Post from "@/components/Post";
import Container from "./components/Container";
import LikePost from "./components/LikePost";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: '',
    routes: [
        {path: '/', component: HomePage, name: 'homepage'},
        {path: '/login', component: Login, name: 'login'},
        {path: '/register', component: Register, name: 'register'},
        {path: '/lab', component: Lab, name: 'lab'},
        {path: '/community', component: Community, name: 'community'},
        {path: '/createPost', component: CreatePost},
        {path: '/postDetail', component: PostDetail},
        {path: '/profile', component: Profile},
        {path: '/post', component: Post},
        {path: '/likePost', component: LikePost},
        {path: '/container', component: Container}
    ]
});
