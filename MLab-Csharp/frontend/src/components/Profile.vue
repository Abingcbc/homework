<template>
    <el-container style="margin-left: 100px;margin-right: 100px;margin-top: 100px">
        <el-aside>
            <el-avatar :size="300"
                       :src="avatarUrl"
                       style="display: block"
            />
            <el-button type="primary"
                       style="margin-top: 50px;margin-left: 80px"
            >
                上传新头像
                <i class="el-icon-upload el-icon--right"/>
            </el-button>
        </el-aside>
        <el-main style="margin-left: 50px;text-align: center">
            <h1>{{ user.username }}</h1>
            <h4>累计获得 {{user.like}} 个赞</h4>
            <div style="margin-top: 100px">
                <div>
                    邮箱：
                    <el-input style="width: 300px" v-model="email">
                    </el-input>
                </div>
                <div style="margin-top: 30px">
                    是否开启训练完成邮件通知：
                    <el-switch
                            v-model="isReceiveNotify"
                    >
                    </el-switch>
                </div>
                <div style="margin-top: 30px">
                    输入原密码：
                    <el-input style="width: 300px" show-password v-model="oldPassword">
                    </el-input>
                </div>
                <div style="margin-top: 30px">
                    输入新密码：
                    <el-input style="width: 300px" show-password v-model="newPassword">
                    </el-input>
                </div>
                <div style="margin-top: 30px">
                    <el-button type="primary">
                        更新
                    </el-button>
                </div>
            </div>
        </el-main>
    </el-container>
</template>

<script>
    export default {
        name: "Profile",
        data() {
            return {
                avatarUrl: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
                user: {},
                email: '',
                oldPassword: '',
                newPassword: '',
                isReceiveNotify: true
            }
        },
        mounted() {
            this.init()
        },
        methods: {
            init() {
                this.user = {
                    'username': 'asdfasdf',
                    'email': 'sdfsadf',
                    'like': 100,
                    'receiveNotify': true
                };
                this.isReceiveNotify = this.user.receiveNotify;
            }
        }
    }
</script>

<style>

</style>
