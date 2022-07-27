FROM java:8
VOLUME /tmp
COPY target/tjmall-0.0.1-SNAPSHOT.jar tjmall.jar
RUN bash -c "touch /tjmall.jar"
EXPOSE 10010
ENTRYPOINT ["java","-jar","tjmall.jar"]