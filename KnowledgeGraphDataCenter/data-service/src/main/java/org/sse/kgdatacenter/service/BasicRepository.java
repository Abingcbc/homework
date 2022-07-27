package org.sse.kgdatacenter.service;

import lombok.extern.slf4j.Slf4j;
import org.neo4j.driver.*;
import org.neo4j.driver.types.Node;
import org.neo4j.driver.types.Path;
import org.neo4j.driver.types.Relationship;
import org.springframework.stereotype.Service;
import org.sse.kgdatacenter.model.BasicQueryDto;
import org.sse.kgdatacenter.model.Entity;
import org.sse.kgdatacenter.model.Relation;

import java.util.*;
import java.util.concurrent.TimeUnit;

@Service
@Slf4j
public class BasicRepository {

    private Driver driver;

    private Session session;

    BasicRepository() {
        Config config = Config.builder().withMaxConnectionPoolSize(50)
                .withConnectionAcquisitionTimeout(10, TimeUnit.SECONDS).build();
        driver = GraphDatabase.driver("bolt://localhost:7687",
                AuthTokens.basic("neo4j", "friday"),
                config);
        session = driver.session();
    }

    public BasicQueryDto queryOneEntity(String name, int jump, int limit) {
        String queryString = "match p=((a) - [r*1.."+jump+"] - (b)) " +
                "where a.name='" + name +
                "' return p limit " + limit;
        log.info(queryString);
        List<Record> result = session.run(queryString).list();
        return dtoTransform(result);
    }

    public BasicQueryDto queryTwoEntity(String name1, String name2, int type, int limit) {
        String queryString = null;
        // 最短路径
        if (type == 0) {
            queryString = "match p = shortestPath( (a) - [*] - (b) ) " +
                    "where a.name='"+name1+ "' and b.name='" + name2 +
                    "' return p limit " + limit;
        } else if (type > 0) {
            queryString = "match p=((a)-[r*1.."+type+"]-(b)) " +
                    "where a.name='" + name1 +
                    "' and b.name='" + name2 +
                    "' return p limit " + limit;
        } else {
            //全部路径
            queryString = "match p=((a)-[r*]-(b)) " +
                    "where a.name='" + name1 +
                    "' and b.name='" + name2 +
                    "' return p limit " + limit;
        }
        log.info(queryString);
        List<Record> result = session.run(queryString).list();
        return dtoTransform(result);
    }

    public void insertNewEntity(String name, String type) {
        String queryString = "create (p:" + type + "{name:'" + name + "', url:'  '}) return p";
        log.info(queryString);
        session.run(queryString);
    }

    public BasicQueryDto dtoTransform(List<Record> queryResult) {
        BasicQueryDto.BasicQueryPath basicQueryPath = new BasicQueryDto.BasicQueryPath();
        basicQueryPath.setNodes(new HashSet<>());
        basicQueryPath.setRelationships(new HashSet<>());
        int count = 1;
        for (Record record : queryResult) {
            for (Value value : record.values()) {
                Path path = value.asPath();
                Iterable<Node> nodes = path.nodes();
                Iterable<Relationship> relationships = path.relationships();
                for (Node node : nodes) {
                    Map<String, Object> map = node.asMap();
                    Entity entity = new Entity();
                    entity.setId(String.valueOf(node.id()));
                    entity.setLabels(new ArrayList<>());
                    entity.getLabels().add(node.labels().iterator().next());
                    entity.setProperties(new HashMap<>());
                    entity.getProperties().put("name", map.get("name").toString());
                    entity.getProperties().put("url", map.get("url").toString());
                    basicQueryPath.getNodes().add(entity);
                }
                for (Relationship relationship : relationships) {
                    Map<String, Object> map = relationship.asMap();
                    Relation relation = new Relation();
                    relation.setId(String.valueOf(count));
                    relation.setStartNode(String.valueOf(relationship.startNodeId()));
                    relation.setEndNode(String.valueOf(relationship.endNodeId()));
                    relation.setType(map.get("type").toString());
                    basicQueryPath.getRelationships().add(relation);
                    count += 1;
                }
            }
        }
        BasicQueryDto.BasicQueryGraph basicQueryGraph = new BasicQueryDto.BasicQueryGraph();
        basicQueryGraph.setGraph(basicQueryPath);
        BasicQueryDto.BasicQueryObject basicQueryObject = new BasicQueryDto.BasicQueryObject();
        basicQueryObject.setColumns(new ArrayList<>(Arrays.asList("user", "entity")));
        basicQueryObject.setData(new ArrayList<>(Collections.singletonList(basicQueryGraph)));
        BasicQueryDto basicQueryDto = new BasicQueryDto();
        basicQueryDto.setResults(new ArrayList<>(Collections.singletonList(basicQueryObject)));
        return basicQueryDto;
    }
}
