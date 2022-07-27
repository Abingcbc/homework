<template>
    <div>
        <div class="register-wrap">
            <img src="../../public/logo_figure.png" class="logo-register" width="100" height="100" alt="">
            <el-form @submit.native.prevent>
                <el-form-item>
                    <el-input type="text" :placeholder="'用户名'" v-model="username" autofocus clearable/>
                </el-form-item>
                <el-form-item>
                    <el-input type="password" :placeholder="'密码'" v-model="password" clearable/>
                </el-form-item>
                <el-form-item>
                    <el-input type="password" :placeholder="'重复密码'" v-model="rPassword" clearable/>
                </el-form-item>
                <el-form-item style="text-align: center">
                    <el-button type="text" @click="register">注册</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>

    export default {
        name: "Register",
        data() {
            return {
                username: '',
                password: '',
                rPassword: '',
            }
        },
        methods: {
            register() {
                if (this.password !== this.rPassword) {
                    alert("两次密码输入不同！");
                    return
                }
                this.$axios({
                    method: "POST",
                    url: "/api/register",
                    data: {
                        username: this.username,
                        password: this.password
                    }
                }).then((response) => {
                    if (response.data["message"] === "success") {
                        localStorage.setItem("mlabUser", this.username);
                        localStorage.setItem("mlabToken", response.data["content"]);
                        window.location.reload();
                        this.$router.push('/');
                    } else {
                        alert(response.data["content"]);
                    }
                })
            }
        }
    }
</script>

<style>
    .register-wrap {
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .register-wrap:before {
        content: '';
        display: table;
    }

    .register-wrap:after {
        content: '';
        display: table;
        clear: both;
    }

    .logo-register {
        display: block;
        margin: 100px auto 50px auto;
    }
</style>
