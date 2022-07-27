package org.sse.biservice.service;

import com.alibaba.fastjson.JSONObject;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.index.query.QueryBuilder;
import org.elasticsearch.index.query.QueryBuilders;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.sse.biservice.model.Entity;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ESservice {

    @Autowired
    RestHighLevelClient restHighLevelClient;

    public List<Entity> searchSinger(String keyword) {
        SearchRequest request = new SearchRequest("bi");
        SearchSourceBuilder builder = new SearchSourceBuilder();
        builder.query(QueryBuilders.matchQuery("name", keyword));
        builder.size(20);
        request.source(builder);
        try {
            SearchResponse response = restHighLevelClient.search(request, RequestOptions.DEFAULT);
            SearchHit[] hits = response.getHits().getHits();
            List<Entity> res = new ArrayList<>(hits.length);
            for (SearchHit hit : hits) {
                res.add(JSONObject.parseObject(hit.getSourceAsString(), Entity.class));
            }
            return res;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public void insert(String type, String name) {
        IndexRequest request = new IndexRequest("bi");
        Map<String, String> sourceMap = new HashMap<>();
        sourceMap.put("name", name);
        sourceMap.put("type", type);
        request.source(sourceMap, XContentType.JSON);
        try {
            restHighLevelClient.index(request, RequestOptions.DEFAULT);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
