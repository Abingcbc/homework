<template>
    <div id="main">
        <el-alert
                v-if="showSuccessAlert"
                :title="successAlert"
                center
                show-icon
                type="success"
                style="position: absolute">
        </el-alert>
        <el-alert
                v-if="showErrorAlert"
                :title="errorAlert"
                center
                show-icon
                type="error"
                style="position: absolute">
        </el-alert>
        <div style="padding-top: 100px; padding-bottom: 30px">
            <img src="../assets/webcraft.png" alt=""/>
        </div>
        <div>
            <el-button @click="showLogin = true" class="MineCraftButton" v-if="!logined">
                <span>登录</span>
            </el-button>
        </div>
        <el-dialog title="登录" :visible.sync="showLogin">
            <el-form :model="loginForm" style="width: 300px; margin: 0px auto">
                <el-form-item label="用户名">
                    <el-input v-model="loginForm.username" autocomplete="off" class="MineCraftInput"/>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="loginForm.password" show-password class="MineCraftInput"/>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showLogin = false" class="MineCraftButton">取 消</el-button>
                <el-button type="primary" @click="login" class="MineCraftButton">确 定</el-button>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="showRegister = true" v-if="!logined">
                <span>注册</span>
            </el-button>
        </div>
        <el-dialog title="注册" :visible.sync="showRegister">
            <el-form :model="registerForm" style="width: 300px; margin: 0px auto">
                <el-form-item label="用户名">
                    <el-input v-model="registerForm.username" autocomplete="off"/>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="registerForm.password" show-password/>
                </el-form-item>
                <el-form-item label="重复密码">
                    <el-input v-model="registerForm.repeatPassword" show-password/>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showRegister = false" class="MineCraftButton">取 消</el-button>
                <el-button type="primary" @click="register" class="MineCraftButton">确 定</el-button>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="showCreate = true" v-if="logined">
                <span>创建新的世界</span>
            </el-button>
        </div>
        <el-dialog title="创建新的世界" :visible.sync="showCreate">
            <el-form :model="createForm" style="width: 300px; margin: 0px auto">
                <el-form-item label="世界名称">
                    <el-input v-model="createForm.filename" autocomplete="off" class="MineCraftInput"/>
                </el-form-item>
                <el-form-item label="世界大小">
                    <el-input-number v-model="createForm.worldSize" :min="2" :max="100"/>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showCreate = false" class="MineCraftButton">取 消</el-button>
                <el-button type="primary" @click="create" class="MineCraftButton">确 定</el-button>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="load" v-if="logined">
                <span>读取存档</span>
            </el-button>
        </div>
        <el-dialog title="读取存档" :visible.sync="showLoad">
            <el-button v-for="(world, index) in savedWorldList" :key="index" class="file"
                       @click.native="chooseFile(index)">
                <el-row style="font-size: 30px">{{ world.filename }}</el-row>
                <el-row>
                    世界大小：{{world.worldSize}}
                </el-row>
                <el-row>
                    创建时间
                </el-row>
                <el-row>
                    {{world.createTime}}
                </el-row>
                <el-row>
                    最近修改时间：
                </el-row>
                <el-row>
                    {{world.updateTime}}
                </el-row>
            </el-button>
            <div slot="footer" class="dialog-footer">
                <el-button type="primary" @click="deleteFile" class="MineCraftButton">删 除</el-button>
                <el-button @click="showLoad = false" class="MineCraftButton">取 消</el-button>
                <el-button type="primary" @click="confirmFile" class="MineCraftButton">确 定</el-button>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="showShare = true" v-if="logined">
                <span>从分享码加载</span>
            </el-button>
        </div>
        <el-dialog title="从分享码加载" :visible.sync="showShare">
            <el-form style="width: 300px; margin: 0px auto">
                <el-form-item label="分享码">
                    <el-input v-model="shareCode" autocomplete="off" class="MineCraftInput"/>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="showShare = false" class="MineCraftButton">取 消</el-button>
                <el-button type="primary" @click="loadShare" class="MineCraftButton">确 定</el-button>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="showTutorial = true">
                <span>教程</span>
            </el-button>
        </div>
        <el-dialog title="教程" :visible.sync="showTutorial">
            <div class="tutorial" >
                <el-row>WASD / 方向键 控制移动</el-row>
                <el-row>Q 开启/关闭创造模式</el-row>
                <el-row>   R / F     创造模式下上下移动</el-row>
                <el-row>   space     跳跃           </el-row>
                <el-row>    esc      打开菜单        </el-row>
                <el-row>鼠标移动控制视角</el-row>
                <el-row>鼠标左键创建方块</el-row>
                <el-row>鼠标右键消除方块</el-row>
                <el-row>鼠标滑轮切换方块</el-row>
            </div>
        </el-dialog>
        <div>
            <el-button class="MineCraftButton" @click="logout" v-if="logined">
                <span>登出</span>
            </el-button>
        </div>
    </div>
</template>

