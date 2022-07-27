<template>
    <div>
        <h3 style="text-align: center">
            创建新的文章
        </h3>
        <mavon-editor ref=mde
                      v-model="value"
                      @imgAdd="$imgAdd"
        />
        <el-select v-model="containerId" placeholder="选择分享的容器" style="margin-top: 30px">
            <el-option
                    v-for="item in containerList"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
            </el-option>
        </el-select>
        <div style="text-align: center; margin-top: 30px">
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item>
                    <el-button type="primary"
                               @click.native="onSubmit">提交</el-button>
                    <el-button type="text">取消</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CreatePost",
        data() {
            return {
                value: '',
                form: {},
                containerList: [],
                containerId: 0
            }
        },
        mounted() {
            this.loadContainer()
        },
        methods: {
            $imgAdd(pos, $file) {
                var formdata = new FormData();
                formdata.append('smfile', $file);
                formdata.append('format', 'json');
                this.$axios({
                    method: 'POST',
                    url: '/image/upload',
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': 'Basic RQdNo5KAYxKItjZt36FyFPutENVaJQZ2',
                        'Accept': '*/*',
                    },
                    data: formdata
                }).then((response) => {
                    console.log(response);
                    if (response.data['success']) {
                        this.$refs.mde.$img2Url(pos, response.data['data']['url'])
                    } else {
                        // repeat upload
                        this.$refs.mde.$img2Url(pos, response.data['images'])
                    }
                })
            },
            onSubmit() {
                this.$axios({
                    method: 'POST',
                    url: '/api/PostPost',
                    data: {
                        username: localStorage.getItem('mlabUser'),
                        title: this.value.split('\n')[0],
                        content: this.value,
                        containerId: this.containerId
                    }
                }).then((response) => {
                    if (response.data['message'] === 'success') {
                        this.$router.push('/community')
                    } else {
                        alert("创建失败！请稍后重试！")
                    }
                })
            },
            loadContainer() {
                let username = localStorage.getItem("mlabUser");
                if (!username) {
                    this.$router.push("/login");
                }
                this.$axios({
                    method: "GET",
                    url: "/api/Containers/GetContainer/"+localStorage.getItem("mlabUser")
                }).then((response) => {
                    let containers = response.data['content']
                    for (let i = 0; i < containers.length; i++) {
                        this.containerList.push({
                            value: containers[i].containerId,
                            label: containers[i].containerName
                        })
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>
