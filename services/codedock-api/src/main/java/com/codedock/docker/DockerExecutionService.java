package com.codedock.docker;

import com.codedock.compiler.LanguageCompiler;
import com.codedock.config.AppConfig;
import com.codedock.exception.ExecutionException;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;

@Service
public class DockerExecutionService {

    private final AppConfig appConfig;

    public DockerExecutionService(AppConfig appConfig) {
        this.appConfig = appConfig;
    }

    public ExecutionResult execute(LanguageCompiler compiler, Path tempDirPath) {
        String image = compiler.getDockerImage();
        int memoryLimit = appConfig.getExecutionMemoryLimitMb();
        int timeoutSeconds = appConfig.getExecutionTimeoutSeconds();

        StringBuilder stdout = new StringBuilder();
        StringBuilder stderr = new StringBuilder();
        int exitCode = 0;
        long executionTime = 0;

        try {
            if (compiler.isCompiled()) {
                String compileCmd = compiler.getCompileCommand();
                ProcessBuilder compilePb = new ProcessBuilder(
                        "docker", "run", "--rm",
                        "-v", tempDirPath.toAbsolutePath().toString() + ":/code",
                        "-w", "/code",
                        "--memory=" + memoryLimit + "m",
                        "--cpus=1",
                        image,
                        "/bin/sh", "-c", compileCmd
                );

                Process compileProcess = compilePb.start();
                if (!compileProcess.waitFor(timeoutSeconds, TimeUnit.SECONDS)) {
                    compileProcess.destroyForcibly();
                    return ExecutionResult.builder()
                            .stdout("")
                            .stderr("Compilation timed out after " + timeoutSeconds + " seconds")
                            .exitCode(-1)
                            .executionTime(TimeUnit.MILLISECONDS.convert(timeoutSeconds, TimeUnit.SECONDS))
                            .build();
                }

                int compileExitCode = compileProcess.exitValue();
                if (compileExitCode != 0) {
                    StringBuilder compileError = new StringBuilder();
                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(compileProcess.getErrorStream()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            compileError.append(line).append("\n");
                        }
                    }
                    try (BufferedReader reader = new BufferedReader(new InputStreamReader(compileProcess.getInputStream()))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            compileError.append(line).append("\n");
                        }
                    }
                    return ExecutionResult.builder()
                            .stdout("")
                            .stderr("Compilation failed:\n" + compileError.toString())
                            .exitCode(compileExitCode)
                            .executionTime(0L)
                            .build();
                }
            }

            String runCmd = compiler.getRunCommand();
            ProcessBuilder runPb = new ProcessBuilder(
                    "docker", "run", "--rm",
                    "-v", tempDirPath.toAbsolutePath().toString() + ":/code",
                    "-w", "/code",
                    "--memory=" + memoryLimit + "m",
                    "--cpus=1",
                    image,
                    "/bin/sh", "-c", runCmd
            );

            long startTime = System.currentTimeMillis();
            Process runProcess = runPb.start();

            if (!runProcess.waitFor(timeoutSeconds, TimeUnit.SECONDS)) {
                runProcess.destroyForcibly();
                return ExecutionResult.builder()
                        .stdout("")
                        .stderr("Execution timed out after " + timeoutSeconds + " seconds")
                        .exitCode(-1)
                        .executionTime(TimeUnit.MILLISECONDS.convert(timeoutSeconds, TimeUnit.SECONDS))
                        .build();
            }

            long endTime = System.currentTimeMillis();
            executionTime = endTime - startTime;
            exitCode = runProcess.exitValue();

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(runProcess.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    stdout.append(line).append("\n");
                }
            }

            try (BufferedReader reader = new BufferedReader(new InputStreamReader(runProcess.getErrorStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    stderr.append(line).append("\n");
                }
            }

        } catch (Exception e) {
            throw new ExecutionException("Docker execution failed: " + e.getMessage());
        }

        return ExecutionResult.builder()
                .stdout(stdout.toString().trim())
                .stderr(stderr.toString().trim())
                .exitCode(exitCode)
                .executionTime(executionTime)
                .build();
    }

    public static class ExecutionResult {
        private final String stdout;
        private final String stderr;
        private final int exitCode;
        private final long executionTime;

        private ExecutionResult(Builder builder) {
            this.stdout = builder.stdout;
            this.stderr = builder.stderr;
            this.exitCode = builder.exitCode;
            this.executionTime = builder.executionTime;
        }

        public String getStdout() { return stdout; }
        public String getStderr() { return stderr; }
        public int getExitCode() { return exitCode; }
        public long getExecutionTime() { return executionTime; }

        public static Builder builder() { return new Builder(); }

        public static class Builder {
            private String stdout;
            private String stderr;
            private int exitCode;
            private long executionTime;

            public Builder stdout(String stdout) { this.stdout = stdout; return this; }
            public Builder stderr(String stderr) { this.stderr = stderr; return this; }
            public Builder exitCode(int exitCode) { this.exitCode = exitCode; return this; }
            public Builder executionTime(long executionTime) { this.executionTime = executionTime; return this; }
            public ExecutionResult build() { return new ExecutionResult(this); }
        }
    }
}