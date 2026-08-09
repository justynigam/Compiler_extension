package com.codedock.service;

import com.codedock.compiler.LanguageCompiler;
import com.codedock.docker.DockerExecutionService;
import com.codedock.dto.ExecutionRequest;
import com.codedock.dto.ExecutionResponse;
import com.codedock.entity.ExecutionHistory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Comparator;

@Service
public class ExecutionService {

    private final LanguageCompilerFactory compilerFactory;
    private final DockerExecutionService dockerExecutionService;
    private final ExecutionHistoryService executionHistoryService;

    public ExecutionService(LanguageCompilerFactory compilerFactory,
                            DockerExecutionService dockerExecutionService,
                            ExecutionHistoryService executionHistoryService) {
        this.compilerFactory = compilerFactory;
        this.dockerExecutionService = dockerExecutionService;
        this.executionHistoryService = executionHistoryService;
    }

    public ExecutionResponse execute(ExecutionRequest request) {
        Path tempDir = null;
        try {
            LanguageCompiler compiler = compilerFactory.getCompiler(request.getLanguage());

            tempDir = Files.createTempDirectory("codedock-exec-");
            Path sourceFile = tempDir.resolve(compiler.getSourceFileName());
            Files.writeString(sourceFile, request.getCode());

            if (request.getInput() != null && !request.getInput().isEmpty()) {
                Path inputFile = tempDir.resolve("input.txt");
                Files.writeString(inputFile, request.getInput());
            }

            DockerExecutionService.ExecutionResult result = dockerExecutionService.execute(compiler, tempDir);

            boolean success = result.getExitCode() == 0 && result.getStderr().isEmpty();
            String status = success ? "SUCCESS" : "ERROR";
            String output = success ? result.getStdout() : null;
            String error = success ? null : (!result.getStderr().isEmpty() ? result.getStderr() : result.getStdout());

            ExecutionHistory history = ExecutionHistory.builder()
                    .programId(null)
                    .input(request.getInput())
                    .output(output)
                    .error(error)
                    .executionTime(result.getExecutionTime())
                    .memory(null)
                    .exitCode(result.getExitCode())
                    .status(status)
                    .build();

            executionHistoryService.saveExecution(history);

            return ExecutionResponse.builder()
                    .status(status)
                    .output(output)
                    .error(error)
                    .executionTime(result.getExecutionTime())
                    .memory(null)
                    .exitCode(result.getExitCode())
                    .build();

        } catch (IOException e) {
            return ExecutionResponse.builder()
                    .status("ERROR")
                    .error("IO error: " + e.getMessage())
                    .exitCode(-1)
                    .build();
        } catch (Exception e) {
            return ExecutionResponse.builder()
                    .status("ERROR")
                    .error(e.getMessage())
                    .exitCode(-1)
                    .build();
        } finally {
            if (tempDir != null) {
                try {
                    Files.walk(tempDir)
                            .sorted(Comparator.reverseOrder())
                            .forEach(p -> {
                                try {
                                    Files.delete(p);
                                } catch (IOException ignored) {
                                }
                            });
                } catch (IOException ignored) {
                }
            }
        }
    }
}