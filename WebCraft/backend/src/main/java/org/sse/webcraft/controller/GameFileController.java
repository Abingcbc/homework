package org.sse.webcraft.controller;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.sse.webcraft.mapper.GameFileMapper;
import org.sse.webcraft.model.GameFile;
import org.sse.webcraft.model.ShareFile;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@Slf4j
@RestController
public class GameFileController {

    @Autowired
    GameFileMapper gameFileMapper;

    @PostMapping("/create")
    public int createGameFile(@RequestBody GameFile gameFile,
                             HttpServletResponse response) {
        log.info(gameFile.getUsername());
        gameFileMapper.createNewGameFile(gameFile);
        return gameFile.getFileId();
    }

    @GetMapping("/file/{username}/{fileId}")
    public GameFile loadGameFile(@PathVariable String username,
                             @PathVariable int fileId) {
        return gameFileMapper.getGameFileByFileId(fileId);
    }

    @GetMapping("/fileList/{username}")
    public List<GameFile> loadGameFileList(@PathVariable String username) {
        return gameFileMapper.getGameFileListWithoutContent(username);
    }

    @PostMapping("/save")
    public void saveGameFile(@RequestBody GameFile gameFile) {
        gameFileMapper.updateGameFileContent(gameFile.getFileContent(),
                gameFile.getFileId());
    }

    @PostMapping("/delete/{username}/{fileId}")
    public void deleteGameFile(@PathVariable String username,
                               @PathVariable int fileId) {
        gameFileMapper.deleteGameFile(fileId);
    }

    @GetMapping("/code/{fileId}")
    public String getFileShareCode(@PathVariable int fileId) {
        GameFile gameFile = gameFileMapper.getGameFileByFileId(fileId);
        ShareFile shareFile = new ShareFile();
        shareFile.setFilename(gameFile.getFilename());
        shareFile.setFileContent(gameFile.getFileContent());
        shareFile.setWorldSize(gameFile.getWorldSize());
        gameFileMapper.createShareFile(shareFile);
        BASE64Encoder encoder = new BASE64Encoder();
        String result = encoder.encode(String.valueOf(shareFile.getFileId()).getBytes());
        log.info(shareFile.getFileId() + " " + result);
        return result;
    }

    @GetMapping("/codeFile/{username}/{code}")
    public GameFile getFileByShareCode(@PathVariable String username,
                                       @PathVariable String code) {
        BASE64Decoder decoder = new BASE64Decoder();
        int fileId = 0;
        try {
            fileId = Integer.parseInt(new String(decoder.decodeBuffer(code)));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        ShareFile shareFile = gameFileMapper.getShareFileByFileId(fileId);
        GameFile gameFile = new GameFile();
        gameFile.setFilename(shareFile.getFilename());
        gameFile.setFileContent(shareFile.getFileContent());
        gameFile.setWorldSize(shareFile.getWorldSize());
        gameFile.setUsername(username);
        gameFileMapper.createNewGameFile(gameFile);
        return gameFile;
    }
}
