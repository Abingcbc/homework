<template>
    <div id="container">
        <img class="blockerImg" :src="blockUrl" alt=""/>
        <img src="../assets/img/cross.png" class="cross" alt="" oncontextmenu="return false"/>
        <el-dialog
                class="menu"
                title="菜单"
                :visible.sync="menuShow"
                width="30%"
                :before-close="closeMenu"
                v-loading.fullscreen.lock="fullscreenLoading"
        >
            <el-button class="MineCraftButton" @click="saveWorld">
                <span>保存</span>
            </el-button>
            <el-button class="MineCraftButton" @click="returnToMainPage">
                <span>返回主页</span>
            </el-button>
            <el-button class="MineCraftButton" @click="returnToGame">
                <span>回到游戏</span>
            </el-button>
            <el-button class="MineCraftButton" @click="copyShareCode">
                <span>分享</span>
            </el-button>
        </el-dialog>
        <el-dialog
                class="menu"
                title="世界未保存，是否返回？"
                :visible.sync="confirmShow"
                width="30%"
                :before-close="closeConfirm"
        >
            <el-button class="MineCraftButton" @click="confirmShow = false">
                <span>取消</span>
            </el-button>
            <el-button class="MineCraftButton" @click="confirmReturn">
                <span>确定</span>
            </el-button>
        </el-dialog>
        <el-alert
                :title="alertTitle"
                type="success"
                center
                show-icon
                v-if="showAlert"
                style="position: absolute"
        >
        </el-alert>
    </div>
</template>

