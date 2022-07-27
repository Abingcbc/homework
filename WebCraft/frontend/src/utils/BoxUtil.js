import * as THREE from "three";
import {Mesh} from "three";

var textureLoader = new THREE.TextureLoader();

const loadMaterials = function (type) {
    switch (type) {
        case 0: // 泥土块
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                })
            ];
        case 1: // 方砖
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick.png')
                })
            ];
        case 2: // 草块
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/grass_dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/grass_dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/grass.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/grass_dirt.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/grass_dirt.png')
                })
            ];
        case 3: // 石块
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/stone.png')
                })
            ];
        case 4: // 玻璃
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/glass.png'),
                    transparent: true
                })
            ];
        case 5: // 木头
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_side.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_side.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_top.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_top.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_side.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/tree_side.png')
                })
            ];
        case 6: // 红砖
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/brick_brown.png')
                })
            ];
        case 7: // 叶子
            return [
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                }),
                new THREE.MeshLambertMaterial({
                    map: textureLoader.load('/textures/leaves.png'),
                    transparent: true
                })
            ];
        case 8: // 草丛
            return [new THREE.MeshLambertMaterial({
                map: textureLoader.load('/textures/tallgrass.png'),
                transparent: true,
                side: THREE.DoubleSide
            }),
                new THREE.MeshBasicMaterial({
                    transparent: true,
                    opacity: 0
                })
            ];
        case 9: // 玫瑰花
            return [new THREE.MeshLambertMaterial({
                map: textureLoader.load('/textures/rose.png'),
                transparent: true,
                side: THREE.DoubleSide
            }),
                new THREE.MeshBasicMaterial({
                    transparent: true,
                    opacity: 0
                })
            ];
        case 10: // 郁金香
            return [new THREE.MeshLambertMaterial({
                map: textureLoader.load('/textures/tulip.png'),
                transparent: true,
                side: THREE.DoubleSide
            }),
                new THREE.MeshBasicMaterial({
                    transparent: true,
                    opacity: 0
                })
            ]

    }
};

const createBox = function (x, y, z, type) {
    if (type < 8) {
        let geometry = new THREE.BoxGeometry(100, 100, 100);
        let materials = loadMaterials(type);
        let result = new THREE.Mesh( geometry, materials );
        result.position.x = x;
        result.position.y = y;
        result.position.z = z;
        return result;
    } else {
        let geometry = new THREE.Geometry();
        let boxSize = 100;
        geometry.vertices = [
            new THREE.Vector3(boxSize / 2, -boxSize / 2, boxSize / 2),
            new THREE.Vector3(boxSize / 2, -boxSize / 2, -boxSize / 2),
            new THREE.Vector3(-boxSize / 2, -boxSize / 2, -boxSize / 2),
            new THREE.Vector3(-boxSize / 2, -boxSize / 2, boxSize / 2),

            new THREE.Vector3(boxSize / 2, boxSize / 2, boxSize / 2),
            new THREE.Vector3(boxSize / 2, boxSize / 2, -boxSize / 2),
            new THREE.Vector3(-boxSize / 2, boxSize / 2, -boxSize / 2),
            new THREE.Vector3(-boxSize / 2, boxSize / 2, boxSize / 2),
        ];
        geometry.faces = [
            //内部交叉面
            new THREE.Face3(0, 2, 6),
            new THREE.Face3(0, 6, 4),
            new THREE.Face3(3, 1, 5),
            new THREE.Face3(3, 5, 7),
            //外部方块面
            new THREE.Face3(0, 3, 2),
            new THREE.Face3(0, 2, 1),
            new THREE.Face3(0, 7, 3),
            new THREE.Face3(0, 4, 7),
            new THREE.Face3(0, 1, 5),
            new THREE.Face3(0, 5, 4),
            new THREE.Face3(6, 4, 5),
            new THREE.Face3(6, 7, 4),
            new THREE.Face3(6, 5, 1),
            new THREE.Face3(6, 1, 2),
            new THREE.Face3(6, 3, 7),
            new THREE.Face3(6, 2, 3),
        ];
        for (let faceIndex in geometry.faces) {
            if (faceIndex < 4) {
                geometry.faces[faceIndex].materialIndex = 0;
            } else {
                geometry.faces[faceIndex].materialIndex = 1;
            }
        }
        let imagePoint = [
            new THREE.Vector2(0, 0), // 左下角
            new THREE.Vector2(1, 0), // 右下角
            new THREE.Vector2(1, 1), // 右上角
            new THREE.Vector2(0, 1), // 左上角
        ];
        geometry.faceVertexUvs[0][0] = [imagePoint[0], imagePoint[1], imagePoint[2]];
        geometry.faceVertexUvs[0][1] = [imagePoint[0], imagePoint[2], imagePoint[3]];
        geometry.faceVertexUvs[0][2] = geometry.faceVertexUvs[0][0];
        geometry.faceVertexUvs[0][3] = geometry.faceVertexUvs[0][1];
        // 透明，所以不需要贴图
        for (let i = 4; i < 16; i++) {
            geometry.faceVertexUvs[0][i] = [new THREE.Vector2(), new THREE.Vector2(), new THREE.Vector2()]
        }
        geometry.computeFaceNormals();
        let result = new Mesh(geometry,
            loadMaterials(type));
        result.position.x = x;
        result.position.y = y;
        result.position.z = z;
        return result;
    }
};

const addNewBox = function (selectedBox, createDataHandler, type, cameraPosition) {
    let normal = selectedBox.face.normal;
    let rotate = selectedBox.object.rotation;
    let position = selectedBox.object.position;

    if (type < 8 && !(selectedBox.object.geometry instanceof THREE.BoxGeometry)) {
        // 覆盖植物
        createDataHandler(Math.floor(position.x/100),
            Math.floor(position.y/100),
            Math.floor(position.z/100), type);
        return createBox(Math.floor(position.x/100)*100,
            Math.floor(position.y/100)*100,
            Math.floor(position.z/100)*100, type
        );
    } else {
        let offsetVector = new THREE.Vector3(normal.x, normal.y, normal.z);
        offsetVector = offsetVector.applyAxisAngle(new THREE.Vector3(0, 0, 1), rotate.z);
        offsetVector = offsetVector.applyAxisAngle(new THREE.Vector3(0, 1, 0), rotate.y);
        offsetVector = offsetVector.applyAxisAngle(new THREE.Vector3(1, 0, 0), rotate.x);
        offsetVector.floor();
        // 只有在点击上顶面的时候才能创建植物
        if (type >= 8 && offsetVector.y !== 1) {
            return null;
        }
        // 创建方块的位置与相机相同
        // 这里x 和 z 都要取round，y 要取floor的原因是y大于targetPosition 150，
        // 所以如果四舍五入会导致相机向上偏移一格
        if (Math.round(cameraPosition.x/100) === Math.round((position.x + offsetVector.x * 100)/100) &&
            Math.floor(cameraPosition.y/100) === Math.floor((position.y + offsetVector.y * 100)/100) &&
            Math.round(cameraPosition.z/100) === Math.round((position.z + offsetVector.z * 100)/100)
        ) {
            return null;
        }

        createDataHandler(Math.floor((position.x + offsetVector.x * 100)/100),
            Math.floor((position.y + offsetVector.y * 100)/100),
            Math.floor((position.z + offsetVector.z * 100)/100), type);
        return createBox(Math.floor((position.x + offsetVector.x * 100)/100)*100,
            Math.floor((position.y + offsetVector.y * 100)/100)*100,
            Math.floor((position.z + offsetVector.z * 100)/100)*100, type
        );
    }
};

export { createBox, addNewBox }
