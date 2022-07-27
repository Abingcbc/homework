import {
    MathUtils,
    Spherical,
    Vector3,
    Raycaster, Vector2
} from "three";
import * as THREE from "three";

import {
    isConflict,
    getHeight
} from "@/utils/SpaceUtil"

import {
    addNewBox
} from "@/utils/BoxUtil";

var FirstPersonControls = function (scene, camera, domElement,
                                    data, objects, worldWidth,
                                    escHandler, boxHelper) {

    if (domElement === undefined) {
        domElement = document;
    }

    this.scene = scene;
    this.camera = camera;
    this.domElement = domElement;
    this.data = data;
    this.objects = objects;
    this.worldWidth = worldWidth;
    this.escHandler = escHandler;
    this.boxHelper = boxHelper;
    this.directRay = new Raycaster();
    this.boxType = 0;

    this.movementSpeed = 500;
    this.lookSpeed = 2;

    this.verticalMin = 0;
    this.verticalMax = Math.PI;

    this.mouseX = 0;
    this.mouseY = 0;

    this.moveForward = false;
    this.moveBackward = false;
    this.moveLeft = false;
    this.moveRight = false;
    this.createNewBox = false;
    this.removeBox = false;
    this.viewLock = false;
    this.jump = 0;
    this.minJumpHeight = 0;
    this.maxJumpHeight = 0;
    this.createMode = false;
    this.moveUp = false;
    this.moveDown = false;

    this.viewHalfX = 0;
    this.viewHalfY = 0;

    var lat = 0;
    var lon = 0;

    var lookDirection = new Vector3();
    var spherical = new Spherical();
    var target = new Vector3();

    document.body.requestPointerLock();

    if (this.domElement !== document) {

        this.domElement.setAttribute('tabindex', -1);

    }

    this.handleResize = function () {

        if (this.domElement === document) {

            this.viewHalfX = window.innerWidth / 2;
            this.viewHalfY = window.innerHeight / 2;

        } else {

            this.viewHalfX = this.domElement.offsetWidth / 2;
            this.viewHalfY = this.domElement.offsetHeight / 2;

        }

    };

    this.onMouseDown = function (event) {

        if (this.viewLock) {
            return;
        }

        if (this.domElement !== document) {
            this.domElement.focus();
        }

        event.preventDefault();
        event.stopPropagation();

        switch (event.button) {

            case 0:
                this.createNewBox = true;
                break;
            case 2:
                this.removeBox = true;
                break;

        }

    };

    this.onMouseUp = function (event) {
        if (this.viewLock) {
            return;
        }

        event.preventDefault();
        event.stopPropagation();
        switch (event.button) {
            case 0:
                this.createNewBox = false;
                break;
            case 2:
                this.removeBox = false;
                break;
        }
    };

    this.onMouseMove = function (event) {

        if (this.domElement === document) {
            if (Math.abs(event.pageX - this.viewHalfX) < 0) {
                this.mouseX = 0;
            } else {
                this.mouseX = event.pageX - this.viewHalfX;
            }
            if (Math.abs(event.pageY - this.viewHalfY) < 0) {
                this.mouseY = 0;
            } else {
                this.mouseY = event.pageY - this.viewHalfY;
            }

        } else {
            if (Math.abs(event.pageX - this.domElement.offsetLeft - this.viewHalfX) < 0) {
                this.mouseX = 0;
            } else {
                // this.mouseX = event.pageX - this.domElement.offsetLeft - this.viewHalfX;
                this.mouseX = event.movementX;
            }
            if (Math.abs(event.pageY - this.domElement.offsetTop - this.viewHalfY) < 0) {
                this.mouseY = 0;
            } else {
                // this.mouseY = event.pageY - this.domElement.offsetTop - this.viewHalfY;
                this.mouseY = event.movementY;
            }
        }

    };

    this.onKeyDown = function (event) {

        event.preventDefault();
        event.stopPropagation();

        switch (event.keyCode) {

            case 38: // up
            case 87: // W
                this.moveForward = true;
                break;

            case 37: // left
            case 65: // A
                this.moveLeft = true;
                break;

            case 40: // down
            case 83: // S
                this.moveBackward = true;
                break;

            case 39: // right
            case 68: // D
                this.moveRight = true;
                break;

            case 32: // space
                if (this.jump === 0) {
                    this.jump = 1;
                    this.maxJumpHeight = this.camera.position.y + 100;
                    this.minJumpHeight = this.camera.position.y;
                }
                break;

            case 81: // Q
                this.createMode = !this.createMode;
                // 停止跳跃
                this.jump = 0;
                this.boxHelper.createModeHandler(this.createMode);
                if (!this.createMode) {
                    this.jump = 2;
                    this.minJumpHeight = getHeight(this.camera.position.y,
                        this.data[Math.round(this.camera.position.x / 100)][Math.round(this.camera.position.z / 100)]) * 100 + 150;
                }
                break;

            case 82: // R
                if (this.createMode) {
                    this.moveUp = true;
                }
                break;

            case 70: // F
                if (this.createMode) {
                    this.moveDown = true;
                }
                break;
        }

    };

    this.onKeyUp = function (event) {

        switch (event.keyCode) {

            case 38: // up
            case 87: // W
                this.moveForward = false;
                break;

            case 37: // left
            case 65: // A
                this.moveLeft = false;
                break;

            case 40: // down
            case 83: // S
                this.moveBackward = false;
                break;

            case 39: // right
            case 68: // D
                this.moveRight = false;
                break;

            case 82: // R
                this.moveUp = false;
                break;

            case 70: // F
                this.moveDown = false;
                break;
        }

    };

    this.lookAt = function (x, y, z) {

        if (x.isVector3) {

            target.copy(x);

        } else {

            target.set(x, y, z);

        }

        this.camera.lookAt(target);

        setOrientation(this);

        return this;

    };

    this.update = function () {

        var targetPosition = new Vector3();

        return function update(delta) {
            this.handleResize();
            // 移动控制
            let actualMoveSpeed = delta * this.movementSpeed;
            if (!this.createMode && this.jump !== 0) {
                let jumpSpeed = actualMoveSpeed;
                // 上升阶段
                if (this.jump === 1) {
                    if (this.camera.position.y + jumpSpeed >= this.maxJumpHeight) {
                        this.camera.position.y = this.maxJumpHeight;
                        this.jump = 2;
                        this.maxJumpHeight = 0;
                    } else {
                        this.camera.position.y += jumpSpeed;
                    }
                } else {
                    if (this.camera.position.y - jumpSpeed <= this.minJumpHeight) {
                        this.camera.position.y = this.minJumpHeight;
                        this.jump = 0;
                    } else {
                        this.camera.position.y -= jumpSpeed;
                    }
                }
            }

            if (this.moveForward) {
                let keepY = this.camera.position.y;
                this.camera.translateZ(-(actualMoveSpeed + 20));
                let pos = this.camera.position;
                if (pos.x < 0 || pos.z < 0
                    || Math.round(pos.x / 100) >= this.worldWidth
                    || Math.round(pos.z / 100) >= this.worldWidth) {
                    this.camera.translateZ((actualMoveSpeed + 20));
                    this.camera.position.y = keepY;
                    return;
                }
                let heightArray = this.data[Math.round(pos.x / 100)][Math.round(pos.z / 100)];
                if (isConflict(pos.y - 100, heightArray)) {
                    this.camera.translateZ((actualMoveSpeed + 20));
                    this.camera.position.y = keepY;
                } else {
                    this.camera.translateZ(20);
                    if (this.createMode) {
                        this.camera.position.y = keepY;
                    } else {
                        if (this.jump !== 0) {
                            this.camera.y = keepY;
                            this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                        } else {
                            if (getHeight(pos.y, heightArray) * 100 + 150 < keepY) {
                                this.jump = 2;
                                this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                            } else {
                                this.camera.position.y = keepY;
                            }
                        }
                    }
                }
            }
            if (this.moveBackward) {
                let keepY = this.camera.position.y;
                this.camera.translateZ(actualMoveSpeed + 20);
                let pos = this.camera.position;
                if (pos.x < 0 || pos.z < 0
                    || Math.round(pos.x / 100) >= this.worldWidth
                    || Math.round(pos.z / 100) >= this.worldWidth) {
                    this.camera.translateZ(-actualMoveSpeed - 20);
                    this.camera.position.y = keepY;
                    return;
                }
                let heightArray = this.data[Math.round(pos.x / 100)][Math.round(pos.z / 100)];
                if (isConflict(pos.y - 100, heightArray)) {
                    this.camera.translateZ(-actualMoveSpeed - 20);
                    this.camera.position.y = keepY;
                } else {
                    this.camera.translateZ(-20);
                    if (this.createMode) {
                        this.camera.position.y = keepY;
                    } else {
                        if (this.jump !== 0) {
                            this.camera.y = keepY;
                            this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                        } else {
                            if (getHeight(pos.y, heightArray) * 100 + 150 < keepY) {
                                this.jump = 2;
                                this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                            } else {
                                this.camera.position.y = keepY;
                            }
                        }
                    }
                }
            }
            if (this.moveLeft) {
                let keepY = this.camera.position.y;
                this.camera.translateX(-actualMoveSpeed - 20);
                let pos = this.camera.position;
                if (pos.x < 0 || pos.z < 0
                    || Math.round(pos.x / 100) >= this.worldWidth
                    || Math.round(pos.z / 100) >= this.worldWidth) {
                    this.camera.translateX(actualMoveSpeed + 20);
                    this.camera.position.y = keepY;
                    return;
                }
                let heightArray = this.data[Math.round(pos.x / 100)][Math.round(pos.z / 100)];
                if (isConflict(pos.y - 100, heightArray)) {
                    this.camera.translateX(actualMoveSpeed + 20);
                    this.camera.position.y = keepY;
                } else {
                    this.camera.translateX(20);
                    if (this.createMode) {
                        this.camera.position.y = keepY;
                    } else {
                        if (this.jump !== 0) {
                            this.camera.y = keepY;
                            this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                        } else {
                            if (getHeight(pos.y, heightArray) * 100 + 150 < keepY) {
                                this.jump = 2;
                                this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                            } else {
                                this.camera.position.y = keepY;
                            }
                        }
                    }
                }
            }
            if (this.moveRight) {
                let keepY = this.camera.position.y;
                this.camera.translateX(actualMoveSpeed + 20);
                let pos = this.camera.position;
                if (pos.x < 0 || pos.z < 0
                    || Math.round(pos.x / 100) >= this.worldWidth
                    || Math.round(pos.z / 100) >= this.worldWidth) {
                    this.camera.translateX(-actualMoveSpeed - 20);
                    this.camera.position.y = keepY;
                    return;
                }
                let heightArray = this.data[Math.round(pos.x / 100)][Math.round(pos.z / 100)];
                if (isConflict(pos.y - 100, heightArray)) {
                    this.camera.translateX(-actualMoveSpeed - 20);
                    this.camera.position.y = keepY;
                } else {
                    this.camera.translateX(-20);
                    if (this.createMode) {
                        this.camera.position.y = keepY;
                    } else {
                        if (this.jump !== 0) {
                            this.camera.y = keepY;
                            this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                        } else {
                            if (getHeight(pos.y, heightArray) * 100 + 150 < keepY) {
                                this.jump = 2;
                                this.minJumpHeight = getHeight(pos.y, heightArray) * 100 + 150;
                            } else {
                                this.camera.position.y = keepY;
                            }
                        }
                    }
                }
            }

            // 创造模式
            if (this.moveUp) {
                if (this.boxHelper.isBlockExist(Math.round(this.camera.position.x/100),
                    Math.round((this.camera.position.y+100+delta*this.movementSpeed)/100) ,
                    Math.round(this.camera.position.z/100)) === -1)
                    this.camera.position.y += delta * this.movementSpeed;
            }
            if (this.moveDown) {
                let minHeight = getHeight(this.camera.position.y,
                    this.data[Math.round(this.camera.position.x / 100)][Math.round(this.camera.position.z / 100)]) * 100 + 150;
                if (this.camera.position.y - delta * this.movementSpeed <= minHeight) {
                    this.camera.position.y = minHeight;
                } else {
                    this.camera.position.y -= delta * this.movementSpeed;
                }
            }

            //视角控制
            if (!this.viewLock) {
                var actualLookSpeed = delta * this.lookSpeed;
                lon -= this.mouseX * actualLookSpeed;
                lat -= this.mouseY * actualLookSpeed;
                lat = Math.max(-85, Math.min(85, lat));
                var phi = MathUtils.degToRad(90 - lat);
                var theta = MathUtils.degToRad(lon);
                phi = MathUtils.mapLinear(phi, 0, Math.PI, this.verticalMin, this.verticalMax);
                var position = this.camera.position;
                targetPosition.setFromSphericalCoords(1, phi, theta).add(position);
                this.camera.lookAt(targetPosition);
                this.mouseX = 0;
                this.mouseY = 0;
            }

            // 创建控制
            if (this.createNewBox || this.removeBox) {
                let type = 0;
                if (this.removeBox) {
                    type = 1;
                }
                // 避免单次点击多次检测
                this.createNewBox = false;
                this.removeBox = false;
                this.directRay.setFromCamera(new Vector2(0, 0), this.camera);
                let selectedBoxes = this.directRay.intersectObjects(this.objects);
                if (selectedBoxes.length > 0) {
                    let selectedBox;
                    // 有可能是在植物中点击的
                    if (Math.round(this.camera.position.x/100) === Math.round(selectedBoxes[0].object.position.x/100) &&
                        Math.floor(this.camera.position.y/100) === Math.floor(selectedBoxes[0].object.position.y/100) &&
                        Math.round(this.camera.position.z/100) === Math.round(selectedBoxes[0].object.position.z/100)
                    ) {
                        for (let i = 1; i < selectedBoxes.length; i++) {
                            if (!selectedBoxes[0].object.position.equals(selectedBoxes[i].object.position)) {
                                if (selectedBoxes[0].object.position.x !== selectedBoxes[i].object.position.x ||
                                selectedBoxes[0].object.position.z !== selectedBoxes[i].object.position.z) {
                                    selectedBox = selectedBoxes[i];
                                }
                                break;
                            }
                        }
                        if (!selectedBox) {
                            return;
                        }
                    } else {
                        selectedBox = selectedBoxes[0];
                    }
                    if (selectedBox && selectedBox.distance <= 500) {
                        // 左键点击，创建新的方块
                        if (type === 0) {
                            if (this.boxType >= 8) {
                                let groundType = this.boxHelper.isBlockExist(
                                    Math.floor(selectedBox.object.position.x / 100),
                                    Math.floor(selectedBox.object.position.y / 100),
                                    Math.floor(selectedBox.object.position.z / 100));
                                if (groundType !== 0 && groundType !== 2) {
                                    return;
                                }
                            }
                            let newBox = addNewBox(selectedBox,
                                this.boxHelper.createDataHandler, this.boxType, this.camera.position);
                            if (newBox === null) {
                                return;
                            }
                            if (this.boxType < 8 && !(selectedBox.object.geometry instanceof THREE.BoxGeometry)) {
                                let index = this.objects.findIndex(
                                    e => e.id === selectedBox.object.id);
                                this.objects.splice(index, 1);
                                this.boxHelper.removeDataHandler(
                                    Math.floor(selectedBox.object.position.x / 100),
                                    Math.floor(selectedBox.object.position.y / 100),
                                    Math.floor(selectedBox.object.position.z / 100));
                                this.scene.remove(this.scene.getObjectById(selectedBox.object.id));
                            }
                            if (this.minJumpHeight < newBox.position.y+150) {
                                this.minJumpHeight = newBox.position.y+150;
                            }
                            this.scene.add(newBox);
                            this.objects.push(newBox);
                        } else {
                            // 挖到底了。。。不允许再挖了
                            if (selectedBox.object.position.y < 200) {
                                return;
                            }
                            let index = this.objects.findIndex(
                                e => e.id === selectedBox.object.id);
                            this.objects.splice(index, 1);
                            this.boxHelper.removeDataHandler(
                                Math.floor(selectedBox.object.position.x / 100),
                                Math.floor(selectedBox.object.position.y / 100),
                                Math.floor(selectedBox.object.position.z / 100));
                            this.scene.remove(this.scene.getObjectById(selectedBox.object.id));
                            if (Math.round(selectedBox.object.position.x/100) === Math.round(this.camera.position.x/100) &&
                            Math.round(selectedBox.object.position.z/100) === Math.round(this.camera.position.z/100)) {
                                if (this.jump === 0) {
                                    this.jump = 2;
                                }
                                this.minJumpHeight = getHeight(this.camera.position.y,
                                    this.data[Math.round(selectedBox.object.position.x/100)][Math.round(selectedBox.object.position.z/100)]) *100 + 150;
                            }
                        }
                    }
                }
            }
        };
    }();

    this.lockView = () => {
        this.viewLock = true;
        document.exitPointerLock();
    };

    this.releaseView = () => {
        this.viewLock = false;
        document.body.requestPointerLock();
    };

    function contextmenu(event) {
        event.preventDefault();
    }

    var _onMouseMove = bind(this, this.onMouseMove);
    var _onMouseDown = bind(this, this.onMouseDown);
    var _onMouseUp = bind(this, this.onMouseUp);
    var _onKeyDown = bind(this, this.onKeyDown);
    var _onKeyUp = bind(this, this.onKeyUp);

    this.domElement.addEventListener('contextmenu', contextmenu, false);
    document.addEventListener('mousemove', _onMouseMove, false);
    document.addEventListener('mousedown', _onMouseDown, false);
    document.addEventListener('mouseup', _onMouseUp, false);
    document.addEventListener('pointerlockchange', escHandler, false );

    document.addEventListener('mousewheel', this.boxHelper.onMouseWheelHandler);
    window.addEventListener('keydown', _onKeyDown, false);
    window.addEventListener('keyup', _onKeyUp, false);

    this.dispose = function() {
        this.domElement.removeEventListener('contextmenu', contextmenu, false);
        document.removeEventListener('mousemove', _onMouseMove, false);
        document.removeEventListener('mousedown', _onMouseDown, false)
        document.removeEventListener('mouseup', _onMouseUp, false)
        document.removeEventListener('pointerlockchange', escHandler, false )
        document.removeEventListener('mousewheel', this.boxHelper.onMouseWheelHandler);
        window.removeEventListener('keydown', _onKeyDown, false);
        window.removeEventListener('keyup', _onKeyUp, false);
        document.exitPointerLock();
    }

    function bind(scope, fn) {
        return function () {
            fn.apply(scope, arguments);
        };
    }

    function setOrientation(controls) {

        var quaternion = controls.camera.quaternion;

        lookDirection.set(0, 0, -1).applyQuaternion(quaternion);
        spherical.setFromVector3(lookDirection);

        lat = 90 - MathUtils.radToDeg(spherical.phi);
        lon = MathUtils.radToDeg(spherical.theta);

    }

    this.handleResize();


    setOrientation(this);

};

export {FirstPersonControls};
