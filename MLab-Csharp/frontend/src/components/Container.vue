<template>
    <el-container v-loading="loading">
        <el-aside style="text-align: center">
            <el-button type="primary" icon="el-icon-plus" style="margin-top: 40px"
                       @click="showCreate = true">
                创建新容器
            </el-button>
            <el-dialog title="创建新容器" :visible.sync="showCreate" style="text-align: center">
                <el-form :model="newContainer" style="width: 200px; display: inline-block">
                    <el-form-item label="容器名称">
                        <el-input v-model="newContainer.name" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="容器类型">
                        <el-select v-model="newContainer.type" placeholder="请选择容器类型">
                            <el-option label="基础包" value="0"></el-option>
                            <el-option label="TensorFlow包" value="1"></el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="showCreate = false">取 消</el-button>
                    <el-button type="primary" @click.native="create">确 定</el-button>
                </div>
            </el-dialog>
        </el-aside>
        <el-main>
            <el-card class="container" v-for="containerData in containerList" :key="containerData.containerId">
                <el-container>
                    <el-main>
                        <el-row style="font-size: 30px">{{ containerData.containerName }}</el-row>
                        <el-row style="font-size: 10px">类型：{{ typeToString(containerData.type) }}</el-row>
                        <el-row style="font-size: 10px">创建时间： {{ containerData.createTime }}</el-row>
                    </el-main>
                    <el-aside style="width: 50px">
                        <el-button type="danger" icon="el-icon-delete" circle style="margin-left: 10px"
                                   @click="deleteContainer(containerData.containerId)"/>
                        <el-button type="primary" icon="el-icon-video-play" circle style="margin-top: 20px"
                                   @click="startContainer(containerData.containerId)"/>
                    </el-aside>
                </el-container>
            </el-card>
            <el-pagination
                    background
                    :current-page.sync="currentPage"
                    :total="totalContainer"
                    layout="total, prev, pager, next"
                    style="margin-top: 20px;text-align: center;margin-bottom: 30px">
            </el-pagination>
        </el-main>
    </el-container>
</template>

<script>
    export default {
        name: "Container",
        data() {
            return {
                containerList: [],
                currentPage: 1,
                totalContainer: 0,
                showCreate: false,
                newContainer: {
                    name: "",
                    type: 0
                },
                loading: false
            }
        },
        mounted() {
            this.init()
        },
        methods: {
            init() {
                this.containerList = [];
                this.$axios({
                    method: "GET",
                    url: "/api/Containers/GetContainer/"+localStorage.getItem("mlabUser")
                }).then((response) => {
                    this.containerList = response.data["content"];
                    this.totalContainer = this.containerList.length;
                })
            },
            create() {
                this.showCreate = false;
                this.$axios({
                    method: "POST",
                    url: "/api/Containers/PostContainer",
                    data: {
                        username: localStorage.getItem("mlabUser"),
                        containerName: this.newContainer.name,
                        type: parseInt(this.newContainer.type)
                    }
                }).then((response) => {
                    if (response.status === 200) {
                        alert("创建成功");
                        window.location.reload();
                    }
                })
            },
            typeToString(containerType) {
                if (containerType === 0) {
                    return "基础包";
                } else {
                    return "Tensorflow包";
                }
            },
            deleteContainer(containerId) {
                this.$axios({
                    method: "POST",
                    url: "/api/Containers/DeleteContainer/"+containerId
                }).then((response) => {
                    if (response.status === 200) {
                        alert("删除成功！");
                        window.location.reload();
                    }
                })
            },
            startContainer(containerId) {
                this.loading = true;
                this.$axios({
                    method: "POST",
                    url: "/api/Containers/StartContainer/"+containerId
                }).then((response) => {
                    this.loading = false;
                    if (response.data.message === "success") {
                        this.$router.replace({
                            name: "lab",
                            params: {
                                notebook: response.data.content,
                                containerId: containerId
                            }
                        });
                    }
                    else {
                        alert("项目正在启动中...请稍后")
                    }
                })
            }
        }
    }
</script>

<style>
    .container {
        width: 300px;
        display: inline-block;
        margin-right: 20px;
        margin-top: 20px;
    }
</style>
