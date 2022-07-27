FROM java:8
VOLUME /tmp
COPY target/webcraft-0.0.1-SNAPSHOT.jar webcraft.jar
RUN bash -c "touch /webcraft.jar"
EXPOSE 10010
ENTRYPOINT ["java","-jar","webcraft.jar"]