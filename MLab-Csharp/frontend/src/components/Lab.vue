<template>
    <el-container v-loading="loading" style="height: 100%">
        <el-main style="height: 100%">
            <iframe :src=containerUrl />
        </el-main>
        <el-aside>
            <el-button type="danger" style="margin-top: 40px"
                       @click="stopContainer">
                停止
            </el-button>
            <el-button type="primary" style="margin-top: 40px"
                       @click="downloadLog">
                下载日志
            </el-button>
        </el-aside>
    </el-container>
</template>

<script>
    export default {
        name: "Lab",
        data() {
            return {
                containerUrl: "",
                containerId: 0,
                loading: false,
            }
        },
        mounted() {
            this.containerUrl = this.$route.params.notebook;
            this.containerId = this.$route.params.containerId;
            console.log(this.containerUrl);
            if (!this.containerUrl) {
                this.$router.push("/");
            }
        },
        methods: {
            stopContainer() {
                this.loading = true;
                this.$axios({
                    method: "GET",
                    url: "/api/Containers/StopContainer/" + this.containerId
                }).then((response) => {
                    if (response.status === 200) {
                        alert("关闭成功！");
                        this.$router.push("/container");
                    }
                })
            },
            downloadLog() {
                this.$axios({
                    method: "GET",
                    url: "/server/docker/Download/" + this.containerId
                }).then((response) => {
                    var urlObject = window.URL || window.webkitURL || window;
                    var export_blob = new Blob([response.data]);
                    var save_link = document.createElementNS("http://www.w3.org/1999/xhtml", "a")
                    save_link.href = urlObject.createObjectURL(export_blob);
                    save_link.download = "mlab"+this.containerId+".txt";
                    this.fakeClick(save_link);
                })
            },
            fakeClick(obj) {
                var ev = document.createEvent("MouseEvents");
                ev.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                obj.dispatchEvent(ev);
            },
        }
    }
</script>

<style>
    iframe {
        width: 100%;
        height: 80%;
        border: 0;
        margin-top: 20px;
    }
</style>
