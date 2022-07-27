<template>
    <div style="margin-right: 100px;margin-left: 100px;">
        <el-card id="article" v-loading="loading">
            <el-row>
                作者：{{ article.username }}
            </el-row>
            <el-row style="margin-top: 20px">
                <markdown-it-vue class="md-body" :content="article.content" :options="options"/>
            </el-row>
            <el-row>
                <el-button icon="el-icon-thumb" id="likeBtn" @click="addLike">
                    赞同
                </el-button>
                {{ likeNum }}
                <el-icon class="el-icon-chat-dot-square"
                         style="margin-left: 10px">
                </el-icon>
                {{ commentNum }}
                <el-button type="primary" icon="el-icon-video-play" style="margin-left: 20px"
                           v-show="showCopy" @click="copyContainer">
                    动手实验
                </el-button>
            </el-row>
        </el-card>
        <div style="margin-top: 15px;">
            <el-input placeholder="评论一下" v-model="newComment" class="input-with-select">
                <el-button slot="append" icon="el-icon-chat-dot-square" @click="publishComment"></el-button>
            </el-input>
        </div>
        <el-card v-for="comment in article.comment" :key="comment.commentId">
            <el-row>
                评论者：{{ comment.username}}
            </el-row>
            <el-row>
                {{ comment.content }}
            </el-row>
        </el-card>
        <el-pagination
                background
                :current-page.sync="currentPage"
                @current-change="loadCommentList"
                :total="article.commentNum"
                layout="total, prev, pager, next"
                style="margin-top: 20px;text-align: center;margin-bottom: 30px"
        >
        </el-pagination>
    </div>
</template>

<script>
    import MarkdownItVue from 'markdown-it-vue'
    import "markdown-it-vue/dist/markdown-it-vue.css"

    export default {
        name: "PostDetail",
        components: {
          MarkdownItVue
        },
        data() {
            return {
                article: {},
                currentPage: 0,
                options: {
                    markdownIt: {
                        linkify: true
                    },
                    linkAttributes: {
                        attrs: {
                            target: '_blank',
                            rel: 'noopener'
                        }
                    }
                },
                isLiked: false,
                newComment: "",
                likeNum: 0,
                commentNum: 0,
                showCopy: false,
                loading: false
            }
        },
        mounted() {
            this.init();
        },
        methods: {
            init() {
                this.$axios({
                    method: "GET",
                    url: "/api/GetPostDetail?id="+this.$router.app.$route.query.id
                }).then((response) => {
                    this.article = response.data.content;
                    this.likeNum = this.article.likeNum;
                    this.commentNum = this.article.commentNum;
                    if (parseInt(this.article.containerId) > 0) {
                        this.showCopy = true
                    }
                })
                this.$axios({
                    method: "GET",
                    url: "/api/Likes/IsLiked?username="+localStorage.getItem("mlabUser")
                        +"&postId="+this.$router.app.$route.query.id
                }).then((response) => {
                    if (response.data.content) {
                        this.isLiked = true;
                        document.getElementById("likeBtn").innerHTML = "已赞同"
                    }
                })
            },
            loadCommentList(value) {
                const path = this.$router.app.$route.query;
                this.currentPage = value;
                if (path.search) {
                    this.init();
                } else {
                    this.init();
                }
                document.body.scrollTop = 0;
                document.documentElement.scrollTop = 0;
            },
            addLike() {
                if (!this.isLiked) {
                    this.$axios({
                        method: "POST",
                        url: "/api/Likes/NewLikes",
                        data: {
                            "postId": this.article.postId,
                            "username": localStorage.getItem("mlabUser")
                        }
                    }).then((response) => {
                        if (response.status === 200) {
                            this.isLiked = true;
                            document.getElementById("likeBtn").innerHTML = "已赞同"
                            window.location.reload();
                        }
                    })
                }
                else {
                    this.$axios({
                        method: "POST",
                        url: "/api/Likes/DeleteLikes",
                        data: {
                            "postId": this.article.postId,
                            "username": localStorage.getItem("mlabUser")
                        }
                    }).then((response) => {
                        if (response.status === 200) {
                            this.isLiked = true;
                            document.getElementById("likeBtn").innerHTML = "赞同"
                            window.location.reload();
                        }
                    })
                }
            },
            publishComment() {
                this.$axios({
                    method: "POST",
                    url: "/api/Comments",
                    data: {
                        username: localStorage.getItem("mlabUser"),
                        content: this.newComment,
                        postId: this.article.postId
                    }
                }).then((response) => {
                    if (response.status === 200) {
                        window.location.reload();
                    }
                })
            },
            copyContainer() {
                this.loading = true;
                this.$axios({
                    method: "POST",
                    url: "/api/Containers/CopyContainer",
                    data: {
                        postId: this.article.postId,
                        containerId: this.article.containerId,
                        username: localStorage.getItem("mlabUser")
                    }
                }).then((response) => {
                    this.loading = false;
                    if (response.data.message === "复制成功") {
                        this.$router.push("/container");
                    } else {
                        alert("复制失败！请稍后重试！")
                    }
                })
            }
        }
    }
</script>

<style>
    .el-row {
        margin-top: 20px;
    }

    .el-card {
        margin-top: 20px;
    }
</style>
