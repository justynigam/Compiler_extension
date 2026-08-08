package com.codedock.service;

import com.codedock.entity.ExecutionHistory;
import com.codedock.repository.ExecutionHistoryRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ExecutionHistoryService {

    private final ExecutionHistoryRepository executionHistoryRepository;

    public ExecutionHistoryService(ExecutionHistoryRepository executionHistoryRepository) {
        this.executionHistoryRepository = executionHistoryRepository;
    }

    public ExecutionHistory saveExecution(ExecutionHistory history) {
        return executionHistoryRepository.save(history);
    }

    public List<ExecutionHistory> getHistoryForProgram(Long programId) {
        return executionHistoryRepository.findByProgramIdOrderByCreatedAtDesc(programId);
    }
}