<script>
    import * as THREE from "three";
    import Stats from "stats-js";
    import {FirstPersonControls} from "../controls/FirstPersonControls";
    import {createBox} from "@/utils/BoxUtil";
    import "../assets/css/main.css";
    import {getHeight} from "@/utils/SpaceUtil";

    export default {
        name: "MainScene",
        data() {
            return {
                fileId: 0,
                filename: "",
                worldWidth: 10,
                data: [], // 自定义的JSON格式，为了判断高度以及保存
                objects: [], // three.js 中的对象，为了判断是否相交
                status: {},
                scene: {},
                camera: {},
                controls: {},
                render: {},
                clock: {},
                blockUrl: "/textures/dirt.png",
                blockerList: [
                    "/textures/dirt.png",
                    "/textures/brick.png",
                    "/textures/grass_dirt.png",
                    "/textures/stone.png",
                    "/textures/glass.png",
                    "/textures/tree_side.png",
                    "/textures/brick_brown.png",
                    "/textures/leaves.png",
                    "/textures/tallgrass.png",
                    "/textures/rose.png",
                    "/textures/tulip.png",
                ],
                menuShow: false,
                fullscreenLoading: true,
                boxHelper: {
                    createDataHandler: this.createDataHandler,
                    removeDataHandler: this.removeDataHandler,
                    createModeHandler: this.createModeHandler,
                    isBlockExist: this.isBlockExist,
                    onMouseWheelHandler: this.onMouseWheelHandler
                },
                alertTitle: "",
                showAlert: false,
                modified: false,
                confirmShow: false
            }
        },
        mounted() {
            // 非法进入
            if (this.$route.params.type === undefined ||
                localStorage.getItem("WebCraftToken") === undefined) {
                this.$router.push("/");
            }
            if (this.$route.params.type === 'new') {
                this.filename = this.$route.params.info.filename;
                this.worldWidth = this.$route.params.info.worldSize;
                this.createNewWorld();
                this.init();
                this.animate();
                this.addCloud();
            }
            else if (this.$route.params.type === 'old') {
                this.fileId = this.$route.params.info.fileId;
                this.$axios({
                    method: 'get',
                    url: '/api/file/' + localStorage.getItem("WebCraftUser")
                        + '/' + this.$route.params.info.fileId,
                    headers: {
                        'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                    },
                }).then((response) => {
                    if (response.status === 200) {
                        this.data = eval(response.data.fileContent);
                        this.worldWidth = eval(response.data.worldSize);
                        this.fileId = response.data.fileId;
                        this.fullscreenLoading = false;
                        this.showAlert = true;
                        this.alertTitle = "加载世界成功！";
                        setTimeout(() => {
                            this.showAlert = false
                        }, 2000);
                        this.init();
                        this.animate();
                        this.addCloud();
                    }
                })
            }
            else {
                this.$axios({
                    method: 'get',
                    url: '/api/codeFile/' + localStorage.getItem("WebCraftUser") +
                        '/' + this.$route.params.info,
                    headers: {
                        'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                    },
                }).then((response) => {
                    if (response.status === 200) {
                        if (response.data === null) {
                            alert("分享码错误！");
                            this.$router.push("/");
                            return;
                        }
                        this.fileId = response.data.fileId;
                        this.data = eval(response.data.fileContent);
                        this.worldWidth = eval(response.data.worldSize);
                        this.fullscreenLoading = false;
                        this.showAlert = true;
                        this.alertTitle = "加载世界成功！";
                        setTimeout(() => {
                            this.showAlert = false
                        }, 2000);
                        this.init();
                        this.animate();
                        this.addCloud();
                    }
                })
            }
        },
        methods: {
            init() {
                const container = document.getElementById('container');
                // fov — 摄像机视锥体垂直视野角度
                // aspect — 摄像机视锥体长宽比
                // near — 摄像机视锥体近端面
                // far — 摄像机视锥体远端面
                // 均使用默认参数，防止之后更改，这里先写明
                this.camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 20000);
                // 设置相机位置到地图的中心
                this.camera.position.x = 100 * Math.floor(this.worldWidth / 2);
                this.camera.position.z = 100 * Math.floor(this.worldWidth / 2);
                this.camera.position.y = getHeight(100000,
                    this.data[Math.floor(this.worldWidth / 2)][Math.floor(this.worldWidth / 2)],
                ) * 100 + 150;

                this.scene = new THREE.Scene();
                this.scene.background = new THREE.Color('rgb(135,206,250)');
                this.scene.fog = new THREE.FogExp2(0xffffff, 0.00015);

                this.loadWorld();

                // 添加环境光
                var ambientLight = new THREE.AmbientLight(0xcccccc);
                this.scene.add(ambientLight);
                // 添加直射光线，模拟日照
                var directionalLight = new THREE.DirectionalLight(0xffffff, 0.9);
                directionalLight.position.set(1, 1, 0.5).normalize();
                this.scene.add(directionalLight);

                this.renderer = new THREE.WebGLRenderer();
                this.renderer.setPixelRatio(window.devicePixelRatio);
                this.renderer.setSize(window.innerWidth, window.innerHeight);
                container.appendChild(this.renderer.domElement);

                this.controls = new FirstPersonControls(this.scene, this.camera,
                    this.renderer.domElement, this.data, this.objects, this.worldWidth,
                    this.escHandler, this.boxHelper
                );

                this.clock = new THREE.Clock();

                // 设置性能监控显示
                this.status = new Stats();
                container.appendChild(this.status.dom);

            },
            generateHeight(width) {
                // 高度恒定为30
                for (let x = 0; x < width; x++) {
                    const temp = [];
                    for (let z = 0; z < width; z++) {
                        temp.push([
                            {
                                start: 0,
                                end: 30,
                                type: 0
                            }
                        ])
                    }
                    this.data.push(temp);
                }
                // 随机生成一棵树
                if (width > 8) {
                    // 最外层叶子
                    let i = 1;
                    for (let j = 1; j < 6; j++) {
                        this.data[i][j].push({
                            start: 35,
                            end: 35,
                            type: 7
                        });
                    }
                    for (let j = 1; j < 6; j++) {
                        this.data[j][i].push({
                            start: 35,
                            end: 35,
                            type: 7
                        });
                    }
                    i = 5;
                    for (let j = 1; j < 6; j++) {
                        this.data[i][j].push({
                            start: 35,
                            end: 35,
                            type: 7
                        });
                    }
                    for (let j = 1; j < 6; j++) {
                        this.data[j][i].push({
                            start: 35,
                            end: 35,
                            type: 7
                        });
                    }
                    i = 2;
                    for (let j = 2; j < 5; j++) {
                        this.data[i][j].push({
                            start: 35,
                            end: 36,
                            type: 7
                        });
                    }
                    for (let j = 2; j < 5; j++) {
                        this.data[j][i].push({
                            start: 35,
                            end: 36,
                            type: 7
                        });
                    }
                    i = 4;
                    for (let j = 2; j < 5; j++) {
                        this.data[i][j].push({
                            start: 35,
                            end: 36,
                            type: 7
                        });
                    }
                    for (let j = 2; j < 5; j++) {
                        this.data[j][i].push({
                            start: 35,
                            end: 36,
                            type: 7
                        });
                    }
                    this.data[3][3].push({
                        start: 31,
                        end: 36,
                        type: 5
                    });
                    this.data[3][3].push({
                        start: 37,
                        end: 37,
                        type: 7
                    });
                }
            },
            animate() {
                requestAnimationFrame(this.animate);
                this.controls.update(this.clock.getDelta());
                this.renderer.render(this.scene, this.camera);
                this.status.update();
            },
            loadWorld() {
                for (var z = 0; z < this.worldWidth; z++) {
                    for (var x = 0; x < this.worldWidth; x++) {
                        let heightArray = this.data[x][z];
                        for (let i = 0; i < heightArray.length; i++) {
                            for (let j = heightArray[i].start; j <= heightArray[i].end; j++) {
                                if (this.shouldDisplay(x, j, z)) {
                                    let box = createBox(
                                        x * 100,
                                        j * 100,
                                        z * 100, heightArray[i].type);
                                    this.scene.add(box);
                                    this.objects.push(box);
                                }
                            }

                        }
                    }
                }
            },
            pauseViewChange() {
                this.controls.lockView();
            },
            recoverViewChange() {
                this.controls.releaseView();
            },
            escHandler() {
                // 解除pointer lock的时候
                if (document.pointerLockElement !== document.body) {
                    this.pauseViewChange();
                    this.menuShow = true;
                }
            },
            closeMenu() {
                this.recoverViewChange();
                this.menuShow = false;
            },
            createNewWorld() {
                this.fullscreenLoading = true;
                this.generateHeight(this.worldWidth);
                this.$axios({
                    method: 'post',
                    url: '/api/create',
                    headers: {
                        'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                    },
                    data: {
                        username: localStorage.getItem("WebCraftUser"),
                        filename: this.filename,
                        fileContent: JSON.stringify(this.data),
                        worldSize: this.worldWidth
                    }
                }).then((response) => {
                    if (response.status === 200) {
                        this.fullscreenLoading = false;
                        this.showAlert = true;
                        this.alertTitle = "加载世界成功！";
                        this.fileId = parseInt(response.data);
                        console.log(this.fileId);
                        setTimeout(() => {
                            this.showAlert = false
                        }, 2000);
                    }
                })
            },
            createDataHandler(x, y, z, type) {
                let heightArray = this.data[x][z];
                let arrayLength = heightArray.length;
                for (let i = 0; i < arrayLength; i++) {
                    if (i + 1 === arrayLength) {
                        if (heightArray[i].type === type && y === heightArray[i].end + 1) {
                            heightArray[i].end += 1;
                        } else {
                            heightArray.push({
                                start: y,
                                end: y,
                                type: type
                            });
                        }
                        this.createMusic(type);
                        this.modified = true;
                    } else {
                        if (heightArray[i].end < y && y < heightArray[i + 1].start) {
                            // 在已有的上面放置方块
                            if (heightArray[i] + 1 === y && heightArray[i].type === type) {
                                heightArray[i].end += 1;
                            } else if (heightArray[i + 1].start - 1 === y && heightArray[i+1].type === type) {
                                heightArray[i + 1].start -= 1;
                            } else {
                                // 通过四周进行悬空的方块或者不同类型的方块
                                this.data[x][z].splice(i+1, 0, {
                                    start: y,
                                    end: y,
                                    type: type
                                })
                            }
                            this.createMusic(type);
                            this.modified = true;
                            break;
                        }
                    }
                }
            },
            removeDataHandler(x, y, z) {
                let heightArray = this.data[x][z];
                for (let i = 0; i < heightArray.length; i++) {
                    // 方块一定属于某个方块段之内
                    if (heightArray[i].start <= y && y <= heightArray[i].end) {
                        let currentType = heightArray[i].type;
                        // 方块段可以移除
                        if (heightArray[i].start === heightArray[i].end) {
                            heightArray.splice(i, 1);
                        } else if (heightArray[i].start === y) {
                            heightArray[i].start += 1;
                        } else if (heightArray[i].end === y) {
                            heightArray[i].end -= 1;
                        } else {
                            let tempEnd = heightArray[i].end;
                            let tempType = heightArray[i].type;
                            heightArray.splice(i + 1, 0, {
                                start: y + 1,
                                end: tempEnd,
                                type: tempType
                            });
                            heightArray[i].end = y - 1;
                        }
                        if (currentType === 4) {
                            this.removeMusic(20);
                        } else {
                            this.removeMusic(currentType);
                        }
                        this.modified = true;
                    }
                }
                if (x - 1 >= 0 &&
                    !this.isBlockDisplayed(x - 1, y, z)) {
                    let currentBlockType = this.isBlockExist(x - 1, y, z);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            (x - 1) * 100,
                            y * 100,
                            z * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
                if (z - 1 >= 0 &&
                    !this.isBlockDisplayed(x, y, z - 1)) {
                    let currentBlockType = this.isBlockExist(x, y, z - 1);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            x * 100,
                            y * 100,
                            (z - 1) * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
                if (x + 1 < this.worldWidth &&
                    !this.isBlockDisplayed(x + 1, y, z)) {
                    let currentBlockType = this.isBlockExist(x + 1, y, z);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            (x + 1) * 100,
                            y * 100,
                            z * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
                if (z + 1 < this.worldWidth &&
                    !this.isBlockDisplayed(x, y, z + 1)) {
                    let currentBlockType = this.isBlockExist(x, y, z + 1);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            x * 100,
                            y * 100,
                            (z + 1) * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
                if (!this.isBlockDisplayed(x, y + 1, z)) {
                    let currentBlockType = this.isBlockExist(x, y + 1, z);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            x * 100,
                            (y + 1) * 100,
                            z * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
                if (!this.isBlockDisplayed(x, y - 1, z)) {
                    let currentBlockType = this.isBlockExist(x, y - 1, z);
                    if (currentBlockType !== -1) {
                        let newBox = createBox(
                            x * 100,
                            (y - 1) * 100,
                            z * 100, currentBlockType);
                        this.scene.add(newBox);
                        this.objects.push(newBox);
                    }
                }
            },
            shouldDisplay(x, y, z) {
                let x1 = this.isBlockExist(x - 1, y, z);
                if (x1 === -1 || x1 === 4 || x1 >= 7) {
                    return true;
                }
                let x2 = this.isBlockExist(x + 1, y, z);
                if (x2 === -1 || x2 === 4 || x2 >= 7) {
                    return true;
                }
                let y1 = this.isBlockExist(x, y - 1, z);
                if (y1 === -1 || y1 === 4 || y1 >= 7) {
                    return true;
                }
                let y2 = this.isBlockExist(x, y + 1, z);
                if (y2 === -1 || y2 === 4 || y2 >= 7) {
                    return true;
                }
                let z1 = this.isBlockExist(x, y, z - 1);
                if (z1 === -1 || z1 === 4 || z1 >= 7) {
                    return true;
                }
                let z2 = this.isBlockExist(x, y, z + 1);
                return z2 === -1 || z2 === 4 || z2 >= 7;
            },
            isBlockExist(x, y, z) {
                if (x < 0 || x >= this.worldWidth || z < 0 || z >= this.worldWidth) {
                    return 12;
                }
                let result = -1;
                let heightArray = this.data[x][z];
                for (let i = 0; i < heightArray.length; i++) {
                    if (heightArray[i].start <= y && y <= heightArray[i].end) {
                        result = heightArray[i].type;
                    }
                }
                return result;
            },
            isBlockDisplayed(x, y, z) {
                for (let object of this.objects) {
                    if (Math.floor(object.position.x / 100) === x &&
                        Math.floor(object.position.y / 100) === y &&
                        Math.floor(object.position.z / 100) === z
                    ) {
                        return true;
                    }
                }
                return false;
            },
            createModeHandler(mode) {
                if (mode) {
                    this.alertTitle = "创造模式开启！";
                    this.showAlert = true;
                    setTimeout(() => {
                        this.showAlert = false;
                    }, 2000);
                } else {
                    this.alertTitle = "创造模式关闭！";
                    this.showAlert = true;
                    setTimeout(() => {
                        this.showAlert = false;
                    }, 2000);
                }
            },
            onMouseWheelHandler(event) {
                if (event.wheelDelta < 0) {
                    this.controls.boxType = (this.controls.boxType + 1) % 11;
                } else {
                    this.controls.boxType = (this.controls.boxType + 10) % 11;
                }
                this.blockUrl = this.blockerList[this.controls.boxType];
            },
            saveWorld() {
                if (this.modified) {
                    this.$axios({
                        method: 'post',
                        url: '/api/save',
                        headers: {
                            'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                        },
                        data: {
                            fileId: this.fileId,
                            fileContent: JSON.stringify(this.data)
                        }
                    }).then((response) => {
                        if (response.status === 200) {
                            this.modified = false;
                            this.showAlert = true;
                            this.alertTitle = "保存成功！";
                            setTimeout(() => {
                                this.showAlert = false
                            }, 2000);
                        }
                    })
                } else {
                    this.showAlert = true;
                    this.alertTitle = "无新的内容！";
                    setTimeout(() => {
                        this.showAlert = false
                    }, 2000);
                }
            },
            returnToMainPage() {
                if (this.modified) {
                    this.confirmShow = true;
                } else {
                    this.$router.push("/");
                }
            },
            returnToGame() {
                this.recoverViewChange();
                this.menuShow = false;
            },
            confirmReturn() {
                this.$router.push("/");
            },
            closeConfirm() {
                this.recoverViewChange();
                this.confirmShow = false;
            },
            addCloud() {
                let material = new THREE.MeshLambertMaterial({
                    transparent: true,
                    opacity: 0.8,
                    color: 0xFFFFFF,
                    side: THREE.DoubleSide
                });
                // 将所有的云merge到一起可以提高性能
                let cloudLayer = new THREE.BoxGeometry(0, 0, 0);
                for (let x = -100; x <= 100; x += 20) {
                    for (let z = -100; z <= 100; z += 20) {
                        let cloud = new THREE.Mesh(
                            new THREE.BoxGeometry(Math.round(Math.random() * 10) * 100, 100,
                                Math.round(Math.random() * 10) * 100),
                            material);
                        cloud.position.x = x * 100 - Math.round(Math.random() * 10) * 100;
                        cloud.position.z = z * 100 - Math.round(Math.random() * 10) * 100;
                        cloud.position.y = 5000;
                        cloudLayer.mergeMesh(cloud);
                    }
                }
                this.scene.add(new THREE.Mesh(cloudLayer, material));
            },
            copyShareCode() {
                this.$axios({
                    method: 'get',
                    url: '/api/code/' + this.fileId,
                    headers: {
                        'Authorization': 'bearer ' + localStorage.getItem("WebCraftToken")
                    }
                }).then((response) => {
                    if (response.status === 200) {
                        this.$copyText(response.data)
                            .then(function () {
                                alert("复制分享码成功！");
                                }, function () {
                                alert("复制分享码失败！");
                                }
                            );
                    }
                });
            },
            createMusic(type) {
                if (type === 0 || type === 2) {
                    new Audio('/music/dirt.mp3').play();
                } else if (type < 7) {
                    new Audio('/music/wood.mp3').play();
                }
            },
            removeMusic(type) {
                if (type === 0 || type === 2) {
                    new Audio('/music/dirt1.mp3').play();
                } else if (type < 7) {
                    new Audio('/music/wood1.mp3').play();
                } else if (type === 20) {
                    new Audio('/music/glass.mp3').play();
                }
            }
        },
    }
</script>

<style>
    body {
        background-color: #fff;
        color: #61443e;
    }

    .cross {
        position: absolute;
        z-index: 1;
        margin: auto;
        width: 40px;
        height: 40px;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        user-select: none;

    }

    .blockerImg {
        position: absolute;

        bottom: 0px;
        left: 5%;

        z-index: 4;
        height: 100px;
        width: 100px;
        margin: 10px;
        user-select: none;
    }

    .menu {
        text-align: center;
    }

    .el-dialog__header {
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
    }

    .el-dialog__title {
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
        font-family: Minecraft;
        color: white;
        font-size: 30px;
    }

    .el-dialog__body {
        background-image: url('http://charliecowan.co.uk/mcbuttongenerator/button_center.png');
        background-repeat: repeat;
    }

    .menu .MineCraftButton {
        width: 100px;
        display: inline-block;
    }

</style>
