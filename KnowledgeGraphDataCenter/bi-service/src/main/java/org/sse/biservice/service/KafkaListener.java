package org.sse.biservice.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

@Slf4j
@Component
public class KafkaListener {

    @Autowired
    ESservice eSservice;

    @org.springframework.kafka.annotation.KafkaListener(topics = "biTopic")
    public void onMessage(String message) {
        log.info(message);
        String[] properList = message.split("/");
        eSservice.insert(properList[0], properList[1]);
    }
}
