<template>
    <div>
        <div class="login-wrap">
            <img src="../../public/logo_figure.png" class="logo-login" width="100" height="100" alt="">
            <el-form @submit.native.prevent>
                <el-form-item>
                    <el-input type="text" :placeholder="'用户名'" v-model="username" autofocus clearable/>
                </el-form-item>
                <el-form-item>
                    <el-input type="password" :placeholder="'密码'" v-model="password" clearable/>
                </el-form-item>
                <el-form-item style="text-align: center">
                    <el-button type="primary" @click="login" round>
                        登录
                    </el-button>
                    <el-button type="text" @click.native="register">注册</el-button>
                </el-form-item>
            </el-form>

        </div>
    </div>
</template>

<script>

    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
            }
        },
        mounted() {
            if (localStorage.getItem("mlabUser")) {
                this.$router.push('/');
            }
        },
        methods: {
            login() {
                this.$axios({
                    method: "POST",
                    url: "/api/login",
                    data: {
                        username: this.username,
                        password: this.password
                    }
                }).then((response) => {
                    if (response.data["message"] === "success") {
                        localStorage.setItem("mlabUser", this.username);
                        localStorage.setItem("mlabToken", response.data["content"]);
                        window.location.reload();
                    } else {
                        alert(response.data["content"]);
                    }
                })
            },
            register() {
                this.$router.push('/register')
            }
        }
    }
</script>

<style>
    .login-wrap {
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .login-wrap:before {
        content: '';
        display: table;
    }

    .login-wrap:after {
        content: '';
        display: table;
        clear: both;
    }

    .logo-login {
        display: block;
        margin: 100px auto 50px auto;
    }
</style>
