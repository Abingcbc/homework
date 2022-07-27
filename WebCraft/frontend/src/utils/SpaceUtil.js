
const isConflict = function (currentHeight, heightArray) {
    if (heightArray === undefined) {
        return true;
    }
    for (let i = 0; i < heightArray.length; i++) {
        if (((heightArray[i].start-1) * 100 <= currentHeight &&
            heightArray[i].end * 100 >= currentHeight) ||
            ((heightArray[i].start-1) * 100 <= currentHeight+100 &&
                heightArray[i].end * 100 >= currentHeight+100)
        ) {
            return heightArray[i].type < 8;
        }
    }
    return false;
};

const getHeight = function (y, heightArray) {
    if (heightArray[heightArray.length-1].end * 100 < y &&
        heightArray[heightArray.length-1].type < 8) {
        return heightArray[heightArray.length-1].end;
    }
    for (let i = 0; i < heightArray.length-1; i++) {
        if (heightArray[i].type >= 8) {
            return heightArray[i-1].end;
        }
        if (heightArray[i].end * 100 < y && y < heightArray[i+1].start * 100) {
            return heightArray[i].end;
        }
    }
};

const getBlockType = function (y, heightArray) {
    for (let i = 0; i < heightArray.length; i++) {
        if (heightArray[i].end * 100 >= y && y >= heightArray[i].start * 100) {
            return heightArray[i].type;
        }
    }
};

export { isConflict, getHeight, getBlockType};
