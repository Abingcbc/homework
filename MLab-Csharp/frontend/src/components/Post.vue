<template>
    <el-container style="margin-right: 300px; margin-left: 300px">
        <el-main>
            <el-card class="post" v-for="postData in postList" :key="postData.postId">
                <el-row style="font-size: 30px">{{ postData.title }}</el-row>
                <el-row>
                    {{ postData.author}}
                </el-row>
                <el-container>
                    <el-aside>
                        <img :src=typeToImage(postData) alt="" style="size: 150px"/>
                    </el-aside>
                    <el-main>
                        {{ postData.content }}...
                        <el-button type="text" @click.native="detail(postData.postId)">
                            查看详情
                        </el-button>
                    </el-main>
                </el-container>
                <el-row>
                    <el-col :span="1">
                        <el-icon class="el-icon-thumb"/>
                        {{ postData.likeNum }}
                    </el-col>
                    <el-col :span="1">
                        <el-icon class="el-icon-chat-dot-square"/>
                        {{ postData.commentNum }}
                    </el-col>
                </el-row>
            </el-card>
            <el-pagination
                    background
                    :current-page.sync="currentPage"
                    @current-change="loadPostList"
                    :total="totalPost"
                    layout="total, prev, pager, next">
            </el-pagination>
        </el-main>
    </el-container>
</template>

<script>
    export default {
        name: "Post",
        data() {
            return {
                postList: [],
                currentPage: 1,
                totalPost: 0
            }
        },
        mounted() {
            // must have the page
            if (!this.$router.app.$route.query.page) {
                this.$router.push('/post?page=1')
            }
            this.init()
        },
        methods: {
            init() {
                this.currentPage = parseInt(this.$router.app.$route.query.page);
                this.postList = [];
                this.$axios({
                    method: "GET",
                    url: "/api/GetMyPost?username="+localStorage.getItem("mlabUser")
                }).then((response) => {
                    this.postList = response.data['content'];
                    this.totalPost = this.postList.length;
                    console.log(this.postList)
                })
            },
            loadPostList(value) {
                this.currentPage = value;
                this.$router.push("/post?page=" + value.toString());
                this.init();
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            },
            detail(id) {
                this.$router.push('/postDetail?id=' + id.toString());
            },
            typeToImage(post) {
                if (post.container.type === 0) {
                    return "./python.png";
                } else {
                    return "./tensorflow.png";
                }
            }
        }
    }
</script>

<style>
    .post {
        margin-bottom: 10px;
    }
</style>