<script>
    import "../assets/css/main.css";

    export default {
        name: "HomePage",
        data() {
            return {
                showLogin: false,
                loginForm: {
                    username: "",
                    password: ""
                },
                showRegister: false,
                registerForm: {
                    username: "",
                    password: "",
                    repeatPassword: ""
                },
                logined: false,
                showCreate: false,
                createForm: {
                    filename: "",
                    worldSize: "",
                },
                showLoad: false,
                savedWorldList: [],
                chosenFileIndex: -1,
                successAlert: "",
                errorAlert: "",
                showSuccessAlert: false,
                showErrorAlert: false,
                showTutorial: false,
                showShare: false,
                shareCode: ""
            }
        },
        mounted() {
            this.init();
        },
        methods: {
            init() {
                if (localStorage.getItem("WebCraftToken")) {
                    this.logined = true;
                }
            },
            login() {
                this.$axios({
                    method: 'post',
                    url: '/api/oauth/token',
                    headers: {
                        'Authorization': 'Basic YnJvd3NlcjpzZWNyZXQ='
                    },
                    params: {
                        'grant_type': 'password',
                        'username': this.loginForm.username,
                        'password': this.loginForm.password,
                        'scope': 'ui'
                    }
                }).then((response) => {
                    if (response.status === 200) {
                        this.showLogin = false;
                        localStorage.setItem("WebCraftToken", response.data.access_token);
                        localStorage.setItem("WebCraftUser", this.loginForm.username);
                        this.logined = true;
                        window.location.href = "/";
                    } else {
                        this.alertError("用户名或密码错误！");
                    }
                })
            },
            register() {
                if (this.registerForm.password !== this.registerForm.repeatPassword) {
                    this.alertError("两次输入密码不一致！");
                } else {
                    this.$axios({
                        method: 'post',
                        url: '/api/register',
                        data: {
                            'username': this.registerForm.username,
                            'password': this.registerForm.password
                        }
                    }).then((response) => {
                        if (response.status === 200) {
                            this.alertSuccess("注册成功！");
                            this.showRegister = false;
                            this.showLogin = true;
                        } else {
                            this.alertError("注册失败！");
                        }
                    })
                }
            },
            create() {
                // 由main页面负责上传，因为文件内容只有在main页面才能确定
                this.$router.push({
                    name: 'main',
                    params: {
                        'type': 'new', 'info': this.createForm
                    }
                })
            },
            load() {
                this.$axios({
                    method: 'get',
                    headers: {
                        'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                    },
                    url: '/api/fileList/' + localStorage.getItem("WebCraftUser")
                }).then((response) => {
                    if (response.status === 200) {
                        this.savedWorldList = response.data;
                    }
                });
                this.showLoad = true;
            },
            chooseFile(index) {
                this.chosenFileIndex = index;
            },
            confirmFile() {
                if (this.chosenFileIndex < 0) {
                    this.alertError("请选择存档！");
                } else {
                    this.$router.push({
                        name: 'main',
                        params: {
                            'type': 'old',
                            'info': this.savedWorldList[this.chosenFileIndex]
                        }
                    });
                }
            },
            deleteFile() {
                if (this.chosenFileIndex < 0) {
                    this.alertError("请选择存档！");
                } else {
                    this.$axios({
                        method: 'post',
                        headers: {
                            'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                        },
                        url: '/api/delete/' + localStorage.getItem("WebCraftUser") + "/" +
                            this.savedWorldList[this.chosenFileIndex].fileId
                    }).then((response) => {
                        if (response.status === 200) {
                            this.alertSuccess("删除成功！");
                            this.showLoad = false;
                        }
                    });
                }
            },
            logout() {
                localStorage.removeItem("WebCraftToken");
                localStorage.removeItem("WebCraftUser");
                window.location.href = "/";
            },
            alertSuccess(message) {
                this.successAlert = message;
                this.showSuccessAlert = true;
                setTimeout(() => {
                    this.showSuccessAlert = false;
                }, 2000);
            },
            alertError(message) {
                this.errorAlert = message;
                this.showErrorAlert = true;
                setTimeout(() => {
                    this.showErrorAlert = false;
                }, 2000);
            },
            loadShare() {
                this.$router.push({
                    name: 'main',
                    params: {
                        'type': 'code', 'info': this.shareCode
                    }
                })
            }
        }
    }
</script>

<style>
    #main {
        background-image: url("../assets/minecraft-background.jpg");
        background-size: 100% 100%;
        height: 100%;
        text-align: center;
    }

    .el-dialog__footer {
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
    }

    .dialog-footer .MineCraftButton {
        width: 100px;
        display: inline-block;
    }

    .el-input__inner {
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
        font-family: Minecraft;
        color: white;
        font-size: 20px;
    }

    .el-form-item__label {
        font-size: 20px;
        font-family: Minecraft;
        color: white;
    }

    .MineCraftInput {
        width: 300px;
    }

    .file {
        width: 200px;
        display: inline-block;
        margin: 10px;
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
        font-family: Minecraft;
        color: white;
    }

    .tutorial {
        font-family: Minecraft;
        font-size: 25px;
        color: white;
    }

</style>
