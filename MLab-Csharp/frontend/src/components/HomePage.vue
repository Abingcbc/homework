<template>
    <div>
        <el-card id="glide">
            <el-carousel style="height: 500px;">
                <el-carousel-item
                                  v-for="picture in pictures"
                                  :key="picture"
                                  style="height: 500px"
                                  >
                    <el-image :src="picture" style="height: 500px; width: 100%">
                        <div slot="placeholder" class="image-slot">
                            加载中<span class="dot">...</span>
                        </div>
                    </el-image>
                </el-carousel-item>
            </el-carousel>
        </el-card>
        <div style="text-align: center; margin-top: 50px">
            <el-button
                    round
                    type="primary"
                    @click.native="start"
            >
                开始
            </el-button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "HomePage",
        data() {
            return {
                pictures: [
                    '/example.jpg',
                    '/example2.jpg',
                    '/example3.jpg',
                ]
            }
        },
        methods: {
            start() {
                if (localStorage.getItem("mlabUser")) {
                    this.$router.push('/container')
                } else {
                    this.$router.push('/login')
                }
            }
        }
    }
</script>

<style>
#glide {
    margin-top: 20px;
    margin-left: 40px;
    margin-right: 40px;
}
</style>
