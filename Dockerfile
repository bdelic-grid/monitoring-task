FROM alpine:3.21

WORKDIR /app

RUN apk add openjdk17
COPY ./spring-petclinic.jar ./petclinic.jar

RUN wget https://github.com/prometheus/jmx_exporter/releases/download/1.2.0/jmx_prometheus_javaagent-1.2.0.jar
COPY ./exporter.yaml ./exporter.yaml

EXPOSE 8080
EXPOSE 12345

ENTRYPOINT ["java", "-javaagent:jmx_prometheus_javaagent-1.2.0.jar=12345:exporter.yaml", "-jar"]
CMD ["petclinic.jar"]