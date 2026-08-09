package com.codedock.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Value("${codedock.docker.socket}")
    private String dockerSocket;

    @Value("${codedock.execution.timeout-seconds}")
    private int executionTimeoutSeconds;

    @Value("${codedock.execution.memory-limit-mb}")
    private int executionMemoryLimitMb;

    public String getDockerSocket() {
        return dockerSocket;
    }

    public int getExecutionTimeoutSeconds() {
        return executionTimeoutSeconds;
    }

    public int getExecutionMemoryLimitMb() {
        return executionMemoryLimitMb;
    }
}